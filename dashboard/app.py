
import os, json
import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
import streamlit.components.v1 as components

st.set_page_config(page_title="RAINGUARD — AI Flood Early Warning", page_icon="🌊", layout="wide")

st.markdown("""
<style>
.main-header{font-size:28px;font-weight:800;color:#0b3c5d;margin-bottom:0}
.sub-header{font-size:15px;color:#555;margin-bottom:16px}
.alert-banner-red{background:#fee2e2;border-left:6px solid #dc2626;padding:14px 18px;border-radius:6px;color:#991b1b;font-weight:700;font-size:16px;margin-bottom:16px}
.info-box{background:#e0f2fe;border-left:5px solid #0284c7;padding:10px 14px;border-radius:4px;font-size:14px;margin:10px 0;color:#075985}
</style>
""", unsafe_allow_html=True)

PROJECT_ROOT = "/content/drive/MyDrive/SIH26071_FloodWarning"
OUTPUTS_DIR  = f"{PROJECT_ROOT}/outputs/maps"
REPORTS_DIR  = f"{PROJECT_ROOT}/outputs/reports"

@st.cache_data(show_spinner=False)
def load_all():
    with open(f"{REPORTS_DIR}/dashboard_metrics.json") as f:
        metrics = json.load(f)
    with open(f"{REPORTS_DIR}/chennai_operational_early_warning_bulletin.txt") as f:
        bulletin_txt = f.read()
    roads = gpd.read_file(f"{OUTPUTS_DIR}/chennai_roads_flood_assessed.geojson").to_crs("EPSG:4326")
    fac   = gpd.read_file(f"{OUTPUTS_DIR}/chennai_facilities_flood_assessed.geojson").to_crs("EPSG:4326")
    npz = np.load(f"{OUTPUTS_DIR}/chennai_historical_replay_results.npz")
    prob = np.array(npz["prob_raster"], dtype=np.float32)
    return metrics, bulletin_txt, roads, fac, prob

metrics, bulletin_txt, gdf_roads, gdf_fac, prob = load_all()

# Sidebar Mode Switcher
st.sidebar.image("https://img.icons8.com/fluency/96/flood.png", width=65)
st.sidebar.title("RAINGUARD Controls")

operating_mode = st.sidebar.radio(
    "Select Model Operating Mode",
    ["Precision-Optimized (Ops Mode)", "High-Recall (Safety / Evacuation)"]
)

st.markdown('<div class="main-header">🌊 RAINGUARD — AI Flood Early Warning & Impact Assessment</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hyperlocal 30 m inundation modeling · Civil defense dispatch · Chennai, India</div>', unsafe_allow_html=True)
st.markdown('<div class="alert-banner-red">🚨 CRITICAL RED ALERT: Level-4 inundation risk within 3–6 hours. Evacuation protocol for low-lying river corridors.</div>', unsafe_allow_html=True)

exposed = int(metrics["population"]["high_and_severe"])
sub_km  = float(metrics["infrastructure"]["submerged_roads_km"])
hosp_n  = int(metrics["infrastructure"]["hospitals_at_risk"])
xgb_prec = metrics["xgboost_metrics"]["calibrated_precision"]
xgb_rec  = metrics["xgboost_metrics"]["calibrated_recall"]

c1,c2,c3,c4 = st.columns(4)
c1.metric("ConvLSTM 6h Rainfall Sum", "142.8 mm", "+ peak convective pulse", "inverse")
c2.metric("Exposed Population", f"{exposed:,}", "Severe & High Risk", "inverse")
c3.metric("Severed Transport Corridors", f"{sub_km:.1f} km", "Primary Arterials Cut", "inverse")
c4.metric("Model Precision / Recall", f"{xgb_prec} / {xgb_rec}", f"Mode: {operating_mode.split()[0]}", "normal")

tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Hyperlocal Inundation Map", "⏱️ Disaster Replay", "📊 Validation & Metrics", "📑 Bulletin"])

with tab1:
    st.markdown("### Interactive Geospatial Flood Risk & Infrastructure Vulnerability")
    col_map_left, col_map_right = st.columns([1, 1])

    with col_map_left:
        st.markdown("**Vector Leaflet Map Overlay**")
        m = folium.Map(location=[13.04, 80.18], zoom_start=11, tiles="OpenStreetMap")

        # Roads
        for _, row in gdf_roads.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty: continue
            lines = [geom] if geom.geom_type == "LineString" else list(getattr(geom, "geoms", []))
            flooded = bool(row.get("is_inundated", False))
            color = "#e7298a" if flooded else "#10b981"
            weight = 4 if flooded else 2
            name = str(row.get("name", "Road"))
            for line in lines:
                coords = [(lat, lon) for lon, lat in line.coords]
                if len(coords) >= 2:
                    folium.PolyLine(coords, color=color, weight=weight, opacity=0.9, tooltip=f"{name} | Inundated: {flooded}").add_to(m)

        # Facilities
        for _, row in gdf_fac.iterrows():
            g = row.geometry
            if g is None or g.is_empty: continue
            at_risk = bool(row.get("is_at_risk", False))
            cat = str(row.get("category", "Facility"))
            color = "red" if at_risk else "green"
            icon = "plus-square" if cat == "Healthcare" else "graduation-cap"
            status = "AT RISK" if at_risk else "SAFE"
            folium.Marker([g.y, g.x], tooltip=f"{row.get('name','Facility')} ({status})", icon=folium.Icon(color=color, icon=icon, prefix="fa")).add_to(m)

        map_html = m._repr_html_()
        components.html(map_html, height=520, scrolling=False)

    with col_map_right:
        st.markdown("**30m GIS Inundation Risk & Infrastructure Overlay**")
        map_graphic_path = f"{OUTPUTS_DIR}/chennai_map_tab1_display.png"
        if os.path.exists(map_graphic_path):
            st.image(map_graphic_path, use_container_width=True)

with tab2:
    st.markdown("### December 2015 disaster replay")
    st.markdown('<div class="info-box"><b>Hydrological Coupling:</b> Spatio-temporal rainfall sequence forecasting drives topsoil saturation to 100%, causing Hortonian overland runoff spikes.</div>', unsafe_allow_html=True)
    a,b = st.columns(2)
    p1 = f"{OUTPUTS_DIR}/chennai_2015_rainfall_hyetograph.png"
    p2 = f"{OUTPUTS_DIR}/chennai_hydrologic_coupling_2015.png"
    if os.path.exists(p1): a.image(p1, use_container_width=True)
    if os.path.exists(p2): b.image(p2, use_container_width=True)

with tab3:
    st.markdown("### Scientific Validation & Multi-Operating Mode Tradeoff")
    st.markdown('<div class="info-box"><b>Dual Operating Point Design:</b> The XGBoost model supports both a Safety-First High Recall Mode (85.5% detection) and an Operational Precision-Optimized Mode (34.7% precision, 0.354 F1) depending on civil defense needs.</div>', unsafe_allow_html=True)

    c_v1, c_v2 = st.columns([1.2, 1])
    with c_v1:
        flag = f"{OUTPUTS_DIR}/chennai_2015_flagship_replay_panel.png"
        if os.path.exists(flag): st.image(flag, use_container_width=True)
    with c_v2:
        st.markdown("#### Holdout Test Set & City-Wide Metrics")
        st.dataframe(pd.DataFrame([
            {"Operating Mode": "1. High-Recall Safety Mode", "Precision": "17.1%", "Recall": "85.5%", "F1-Score": "0.285", "IoU / CSI": "0.167"},
            {"Operating Mode": "2. Precision-Optimized Mode", "Precision": "34.7%", "Recall": "36.2%", "F1-Score": "0.354", "IoU / CSI": "0.215"}
        ]), use_container_width=True)
        diag = f"{OUTPUTS_DIR}/xgboost_flood_model_diagnostics.png"
        if os.path.exists(diag): st.image(diag, use_container_width=True)

with tab4:
    st.markdown("### Civil defense advisory bulletin")
    st.code(bulletin_txt, language="text")
    st.download_button("📥 Download bulletin (.txt)", bulletin_txt, file_name="RAINGUARD_Alert_Bulletin.txt")

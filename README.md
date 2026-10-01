# 🌧️ RAINGUARD

## AI/ML-Based Heavy Rainfall Early Warning and Urban Inundation Prediction System

> **Forecast → Risk → Impact → Action**

RAINGUARD is an AI/ML-based flood-risk intelligence system designed to translate rainfall forecasts into localized urban inundation-risk information.

The system combines meteorological, terrain, hydrological, land-cover, population and infrastructure information to estimate where heavy rainfall is more likely to result in localized flooding and which areas may be more exposed.

The current study focuses on **Chennai, India**, with historical validation using a major flood event and satellite-derived flood observations.

---

## 🚨 Problem Statement

### Heavy rainfall does not always produce the same level of flooding.

Two locations receiving similar rainfall can experience very different flood impacts because of differences in:

- Elevation and slope
- Drainage characteristics
- Soil saturation
- Land cover and urbanization
- Runoff pathways
- Hydrological characteristics
- Distance from rivers and drainage channels

Traditional rainfall forecasting mainly answers:

> **"How much rain is expected?"**

RAINGUARD focuses on the next question:

> **"Where is that rainfall more likely to create localized flood risk, and what could be affected?"**

---

# 💡 RAINGUARD Solution

RAINGUARD follows a four-stage decision-support pipeline:

```text
FORECAST
   ↓
Rainfall prediction
   ↓
RISK
   ↓
30 m flood-risk analysis
   ↓
IMPACT
   ↓
Population + Roads + Critical Facilities
   ↓
ACTION
   ↓
Risk information and operational advisories
```

The system combines rainfall information with physical and urban characteristics to produce a localized flood-risk surface.

---

# 🧠 AI/ML Approach

## 1. Rainfall Forecasting — ConvLSTM

A **Convolutional Long Short-Term Memory (ConvLSTM)** model is used for short-term rainfall forecasting.

The model learns spatial and temporal patterns in rainfall data and produces a near-term rainfall forecast.

### Output

```text
Near-term rainfall forecast
        ↓
Spatial rainfall information
```

---

## 2. Flood-Risk Prediction — XGBoost

The predicted rainfall information is combined with environmental and physical features and passed to an **XGBoost classifier**.

The model estimates flood probability at cells on the **30 m analysis grid**.

Important:

> The 30 m resolution refers to the flood-risk analysis/output grid. It does not mean that the original rainfall observations have 30 m spatial resolution.

### Example feature groups

- Rainfall
- Elevation
- Slope
- Terrain characteristics
- Hydrological features
- Soil-related features
- Land-cover information
- Flow/drainage characteristics

---

# 🗺️ 30 m Flood-Risk Analysis

RAINGUARD integrates multiple datasets onto a common spatial analysis framework.

The final flood-risk output is generated on a:

**30 m × 30 m analysis grid**

The system produces localized flood-probability information rather than treating the entire city as having the same flood response.

---

# 🛰️ Data Sources

RAINGUARD integrates multiple Earth-observation, meteorological, terrain and infrastructure datasets.

| Data Source | Role |
|---|---|
| **NASA GPM IMERG** | Rainfall / precipitation information |
| **ERA5-Land** | Land-surface and hydrological variables such as soil moisture and runoff |
| **Copernicus DEM GLO-30** | Elevation and terrain characteristics |
| **MERIT Hydro** | Drainage and flow-related information |
| **ESA WorldCover** | Land-cover classification |
| **Sentinel-1 SAR** | Independent flood-observation / validation data |
| **JRC GHSL** | Population exposure estimation |
| **OpenStreetMap** | Roads and critical infrastructure |

### Data-resolution note

Different datasets have different native spatial and temporal resolutions.

RAINGUARD therefore performs preprocessing and spatial alignment before generating the final flood-risk analysis.

---

# 🔬 Sentinel-1 SAR Validation

Sentinel-1 SAR is used as an **independent flood-observation source** for validation.

It is important that Sentinel-1 flood observations are not used as predictive features for the same event being evaluated.

```text
Predictive Inputs
      ↓
Rainfall + Terrain + Hydrology + Land Cover
      ↓
      XGBoost
      ↓
Predicted Flood Risk
      ↓
      COMPARE
      ↑
Sentinel-1 SAR Flood Mask
      ↓
Observed Flood Reference
```

This provides an independent reference for evaluating the predicted inundation map.

---

# 🧪 Spatial Validation Strategy

A major concern in spatial flood prediction is **spatial data leakage**.

Neighboring 30 m pixels can have very similar characteristics. Randomly splitting individual pixels can therefore make a model appear more accurate than it is on geographically unseen areas.

To reduce this problem, Chennai is divided into **16 geographically disjoint spatial blocks**.

```text
Chennai Study Area

┌────┬────┬────┬────┐
│    │    │    │    │
├────┼────┼────┼────┤
│    │    │    │    │
├────┼────┼────┼────┤
│    │    │    │    │
├────┼────┼────┼────┤
│    │    │    │    │
└────┴────┴────┴────┘

16 Spatial Blocks

11 → Training
2  → Validation
3  → Testing
```

The test blocks are geographically separated from the training blocks and are not used during model training or hyperparameter tuning.

This provides a stronger test of spatial generalization than a simple random pixel split.

---

# 📊 Model Evaluation

Flood-risk predictions are evaluated against satellite-derived flood observations.

The evaluation includes:

- Precision
- Recall
- F1-score
- IoU / CSI
- Spatial-tolerance analysis

Spatial tolerance is useful because flood boundaries derived from satellite imagery and model predictions can contain positional uncertainty.

### Important interpretation

Strict pixel-level matching and neighborhood-based matching measure different aspects of performance.

A higher tolerance can increase the number of predicted pixels that spatially correspond to an observed flood region, but it should not be interpreted as proof that every strict false positive is simply a displaced prediction.

---

# 🏙️ Impact Assessment

After generating flood-risk information, RAINGUARD can combine the risk map with exposure layers to identify potentially affected assets.

### 👥 Population

Estimate population exposure across different flood-risk areas.

### 🛣️ Roads

Identify potentially affected road segments and areas where road disruption may occur.

### 🏥 Critical Facilities

Identify hospitals, schools and other mapped facilities located within higher-risk areas.

### 🚨 Emergency Planning

The resulting information can help authorities prioritize areas for preparedness and response planning.

---

# 🖥️ Dashboard

RAINGUARD includes a **Streamlit-based visualization/dashboard component** for presenting spatial risk information and impact-related outputs.

The intended dashboard workflow is:

```text
Rainfall Forecast
       ↓
Flood Risk Prediction
       ↓
Interactive Risk Map
       ↓
Risk Tiers
       ↓
Population Exposure
       ↓
Roads at Risk
       ↓
Critical Facilities
       ↓
Operational Advisory
```

---

# ⚙️ System Architecture

```text
┌─────────────────────────────────────────────┐
│              DATA SOURCES                   │
│                                             │
│ GPM • ERA5-Land • DEM • MERIT Hydro        │
│ WorldCover • Sentinel-1 • GHSL • OSM        │
└──────────────────────┬──────────────────────┘
                       ↓
              DATA PREPROCESSING
                       ↓
             COMMON SPATIAL GRID
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
   RAINFALL FORECAST          PHYSICAL FEATURES
      ConvLSTM               Terrain / Hydrology
          ↓                  Soil / Land Cover
          └────────────┬────────────┘
                       ↓
                 XGBOOST MODEL
                       ↓
            FLOOD-RISK PROBABILITY
                       ↓
             30 m RISK MAP
                       ↓
              IMPACT ASSESSMENT
             /       |        \
            ↓        ↓         ↓
       Population   Roads   Facilities
             \       |        /
              \      |       /
                 ↓
         ACTIONABLE RISK
          INFORMATION
                 ↓
          STREAMLIT DASHBOARD
```

---

# 🛡️ Key Technical Considerations

## Spatial Scale Mismatch

Rainfall products are generally much coarser than the 30 m flood-risk analysis grid.

### Approach

RAINGUARD combines rainfall forcing with higher-resolution terrain, hydrological and land-cover features to estimate localized flood risk.

---

## Spatial Data Leakage

Random pixel splitting can result in neighboring pixels appearing in both training and testing datasets.

### Approach

A geographically disjoint block-based split is used:

**11 Train / 2 Validation / 3 Test**

---

## Class Imbalance

Flooded pixels can represent a relatively small fraction of the complete study area.

### Approach

Class weighting and precision/recall-based evaluation are used to account for imbalanced flood classes.

---

## SAR Observation Noise

Urban SAR imagery can contain effects such as building layover, shadows and permanent-water areas.

### Approach

Preprocessing and masking techniques are applied to improve the flood-observation reference.

---

# 🌊 Current Scope and Future Development

## Current Scope

The current system focuses on:

- Rainfall-driven / pluvial inundation
- Flood-risk prediction using terrain and hydrological characteristics
- Topographic fluvial/coastal susceptibility
- Population and infrastructure exposure
- Historical satellite-based validation
- Spatially disjoint model evaluation

## Future Roadmap

A future compound-flood module can incorporate additional dynamic forcing such as:

- Coastal tide-gauge observations
- Storm-surge information
- River discharge
- Reservoir-release information
- Additional operational weather-radar/NWP inputs
- Multi-city deployment

These components are considered part of the **future expansion roadmap**, rather than being treated as fully integrated dynamic forcing in the current model.

---

# 📈 Scalability

RAINGUARD is designed as a modular pipeline.

```text
Chennai
   ↓
Other Cities
   ↓
Multi-City Deployment
   ↓
National-Scale Expansion
```

For deployment to another city, the system can incorporate:

- Local terrain
- Local rainfall characteristics
- Local hydrological information
- Historical flood observations
- Local population data
- Local road and infrastructure information

Future deployment can use cloud-based inference and technologies such as FastAPI, PostGIS and Docker.

---

# 📁 Repository Structure

```text
RAINGUARD/
│
├── README.md
├── RainGuard.ipynb
└── requirements.txt
```

### Files

| File | Description |
|---|---|
| `README.md` | Project documentation |
| `RainGuard.ipynb` | Main research and implementation notebook |
| `requirements.txt` | Python dependencies |

---

# ▶️ How to Run

## Option 1 — Google Colab

The primary development environment for the current notebook is Google Colab.

1. Open `RainGuard.ipynb`.
2. Open the notebook using Google Colab.
3. Run the environment/setup cells.
4. Configure the required data sources and paths.
5. Run the notebook cells in sequence.

The notebook contains the required package installation and project-processing steps.

---

## Option 2 — Local Environment

Clone the repository:

```bash
git clone https://github.com/omprakash2468/RAINGUARD.git
```

Enter the project directory:

```bash
cd RAINGUARD
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Launch the notebook:

```bash
jupyter notebook RainGuard.ipynb
```

Some components may require external data services, authentication, or configuration described in the notebook.

---

# 📚 Research and References

RAINGUARD is informed by research in:

- Urban flood prediction
- Rainfall forecasting
- ConvLSTM-based spatiotemporal forecasting
- Machine-learning-based flood mapping
- Remote-sensing flood detection
- Hydrological modelling
- Impact-based forecasting
- Compound flood modelling

Key external systems and data resources considered by the project include:

- NASA GPM / IMERG
- ECMWF ERA5-Land
- Copernicus DEM
- MERIT Hydro
- ESA WorldCover
- Sentinel-1 SAR
- JRC GHSL
- OpenStreetMap
- India Meteorological Department
- Central Water Commission
- NDMA

---

# 📍 Historical Validation Event

### Chennai Flood — December 2015

The project uses the **December 2015 Chennai flood event** as a historical validation case.

A Sentinel-1 SAR-derived flood mask is used as an independent observed-flood reference for evaluating predicted inundation.

The validation is performed on the project's 30 m flood-risk analysis framework.

---

# 🎯 Expected Benefits

### ⏱️ Earlier Action

Provides forecast-derived risk information that can support disaster preparedness and response planning.

### 📍 Localized Risk

Produces flood-risk information at a 30 m analysis grid rather than relying only on regional rainfall information.

### 🎯 Resource Prioritization

Helps identify areas where emergency resources may need greater attention.

### 👥 Population Exposure

Provides population exposure information across flood-risk areas.

### 🛣️ Road Disruption

Helps identify potentially affected road segments.

### 🏥 Critical Infrastructure

Highlights mapped critical facilities located in higher-risk areas.

### 🔄 Scalability

The modular approach can be adapted to additional cities with suitable local data and historical flood observations.

---

# ⚠️ Limitations

The current system has several limitations:

- Meteorological datasets have different native spatial and temporal resolutions.
- Flood observations from satellite imagery contain positional and classification uncertainty.
- Urban drainage networks and underground drainage capacity are not completely represented by surface datasets.
- Dynamic coastal forcing is not fully integrated into the current flood model.
- Dynamic reservoir-release and river-discharge forcing are part of the future roadmap.
- Operational deployment requires reliable real-time data feeds and infrastructure.
- Model performance depends on the quality and representativeness of training and validation events.

These limitations are considered in the project's future development roadmap.

---

# 👥 Team

### Team Name

**npm-run-myFriend**

### Smart India Hackathon 2026

**Problem Statement ID:** SIH26071

**Theme:** Disaster Management

**Category:** Software

---

# 🚀 Project Vision

RAINGUARD aims to move from:

> **Rainfall Forecasting**

towards:

> **Impact-Based Flood-Risk Intelligence**

by connecting:

```text
FORECAST
    ↓
RAINFALL
    ↓
FLOOD RISK
    ↓
EXPOSURE
    ↓
IMPACT
    ↓
ACTION
```

The goal is to provide localized information that can support better flood preparedness, infrastructure protection and emergency-response planning.

---

## 👨‍💻 Project Status

**Current Stage:** Research / Prototype / MVP

**Study Area:** Chennai, India

**Primary Environment:** Google Colab

**Machine Learning:** XGBoost

**Deep Learning:** ConvLSTM / PyTorch

**Visualization:** Streamlit

**Flood Validation:** Sentinel-1 SAR

**Analysis Grid:** 30 m

---

## 📌 Disclaimer

RAINGUARD is a research and prototype system developed for the Smart India Hackathon 2026 problem statement.

Its outputs are intended to support analysis and disaster preparedness. They should not be treated as a replacement for official warnings, emergency-management decisions, or authoritative meteorological and hydrological services.

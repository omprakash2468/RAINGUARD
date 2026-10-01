# RAINGUARD

### AI/ML-Based Heavy Rainfall Early Warning and Urban Inundation Prediction System

RAINGUARD is an AI/ML-based system designed to combine rainfall, weather, terrain, hydrological, land-cover and flood-observation data to estimate localized flood risk and support disaster preparedness.

## 🚨 Problem

Heavy rainfall does not always produce the same level of flooding across a city.

Flood impact depends on factors such as:

- Rainfall intensity
- Elevation and slope
- Drainage and hydrological characteristics
- Soil and land-cover conditions
- Surface runoff pathways
- Population and critical infrastructure exposure

Therefore, rainfall forecasts alone may not provide sufficiently localized flood-risk information.

## 💡 Solution

RAINGUARD follows a:

**Forecast → Risk → Impact → Action**

approach.

The system:

1. Forecasts near-term rainfall using **ConvLSTM**.
2. Combines rainfall and geographical/hydrological features.
3. Uses **XGBoost** to estimate flood probability on a **30 m analysis grid**.
4. Uses satellite-derived flood observations for validation.
5. Maps potential impacts on population and critical infrastructure.
6. Provides localized risk information to support disaster preparedness.

## 🧠 AI/ML Models

### ConvLSTM
Used for short-term rainfall forecasting.

### XGBoost
Used for cell-level flood-risk probability estimation using multiple environmental and meteorological features.

## 🛰️ Data Sources

The project uses/targets multiple data sources, including:

- GPM IMERG — precipitation
- ERA5-Land — land-surface and hydrological variables
- Copernicus DEM — elevation/topography
- MERIT Hydro — hydrological information
- ESA WorldCover — land-cover information
- Sentinel-1 SAR — flood observation/validation
- GHSL — population exposure
- OpenStreetMap — infrastructure information

## 🗺️ Spatial Validation

The Chennai study area is divided into geographically disjoint blocks for model evaluation.

This helps reduce spatial leakage caused by neighboring pixels having highly similar characteristics.

## 📊 Validation

Flood predictions are evaluated against satellite-derived flood observations using spatial matching at different tolerance levels.

Evaluation metrics include:

- Precision
- Recall
- F1-score
- IoU / CSI

## 🏗️ System Pipeline

```text
Meteorological + Satellite + Terrain + Hydrological Data
                         ↓
                Data Preprocessing
                         ↓
              Rainfall Forecasting
                   (ConvLSTM)
                         ↓
              Feature Engineering
                         ↓
             Flood Risk Prediction
                   (XGBoost)
                         ↓
              Flood Risk Map
                         ↓
           Exposure & Impact Analysis
                         ↓
              Actionable Risk
                Information

# MyHealthPal Model Files

This directory contains the pre-trained machine learning models for health risk predictions.

## Required Model Files

Please place the following model files in this directory:

### Obesity Risk Models

- `obesity_risk_model.pkl` - Main obesity prediction model (Logistic Regression, 98.4% accuracy)
- `obesity_scaler.pkl` - Feature scaling for obesity model
- `obesity_imputer.pkl` - Handles missing values for obesity model
- `activity_encoder.pkl` - Encodes activity levels (Sedentary/Light/Moderate/Active/Very Active)

### Heart Disease Models

- `heart_disease_model.pkl` - Heart disease prediction model (87.6% AUC)
- `heart_disease_scaler.pkl` - Feature scaling for heart disease model

### Metadata

- `model_metadata.json` - Model performance metrics and configuration

## Model Status

When models are available:

- ✅ Real ML predictions will be used
- Higher accuracy obesity and heart disease risk assessments
- Model metadata will be included in health checks

When models are missing:

- ⚠️ Fallback mode will be used
- Clinical rule-based predictions
- Still functional but less accurate

## Loading Process

Models are automatically loaded when the ML service initializes:

1. Service checks for model files in this directory
2. Loads each model using `joblib.load()`
3. If critical models are missing, switches to fallback mode
4. All model loading is logged for debugging

## File Format

All model files should be:

- Saved using `joblib.dump()` or `pickle.dump()`
- Compatible with scikit-learn models
- Pre-trained and ready for inference

## To Add Models

1. Copy your `.pkl` and `.json` files to this directory
2. Restart the backend service
3. Check the health endpoint to verify models are loaded: `/api/health`

The service will automatically detect and load the models on next startup.

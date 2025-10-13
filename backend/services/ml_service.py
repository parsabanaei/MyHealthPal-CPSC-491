import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLService:
    """
    Real ML prediction service for MyHealthPal using pre-trained models
    
    Handles:
    - Loading pre-trained model files (.pkl)
    - Converting user inputs to model format
    - Real obesity risk predictions
    - Real heart disease risk predictions
    - Clinical diabetes risk assessments
    - BMI calculations and categorization
    """
    
    def __init__(self):
        """Initialize ML service and load models"""
        self.models_path = Path(__file__).parent.parent / "models"
        self.models_loaded = False
        self.fallback_mode = False
        
        # Model containers
        self.obesity_model = None
        self.obesity_scaler = None
        self.obesity_imputer = None
        self.activity_encoder = None
        self.heart_disease_model = None
        self.heart_disease_scaler = None
        self.model_metadata = None
        
        # Load models on initialization
        self.load_models()
    
    def load_models(self) -> bool:
        """
        Load all pre-trained models from the models directory
        
        Returns:
            True if models loaded successfully, False if fallback mode
        """
        try:
            logger.info(f"Loading models from: {self.models_path}")
            
            # Check if models directory exists
            if not self.models_path.exists():
                logger.warning(f"Models directory not found: {self.models_path}")
                self.fallback_mode = True
                return False
            
            # Expected model files
            model_files = {
                'obesity_model': 'obesity_risk_model.pkl',
                'obesity_scaler': 'obesity_scaler.pkl',
                'obesity_imputer': 'obesity_imputer.pkl',
                'activity_encoder': 'activity_encoder.pkl',
                'heart_disease_model': 'heart_disease_model.pkl',
                'heart_disease_scaler': 'heart_disease_scaler.pkl',
                'metadata': 'model_metadata.json'
            }
            
            # Load each model file
            for model_name, filename in model_files.items():
                file_path = self.models_path / filename
                
                if not file_path.exists():
                    logger.warning(f"Model file not found: {filename}")
                    continue
                
                try:
                    if filename.endswith('.json'):
                        # Load JSON metadata
                        with open(file_path, 'r') as f:
                            self.model_metadata = json.load(f)
                        logger.info(f"Loaded metadata: {filename}")
                    else:
                        # Load pickle files
                        model = joblib.load(file_path)
                        setattr(self, model_name, model)
                        logger.info(f"Loaded model: {filename}")
                        
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
                    continue
            
            # Check if critical models are loaded
            if self.obesity_model is not None:
                self.models_loaded = True
                self.fallback_mode = False
                logger.info("✅ ML models loaded successfully - Real predictions enabled")
                return True
            else:
                logger.warning("⚠️ Critical models missing - Using fallback mode")
                self.fallback_mode = True
                return False
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.fallback_mode = True
            return False
    
    def convert_inputs(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert user inputs to model-expected format
        
        Args:
            user_input: Raw user input data
            
        Returns:
            Model-ready feature dictionary
        """
        try:
            # Extract and convert inputs
            age = int(user_input.get('age', 30))
            gender = user_input.get('gender', 'Male')
            height_feet = int(user_input.get('height_feet', 5))
            height_inches = int(user_input.get('height_inches', 8))
            weight_lbs = float(user_input.get('weight_lbs', 150))
            activity_level = user_input.get('activity_level', 'Moderate')
            family_history = bool(user_input.get('family_history', False))
            smoking = bool(user_input.get('smoking', False))
            
            # Unit conversions
            height_cm = ((height_feet * 12) + height_inches) * 2.54
            weight_kg = weight_lbs / 2.20462
            
            # Gender conversion (Male=1, Female=0)
            gender_male = 1 if gender.lower() == 'male' else 0
            
            # Create model input format
            model_features = {
                'RIDAGEYR': age,  # Age in years
                'Gender_Male': gender_male,  # Gender (1=Male, 0=Female)
                'BMXHT': height_cm,  # Height in cm
                'BMXWT': weight_kg,  # Weight in kg
                'Activity_Level': activity_level,  # Activity level (will be encoded)
                'family_history': 1 if family_history else 0,
                'smoking': 1 if smoking else 0
            }
            
            logger.info(f"Converted inputs: Age={age}, Gender={gender}({gender_male}), "
                       f"Height={height_cm:.1f}cm, Weight={weight_kg:.1f}kg, Activity={activity_level}")
            
            return model_features
            
        except Exception as e:
            logger.error(f"Error converting inputs: {e}")
            raise ValueError(f"Invalid input format: {e}")
    
    def calculate_bmi(self, height_cm: float, weight_kg: float) -> Tuple[float, str]:
        """
        Calculate BMI and category
        
        Args:
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms
            
        Returns:
            Tuple of (BMI value, BMI category)
        """
        try:
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)
            
            # BMI categorization
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal Weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            return round(bmi, 1), category
            
        except Exception as e:
            logger.error(f"Error calculating BMI: {e}")
            return 25.0, "Normal Weight"
    
    def predict_obesity_risk(self, model_features: Dict[str, Any]) -> Tuple[str, float]:
        """
        Predict obesity risk using the real ML model
        
        Args:
            model_features: Model-ready features
            
        Returns:
            Tuple of (risk_category, risk_percentage)
        """
        try:
            if self.fallback_mode or self.obesity_model is None:
                return self._fallback_obesity_prediction(model_features)
            
            # Prepare features for the model
            features_df = pd.DataFrame([model_features])
            
            # Encode activity level if encoder is available
            if self.activity_encoder is not None:
                try:
                    # Ensure activity level is in the expected format
                    activity_level = model_features['Activity_Level']
                    # Map to model-expected values if needed
                    if activity_level not in ['Sedentary', 'Moderate', 'Active']:
                        if activity_level in ['Light']:
                            activity_level = 'Moderate'
                        elif activity_level in ['Very Active']:
                            activity_level = 'Active'
                    
                    activity_encoded = self.activity_encoder.transform([activity_level])[0]
                    features_df['Activity_Level_Encoded'] = activity_encoded
                    features_df = features_df.drop('Activity_Level', axis=1)
                except Exception as e:
                    logger.warning(f"Activity encoding failed: {e}")
                    features_df['Activity_Level_Encoded'] = 1  # Default moderate encoded value
            
            # Apply imputation if available
            if self.obesity_imputer is not None:
                try:
                    features_df = pd.DataFrame(
                        self.obesity_imputer.transform(features_df),
                        columns=features_df.columns
                    )
                except Exception as e:
                    logger.warning(f"Imputation failed: {e}")
            
            # Apply scaling if available
            if self.obesity_scaler is not None:
                try:
                    features_scaled = self.obesity_scaler.transform(features_df)
                    features_df = pd.DataFrame(features_scaled, columns=features_df.columns)
                except Exception as e:
                    logger.warning(f"Scaling failed: {e}")
            
            # Get prediction probability
            risk_probability = self.obesity_model.predict_proba(features_df)[0]
            
            # Extract high-risk probability (usually index 1)
            if len(risk_probability) > 1:
                risk_score = risk_probability[1] * 100  # Convert to percentage
            else:
                risk_score = risk_probability[0] * 100
            
            # Categorize risk
            if risk_score < 30:
                risk_category = "Low"
            elif risk_score < 70:
                risk_category = "Medium"
            else:
                risk_category = "High"
            
            logger.info(f"Obesity prediction: {risk_category} ({risk_score:.1f}%)")
            return risk_category, round(risk_score, 1)
            
        except Exception as e:
            logger.error(f"Error in obesity prediction: {e}")
            return self._fallback_obesity_prediction(model_features)
    
    def predict_heart_disease_risk(self, model_features: Dict[str, Any]) -> Tuple[str, float]:
        """
        Predict heart disease risk using ML model + clinical rules
        
        Args:
            model_features: Model-ready features
            
        Returns:
            Tuple of (risk_category, risk_percentage)
        """
        try:
            if self.fallback_mode or self.heart_disease_model is None:
                return self._fallback_heart_disease_prediction(model_features)
            
            # Prepare features for heart disease model
            # Heart disease model may expect different features than obesity model
            hd_features = {
                'RIDAGEYR': model_features['RIDAGEYR'],
                'Gender_Male': model_features['Gender_Male'],
                'BMXHT': model_features['BMXHT'],
                'BMXWT': model_features['BMXWT']
            }
            
            # Add encoded activity level if available
            if self.activity_encoder is not None:
                try:
                    activity_level = model_features['Activity_Level']
                    if activity_level not in ['Sedentary', 'Moderate', 'Active']:
                        if activity_level in ['Light']:
                            activity_level = 'Moderate'
                        elif activity_level in ['Very Active']:
                            activity_level = 'Active'
                    
                    activity_encoded = self.activity_encoder.transform([activity_level])[0]
                    hd_features['Activity_Level_Encoded'] = activity_encoded
                except Exception as e:
                    logger.warning(f"Heart disease activity encoding failed: {e}")
                    hd_features['Activity_Level_Encoded'] = 1
            
            features_df = pd.DataFrame([hd_features])
            
            # Calculate BMI for clinical rules
            bmi, _ = self.calculate_bmi(model_features['BMXHT'], model_features['BMXWT'])
            
            # Apply scaling if available
            if self.heart_disease_scaler is not None:
                try:
                    features_scaled = self.heart_disease_scaler.transform(features_df)
                    features_df = pd.DataFrame(features_scaled, columns=features_df.columns)
                except Exception as e:
                    logger.warning(f"Heart disease scaling failed: {e}")
            
            # Get ML model prediction
            risk_probability = self.heart_disease_model.predict_proba(features_df)[0]
            
            if len(risk_probability) > 1:
                ml_risk_score = risk_probability[1] * 100
            else:
                ml_risk_score = risk_probability[0] * 100
            
            # Apply clinical risk factors adjustment
            clinical_adjustment = 0
            
            # Age risk
            age = model_features['RIDAGEYR']
            if age > 65:
                clinical_adjustment += 15
            elif age > 55:
                clinical_adjustment += 10
            elif age > 45:
                clinical_adjustment += 5
            
            # Gender risk (males higher risk)
            if model_features['Gender_Male'] == 1:
                clinical_adjustment += 5
            
            # BMI risk
            if bmi >= 30:
                clinical_adjustment += 10
            elif bmi >= 25:
                clinical_adjustment += 5
            
            # Family history
            if model_features['family_history'] == 1:
                clinical_adjustment += 15
            
            # Smoking
            if model_features['smoking'] == 1:
                clinical_adjustment += 20
            
            # Combine ML prediction with clinical factors
            final_risk_score = min(95, ml_risk_score + clinical_adjustment)
            
            # Categorize risk
            if final_risk_score < 30:
                risk_category = "Low"
            elif final_risk_score < 70:
                risk_category = "Medium"
            else:
                risk_category = "High"
            
            logger.info(f"Heart disease prediction: {risk_category} ({final_risk_score:.1f}%)")
            return risk_category, round(final_risk_score, 1)
            
        except Exception as e:
            logger.error(f"Error in heart disease prediction: {e}")
            return self._fallback_heart_disease_prediction(model_features)
    
    def predict_diabetes_risk(self, model_features: Dict[str, Any]) -> Tuple[str, float]:
        """
        Predict diabetes risk using clinical assessment
        
        Args:
            model_features: Model-ready features
            
        Returns:
            Tuple of (risk_category, risk_percentage)
        """
        try:
            # Clinical diabetes risk assessment
            risk_score = 0
            
            # Age factor
            age = model_features['RIDAGEYR']
            if age >= 65:
                risk_score += 20
            elif age >= 55:
                risk_score += 15
            elif age >= 45:
                risk_score += 10
            elif age >= 35:
                risk_score += 5
            
            # BMI factor
            bmi, _ = self.calculate_bmi(model_features['BMXHT'], model_features['BMXWT'])
            if bmi >= 35:
                risk_score += 25
            elif bmi >= 30:
                risk_score += 20
            elif bmi >= 25:
                risk_score += 10
            
            # Family history
            if model_features['family_history'] == 1:
                risk_score += 15
            
            # Activity level (inverse relationship)
            activity = model_features['Activity_Level'].lower()
            if 'sedentary' in activity:
                risk_score += 15
            elif 'light' in activity:
                risk_score += 10
            elif 'moderate' in activity:
                risk_score += 5
            # No additional risk for active/very active
            
            # Smoking
            if model_features['smoking'] == 1:
                risk_score += 10
            
            # Gender (slightly higher risk for males)
            if model_features['Gender_Male'] == 1:
                risk_score += 5
            
            # Cap at 95%
            risk_score = min(95, risk_score)
            
            # Categorize
            if risk_score < 25:
                risk_category = "Low"
            elif risk_score < 60:
                risk_category = "Medium"
            else:
                risk_category = "High"
            
            logger.info(f"Diabetes prediction: {risk_category} ({risk_score:.1f}%)")
            return risk_category, round(risk_score, 1)
            
        except Exception as e:
            logger.error(f"Error in diabetes prediction: {e}")
            return "Medium", 40.0
    
    def get_comprehensive_assessment(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive health risk assessment
        
        Args:
            user_input: Raw user input data
            
        Returns:
            Complete assessment results
        """
        try:
            # Convert inputs to model format
            model_features = self.convert_inputs(user_input)
            
            # Calculate BMI
            bmi, bmi_category = self.calculate_bmi(
                model_features['BMXHT'], 
                model_features['BMXWT']
            )
            
            # Get risk predictions
            obesity_risk, obesity_score = self.predict_obesity_risk(model_features)
            heart_risk, heart_score = self.predict_heart_disease_risk(model_features)
            diabetes_risk, diabetes_score = self.predict_diabetes_risk(model_features)
            
            # Calculate overall health score (10-point scale)
            avg_risk = (obesity_score + heart_score + diabetes_score) / 3
            health_score = max(1, 10 - (avg_risk / 10))
            
            return {
                'bmi': bmi,
                'bmi_category': bmi_category,
                'obesity_risk': obesity_risk,
                'obesity_score': obesity_score,
                'heart_disease_risk': heart_risk,
                'heart_disease_score': heart_score,
                'diabetes_risk': diabetes_risk,
                'diabetes_score': diabetes_score,
                'overall_health_score': round(health_score, 1),
                'model_status': 'real_models' if not self.fallback_mode else 'fallback_mode',
                'recommendations': self._generate_recommendations(
                    bmi_category, obesity_risk, heart_risk, diabetes_risk
                )
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive assessment: {e}")
            raise ValueError(f"Assessment failed: {e}")
    
    def _fallback_obesity_prediction(self, features: Dict[str, Any]) -> Tuple[str, float]:
        """Fallback obesity prediction using clinical rules"""
        try:
            bmi, _ = self.calculate_bmi(features['BMXHT'], features['BMXWT'])
            age = features['RIDAGEYR']
            
            risk_score = 0
            if bmi >= 30:
                risk_score = 75
            elif bmi >= 25:
                risk_score = 45
            else:
                risk_score = 15
            
            # Age adjustment
            if age > 50:
                risk_score += 10
            
            # Activity adjustment
            activity = features.get('Activity_Level', '').lower()
            if 'sedentary' in activity:
                risk_score += 15
            
            risk_score = min(95, risk_score)
            
            if risk_score < 30:
                return "Low", risk_score
            elif risk_score < 70:
                return "Medium", risk_score
            else:
                return "High", risk_score
                
        except:
            return "Medium", 45.0
    
    def _fallback_heart_disease_prediction(self, features: Dict[str, Any]) -> Tuple[str, float]:
        """Fallback heart disease prediction using clinical rules"""
        try:
            risk_score = 20  # Base risk
            
            age = features['RIDAGEYR']
            if age > 65:
                risk_score += 25
            elif age > 55:
                risk_score += 15
            elif age > 45:
                risk_score += 10
            
            if features['Gender_Male'] == 1:
                risk_score += 10
            
            if features['family_history'] == 1:
                risk_score += 20
            
            if features['smoking'] == 1:
                risk_score += 25
            
            bmi, _ = self.calculate_bmi(features['BMXHT'], features['BMXWT'])
            if bmi >= 30:
                risk_score += 15
            
            risk_score = min(95, risk_score)
            
            if risk_score < 30:
                return "Low", risk_score
            elif risk_score < 70:
                return "Medium", risk_score
            else:
                return "High", risk_score
                
        except:
            return "Medium", 40.0
    
    def _generate_recommendations(self, bmi_category: str, obesity_risk: str, 
                                 heart_risk: str, diabetes_risk: str) -> List[str]:
        """Generate personalized health recommendations"""
        recommendations = []
        
        # BMI-based recommendations
        if bmi_category == "Underweight":
            recommendations.append("Consider consulting a nutritionist for healthy weight gain strategies")
        elif bmi_category in ["Overweight", "Obese"]:
            recommendations.append("Focus on gradual weight loss through balanced diet and exercise")
        
        # Risk-based recommendations
        if obesity_risk == "High":
            recommendations.append("Implement portion control and increase physical activity")
        
        if heart_risk == "High":
            recommendations.append("Regular cardiovascular exercise and heart-healthy diet recommended")
            recommendations.append("Consider regular blood pressure and cholesterol monitoring")
        
        if diabetes_risk == "High":
            recommendations.append("Monitor blood sugar levels and limit refined carbohydrates")
            recommendations.append("Increase fiber intake and maintain regular meal timing")
        
        # General recommendations
        recommendations.extend([
            "Maintain regular physical activity (150+ minutes moderate exercise per week)",
            "Follow a balanced diet rich in fruits, vegetables, and whole grains",
            "Get adequate sleep (7-9 hours per night)",
            "Schedule regular health check-ups with your healthcare provider"
        ])
        
        return recommendations[:6]  # Limit to 6 recommendations
    
    def health_check(self) -> Dict[str, Any]:
        """Return ML service health status"""
        return {
            'models_loaded': self.models_loaded,
            'fallback_mode': self.fallback_mode,
            'models_path': str(self.models_path),
            'available_models': {
                'obesity_model': self.obesity_model is not None,
                'obesity_scaler': self.obesity_scaler is not None,
                'obesity_imputer': self.obesity_imputer is not None,
                'activity_encoder': self.activity_encoder is not None,
                'heart_disease_model': self.heart_disease_model is not None,
                'heart_disease_scaler': self.heart_disease_scaler is not None,
                'metadata': self.model_metadata is not None
            },
            'status': 'ready' if self.models_loaded else 'fallback'
        } 
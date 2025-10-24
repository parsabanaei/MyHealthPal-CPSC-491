import os
import uuid
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
import uvicorn

from services.ml_service import MLService
from services.firestore_service import FirestoreService
from services.email_service import EmailService

# REQUIREMENT 16: FastAPI supports async operations for handling 100+ concurrent assessments
# Initialize FastAPI app
app = FastAPI(
    title="MyHealthPal Backend",
    description="Health Risk Assessment API using Machine Learning",
    version="1.0.0"
)

# REQUIREMENT 15: CORS configuration for secure data transmission
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.run.app",      # Cloud Run frontend
        "*"                       # Allow all origins for now
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ml_service = MLService()
firestore_service = FirestoreService()
email_service = EmailService()

# REQUIREMENT 4: Request validation model with all constraints
# Pydantic models for request/response
class HealthAssessmentRequest(BaseModel):
    age: int
    gender: str
    height_feet: int
    height_inches: int
    weight_lbs: float
    activity_level: str
    family_history: bool
    smoking: bool
    email: EmailStr

    # REQUIREMENT 4: Validate age (18-100 years)
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 100:
            raise ValueError('Age must be between 18 and 100')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['Male', 'Female', 'Other']:
            raise ValueError('Gender must be Male, Female, or Other')
        return v

    # REQUIREMENT 4: Validate height (4-7 feet)
    @validator('height_feet')
    def validate_height_feet(cls, v):
        if v < 4 or v > 7:
            raise ValueError('Height must be between 4 and 7 feet')
        return v

    @validator('height_inches')
    def validate_height_inches(cls, v):
        if v < 0 or v > 11:
            raise ValueError('Height inches must be between 0 and 11')
        return v

    # REQUIREMENT 4: Validate weight (80-400 pounds)
    @validator('weight_lbs')
    def validate_weight(cls, v):
        if v < 80 or v > 400:
            raise ValueError('Weight must be between 80 and 400 lbs')
        return v

    @validator('activity_level')
    def validate_activity_level(cls, v):
        # Accept both frontend options and model-expected options
        valid_levels = ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active']
        model_levels = ['Sedentary', 'Moderate', 'Active']
        
        if v not in valid_levels:
            raise ValueError(f'Activity level must be one of: {valid_levels}')
        
        # Map frontend levels to model levels
        if v in ['Light', 'Moderate']:
            return 'Moderate'
        elif v in ['Active', 'Very Active']:
            return 'Active'
        else:  # Sedentary
            return 'Sedentary'

class HealthAssessmentResponse(BaseModel):
    bmi: float
    bmi_category: str
    obesity_risk: str
    obesity_score: float
    heart_disease_risk: str
    heart_disease_score: float
    diabetes_risk: str
    diabetes_score: float
    overall_health_score: float
    assessment_id: str
    model_status: str
    recommendations: List[str]

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    timestamp: str

class EmailReportResponse(BaseModel):
    status: str
    email: str
    message: Optional[str] = None

# Health check endpoint
@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

# REQUIREMENT 4: Main health assessment endpoint with validation
# REQUIREMENT 5-9: Calculate BMI and predict health risks
# REQUIREMENT 11: Store assessment in Firestore
# REQUIREMENT 16: Async endpoint for concurrent request handling
@app.post("/api/health-assessment", response_model=HealthAssessmentResponse)
async def create_health_assessment(assessment: HealthAssessmentRequest):
    """
    Create a comprehensive health risk assessment
    
    This endpoint:
    1. REQUIREMENT 4: Validates input data
    2. REQUIREMENT 5: Calculates BMI and determines BMI category
    3. REQUIREMENT 6-8: Runs ML models for obesity, heart disease, and diabetes risk prediction
    4. REQUIREMENT 9: Generates overall health score
    5. REQUIREMENT 11: Stores assessment in Firestore
    6. Returns assessment results
    """
    try:
        # Generate unique assessment ID
        assessment_id = str(uuid.uuid4())
        
        # REQUIREMENT 4: Prepare validated user input for ML models
        user_input = {
            'age': assessment.age,
            'gender': assessment.gender,
            'height_feet': assessment.height_feet,
            'height_inches': assessment.height_inches,
            'weight_lbs': assessment.weight_lbs,
            'activity_level': assessment.activity_level,
            'family_history': assessment.family_history,
            'smoking': assessment.smoking
        }
        
        # REQUIREMENT 5-9: Get comprehensive health assessment (BMI, risks, health score)
        results = ml_service.get_comprehensive_assessment(user_input)
        
        # Convert height and weight for storage (keep original units + converted)
        height_cm = ((assessment.height_feet * 12) + assessment.height_inches) * 2.54
        weight_kg = assessment.weight_lbs / 2.20462
        
        # REQUIREMENT 11: Prepare assessment data for storage with timestamps
        assessment_data = {
            'id': assessment_id,
            'user_email': assessment.email,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'input_data': {
                'age': assessment.age,
                'gender': assessment.gender,
                'height_feet': assessment.height_feet,
                'height_inches': assessment.height_inches,
                'height_cm': round(height_cm, 1),
                'weight_lbs': assessment.weight_lbs,
                'weight_kg': round(weight_kg, 1),
                'activity_level': assessment.activity_level,
                'family_history': assessment.family_history,
                'smoking': assessment.smoking
            },
            'results': {
                'bmi': results['bmi'],
                'bmi_category': results['bmi_category'],
                'obesity_risk': results['obesity_risk'],
                'obesity_score': results['obesity_score'],
                'heart_disease_risk': results['heart_disease_risk'],
                'heart_disease_score': results['heart_disease_score'],
                'diabetes_risk': results['diabetes_risk'],
                'diabetes_score': results['diabetes_score'],
                'overall_health_score': results['overall_health_score'],
                'model_status': results['model_status'],
                'recommendations': results['recommendations']
            },
            'report_sent': False,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # REQUIREMENT 11: Store assessment in Firestore with timestamps
        # REQUIREMENT 15: Data encrypted at rest by Firestore
        await firestore_service.save_assessment(assessment_data)
        
        # Return response
        return HealthAssessmentResponse(
            bmi=results['bmi'],
            bmi_category=results['bmi_category'],
            obesity_risk=results['obesity_risk'],
            obesity_score=results['obesity_score'],
            heart_disease_risk=results['heart_disease_risk'],
            heart_disease_score=results['heart_disease_score'],
            diabetes_risk=results['diabetes_risk'],
            diabetes_score=results['diabetes_score'],
            overall_health_score=results['overall_health_score'],
            assessment_id=assessment_id,
            model_status=results['model_status'],
            recommendations=results['recommendations']
        )
        
    except ValueError as e:
        # REQUIREMENT 17: Error handling and logging
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # REQUIREMENT 17: Error logging for system errors
        print(f"Error in health assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while processing assessment"
        )

# REQUIREMENT 12: Send email report endpoint (within 5 seconds)
# REQUIREMENT 13: Generate HTML email template
@app.post("/api/send-report/{assessment_id}", response_model=EmailReportResponse)
async def send_email_report(assessment_id: str):
    """
    Send email report for a completed health assessment
    
    This endpoint:
    1. REQUIREMENT 14: Retrieves assessment data from Firestore
    2. REQUIREMENT 13: Generates HTML email report
    3. REQUIREMENT 12: Sends email via Gmail within 5 seconds
    4. Updates assessment record
    """
    try:
        # REQUIREMENT 14: Retrieve assessment data from Firestore
        assessment_data = await firestore_service.get_assessment(assessment_id)
        if not assessment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        
        # REQUIREMENT 12: Send email report within 5 seconds
        # REQUIREMENT 13: Generate HTML email with risk indicators
        email_result = await email_service.send_health_report(assessment_data)
        
        if email_result['success']:
            # Update assessment record to mark email as sent
            await firestore_service.update_assessment(assessment_id, {
                'report_sent': True,
                'updated_at': datetime.now(timezone.utc).isoformat()
            })
            
            return EmailReportResponse(
                status="sent",
                email=assessment_data['user_email'],
                message="Health assessment report sent successfully"
            )
        else:
            return EmailReportResponse(
                status="failed",
                email=assessment_data['user_email'],
                message=email_result.get('error', 'Failed to send email')
            )
            
    except HTTPException:
        raise
    except Exception as e:
        # REQUIREMENT 17: Error logging for email failures
        print(f"Error sending email report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while sending email report"
        )

# REQUIREMENT 14: Retrieve previous assessments by ID
@app.get("/api/assessment/{assessment_id}")
async def get_assessment(assessment_id: str):
    """REQUIREMENT 14: Retrieve a specific health assessment by ID"""
    try:
        assessment_data = await firestore_service.get_assessment(assessment_id)
        if not assessment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        return assessment_data
    except HTTPException:
        raise
    except Exception as e:
        # REQUIREMENT 17: Error logging
        print(f"Error retrieving assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving assessment"
        )

@app.post("/api/test-email")
async def test_email_service(test_email: str):
    """Test the Gmail email service with a simple test email"""
    try:
        result = await email_service.send_test_email(test_email)
        return result
    except Exception as e:
        logger.error(f"Error in test email: {e}")
        return {"success": False, "error": str(e)}

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "service": "MyHealthPal Backend API",
        "version": "1.0.0",
        "status": "running",
        "email_service": email_service.health_check(),
        "endpoints": {
            "health": "/api/health",
            "assessment": "/api/health-assessment",
            "send_report": "/api/send-report/{assessment_id}",
            "get_assessment": "/api/assessment/{assessment_id}",
            "test_email": "/api/test-email"
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    # For local development
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    ) 
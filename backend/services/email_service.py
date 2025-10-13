import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import asyncio
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    """
    Email service for MyHealthPal health reports using Gmail SMTP
    
    Handles:
    - Sending HTML email reports via Gmail SMTP
    - Generating personalized health report templates
    - Managing email delivery status
    - Error handling and logging
    """
    
    def __init__(self):
        """Initialize email service with Gmail SMTP configuration"""
        # Gmail SMTP Configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # Using 587 (STARTTLS)
        self.smtp_username = "mynutriai@gmail.com"
        self.smtp_password = "nxil yivo tfyo ydea"
        self.sender_email = "mynutriai@gmail.com"
        self.sender_name = "MyHealthPal Health Team"
        
        # Override with environment variables if available (for production security)
        self.smtp_server = os.getenv("SMTP_SERVER", self.smtp_server)
        self.smtp_port = int(os.getenv("SMTP_PORT", self.smtp_port))
        self.smtp_username = os.getenv("SMTP_USERNAME", self.smtp_username)
        self.smtp_password = os.getenv("SMTP_PASSWORD", self.smtp_password)
        self.sender_email = os.getenv("SENDER_EMAIL", self.sender_email)
        
        self.connected = True
        logger.info(f"Gmail email service initialized - SMTP: {self.smtp_server}:{self.smtp_port}")
    
    async def send_health_report(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a comprehensive health assessment report via Gmail SMTP
        
        Args:
            assessment_data: Complete assessment data including results
            
        Returns:
            Dictionary with success status and details
        """
        try:
            user_email = assessment_data.get('user_email')
            if not user_email:
                return {'success': False, 'error': 'No email address provided'}
            
            # Generate HTML email content
            html_content = self._generate_html_report(assessment_data)
            subject = "Your MyHealthPal Health Assessment Report"
            
            # Send via Gmail SMTP
            return await self._send_via_smtp(user_email, subject, html_content, assessment_data)
                
        except Exception as e:
            logger.error(f"Error sending health report: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _send_via_smtp(self, to_email: str, subject: str, html_content: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send email via Gmail SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            assessment_data: Assessment data for logging
            
        Returns:
            Success status and details
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = to_email
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send via SMTP
            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                start_tls=True,
                username=self.smtp_username,
                password=self.smtp_password,
            )
            
            logger.info(f"Email sent successfully to {to_email} via Gmail")
            logger.info(f"Assessment ID: {assessment_data.get('id')}")
            logger.info(f"BMI: {assessment_data.get('results', {}).get('bmi')}")
            logger.info(f"Obesity Risk: {assessment_data.get('results', {}).get('obesity_risk')}")
            logger.info(f"Heart Disease Risk: {assessment_data.get('results', {}).get('heart_disease_risk')}")
            
            return {
                'success': True,
                'message': 'Email sent successfully via Gmail',
                'email': to_email,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'provider': 'Gmail'
            }
            
        except Exception as e:
            logger.error(f"Gmail SMTP error: {e}")
            return {'success': False, 'error': f"SMTP error: {str(e)}"}
    
    def _generate_html_report(self, assessment_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive HTML health assessment report
        
        Args:
            assessment_data: Complete assessment data
            
        Returns:
            HTML email content
        """
        try:
            # Extract data
            input_data = assessment_data.get('input_data', {})
            results = assessment_data.get('results', {})
            assessment_id = assessment_data.get('id', 'N/A')
            timestamp = assessment_data.get('timestamp', datetime.now(timezone.utc).isoformat())
            
            # Generate recommendations (you could integrate ML service here)
            recommendations = self._generate_recommendations(assessment_data)
            
            # HTML template
            html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyHealthPal Health Assessment Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8fafc;
        }
        .header {
            background: linear-gradient(135deg, #10b981, #06b6d4);
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #10b981;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #10b981;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #374151;
        }
        .metric-label {
            color: #6b7280;
            font-size: 14px;
            margin-top: 5px;
        }
        .risk-low { border-left-color: #10b981; }
        .risk-medium { border-left-color: #f59e0b; }
        .risk-high { border-left-color: #ef4444; }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .data-table th, .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        .data-table th {
            background-color: #f3f4f6;
            font-weight: 600;
        }
        .recommendations {
            background: #eff6ff;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }
        .rec-list {
            margin: 10px 0;
            padding-left: 20px;
        }
        .disclaimer {
            background: #fef3c7;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            border-left: 4px solid #f59e0b;
        }
        .disclaimer h3 {
            color: #92400e;
            margin-top: 0;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #6b7280;
            font-size: 14px;
        }

    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 MyHealthPal Health Assessment Report</h1>
        <p>Personalized health insights powered by artificial intelligence</p>
    </div>
    
    <div class="content">
        <!-- Assessment Overview -->
        <div class="section">
            <h2>📊 Assessment Overview</h2>
            <p><strong>Assessment ID:</strong> {{ assessment_id }}</p>
            <p><strong>Date:</strong> {{ assessment_date }}</p>
            <p><strong>Email:</strong> {{ user_email }}</p>
        </div>
        
        <!-- Key Metrics -->
        <div class="section">
            <h2>📈 Your Health Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ bmi }}</div>
                    <div class="metric-label">BMI (kg/m²)</div>
                    <div class="metric-label"><strong>{{ bmi_category }}</strong></div>
                </div>
                <div class="metric-card risk-{{ obesity_risk_class }}">
                    <div class="metric-value">{{ obesity_risk }}</div>
                    <div class="metric-label">Obesity Risk</div>
                </div>
                <div class="metric-card risk-{{ heart_risk_class }}">
                    <div class="metric-value">{{ heart_disease_risk }}</div>
                    <div class="metric-label">Heart Disease Risk</div>
                </div>
            </div>
        </div>
        
        <!-- Input Data Summary -->
        <div class="section">
            <h2>📋 Assessment Data</h2>
            <table class="data-table">
                <tr><th>Parameter</th><th>Your Value</th></tr>
                <tr><td>Age</td><td>{{ age }} years</td></tr>
                <tr><td>Gender</td><td>{{ gender }}</td></tr>
                <tr><td>Height</td><td>{{ height_cm }} cm ({{ height_ft_in }})</td></tr>
                <tr><td>Weight</td><td>{{ weight_kg }} kg ({{ weight_lbs }} lbs)</td></tr>
                <tr><td>Activity Level</td><td>{{ activity_level }}</td></tr>
                <tr><td>Family History of Heart Disease</td><td>{{ family_history }}</td></tr>
                <tr><td>Smoking Status</td><td>{{ smoking_status }}</td></tr>
            </table>
        </div>
        
        <!-- BMI Analysis -->
        <div class="section">
            <h2>⚖️ BMI Analysis</h2>
            <p>Your BMI of <strong>{{ bmi }}</strong> places you in the <strong>{{ bmi_category }}</strong> category.</p>
            <p><strong>BMI Categories:</strong></p>
            <ul>
                <li>Underweight: < 18.5</li>
                <li>Normal Weight: 18.5 - 24.9</li>
                <li>Overweight: 25.0 - 29.9</li>
                <li>Obese: ≥ 30.0</li>
            </ul>
        </div>
        
        <!-- Recommendations -->
        <div class="section">
            <h2>💡 Personalized Recommendations</h2>
            <div class="recommendations">
                <h3>🚨 Immediate Actions</h3>
                <ul class="rec-list">
                    {% for rec in immediate_recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
                
                <h3>🏃‍♂️ Lifestyle Improvements</h3>
                <ul class="rec-list">
                    {% for rec in lifestyle_recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
                
                <h3>🔍 Health Monitoring</h3>
                <ul class="rec-list">
                    {% for rec in monitoring_recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
                
                <h3>👨‍⚕️ Professional Consultation</h3>
                <ul class="rec-list">
                    {% for rec in professional_recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <!-- Next Steps -->
        <div class="section">
            <h2>🎯 Next Steps</h2>
            <p>Based on your assessment results, we recommend:</p>
            <ol>
                <li><strong>Review your results</strong> with a healthcare professional</li>
                <li><strong>Implement gradual lifestyle changes</strong> based on our recommendations</li>
                <li><strong>Monitor your progress</strong> regularly</li>
                <li><strong>Take another assessment</strong> in 3-6 months to track improvements</li>
            </ol>
        </div>
        
        <!-- Disclaimer -->
        <div class="disclaimer">
            <h3>⚠️ Important Medical Disclaimer</h3>
            <p><strong>This assessment is for educational purposes only and is not intended to replace professional medical advice, diagnosis, or treatment.</strong></p>
            <p>Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read in this report.</p>
            <p><strong>In case of a medical emergency, immediately call your doctor or 911.</strong></p>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2025 MyHealthPal - AI-Powered Health Risk Assessment</p>
        <p>For questions about this report, contact: mynutriai@gmail.com</p>
        <p>To retake the assessment, visit: <a href="https://mynutriai-frontend-5m3z5i4pga-uc.a.run.app">MyHealthPal Platform</a></p>
    </div>
</body>
</html>
            """
            
            # Prepare template data
            template_data = {
                'assessment_id': assessment_id,
                'assessment_date': self._format_date(timestamp),
                'user_email': assessment_data.get('user_email', ''),
                
                # Results
                'bmi': results.get('bmi', 'N/A'),
                'bmi_category': results.get('bmi_category', 'N/A'),
                'obesity_risk': results.get('obesity_risk', 'N/A'),
                'heart_disease_risk': results.get('heart_disease_risk', 'N/A'),
                
                # Risk classes for styling
                'obesity_risk_class': results.get('obesity_risk', 'medium').lower(),
                'heart_risk_class': results.get('heart_disease_risk', 'medium').lower(),
                
                # Input data
                'age': input_data.get('age', 'N/A'),
                'gender': input_data.get('gender', 'N/A'),
                'height_cm': round(input_data.get('height_cm', 0), 1),
                'height_ft_in': self._cm_to_feet_inches(input_data.get('height_cm', 0)),
                'weight_kg': round(input_data.get('weight_kg', 0), 1),
                'weight_lbs': round(input_data.get('weight_kg', 0) * 2.20462, 1),
                'activity_level': input_data.get('activity_level', 'N/A'),
                'family_history': 'Yes' if input_data.get('family_history') else 'No',
                'smoking_status': 'Current smoker' if input_data.get('smoking') else 'Non-smoker',
                
                # Recommendations
                'immediate_recommendations': recommendations.get('immediate', ['Continue current health practices']),
                'lifestyle_recommendations': recommendations.get('lifestyle', ['Maintain a balanced diet and regular exercise']),
                'monitoring_recommendations': recommendations.get('monitoring', ['Regular health checkups are recommended']),
                'professional_recommendations': recommendations.get('professional', ['Consult healthcare providers as needed'])
            }
            
            # Render template
            template = Template(html_template)
            html_content = template.render(**template_data)
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return self._generate_fallback_html(assessment_data)
    
    def _generate_recommendations(self, assessment_data: Dict[str, Any]) -> Dict[str, list]:
        """
        Generate health recommendations based on assessment results
        
        Args:
            assessment_data: Complete assessment data
            
        Returns:
            Dictionary with categorized recommendations
        """
        recommendations = {
            'immediate': [],
            'lifestyle': [],
            'monitoring': [],
            'professional': []
        }
        
        try:
            results = assessment_data.get('results', {})
            input_data = assessment_data.get('input_data', {})
            
            bmi = results.get('bmi', 25)
            bmi_category = results.get('bmi_category', 'Normal Weight')
            obesity_risk = results.get('obesity_risk', 'Medium')
            heart_risk = results.get('heart_disease_risk', 'Medium')
            
            # BMI-based recommendations
            if bmi_category == 'Underweight':
                recommendations['professional'].append("Consult a nutritionist for healthy weight gain strategies")
                recommendations['lifestyle'].append("Include nutrient-dense, calorie-rich foods in your diet")
            elif bmi_category == 'Overweight':
                recommendations['immediate'].append("Consider starting a gradual weight loss program")
                recommendations['lifestyle'].append("Focus on portion control and balanced nutrition")
            elif bmi_category == 'Obese':
                recommendations['immediate'].append("Consult a healthcare provider for comprehensive weight management")
                recommendations['professional'].append("Consider working with a registered dietitian")
            
            # Activity recommendations
            activity_level = input_data.get('activity_level', 'Moderate')
            if activity_level in ['Sedentary', 'Light']:
                recommendations['immediate'].append("Gradually increase daily physical activity")
                recommendations['lifestyle'].append("Aim for at least 150 minutes of moderate exercise per week")
                recommendations['lifestyle'].append("Start with 10-minute daily walks and gradually increase")
            
            # Smoking recommendations
            if input_data.get('smoking'):
                recommendations['immediate'].append("Consider smoking cessation programs immediately")
                recommendations['professional'].append("Discuss smoking cessation aids with your doctor")
                recommendations['monitoring'].append("Monitor lung function and cardiovascular health regularly")
            
            # Risk-based recommendations
            if obesity_risk == 'High':
                recommendations['professional'].append("Schedule a comprehensive metabolic health evaluation")
                recommendations['monitoring'].append("Regular monitoring of blood sugar and metabolic markers")
            
            if heart_risk == 'High':
                recommendations['immediate'].append("Schedule a cardiovascular health assessment")
                recommendations['monitoring'].append("Regular blood pressure and cholesterol monitoring")
                recommendations['professional'].append("Consider consultation with a cardiologist")
            
            # Family history recommendations
            if input_data.get('family_history'):
                recommendations['monitoring'].append("Annual cardiovascular screenings due to family history")
                recommendations['professional'].append("Discuss family medical history with your healthcare provider")
            
            # General recommendations
            if not recommendations['lifestyle']:
                recommendations['lifestyle'].append("Maintain a balanced diet rich in fruits, vegetables, and whole grains")
                recommendations['lifestyle'].append("Stay hydrated and limit processed foods")
            
            if not recommendations['monitoring']:
                recommendations['monitoring'].append("Annual health checkups and preventive screenings")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Provide default recommendations
            recommendations = {
                'immediate': ["Continue current health practices"],
                'lifestyle': ["Maintain a balanced diet and regular exercise"],
                'monitoring': ["Regular health checkups"],
                'professional': ["Consult healthcare providers as needed"]
            }
        
        return recommendations
    
    def _format_date(self, iso_date: str) -> str:
        """Format ISO date string to readable format"""
        try:
            dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y at %I:%M %p UTC')
        except:
            return iso_date
    
    def _cm_to_feet_inches(self, cm: float) -> str:
        """Convert centimeters to feet and inches"""
        try:
            total_inches = cm * 0.393701
            feet = int(total_inches // 12)
            inches = int(total_inches % 12)
            return f"{feet}' {inches}\""
        except:
            return "N/A"
    
    def _generate_fallback_html(self, assessment_data: Dict[str, Any]) -> str:
        """Generate simple fallback HTML if main template fails"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>MyHealthPal Health Assessment Report</h1>
            <p>Assessment ID: {assessment_data.get('id', 'N/A')}</p>
            <p>Thank you for using MyHealthPal. Your health assessment has been completed.</p>
            <p>For detailed results, please visit our platform or contact support.</p>
            <p><strong>Disclaimer:</strong> This is for educational purposes only and not a substitute for professional medical advice.</p>
        </body>
        </html>
        """
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check email service health
        
        Returns:
            Health status dictionary
        """
        return {
            'status': 'ready',
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'sender_email': self.sender_email,
            'provider': 'Gmail'
        }
    
    async def send_test_email(self, to_email: str) -> Dict[str, Any]:
        """
        Send a test email to verify Gmail functionality
        
        Args:
            to_email: Test recipient email
            
        Returns:
            Test result dictionary
        """
        test_assessment = {
            'id': 'test-assessment-gmail',
            'user_email': to_email,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'input_data': {
                'age': 30,
                'gender': 'Male',
                'height_cm': 175.0,
                'weight_kg': 70.0,
                'activity_level': 'Moderate',
                'family_history': False,
                'smoking': False
            },
            'results': {
                'bmi': 22.9,
                'bmi_category': 'Normal Weight',
                'obesity_risk': 'Low',
                'heart_disease_risk': 'Low'
            }
        }
        
        return await self.send_health_report(test_assessment) 
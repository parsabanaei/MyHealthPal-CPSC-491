# MyHealthPal - AI-Powered Health Risk Assessment

MyHealthPal is a cloud-based health analytics web application that provides personalized health risk assessments using machine learning. Users input health data and receive automated email reports with BMI calculations and risk predictions.

## 🚀 Features

- **AI-Powered Analysis**: Advanced machine learning models for obesity and heart disease risk assessment
- **Real-time BMI Calculator**: Instant BMI calculation with category classification
- **Comprehensive Health Form**: Collects age, gender, physical measurements, activity level, family history, and smoking status
- **Email Reports**: Automated HTML email reports with personalized recommendations
- **Cloud Infrastructure**: Deployed on Google Cloud Platform with Firestore database
- **Responsive Design**: Mobile-friendly interface built with React and Tailwind CSS
- **Health Awareness**: Educational content about BMI categories and risk factors

## 🏗️ Architecture

### Frontend (React.js)

- **Port**: 3000
- **Framework**: React 18 with React Router
- **Styling**: Tailwind CSS with custom health theme
- **State Management**: React Hook Form for form handling
- **API Client**: Axios for backend communication
- **Icons**: Lucide React

### Backend (FastAPI)

- **Port**: 8000
- **Framework**: FastAPI with Pydantic validation
- **ML Models**: Mock implementations with realistic algorithms
- **Database**: Google Firestore for assessment storage
- **Email Service**: Mock Gmail API integration
- **Features**: Health check endpoints, comprehensive validation, error handling

### Cloud Infrastructure

- **Platform**: Google Cloud Platform
- **Compute**: Cloud Run (containerized deployment)
- **Database**: Firestore (NoSQL document database)
- **Build**: Cloud Build for CI/CD
- **Region**: us-central1

## 📋 Prerequisites

1. **Google Cloud SDK**: Install and configure gcloud CLI
2. **Google Cloud Project**: Project ID `mynutriai`
3. **Enabled APIs**: Cloud Run, Cloud Build, Firestore, Storage
4. **Authentication**: `gcloud auth login`

## 🚀 Quick Start

### One-Command Deployment

```bash
# Clone the repository
git clone <repository-url>
cd MyHealthPal

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project mynutriai

# Deploy the entire application
./deploy.sh
```

### Manual Setup (Development)

#### Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm start
```

## 🔧 Configuration

### Environment Variables

#### Frontend (.env.production)

```
REACT_APP_API_URL=<backend-url>
```

#### Backend

```
GOOGLE_CLOUD_PROJECT=mynutriai
PORT=8000
```

### Project Structure

```
MyHealthPal/
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/             # Page components
│   │   └── services/          # API configuration
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── Dockerfile            # Frontend container
│   └── .gcloudignore         # Cloud Build ignore
├── backend/                     # FastAPI application
│   ├── services/              # Business logic services
│   ├── models/               # ML model files (mock)
│   ├── templates/            # Email templates
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── .gcloudignore       # Cloud Build ignore
├── deploy.sh                   # Deployment script
└── README.md                  # Project documentation
```

## 📊 API Endpoints

### Health Check

```
GET /api/health
Response: {"status": "healthy", "version": "1.0.0", "timestamp": "..."}
```

### Health Assessment

```
POST /api/health-assessment
Content-Type: application/json

Request Body:
{
  "age": 35,
  "gender": "Male",
  "height_cm": 175.0,
  "weight_kg": 80.0,
  "activity_level": "Moderate",
  "family_history": false,
  "smoking": false,
  "email": "user@example.com"
}

Response:
{
  "bmi": 26.1,
  "bmi_category": "Overweight",
  "obesity_risk": "Medium",
  "heart_disease_risk": "Low",
  "assessment_id": "uuid"
}
```

### Send Email Report

```
POST /api/send-report/{assessment_id}
Response: {"status": "sent", "email": "user@example.com"}
```

## 🔍 Health Assessment Features

### BMI Calculation

- **Formula**: weight (kg) / height (m)²
- **Categories**: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (≥30)
- **Real-time Updates**: BMI updates as user types

### Risk Assessment

- **Obesity Risk**: Based on BMI, age, activity level, family history
- **Heart Disease Risk**: Incorporates cardiovascular risk factors
- **Levels**: Low, Medium, High

### Personalized Recommendations

- **Immediate Actions**: Urgent health steps
- **Lifestyle Changes**: Diet and exercise recommendations
- **Health Monitoring**: Screening and checkup advice
- **Professional Consultation**: When to see healthcare providers

## 📧 Email Reports

### Features

- **HTML Format**: Professional, mobile-responsive design
- **Comprehensive Data**: All input parameters and results
- **Visual Metrics**: Color-coded risk indicators
- **Recommendations**: Personalized health advice
- **Medical Disclaimer**: Important legal disclaimers

### Sample Report Sections

1. Assessment Overview
2. Key Health Metrics
3. Input Data Summary
4. BMI Analysis
5. Personalized Recommendations
6. Next Steps
7. Medical Disclaimer

## 🛡️ Security & Privacy

### Data Protection

- **Encryption**: All data encrypted in transit and at rest
- **HIPAA Compliance**: Healthcare data protection standards
- **Firestore Security**: Restrictive database rules
- **Authentication**: Service account-based access

### Privacy Policy

- **Data Collection**: Only essential health information
- **Data Usage**: Exclusively for risk assessment and reports
- **Data Retention**: Stored for service improvement
- **User Rights**: Data deletion upon request

## 🔧 Development

### Adding New Features

1. **Frontend**: Add components in `frontend/src/components/`
2. **Backend**: Add endpoints in `backend/main.py`
3. **Services**: Extend services in `backend/services/`
4. **Deploy**: Run `./deploy.sh` to update

### Testing

- **Frontend**: `npm test`
- **Backend**: `pytest` (add test files)
- **Integration**: Test via deployed endpoints

### Monitoring

```bash
# View application logs
gcloud run services logs read mynutriai-frontend --region=us-central1
gcloud run services logs read mynutriai-backend --region=us-central1

# Check service status
gcloud run services list --region=us-central1
```

## 📈 Performance

### Optimization

- **Frontend**: Code splitting, image optimization
- **Backend**: Efficient ML model loading, caching
- **Database**: Indexed queries, batch operations
- **CDN**: Static asset delivery optimization

### Scaling

- **Auto-scaling**: Cloud Run handles traffic spikes
- **Resource Limits**: Configurable memory and CPU
- **Geographic Distribution**: Multi-region deployment ready

## 🚨 Important Disclaimers

### Medical Disclaimer

**This platform is for educational and informational purposes only.** The health risk assessments and recommendations provided by MyHealthPal are not intended to replace professional medical advice, diagnosis, or treatment.

**Always seek the advice of your physician or other qualified health provider** with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read on this platform.

**In case of a medical emergency, immediately call your doctor or 911.**

### Technology Disclaimer

- **Mock Implementation**: ML models use algorithmic predictions, not trained models
- **Development Stage**: This is a demonstration application
- **Production Use**: Requires additional validation and testing

## 📞 Support

### Contact Information

- **Email**: support@mynutriai.com
- **Privacy**: privacy@mynutriai.com
- **Emergency**: Contact your healthcare provider or 911

### Troubleshooting

1. **Deployment Issues**: Check gcloud authentication and project settings
2. **API Errors**: Verify environment variables and service URLs
3. **Frontend Issues**: Clear browser cache and check network connectivity

## 📄 License

This project is for educational purposes. See LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Platform for infrastructure
- React and FastAPI communities
- Tailwind CSS for styling framework
- Lucide React for icons

---

**Built with ❤️ for health awareness and education**

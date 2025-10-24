import React from 'react';
import { Brain, Heart, Shield, TrendingUp, Users, Award } from 'lucide-react';
import HealthForm from '../components/HealthForm';

// REQUIREMENT 1: Display MyHealthPal landing page
// REQUIREMENT 19: Display medical disclaimers
// REQUIREMENT 22: Responsive design for different devices
const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* REQUIREMENT 1: Hero Section of landing page */}
      {/* REQUIREMENT 22: Responsive layout */}
      <section className="bg-gradient-to-br from-health-primary to-health-accent text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-white/20 rounded-full">
                  <Brain className="h-12 w-12 text-white" />
                </div>
                <div className="p-3 bg-white/20 rounded-full">
                  <Heart className="h-12 w-12 text-white" />
                </div>
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              MyHealthPal
            </h1>
            <p className="text-xl md:text-2xl mb-4 opacity-90">
              AI-Powered Health Risk Assessment
            </p>
            <p className="text-lg md:text-xl mb-8 max-w-3xl mx-auto opacity-80">
              Get personalized health insights and risk assessments using advanced machine learning. 
              Make informed decisions about your wellness journey with data-driven recommendations.
            </p>
            
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="flex items-center space-x-2 bg-white/20 px-4 py-2 rounded-full">
                <Shield className="h-4 w-4" />
                <span>HIPAA Compliant</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/20 px-4 py-2 rounded-full">
                <Award className="h-4 w-4" />
                <span>ML-Powered</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/20 px-4 py-2 rounded-full">
                <TrendingUp className="h-4 w-4" />
                <span>Instant Results</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Comprehensive Health Assessment
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our platform analyzes multiple health factors to provide you with accurate, 
              personalized risk assessments and actionable health insights.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Feature 1 */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-health-primary/10 rounded-full flex items-center justify-center mb-4">
                <Brain className="h-8 w-8 text-health-primary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Advanced machine learning models analyze your health data for accurate risk predictions.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-health-accent/10 rounded-full flex items-center justify-center mb-4">
                <Heart className="h-8 w-8 text-health-accent" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Heart Health</h3>
              <p className="text-gray-600">
                Comprehensive cardiovascular risk assessment based on lifestyle and medical history.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-health-secondary/10 rounded-full flex items-center justify-center mb-4">
                <TrendingUp className="h-8 w-8 text-health-secondary" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">BMI Tracking</h3>
              <p className="text-gray-600">
                Real-time BMI calculation with obesity risk assessment and recommendations.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-health-warning/10 rounded-full flex items-center justify-center mb-4">
                <Users className="h-8 w-8 text-health-warning" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Family History</h3>
              <p className="text-gray-600">
                Considers genetic predispositions and family medical history in risk calculations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600">
              Get your personalized health assessment in three simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="mx-auto w-12 h-12 bg-health-primary text-white rounded-full flex items-center justify-center mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Complete Assessment</h3>
              <p className="text-gray-600">
                Fill out our comprehensive health questionnaire with your personal information, 
                measurements, and lifestyle factors.
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="mx-auto w-12 h-12 bg-health-accent text-white rounded-full flex items-center justify-center mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Analysis</h3>
              <p className="text-gray-600">
                Our machine learning models process your data to calculate BMI, obesity risk, 
                and cardiovascular health indicators.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="mx-auto w-12 h-12 bg-health-secondary text-white rounded-full flex items-center justify-center mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Get Results</h3>
              <p className="text-gray-600">
                Receive instant results and a detailed email report with personalized 
                recommendations for improving your health.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Health Assessment Form Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <HealthForm />
        </div>
      </section>

      {/* REQUIREMENT 19: Medical disclaimer stating tool is not medical advice */}
      <section className="py-12 bg-yellow-50 border-t border-yellow-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg p-6 border border-yellow-200">
            <div className="flex items-start space-x-3">
              <Shield className="h-6 w-6 text-yellow-600 mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Important Medical Disclaimer</h3>
                <div className="text-sm text-gray-700 space-y-2">
                {/* REQUIREMENT 19: Disclaimer stating platform is educational only */}
                <p>
                  <strong>This platform is for educational and informational purposes only.</strong> 
                  The health risk assessments and recommendations provided by MyHealthPal are not 
                  intended to replace professional medical advice, diagnosis, or treatment.
                </p>
                  <p>
                    Always seek the advice of your physician or other qualified health provider 
                    with any questions you may have regarding a medical condition. Never disregard 
                    professional medical advice or delay in seeking it because of something you 
                    have read on this platform.
                  </p>
                  <p>
                    <strong>In case of a medical emergency, immediately call your doctor or 911.</strong>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home; 
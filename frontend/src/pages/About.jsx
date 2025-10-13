import React from 'react';
import { Brain, Shield, Lock, Server, Award, Users, TrendingUp, Heart } from 'lucide-react';

const About = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <section className="bg-gradient-to-br from-health-secondary to-health-primary text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">About MyHealthPal</h1>
          <p className="text-xl md:text-2xl opacity-90">
            Revolutionizing personal health assessment through artificial intelligence
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Platform</h2>
            <p className="text-lg text-gray-600 leading-relaxed">
              MyHealthPal is a cutting-edge health analytics platform that leverages machine learning 
              to provide personalized health risk assessments. Our mission is to democratize access 
              to advanced health insights, empowering individuals to make informed decisions about 
              their wellness journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-health-primary mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">AI-Powered Analysis</h3>
              </div>
              <p className="text-gray-600">
                Our platform utilizes advanced machine learning algorithms trained on comprehensive 
                health datasets to analyze multiple risk factors and provide accurate assessments 
                for obesity and cardiovascular disease.
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <TrendingUp className="h-8 w-8 text-health-accent mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Instant Results</h3>
              </div>
              <p className="text-gray-600">
                Get immediate feedback on your health metrics including BMI calculation, obesity 
                risk assessment, and cardiovascular health indicators, all processed in real-time 
                through our cloud infrastructure.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How Risk Assessment Works */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">How Our Risk Assessment Works</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Our platform analyzes multiple health indicators using scientifically-validated models 
              to provide comprehensive risk assessments.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-10 h-10 bg-health-primary rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">1</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Data Collection</h3>
                  <p className="text-gray-600">
                    We collect essential health metrics including age, gender, height, weight, 
                    activity level, family history, and smoking status.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-10 h-10 bg-health-accent rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">2</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">BMI Calculation</h3>
                  <p className="text-gray-600">
                    Automatic calculation of Body Mass Index using the standard formula: 
                    weight (kg) / height (m)². Results are categorized into standard BMI ranges.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-10 h-10 bg-health-secondary rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">3</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Risk Modeling</h3>
                  <p className="text-gray-600">
                    Machine learning models analyze your data against established health patterns 
                    to assess obesity and cardiovascular disease risk levels.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-10 h-10 bg-health-warning rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">4</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Report Generation</h3>
                  <p className="text-gray-600">
                    Comprehensive HTML email reports with personalized recommendations 
                    and actionable health insights based on your assessment results.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">Assessment Factors</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Body Mass Index (BMI)</span>
                  <Heart className="h-5 w-5 text-health-primary" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Age & Gender</span>
                  <Users className="h-5 w-5 text-health-accent" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Physical Activity Level</span>
                  <TrendingUp className="h-5 w-5 text-health-secondary" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Family Medical History</span>
                  <Users className="h-5 w-5 text-health-warning" />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Smoking Status</span>
                  <Shield className="h-5 w-5 text-health-danger" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Technology & Infrastructure</h2>
            <p className="text-lg text-gray-600">
              Built on Google Cloud Platform with enterprise-grade security and scalability
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Server className="h-8 w-8 text-health-primary mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Cloud Infrastructure</h3>
              </div>
              <ul className="text-gray-600 space-y-2">
                <li>• Google Cloud Run for scalable containerized deployment</li>
                <li>• Firestore for secure, real-time data storage</li>
                <li>• Cloud Build for automated CI/CD pipelines</li>
                <li>• Global load balancing for optimal performance</li>
              </ul>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Lock className="h-8 w-8 text-health-accent mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Security & Privacy</h3>
              </div>
              <ul className="text-gray-600 space-y-2">
                <li>• End-to-end data encryption in transit and at rest</li>
                <li>• HIPAA-compliant data handling procedures</li>
                <li>• Secure service account authentication</li>
                <li>• Regular security audits and monitoring</li>
              </ul>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-health-secondary mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Machine Learning</h3>
              </div>
              <ul className="text-gray-600 space-y-2">
                <li>• Scikit-learn based prediction models</li>
                <li>• Ensemble methods for improved accuracy</li>
                <li>• Feature scaling and preprocessing pipelines</li>
                <li>• Cross-validated model performance metrics</li>
              </ul>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Award className="h-8 w-8 text-health-warning mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Quality Assurance</h3>
              </div>
              <ul className="text-gray-600 space-y-2">
                <li>• Comprehensive input validation and sanitization</li>
                <li>• Real-time error monitoring and alerting</li>
                <li>• Automated testing and deployment pipelines</li>
                <li>• Performance optimization and monitoring</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Privacy Policy Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center mb-6">
              <Shield className="h-8 w-8 text-health-primary mr-3" />
              <h2 className="text-3xl font-bold text-gray-900">Privacy Policy</h2>
            </div>

            <div className="space-y-6 text-gray-700">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Collection</h3>
                <p>
                  We collect only the health information necessary to provide accurate risk assessments. 
                  This includes basic demographic information, physical measurements, lifestyle factors, 
                  and medical history relevant to cardiovascular and obesity risk calculation.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Usage</h3>
                <p>
                  Your health data is used exclusively for generating your personalized risk assessment 
                  and email report. We do not share, sell, or use your information for marketing purposes. 
                  Data may be anonymized and aggregated for improving our machine learning models.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Security</h3>
                <p>
                  All data is encrypted in transit and at rest using industry-standard encryption protocols. 
                  Our infrastructure follows Google Cloud's security best practices and undergoes regular 
                  security audits to ensure compliance with healthcare data protection standards.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Data Retention</h3>
                <p>
                  Assessment data is retained for analytical purposes and service improvement. 
                  You may request deletion of your data at any time by contacting our support team. 
                  Email reports are sent once and not stored on our servers.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Contact Information</h3>
                <p>
                  For questions about our privacy practices or to request data deletion, 
                  please contact us at <strong>privacy@mynutriai.com</strong>. 
                  We are committed to responding to all privacy inquiries within 48 hours.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-12 bg-yellow-50 border-t border-yellow-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg p-6 border border-yellow-200">
            <div className="flex items-start space-x-3">
              <Shield className="h-6 w-6 text-yellow-600 mt-1 flex-shrink-0" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Medical Disclaimer</h3>
                <p className="text-sm text-gray-700">
                  MyHealthPal provides educational health insights and risk assessments based on 
                  machine learning analysis. This platform is not intended to replace professional 
                  medical advice, diagnosis, or treatment. Always consult with qualified healthcare 
                  providers for medical decisions and emergency situations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About; 
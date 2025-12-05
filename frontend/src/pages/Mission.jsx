import React from 'react';
import { Heart, Target, Users, Globe, Shield, TrendingUp, Award, Brain } from 'lucide-react';

const Mission = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <section className="bg-gradient-to-br from-health-accent to-health-secondary text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Our Mission</h1>
          <p className="text-xl md:text-2xl opacity-90">
            Democratizing health awareness through accessible AI-driven insights
          </p>
        </div>
      </section>

      {/* Core Mission */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="p-4 bg-health-primary/10 rounded-full">
                <Target className="h-12 w-12 text-health-primary" />
              </div>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Empowering Health Awareness</h2>
            <p className="text-xl text-gray-600 leading-relaxed">
              At MyHealthPal AI, we believe that everyone deserves access to personalized health insights. 
              Our mission is to bridge the gap between advanced medical analytics and individual 
              health awareness, making sophisticated risk assessment tools accessible to all.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-health-primary/5 to-health-accent/5 rounded-lg p-6 border border-health-primary/20">
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-health-primary mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Advancing Prevention</h3>
              </div>
              <p className="text-gray-700">
                By providing early risk identification through AI analysis, we enable individuals 
                to take proactive steps toward better health outcomes before problems develop.
              </p>
            </div>

            <div className="bg-gradient-to-br from-health-accent/5 to-health-secondary/5 rounded-lg p-6 border border-health-accent/20">
              <div className="flex items-center mb-4">
                <Users className="h-8 w-8 text-health-accent mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">Building Community</h3>
              </div>
              <p className="text-gray-700">
                We foster health consciousness by providing tools that help individuals make 
                informed decisions and engage meaningfully with healthcare providers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Goals Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Health Awareness Goals</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              We are committed to advancing public health through education, technology, and accessibility
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Goal 1: Education */}
            <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-center w-16 h-16 bg-health-primary/10 rounded-full mx-auto mb-4">
                <Award className="h-8 w-8 text-health-primary" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Health Education</h3>
              <p className="text-gray-600 text-center mb-4">
                Provide clear, understandable health information that empowers individuals to make informed decisions.
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• BMI education and healthy weight ranges</li>
                <li>• Cardiovascular risk factor awareness</li>
                <li>• Lifestyle impact on health outcomes</li>
                <li>• When to consult healthcare professionals</li>
              </ul>
            </div>

            {/* Goal 2: Accessibility */}
            <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-center w-16 h-16 bg-health-accent/10 rounded-full mx-auto mb-4">
                <Globe className="h-8 w-8 text-health-accent" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Universal Access</h3>
              <p className="text-gray-600 text-center mb-4">
                Make advanced health analytics accessible to everyone, regardless of location or resources.
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Free health risk assessments</li>
                <li>• Mobile-responsive platform design</li>
                <li>• Multi-language support (planned)</li>
                <li>• No registration required for assessments</li>
              </ul>
            </div>

            {/* Goal 3: Prevention */}
            <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-center w-16 h-16 bg-health-secondary/10 rounded-full mx-auto mb-4">
                <Heart className="h-8 w-8 text-health-secondary" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 text-center">Disease Prevention</h3>
              <p className="text-gray-600 text-center mb-4">
                Focus on early identification and prevention of chronic diseases through risk assessment.
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Early obesity risk detection</li>
                <li>• Cardiovascular disease prevention</li>
                <li>• Lifestyle modification recommendations</li>
                <li>• Screening guideline awareness</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Core Values</h2>
            <p className="text-lg text-gray-600">
              The principles that guide our mission and platform development
            </p>
          </div>

          <div className="space-y-8">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-health-primary rounded-full flex items-center justify-center">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Privacy & Security First</h3>
                <p className="text-gray-600">
                  We prioritize user privacy and data security above all else. Your health information 
                  is encrypted, protected, and never shared without explicit consent. We maintain 
                  transparency about our data practices and give users control over their information.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-health-accent rounded-full flex items-center justify-center">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Evidence-Based Technology</h3>
                <p className="text-gray-600">
                  Our machine learning models are built on peer-reviewed research and validated datasets. 
                  We continuously update our algorithms based on the latest scientific evidence and 
                  maintain high standards for accuracy and reliability.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-health-secondary rounded-full flex items-center justify-center">
                <Users className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Ethical AI Development</h3>
                <p className="text-gray-600">
                  We are committed to developing AI systems that are fair, unbiased, and beneficial. 
                  Our models are tested for bias across different demographics, and we continuously 
                  work to improve representation and accuracy for all users.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-health-warning rounded-full flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Continuous Improvement</h3>
                <p className="text-gray-600">
                  We believe in iterative improvement and user-centered design. We regularly update 
                  our platform based on user feedback, scientific advances, and technology improvements 
                  to provide the best possible experience and accuracy.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Impact & Future */}
      <section className="py-16 bg-gradient-to-br from-health-primary/5 to-health-accent/5">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Vision for the Future</h2>
            <p className="text-lg text-gray-600">
              Looking ahead to expand our impact on global health awareness
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Short-term Goals (2025)</h3>
              <ul className="text-gray-600 space-y-2">
                <li>• Expand ML models to include diabetes risk assessment</li>
                <li>• Implement multi-language support for global accessibility</li>
                <li>• Develop mobile applications for iOS and Android</li>
                <li>• Partner with healthcare organizations for broader reach</li>
                <li>• Launch health awareness educational content library</li>
              </ul>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Long-term Vision (2026+)</h3>
              <ul className="text-gray-600 space-y-2">
                <li>• Integration with wearable devices and health trackers</li>
                <li>• Personalized health coaching recommendations</li>
                <li>• Community features for health goal sharing</li>
                <li>• Healthcare provider integration and referral systems</li>
                <li>• AI-powered nutrition and exercise recommendations</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Join Our Mission</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Help us democratize health awareness by using our platform, sharing feedback, 
            and spreading awareness about the importance of preventive health measures.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/" 
              className="px-8 py-3 bg-health-primary hover:bg-health-primary/90 text-white font-semibold rounded-lg transition-colors"
            >
              Take Assessment
            </a>
            <a 
              href="/about" 
              className="px-8 py-3 border border-health-primary text-health-primary hover:bg-health-primary/10 font-semibold rounded-lg transition-colors"
            >
              Learn More
            </a>
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
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Important Health Disclaimer</h3>
                <div className="text-sm text-gray-700 space-y-2">
                  <p>
                    <strong>Educational Purpose Only:</strong> MyHealthPal AI is designed for educational 
                    and awareness purposes. Our risk assessments provide general health insights 
                    based on population data and should not be considered medical diagnoses.
                  </p>
                  <p>
                    <strong>Professional Medical Care:</strong> Always consult with qualified 
                    healthcare professionals for medical advice, diagnosis, treatment, and 
                    health management decisions. This platform does not replace professional medical care.
                  </p>
                  <p>
                    <strong>Emergency Situations:</strong> In case of medical emergencies, 
                    immediately contact emergency services (911) or your healthcare provider. 
                    Do not rely on this platform for urgent medical situations.
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

export default Mission; 
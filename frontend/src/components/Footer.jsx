import React from 'react';
import { Heart, Shield, Mail } from 'lucide-react';

// REQUIREMENT 18: Provide contact email for technical support
// REQUIREMENT 22: Responsive design for different devices
const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* REQUIREMENT 22: Responsive grid layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-health-primary to-health-accent rounded-lg">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold">MyHealthPal</h3>
                <p className="text-sm text-gray-400">Health Risk Assessment</p>
              </div>
            </div>
            <p className="text-gray-400 text-sm max-w-md">
              Empowering individuals with AI-driven health insights for better wellness decisions.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">Quick Links</h4>
            <div className="space-y-2">
              <a href="/about" className="block text-gray-400 hover:text-health-primary transition-colors">
                About Platform
              </a>
              <a href="/mission" className="block text-gray-400 hover:text-health-primary transition-colors">
                Our Mission
              </a>
              <a href="#privacy" className="block text-gray-400 hover:text-health-primary transition-colors">
                Privacy Policy
              </a>
              <a href="#terms" className="block text-gray-400 hover:text-health-primary transition-colors">
                Terms of Service
              </a>
            </div>
          </div>

          {/* REQUIREMENT 18: Contact information for technical support */}
          <div className="space-y-4">
            <h4 className="text-lg font-semibold">Important Information</h4>
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <Shield className="h-5 w-5 text-health-warning mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-400">
                  This platform provides educational health insights only. Always consult healthcare professionals for medical decisions.
                </p>
              </div>
              {/* REQUIREMENT 18: Contact email for technical support */}
              <div className="flex items-start space-x-2">
                <Mail className="h-5 w-5 text-health-accent mt-0.5 flex-shrink-0" />
                <div className="text-sm text-gray-400">
                  <p>Contact: support@mynutriai.com</p>
                  <p>Emergency: Contact your healthcare provider</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2025 MyHealthPal. All rights reserved. | 
            <span className="text-health-warning"> Not a substitute for professional medical advice.</span>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
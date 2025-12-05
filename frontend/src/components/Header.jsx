import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Heart, Activity } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-lg border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo and Brand */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-health-primary to-health-accent rounded-lg">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">MyHealthPal AI</h1>
              <p className="text-sm text-health-primary">Health Risk Assessment</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'text-health-primary bg-health-primary/10' 
                  : 'text-gray-600 hover:text-health-primary hover:bg-gray-50'
              }`}
            >
              Home
            </Link>
            <Link
              to="/about"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/about') 
                  ? 'text-health-primary bg-health-primary/10' 
                  : 'text-gray-600 hover:text-health-primary hover:bg-gray-50'
              }`}
            >
              About
            </Link>
            <Link
              to="/mission"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/mission') 
                  ? 'text-health-primary bg-health-primary/10' 
                  : 'text-gray-600 hover:text-health-primary hover:bg-gray-50'
              }`}
            >
              Mission
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden p-2 rounded-md text-gray-600 hover:text-health-primary hover:bg-gray-50">
            <Activity className="h-6 w-6" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header; 
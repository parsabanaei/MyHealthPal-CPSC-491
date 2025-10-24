import React from 'react';
import { Calculator, TrendingUp } from 'lucide-react';

// REQUIREMENT 3: When the user enters their height and weight, the system calculates their BMI in real-time
// REQUIREMENT 5: When the BMI is calculated, the system categorizes it as Underweight, Normal, Overweight, or Obese
const BMICalculator = ({ heightCm, weightKg }) => {
  // REQUIREMENT 3: Calculate BMI in real-time
  const calculateBMI = () => {
    if (!heightCm || !weightKg || heightCm <= 0 || weightKg <= 0) {
      return null;
    }
    const heightM = heightCm / 100;
    return (weightKg / (heightM * heightM)).toFixed(1);
  };

  // REQUIREMENT 5: Get BMI category - Underweight, Normal, Overweight, or Obese
  const getBMICategory = (bmi) => {
    if (!bmi) return { category: 'Enter height and weight', className: 'text-gray-500', bgClass: 'bg-gray-50' };
    
    const bmiValue = parseFloat(bmi);
    // REQUIREMENT 5: BMI < 18.5 = Underweight
    if (bmiValue < 18.5) {
      return { 
        category: 'Underweight', 
        className: 'text-blue-600', 
        bgClass: 'bg-blue-50 border-blue-200',
        description: 'Below normal weight range'
      };
    // REQUIREMENT 5: BMI 18.5-24.9 = Normal Weight
    } else if (bmiValue < 25) {
      return { 
        category: 'Normal Weight', 
        className: 'text-green-600', 
        bgClass: 'bg-green-50 border-green-200',
        description: 'Healthy weight range'
      };
    // REQUIREMENT 5: BMI 25-29.9 = Overweight
    } else if (bmiValue < 30) {
      return { 
        category: 'Overweight', 
        className: 'text-yellow-600', 
        bgClass: 'bg-yellow-50 border-yellow-200',
        description: 'Above normal weight range'
      };
    // REQUIREMENT 5: BMI >= 30 = Obese
    } else {
      return { 
        category: 'Obese', 
        className: 'text-red-600', 
        bgClass: 'bg-red-50 border-red-200',
        description: 'Significantly above normal weight'
      };
    }
  };

  const bmi = calculateBMI();
  const { category, className, bgClass, description } = getBMICategory(bmi);

  return (
    <div className={`p-6 rounded-lg border-2 transition-all duration-300 ${bgClass || 'bg-gray-50 border-gray-200'}`}>
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-white rounded-lg shadow-sm">
          <Calculator className="h-5 w-5 text-health-primary" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-900">BMI Calculator</h3>
          <p className="text-sm text-gray-600">Real-time body mass index</p>
        </div>
      </div>

      {/* BMI Value Display */}
      <div className="text-center mb-4">
        <div className="text-3xl font-bold text-gray-900 mb-1">
          {bmi || '--'}
          {bmi && <span className="text-lg font-normal text-gray-600 ml-1">kg/m²</span>}
        </div>
        <div className={`text-lg font-semibold ${className}`}>
          {category}
        </div>
        {description && (
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        )}
      </div>

      {/* BMI Scale Visual */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-600 mb-1">
          <span>Underweight</span>
          <span>Normal</span>
          <span>Overweight</span>
          <span>Obese</span>
        </div>
        <div className="flex h-2 rounded-full overflow-hidden">
          <div className="flex-1 bg-blue-300"></div>
          <div className="flex-1 bg-green-400"></div>
          <div className="flex-1 bg-yellow-400"></div>
          <div className="flex-1 bg-red-400"></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>&lt;18.5</span>
          <span>18.5-24.9</span>
          <span>25-29.9</span>
          <span>≥30</span>
        </div>
      </div>

      {/* Current Position Indicator */}
      {bmi && (
        <div className="flex items-center justify-center space-x-2 text-sm">
          <TrendingUp className="h-4 w-4 text-health-accent" />
          <span className="text-gray-600">
            Your BMI: <span className={`font-semibold ${className}`}>{bmi}</span>
          </span>
        </div>
      )}

      {/* BMI Categories Reference */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">BMI Categories:</h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-300 rounded"></div>
            <span>&lt; 18.5 Underweight</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-400 rounded"></div>
            <span>18.5-24.9 Normal</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-yellow-400 rounded"></div>
            <span>25-29.9 Overweight</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-400 rounded"></div>
            <span>≥ 30 Obese</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BMICalculator; 
import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { User, Mail, Heart, Activity, Ruler, Scale, Users, Cigarette, Send, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import BMICalculator from './BMICalculator';
import api from '../services/api';

const HealthForm = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [assessmentResults, setAssessmentResults] = useState(null);
  const [heightCm, setHeightCm] = useState(0);
  const [weightKg, setWeightKg] = useState(0);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset
  } = useForm();

  // Watch form values for real-time BMI calculation
  const watchedValues = watch();

  // Convert feet/inches to cm for BMI calculation
  useEffect(() => {
    const { heightFeet, heightInches } = watchedValues;
    if (heightFeet && heightInches !== undefined) {
      const totalInches = parseInt(heightFeet) * 12 + parseInt(heightInches || 0);
      const cm = totalInches * 2.54;
      setHeightCm(cm);
    }
  }, [watchedValues.heightFeet, watchedValues.heightInches]);

  // Convert lbs to kg for BMI calculation
  useEffect(() => {
    const { weight } = watchedValues;
    if (weight) {
      const kg = parseFloat(weight) * 0.453592;
      setWeightKg(kg);
    }
  }, [watchedValues.weight]);

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const payload = {
        age: parseInt(data.age),
        gender: data.gender,
        height_feet: parseInt(data.heightFeet),
        height_inches: parseInt(data.heightInches || 0),
        weight_lbs: parseFloat(data.weight),
        activity_level: data.activityLevel,
        family_history: data.familyHistory === 'yes',
        smoking: data.smoking === 'yes',
        email: data.email
      };

      // Submit health assessment
      const response = await api.post('/api/health-assessment', payload);
      const results = response.data;
      
      setAssessmentResults(results);
      setSubmitStatus({ type: 'success', message: 'Health assessment completed successfully!' });

      // Send email report
      try {
        await api.post(`/api/send-report/${results.assessment_id}`);
        setSubmitStatus({ 
          type: 'success', 
          message: 'Assessment completed! Email report has been sent to your inbox.' 
        });
      } catch (emailError) {
        console.error('Email sending failed:', emailError);
        setSubmitStatus({ 
          type: 'warning', 
          message: 'Assessment completed but email report could not be sent.' 
        });
      }

    } catch (error) {
      console.error('Submission error:', error);
      setSubmitStatus({ 
        type: 'error', 
        message: 'Failed to complete assessment. Please try again.' 
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    reset();
    setAssessmentResults(null);
    setSubmitStatus(null);
    setHeightCm(0);
    setWeightKg(0);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Health Risk Assessment</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Complete this comprehensive health questionnaire to receive personalized risk assessments 
          and health insights powered by machine learning.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Form */}
        <div className="lg:col-span-2">
          <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            
            {/* Personal Information */}
            <div className="space-y-4">
              <h3 className="flex items-center text-lg font-semibold text-gray-900">
                <User className="h-5 w-5 mr-2 text-health-primary" />
                Personal Information
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Age */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Age (years)
                  </label>
                  <input
                    type="number"
                    {...register('age', { 
                      required: 'Age is required',
                      min: { value: 18, message: 'Must be at least 18 years old' },
                      max: { value: 100, message: 'Must be 100 years or younger' }
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                    placeholder="25"
                  />
                  {errors.age && <p className="mt-1 text-sm text-red-600">{errors.age.message}</p>}
                </div>

                {/* Gender */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender
                  </label>
                  <select
                    {...register('gender', { required: 'Gender is required' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                  >
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                  {errors.gender && <p className="mt-1 text-sm text-red-600">{errors.gender.message}</p>}
                </div>
              </div>
            </div>

            {/* Physical Measurements */}
            <div className="space-y-4">
              <h3 className="flex items-center text-lg font-semibold text-gray-900">
                <Ruler className="h-5 w-5 mr-2 text-health-primary" />
                Physical Measurements
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Height */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Height
                  </label>
                  <div className="flex space-x-2">
                    <div className="flex-1">
                      <input
                        type="number"
                        {...register('heightFeet', { 
                          required: 'Height is required',
                          min: { value: 3, message: 'Must be at least 3 feet' },
                          max: { value: 8, message: 'Must be 8 feet or less' }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                        placeholder="5"
                      />
                      <span className="text-xs text-gray-500">feet</span>
                    </div>
                    <div className="flex-1">
                      <input
                        type="number"
                        {...register('heightInches', { 
                          min: { value: 0, message: 'Cannot be negative' },
                          max: { value: 11, message: 'Must be less than 12 inches' }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                        placeholder="8"
                      />
                      <span className="text-xs text-gray-500">inches</span>
                    </div>
                  </div>
                  {(errors.heightFeet || errors.heightInches) && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.heightFeet?.message || errors.heightInches?.message}
                    </p>
                  )}
                </div>

                {/* Weight */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Weight (lbs)
                  </label>
                  <div className="relative">
                    <Scale className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                    <input
                      type="number"
                      step="0.1"
                      {...register('weight', { 
                        required: 'Weight is required',
                        min: { value: 50, message: 'Must be at least 50 lbs' },
                        max: { value: 1000, message: 'Must be 1000 lbs or less' }
                      })}
                      className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                      placeholder="150"
                    />
                  </div>
                  {errors.weight && <p className="mt-1 text-sm text-red-600">{errors.weight.message}</p>}
                </div>
              </div>
            </div>

            {/* Lifestyle & Health History */}
            <div className="space-y-4">
              <h3 className="flex items-center text-lg font-semibold text-gray-900">
                <Heart className="h-5 w-5 mr-2 text-health-primary" />
                Lifestyle & Health History
              </h3>

              {/* Activity Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Activity Level
                </label>
                <select
                  {...register('activityLevel', { required: 'Activity level is required' })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                >
                  <option value="">Select activity level</option>
                  <option value="Sedentary">Sedentary (little or no exercise)</option>
                  <option value="Light">Light (light exercise 1-3 days/week)</option>
                  <option value="Moderate">Moderate (moderate exercise 3-5 days/week)</option>
                  <option value="Active">Active (hard exercise 6-7 days/week)</option>
                  <option value="Very Active">Very Active (very hard exercise, physical job)</option>
                </select>
                {errors.activityLevel && <p className="mt-1 text-sm text-red-600">{errors.activityLevel.message}</p>}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Family History */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    <Users className="h-4 w-4 inline mr-1" />
                    Family History of Heart Disease
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="yes"
                        {...register('familyHistory', { required: 'Family history selection is required' })}
                        className="h-4 w-4 text-health-primary focus:ring-health-primary border-gray-300"
                      />
                      <span className="ml-2 text-sm text-gray-700">Yes</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="no"
                        {...register('familyHistory', { required: 'Family history selection is required' })}
                        className="h-4 w-4 text-health-primary focus:ring-health-primary border-gray-300"
                      />
                      <span className="ml-2 text-sm text-gray-700">No</span>
                    </label>
                  </div>
                  {errors.familyHistory && <p className="mt-1 text-sm text-red-600">{errors.familyHistory.message}</p>}
                </div>

                {/* Smoking Status */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    <Cigarette className="h-4 w-4 inline mr-1" />
                    Smoking Status
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="yes"
                        {...register('smoking', { required: 'Smoking status selection is required' })}
                        className="h-4 w-4 text-health-primary focus:ring-health-primary border-gray-300"
                      />
                      <span className="ml-2 text-sm text-gray-700">Current smoker</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="no"
                        {...register('smoking', { required: 'Smoking status selection is required' })}
                        className="h-4 w-4 text-health-primary focus:ring-health-primary border-gray-300"
                      />
                      <span className="ml-2 text-sm text-gray-700">Non-smoker</span>
                    </label>
                  </div>
                  {errors.smoking && <p className="mt-1 text-sm text-red-600">{errors.smoking.message}</p>}
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="space-y-4">
              <h3 className="flex items-center text-lg font-semibold text-gray-900">
                <Mail className="h-5 w-5 mr-2 text-health-primary" />
                Report Delivery
              </h3>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                  <input
                    type="email"
                    {...register('email', { 
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                      }
                    })}
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-health-primary focus:border-health-primary"
                    placeholder="your.email@example.com"
                  />
                </div>
                {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
                <p className="mt-1 text-sm text-gray-500">
                  Your detailed health assessment report will be sent to this email address.
                </p>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-6 border-t border-gray-200">
              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 bg-health-primary hover:bg-health-primary/90 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
                >
                  {isSubmitting ? (
                    <>
                      <Loader className="h-5 w-5 animate-spin" />
                      <span>Processing Assessment...</span>
                    </>
                  ) : (
                    <>
                      <Send className="h-5 w-5" />
                      <span>Submit Health Assessment</span>
                    </>
                  )}
                </button>
                
                {assessmentResults && (
                  <button
                    type="button"
                    onClick={resetForm}
                    className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    New Assessment
                  </button>
                )}
              </div>
            </div>

            {/* Status Messages */}
            {submitStatus && (
              <div className={`p-4 rounded-lg flex items-center space-x-2 ${
                submitStatus.type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' :
                submitStatus.type === 'warning' ? 'bg-yellow-50 text-yellow-800 border border-yellow-200' :
                'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {submitStatus.type === 'success' ? <CheckCircle className="h-5 w-5" /> : <AlertCircle className="h-5 w-5" />}
                <span>{submitStatus.message}</span>
              </div>
            )}
          </form>
        </div>

        {/* Sidebar with BMI Calculator and Results */}
        <div className="space-y-6">
          {/* BMI Calculator */}
          <BMICalculator heightCm={heightCm} weightKg={weightKg} />

          {/* Assessment Results */}
          {assessmentResults && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Activity className="h-5 w-5 mr-2 text-health-primary" />
                Assessment Results
              </h3>
              
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{assessmentResults.bmi}</div>
                    <div className="text-sm text-blue-600">{assessmentResults.bmi_category}</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <div className="text-lg font-bold text-green-600">{assessmentResults.obesity_risk}</div>
                    <div className="text-sm text-green-600">Obesity Risk</div>
                  </div>
                </div>
                
                <div className="text-center p-3 bg-purple-50 rounded-lg">
                  <div className="text-lg font-bold text-purple-600">{assessmentResults.heart_disease_risk}</div>
                  <div className="text-sm text-purple-600">Heart Disease Risk</div>
                </div>

                <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                  <p className="font-medium mb-1">Assessment ID:</p>
                  <p className="font-mono text-xs">{assessmentResults.assessment_id}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HealthForm; 
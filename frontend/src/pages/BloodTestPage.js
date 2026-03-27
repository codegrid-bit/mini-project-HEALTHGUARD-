import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { historyAPI, bloodTestAPI } from '../api';
import { Activity, Upload, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';

const BloodTestPage = () => {
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState([]);
  const [selectedAssessment, setSelectedAssessment] = useState('');
  const [formData, setFormData] = useState({
    ldl: '',
    hdl: '',
    triglycerides: '',
    hba1c: '',
    glucose: '',
    blood_pressure: '',
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const response = await historyAPI.getAssessments();
      const assessmentsList = response.data.assessments;
      console.log('Loaded assessments:', assessmentsList);
      setAssessments(assessmentsList);
      if (assessmentsList.length > 0) {
        setSelectedAssessment(assessmentsList[0].id);
        console.log('Selected assessment:', assessmentsList[0].id);
      } else {
        console.warn('No assessments found');
      }
    } catch (error) {
      console.error('Failed to load assessments:', error);
      toast.error('Failed to load assessments');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAssessment) {
      toast.error('Please select an assessment');
      return;
    }

    // Validate all required fields
    if (!formData.ldl || !formData.hdl || !formData.triglycerides || !formData.hba1c) {
      toast.error('Please fill in all required fields (LDL, HDL, Triglycerides, HbA1c)');
      return;
    }

    setLoading(true);
    try {
      const bloodTestData = {
        assessment_id: selectedAssessment,
        blood_test: {
          ldl: parseFloat(formData.ldl),
          hdl: parseFloat(formData.hdl),
          triglycerides: parseFloat(formData.triglycerides),
          hba1c: parseFloat(formData.hba1c),
          glucose: formData.glucose ? parseFloat(formData.glucose) : null,
          blood_pressure: formData.blood_pressure ? parseFloat(formData.blood_pressure) : null,
        },
      };
      
      console.log('Submitting blood test:', bloodTestData);
      const response = await bloodTestAPI.submitBloodTest(bloodTestData);
      console.log('Blood test response:', response.data);
      
      setResults(response.data);
      toast.success('Blood test results uploaded successfully!');
    } catch (error) {
      console.error('Blood test error:', error);
      const errorMessage = error.response?.data?.detail 
        || error.message 
        || 'Failed to upload blood test. Please check all values are valid numbers.';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getRiskIcon = (risk) => {
    if (risk.includes('Normal')) return <CheckCircle className="w-5 h-5 text-emerald-600" />;
    if (risk.includes('High')) return <XCircle className="w-5 h-5 text-rose-600" />;
    return <AlertCircle className="w-5 h-5 text-amber-600" />;
  };

  if (results) {
    return (
      <div className="p-6 md:p-12 page-transition" data-testid="blood-test-results">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <CheckCircle className="w-16 h-16 text-sage-teal mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Blood Test Analysis Complete</h1>
            <p className="text-slate-600">Here's the analysis of your blood test results</p>
          </div>

          <div className="card-dashboard p-8 mb-6">
            <h3 className="text-xl font-bold text-slate-800 mb-6">Risk Assessment</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                <span className="font-medium text-slate-700">Diabetes Risk</span>
                <div className="flex items-center space-x-2">
                  {getRiskIcon(results.analysis.diabetes_risk)}
                  <span className="font-semibold">{results.analysis.diabetes_risk}</span>
                </div>
              </div>
              <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                <span className="font-medium text-slate-700">Cholesterol Risk</span>
                <div className="flex items-center space-x-2">
                  {getRiskIcon(results.analysis.cholesterol_risk)}
                  <span className="font-semibold">{results.analysis.cholesterol_risk}</span>
                </div>
              </div>
            </div>
          </div>

          {results.analysis.recommendations.length > 0 && (
            <div className="card-dashboard p-8 mb-6">
              <h3 className="text-xl font-bold text-slate-800 mb-4">Recommendations</h3>
              <div className="space-y-3">
                {results.analysis.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    <p className="text-slate-700">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {results.analysis.requires_doctor && (
            <div className="card-dashboard p-8 bg-rose-50 border-2 border-rose-200 mb-6">
              <div className="flex items-start space-x-4">
                <AlertCircle className="w-8 h-8 text-rose-600 flex-shrink-0" />
                <div>
                  <h3 className="text-xl font-bold text-slate-800 mb-2">Doctor Consultation Required</h3>
                  <p className="text-slate-700">
                    Based on your blood test results, we strongly recommend consulting with a healthcare
                    professional for proper diagnosis and treatment planning.
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="card-dashboard p-6 bg-sage-teal/10">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-slate-800">Next Blood Test Reminder</h3>
                <p className="text-sm text-slate-600">
                  {new Date(results.next_test_date).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => navigate('/dashboard/reminders')}
                className="btn-secondary"
                data-testid="view-reminders-btn"
              >
                View Reminders
              </button>
            </div>
          </div>

          <div className="mt-8 text-center">
            <button
              onClick={() => navigate('/dashboard')}
              className="btn-primary"
              data-testid="back-dashboard-btn"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-12 page-transition" data-testid="blood-test-page">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Upload Blood Test Results</h1>
          <p className="text-slate-600">
            Enter your latest blood test values for comprehensive health analysis.
          </p>
        </div>

        {assessments.length === 0 ? (
          <div className="card-dashboard p-8 text-center">
            <AlertCircle className="w-12 h-12 text-amber-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-slate-800 mb-2">No Assessment Found</h3>
            <p className="text-slate-600 mb-6">
              Please complete a health assessment first before uploading blood test results.
            </p>
            <button
              onClick={() => navigate('/dashboard/quiz')}
              className="btn-primary"
              data-testid="start-assessment-btn"
            >
              Start Assessment
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="card-dashboard p-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">Select Assessment</label>
              <select
                value={selectedAssessment}
                onChange={(e) => setSelectedAssessment(e.target.value)}
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                data-testid="assessment-select"
              >
                {assessments.map((assessment) => (
                  <option key={assessment.id} value={assessment.id}>
                    Assessment from {new Date(assessment.created_at).toLocaleDateString()} - {assessment.risk_level} Risk
                  </option>
                ))}
              </select>
            </div>

            <div className="card-dashboard p-6">
              <h3 className="text-lg font-bold text-slate-800 mb-4">Required Values</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    LDL Cholesterol (mg/dL) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="ldl"
                    required
                    value={formData.ldl}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 120"
                    data-testid="ldl-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    HDL Cholesterol (mg/dL) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="hdl"
                    required
                    value={formData.hdl}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 50"
                    data-testid="hdl-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Triglycerides (mg/dL) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="triglycerides"
                    required
                    value={formData.triglycerides}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 150"
                    data-testid="triglycerides-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    HbA1c (%) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="hba1c"
                    required
                    value={formData.hba1c}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 5.5"
                    data-testid="hba1c-input"
                  />
                </div>
              </div>
            </div>

            <div className="card-dashboard p-6">
              <h3 className="text-lg font-bold text-slate-800 mb-4">Optional Values</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Fasting Glucose (mg/dL)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="glucose"
                    value={formData.glucose}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 100"
                    data-testid="glucose-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Blood Pressure (mmHg)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="blood_pressure"
                    value={formData.blood_pressure}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal"
                    placeholder="e.g., 120"
                    data-testid="blood-pressure-input"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="submit-blood-test-btn"
            >
              {loading ? 'Uploading...' : (
                <>
                  <Upload className="inline w-5 h-5 mr-2" />
                  Upload & Analyze Results
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default BloodTestPage;

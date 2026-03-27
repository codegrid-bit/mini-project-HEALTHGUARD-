import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { CheckCircle, AlertCircle, XCircle, ArrowRight, FileText, Activity } from 'lucide-react';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results;

  if (!results) {
    navigate('/dashboard');
    return null;
  }

  const { assessment, score_result, recommendations, requires_blood_test } = results;
  const riskLevel = score_result.risk_level;

  const getRiskColor = () => {
    if (riskLevel === 'Low') return '#10b981';
    if (riskLevel === 'Medium') return '#f59e0b';
    return '#ef4444';
  };

  const getRiskIcon = () => {
    if (riskLevel === 'Low') return CheckCircle;
    if (riskLevel === 'Medium') return AlertCircle;
    return XCircle;
  };

  const getRiskBg = () => {
    if (riskLevel === 'Low') return 'bg-emerald-50 border-emerald-200';
    if (riskLevel === 'Medium') return 'bg-amber-50 border-amber-200';
    return 'bg-rose-50 border-rose-200';
  };

  const getRiskText = () => {
    if (riskLevel === 'Low') return 'text-emerald-600';
    if (riskLevel === 'Medium') return 'text-amber-600';
    return 'text-rose-600';
  };

  const RiskIcon = getRiskIcon();

  return (
    <div className="p-6 md:p-12 page-transition" data-testid="results-page">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-800 mb-4">Your Health Assessment Results</h1>
          <p className="text-lg text-slate-600">
            Here's a comprehensive analysis of your health risk factors
          </p>
        </div>

        {/* Risk Score Card */}
        <div className={`card-dashboard p-8 mb-8 border-2 ${getRiskBg()}`} data-testid="risk-score-card">
          <div className="grid md:grid-cols-3 gap-8 items-center">
            <div className="flex justify-center">
              <div style={{ width: 200, height: 200 }}>
                <CircularProgressbar
                  value={score_result.total_score}
                  text={`${score_result.total_score}%`}
                  styles={buildStyles({
                    textColor: getRiskColor(),
                    pathColor: getRiskColor(),
                    trailColor: '#e2e8f0',
                    textSize: '16px',
                  })}
                />
              </div>
            </div>

            <div className="md:col-span-2 space-y-4">
              <div className="flex items-center space-x-3">
                <RiskIcon className={`w-12 h-12 ${getRiskText()}`} />
                <div>
                  <h2 className="text-3xl font-bold text-slate-800">{riskLevel} Risk</h2>
                  <p className="text-slate-600">Overall Health Risk Level</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mt-6">
                <div className="bg-white rounded-lg p-4">
                  <div className="text-3xl font-bold text-sage-teal">{score_result.diabetes_score}%</div>
                  <div className="text-sm text-slate-600">Diabetes Risk Score</div>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <div className="text-3xl font-bold text-soft-coral">{score_result.cholesterol_score}%</div>
                  <div className="text-sm text-slate-600">Cholesterol Risk Score</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="card-dashboard p-8 mb-8" data-testid="recommendations-section">
          <h3 className="text-2xl font-bold text-slate-800 mb-6">Personalized Recommendations</h3>
          <div className="space-y-3">
            {recommendations.map((rec, index) => (
              <div key={index} className="flex items-start space-x-3">
                <CheckCircle className="w-5 h-5 text-sage-teal flex-shrink-0 mt-0.5" />
                <p className="text-slate-700 leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Next Steps */}
        {requires_blood_test ? (
          <div className="card-dashboard p-8 bg-amber-50 border-2 border-amber-200 mb-8" data-testid="blood-test-required">
            <div className="flex items-start space-x-4">
              <Activity className="w-8 h-8 text-amber-600 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-xl font-bold text-slate-800 mb-2">Blood Test Required</h3>
                <p className="text-slate-700 mb-4">
                  Based on your risk level, we recommend getting the following blood tests done:
                </p>
                <ul className="list-disc list-inside space-y-1 text-slate-700 mb-6">
                  <li>LDL Cholesterol (Bad cholesterol)</li>
                  <li>HDL Cholesterol (Good cholesterol)</li>
                  <li>Triglycerides</li>
                  <li>HbA1c (3-month average blood sugar)</li>
                  <li>Fasting Glucose (optional)</li>
                  <li>Blood Pressure (optional)</li>
                </ul>
                <button
                  onClick={() => navigate('/dashboard/blood-test')}
                  className="btn-primary"
                  data-testid="upload-blood-test-btn"
                >
                  Upload Blood Test Results
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="card-dashboard p-8 bg-emerald-50 border-2 border-emerald-200" data-testid="low-risk-message">
            <div className="flex items-start space-x-4">
              <CheckCircle className="w-8 h-8 text-emerald-600 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-bold text-slate-800 mb-2">Great News!</h3>
                <p className="text-slate-700 mb-4">
                  Your risk level is low. Keep maintaining your healthy lifestyle with the recommendations
                  above. Regular health check-ups are still important for prevention.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/dashboard/history')}
            className="btn-secondary"
            data-testid="view-history-btn"
          >
            <FileText className="w-5 h-5 inline mr-2" />
            View History
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn-primary"
            data-testid="back-to-dashboard-btn"
          >
            Back to Dashboard
            <ArrowRight className="w-5 h-5 inline ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;

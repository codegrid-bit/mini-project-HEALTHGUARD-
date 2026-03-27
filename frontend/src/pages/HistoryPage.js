import React, { useState, useEffect } from 'react';
import { historyAPI } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FileText, Activity, TrendingUp, Calendar } from 'lucide-react';
import { toast } from 'sonner';

const HistoryPage = () => {
  const [assessments, setAssessments] = useState([]);
  const [bloodTests, setBloodTests] = useState([]);
  const [activeTab, setActiveTab] = useState('assessments');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const [assessmentsRes, bloodTestsRes] = await Promise.all([
        historyAPI.getAssessments(),
        historyAPI.getBloodTests(),
      ]);
      setAssessments(assessmentsRes.data.assessments);
      setBloodTests(bloodTestsRes.data.blood_tests);
    } catch (error) {
      toast.error('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (level === 'Low') return 'text-emerald-600 bg-emerald-50';
    if (level === 'Medium') return 'text-amber-600 bg-amber-50';
    return 'text-rose-600 bg-rose-50';
  };

  // Prepare chart data
  const chartData = assessments.map((assessment) => ({
    date: new Date(assessment.created_at).toLocaleDateString(),
    diabetes: assessment.diabetes_score,
    cholesterol: assessment.cholesterol_score,
    overall: assessment.total_score,
  })).reverse();

  return (
    <div className="p-6 md:p-12 page-transition" data-testid="history-page">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Health History</h1>
          <p className="text-slate-600">Track your health journey over time</p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-4 mb-8 border-b border-slate-200">
          <button
            onClick={() => setActiveTab('assessments')}
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              activeTab === 'assessments'
                ? 'border-sage-teal text-sage-teal'
                : 'border-transparent text-slate-600 hover:text-slate-800'
            }`}
            data-testid="tab-assessments"
          >
            <FileText className="inline w-5 h-5 mr-2" />
            Assessments ({assessments.length})
          </button>
          <button
            onClick={() => setActiveTab('blood-tests')}
            className={`px-6 py-3 font-medium border-b-2 transition-colors ${
              activeTab === 'blood-tests'
                ? 'border-sage-teal text-sage-teal'
                : 'border-transparent text-slate-600 hover:text-slate-800'
            }`}
            data-testid="tab-blood-tests"
          >
            <Activity className="inline w-5 h-5 mr-2" />
            Blood Tests ({bloodTests.length})
          </button>
        </div>

        {/* Chart */}
        {activeTab === 'assessments' && chartData.length > 0 && (
          <div className="card-dashboard p-8 mb-8" data-testid="risk-chart">
            <h3 className="text-xl font-bold text-slate-800 mb-6">Risk Score Trends</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="diabetes" stroke="#2A9D8F" strokeWidth={2} name="Diabetes" />
                <Line type="monotone" dataKey="cholesterol" stroke="#E76F51" strokeWidth={2} name="Cholesterol" />
                <Line type="monotone" dataKey="overall" stroke="#E9C46A" strokeWidth={2} name="Overall" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Assessments Tab */}
        {activeTab === 'assessments' && (
          <div className="space-y-6">
            {assessments.length === 0 ? (
              <div className="card-dashboard p-8 text-center">
                <FileText className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No assessments found</p>
              </div>
            ) : (
              assessments.map((assessment) => (
                <div key={assessment.id} className="card-dashboard p-6" data-testid={`assessment-${assessment.id}`}>
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <div className={`px-4 py-2 rounded-full font-semibold ${getRiskColor(assessment.risk_level)}`}>
                          {assessment.risk_level} Risk
                        </div>
                        <div className="flex items-center text-sm text-slate-500">
                          <Calendar className="w-4 h-4 mr-1" />
                          {new Date(assessment.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="text-3xl font-bold text-slate-800">
                      {assessment.total_score}%
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-sage-teal/10 rounded-lg p-4">
                      <div className="text-sm text-slate-600 mb-1">Diabetes Score</div>
                      <div className="text-2xl font-bold text-sage-teal">{assessment.diabetes_score}%</div>
                    </div>
                    <div className="bg-soft-coral/10 rounded-lg p-4">
                      <div className="text-sm text-slate-600 mb-1">Cholesterol Score</div>
                      <div className="text-2xl font-bold text-soft-coral">{assessment.cholesterol_score}%</div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Blood Tests Tab */}
        {activeTab === 'blood-tests' && (
          <div className="space-y-6">
            {bloodTests.length === 0 ? (
              <div className="card-dashboard p-8 text-center">
                <Activity className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No blood tests found</p>
              </div>
            ) : (
              bloodTests.map((test) => (
                <div key={test.id} className="card-dashboard p-6" data-testid={`blood-test-${test.id}`}>
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center text-sm text-slate-500">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(test.created_at).toLocaleDateString()}
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-slate-600">Diabetes:</span>
                      <span className="font-semibold text-slate-800">{test.analysis.diabetes_risk}</span>
                      <span className="text-slate-300 mx-2">|</span>
                      <span className="text-sm font-medium text-slate-600">Cholesterol:</span>
                      <span className="font-semibold text-slate-800">{test.analysis.cholesterol_risk}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="text-xs text-slate-600 mb-1">LDL</div>
                      <div className="text-xl font-bold text-slate-800">{test.ldl}</div>
                      <div className="text-xs text-slate-500">mg/dL</div>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="text-xs text-slate-600 mb-1">HDL</div>
                      <div className="text-xl font-bold text-slate-800">{test.hdl}</div>
                      <div className="text-xs text-slate-500">mg/dL</div>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="text-xs text-slate-600 mb-1">Triglycerides</div>
                      <div className="text-xl font-bold text-slate-800">{test.triglycerides}</div>
                      <div className="text-xs text-slate-500">mg/dL</div>
                    </div>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <div className="text-xs text-slate-600 mb-1">HbA1c</div>
                      <div className="text-xl font-bold text-slate-800">{test.hba1c}</div>
                      <div className="text-xs text-slate-500">%</div>
                    </div>
                  </div>

                  {test.analysis.requires_doctor && (
                    <div className="mt-4 p-4 bg-rose-50 border border-rose-200 rounded-lg">
                      <p className="text-sm font-medium text-rose-800">
                        Doctor consultation was recommended for this test
                      </p>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { historyAPI, remindersAPI } from '../api';
import { FileText, Activity, TrendingUp, Bell, ArrowRight, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [stats, setStats] = useState({
    assessments: 0,
    bloodTests: 0,
    pendingReminders: 0,
    lastAssessment: null,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [assessmentsRes, bloodTestsRes, remindersRes] = await Promise.all([
        historyAPI.getAssessments(),
        historyAPI.getBloodTests(),
        remindersAPI.getReminders(),
      ]);

      const assessments = assessmentsRes.data.assessments;
      setStats({
        assessments: assessments.length,
        bloodTests: bloodTestsRes.data.blood_tests.length,
        pendingReminders: remindersRes.data.reminders.length,
        lastAssessment: assessments[0] || null,
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (level === 'Low') return 'text-emerald-600 bg-emerald-50';
    if (level === 'Medium') return 'text-amber-600 bg-amber-50';
    return 'text-rose-600 bg-rose-50';
  };

  return (
    <div className="p-6 md:p-12 page-transition" data-testid="dashboard-page">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-lg text-slate-600">
            Here's your health overview and what you need to do next.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="card-dashboard p-6" data-testid="stat-assessments">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center">
                <FileText className="w-6 h-6 text-sage-teal" />
              </div>
            </div>
            <div className="text-3xl font-bold text-slate-800">{stats.assessments}</div>
            <div className="text-sm text-slate-600">Total Assessments</div>
          </div>

          <div className="card-dashboard p-6" data-testid="stat-blood-tests">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-soft-coral/10 rounded-xl flex items-center justify-center">
                <Activity className="w-6 h-6 text-soft-coral" />
              </div>
            </div>
            <div className="text-3xl font-bold text-slate-800">{stats.bloodTests}</div>
            <div className="text-sm text-slate-600">Blood Tests</div>
          </div>

          <div className="card-dashboard p-6" data-testid="stat-reminders">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center">
                <Bell className="w-6 h-6 text-amber-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-slate-800">{stats.pendingReminders}</div>
            <div className="text-sm text-slate-600">Pending Reminders</div>
          </div>

          <div className="card-dashboard p-6" data-testid="stat-risk">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-emerald-600" />
              </div>
            </div>
            {stats.lastAssessment ? (
              <>
                <div className={`text-2xl font-bold ${getRiskColor(stats.lastAssessment.risk_level).split(' ')[0]}`}>
                  {stats.lastAssessment.risk_level}
                </div>
                <div className="text-sm text-slate-600">Current Risk Level</div>
              </>
            ) : (
              <>
                <div className="text-2xl font-bold text-slate-400">-</div>
                <div className="text-sm text-slate-600">No Assessment Yet</div>
              </>
            )}
          </div>
        </div>

        {/* Last Assessment */}
        {stats.lastAssessment && (
          <div className="card-dashboard p-8 mb-8" data-testid="last-assessment">
            <h2 className="text-2xl font-bold text-slate-800 mb-6">Latest Assessment</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <div className="text-sm text-slate-600 mb-1">Overall Risk</div>
                <div className={`inline-block px-4 py-2 rounded-full font-semibold ${getRiskColor(stats.lastAssessment.risk_level)}`}>
                  {stats.lastAssessment.risk_level}
                </div>
              </div>
              <div>
                <div className="text-sm text-slate-600 mb-1">Diabetes Score</div>
                <div className="text-2xl font-bold text-sage-teal">{stats.lastAssessment.diabetes_score}%</div>
              </div>
              <div>
                <div className="text-sm text-slate-600 mb-1">Cholesterol Score</div>
                <div className="text-2xl font-bold text-soft-coral">{stats.lastAssessment.cholesterol_score}%</div>
              </div>
            </div>
            <div className="mt-6 text-sm text-slate-500">
              Completed on {new Date(stats.lastAssessment.created_at).toLocaleDateString()}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card-dashboard p-8 bg-gradient-to-br from-sage-teal to-sage-teal-dark text-white" data-testid="quick-action-quiz">
            <FileText className="w-12 h-12 mb-4" />
            <h3 className="text-2xl font-bold mb-2">
              {stats.assessments === 0 ? 'Start Your First Assessment' : 'Take Another Assessment'}
            </h3>
            <p className="mb-6 text-white/90">
              Complete a quick 5-minute health quiz to assess your diabetes and cholesterol risk.
            </p>
            <button
              onClick={() => navigate('/dashboard/quiz')}
              className="bg-white text-sage-teal px-6 py-3 rounded-full font-semibold hover:shadow-lg transition-all"
              data-testid="start-quiz-btn"
            >
              {stats.assessments === 0 ? 'Start Quiz' : 'Take Quiz Again'}
              <ArrowRight className="inline ml-2 w-5 h-5" />
            </button>
          </div>

          {stats.lastAssessment && stats.lastAssessment.risk_level !== 'Low' && (
            <div className="card-dashboard p-8 bg-gradient-to-br from-soft-coral to-amber-500 text-white" data-testid="quick-action-blood-test">
              <Activity className="w-12 h-12 mb-4" />
              <h3 className="text-2xl font-bold mb-2">Upload Blood Test Results</h3>
              <p className="mb-6 text-white/90">
                Track your health metrics by uploading your latest blood test results.
              </p>
              <button
                onClick={() => navigate('/dashboard/blood-test')}
                className="bg-white text-soft-coral px-6 py-3 rounded-full font-semibold hover:shadow-lg transition-all"
                data-testid="upload-test-btn"
              >
                Upload Results
                <ArrowRight className="inline ml-2 w-5 h-5" />
              </button>
            </div>
          )}
        </div>

        {/* Pending Reminders */}
        {stats.pendingReminders > 0 && (
          <div className="mt-8 card-dashboard p-6 bg-amber-50 border-2 border-amber-200" data-testid="pending-reminders">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-6 h-6 text-amber-600" />
              <div className="flex-1">
                <h3 className="font-semibold text-slate-800">
                  You have {stats.pendingReminders} pending reminder{stats.pendingReminders > 1 ? 's' : ''}
                </h3>
                <p className="text-sm text-slate-600">Check your reminders to stay on track with your health.</p>
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
        )}
      </div>
    </div>
  );
};

export default DashboardPage;

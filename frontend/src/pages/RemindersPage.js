import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { remindersAPI } from '../api';
import { Bell, Calendar, CheckCircle, Clock, Activity } from 'lucide-react';
import { toast } from 'sonner';

const RemindersPage = () => {
  const navigate = useNavigate();
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReminders();
  }, []);

  const loadReminders = async () => {
    try {
      const response = await remindersAPI.getReminders();
      setReminders(response.data.reminders);
    } catch (error) {
      toast.error('Failed to load reminders');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteReminder = async (reminderId) => {
    try {
      await remindersAPI.completeReminder(reminderId);
      toast.success('Reminder marked as complete');
      loadReminders();
    } catch (error) {
      toast.error('Failed to complete reminder');
    }
  };

  const isOverdue = (dueDate) => {
    return new Date(dueDate) < new Date();
  };

  const getDaysUntil = (dueDate) => {
    const diff = new Date(dueDate) - new Date();
    const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
    return days;
  };

  return (
    <div className="p-6 md:p-12 page-transition" data-testid="reminders-page">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Health Reminders</h1>
          <p className="text-slate-600">
            Stay on track with your health by completing your scheduled blood tests
          </p>
        </div>

        {loading ? (
          <div className="card-dashboard p-8 text-center">
            <p className="text-slate-600">Loading reminders...</p>
          </div>
        ) : reminders.length === 0 ? (
          <div className="card-dashboard p-8 text-center" data-testid="no-reminders">
            <Bell className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-slate-800 mb-2">No Pending Reminders</h3>
            <p className="text-slate-600 mb-6">
              You're all caught up! Take a health assessment to get personalized recommendations.
            </p>
            <button
              onClick={() => navigate('/dashboard/quiz')}
              className="btn-primary"
              data-testid="take-quiz-btn"
            >
              Take Health Quiz
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {reminders.map((reminder) => {
              const overdue = isOverdue(reminder.due_date);
              const daysUntil = getDaysUntil(reminder.due_date);

              return (
                <div
                  key={reminder.id}
                  className={`card-dashboard p-6 border-2 ${
                    overdue ? 'border-rose-200 bg-rose-50' : 'border-amber-200 bg-amber-50'
                  }`}
                  data-testid={`reminder-${reminder.id}`}
                >
                  <div className="flex items-start space-x-4">
                    <div
                      className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                        overdue ? 'bg-rose-100' : 'bg-amber-100'
                      }`}
                    >
                      {overdue ? (
                        <Clock className="w-6 h-6 text-rose-600" />
                      ) : (
                        <Bell className="w-6 h-6 text-amber-600" />
                      )}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Activity className="w-5 h-5 text-slate-600" />
                        <h3 className="text-lg font-semibold text-slate-800">
                          Blood Test Reminder
                        </h3>
                      </div>

                      <div className="flex items-center space-x-2 mb-3">
                        <Calendar className="w-4 h-4 text-slate-500" />
                        <span className="text-sm text-slate-600">
                          Due: {new Date(reminder.due_date).toLocaleDateString()}
                        </span>
                        {overdue ? (
                          <span className="text-sm font-semibold text-rose-600">
                            (Overdue by {Math.abs(daysUntil)} days)
                          </span>
                        ) : (
                          <span className="text-sm font-semibold text-amber-600">
                            (In {daysUntil} days)
                          </span>
                        )}
                      </div>

                      <p className="text-slate-700 mb-4">
                        It's time for your scheduled blood test. Regular monitoring helps track your
                        health progress and detect any changes early.
                      </p>

                      <div className="flex space-x-3">
                        <button
                          onClick={() => navigate('/dashboard/blood-test')}
                          className="btn-primary"
                          data-testid={`upload-test-${reminder.id}`}
                        >
                          Upload Test Results
                        </button>
                        <button
                          onClick={() => handleCompleteReminder(reminder.id)}
                          className="flex items-center space-x-2 px-6 py-3 rounded-full border-2 border-sage-teal text-sage-teal hover:bg-sage-teal/5 transition-colors font-medium"
                          data-testid={`complete-${reminder.id}`}
                        >
                          <CheckCircle className="w-5 h-5" />
                          <span>Mark as Complete</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Info Card */}
        <div className="mt-8 card-dashboard p-6 bg-sage-teal/10">
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Why Regular Testing Matters</h3>
          <p className="text-slate-700">
            Regular blood tests every 2 months help you:
          </p>
          <ul className="list-disc list-inside space-y-1 text-slate-700 mt-2">
            <li>Track changes in your cholesterol and blood sugar levels</li>
            <li>Evaluate the effectiveness of lifestyle changes</li>
            <li>Detect potential issues before they become serious</li>
            <li>Make informed decisions about your health with your doctor</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RemindersPage;

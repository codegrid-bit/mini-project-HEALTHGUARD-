import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Heart, Mail, Lock, User, Calendar, Users, AlertCircle, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    age: '',
    sex: 'male',
    consent_privacy: false,
    consent_terms: false,
  });
  const [loading, setLoading] = useState(false);
  const [showConsent, setShowConsent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.consent_privacy || !formData.consent_terms) {
      toast.error('Please accept the privacy policy and terms of service');
      setShowConsent(true);
      return;
    }
    
    setLoading(true);

    try {
      await register({
        ...formData,
        age: parseInt(formData.age),
      });
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  return (
    <div className="min-h-screen gradient-hero flex items-center justify-center px-6 py-12" data-testid="register-page">
      <div className="w-full max-w-2xl">
        <div className="bg-white rounded-2xl shadow-float p-8">
          <div className="flex items-center justify-center mb-6">
            <Heart className="w-10 h-10 text-sage-teal" />
          </div>
          <h2 className="text-3xl font-bold text-center text-slate-800 mb-2">Create Account</h2>
          <p className="text-center text-slate-600 mb-8">Start your health journey today</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                  <input
                    type="text"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal transition-all"
                    placeholder="John Doe"
                    data-testid="register-name-input"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal transition-all"
                    placeholder="john@example.com"
                    data-testid="register-email-input"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                <input
                  type="password"
                  name="password"
                  required
                  minLength="6"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal transition-all"
                  placeholder="••••••••"
                  data-testid="register-password-input"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Age</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                  <input
                    type="number"
                    name="age"
                    required
                    min="18"
                    max="120"
                    value={formData.age}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal transition-all"
                    placeholder="30"
                    data-testid="register-age-input"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Sex</label>
                <div className="relative">
                  <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                  <select
                    name="sex"
                    value={formData.sex}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-sage-teal/20 focus:border-sage-teal transition-all appearance-none bg-white cursor-pointer"
                    data-testid="register-sex-select"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Medical Disclaimer */}
            <div className="bg-amber-50 border-2 border-amber-200 rounded-lg p-4 mt-6">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-slate-700">
                  <strong className="text-amber-800">Important Medical Disclaimer:</strong>
                  <p className="mt-1">HealthGuard AI is an informational tool only and does NOT provide medical advice, diagnosis, or treatment. All assessments are for educational purposes. Always consult qualified healthcare providers for medical decisions.</p>
                </div>
              </div>
            </div>

            {/* Informed Consent */}
            <div className="space-y-3 border-t pt-4">
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="consent_privacy"
                  checked={formData.consent_privacy}
                  onChange={handleChange}
                  className="mt-1 w-4 h-4 text-sage-teal border-slate-300 rounded focus:ring-sage-teal"
                  data-testid="consent-privacy"
                />
                <label className="text-sm text-slate-700">
                  I understand and accept the <span className="text-sage-teal font-semibold cursor-pointer hover:underline">Privacy Policy</span> and consent to the collection and processing of my health data for risk assessment purposes.
                </label>
              </div>

              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="consent_terms"
                  checked={formData.consent_terms}
                  onChange={handleChange}
                  className="mt-1 w-4 h-4 text-sage-teal border-slate-300 rounded focus:ring-sage-teal"
                  data-testid="consent-terms"
                />
                <label className="text-sm text-slate-700">
                  I agree to the <span className="text-sage-teal font-semibold cursor-pointer hover:underline">Terms of Service</span> and acknowledge that HealthGuard AI is not a substitute for professional medical advice.
                </label>
              </div>
            </div>

            {(showConsent && (!formData.consent_privacy || !formData.consent_terms)) && (
              <div className="bg-rose-50 border border-rose-200 rounded-lg p-3 flex items-center space-x-2">
                <AlertCircle className="w-5 h-5 text-rose-600" />
                <span className="text-sm text-rose-700">Please accept both consents to continue</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !formData.consent_privacy || !formData.consent_terms}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="register-submit-btn"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-center text-slate-600 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-sage-teal font-semibold hover:underline" data-testid="register-login-link">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;

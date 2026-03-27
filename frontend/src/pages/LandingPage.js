import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Activity, FileText, Bell, TrendingUp, CheckCircle, Shield, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const LandingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  React.useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-100 fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Heart className="w-8 h-8 text-sage-teal" />
            <span className="text-2xl font-bold font-manrope text-slate-800">HealthGuard AI</span>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/login')}
              className="text-slate-600 hover:text-slate-900 font-medium transition-colors"
              data-testid="nav-login-btn"
            >
              Login
            </button>
            <button
              onClick={() => navigate('/register')}
              className="btn-primary"
              data-testid="nav-register-btn"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="gradient-hero pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6" data-testid="hero-content">
              <h1 className="text-4xl md:text-6xl font-bold text-slate-800 leading-tight">
                Take Control of Your <span className="text-sage-teal">Health</span> Today
              </h1>
              <p className="text-lg text-slate-600 leading-relaxed">
                Early detection saves lives. Our AI-powered health assessment helps you understand your
                diabetes and cholesterol risk in minutes.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <button
                  onClick={() => navigate('/register')}
                  className="btn-primary"
                  data-testid="hero-get-started-btn"
                >
                  Start Free Assessment
                </button>
                <button
                  onClick={() => navigate('/login')}
                  className="btn-secondary"
                  data-testid="hero-learn-more-btn"
                >
                  Learn More
                </button>
              </div>
              <div className="flex items-center space-x-8 pt-4">
                <div>
                  <div className="text-3xl font-bold text-sage-teal">25</div>
                  <div className="text-sm text-slate-600">Quick Questions</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-sage-teal">15 min</div>
                  <div className="text-sm text-slate-600">Assessment Time</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-sage-teal">AI</div>
                  <div className="text-sm text-slate-600">Powered Analysis</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1759503610767-4bb217fa45ed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODl8MHwxfHNlYXJjaHwxfHx3ZWxsbmVzcyUyMGhhcHB5JTIwcGVyc29uJTIwbmF0dXJlfGVufDB8fHx8MTc3MTI1NjM2NHww&ixlib=rb-4.1.0&q=85"
                alt="Healthy lifestyle"
                className="rounded-2xl shadow-float w-full h-[500px] object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-white" data-testid="features-section">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4">
              Comprehensive Health Assessment
            </h2>
            <p className="text-lg text-slate-600">
              Everything you need to understand and manage your health risks
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="card-dashboard p-8" data-testid="feature-quiz">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Smart Health Quiz</h3>
              <p className="text-slate-600">
                Answer 25 carefully selected questions based on medical research to assess your diabetes
                and cholesterol risk.
              </p>
            </div>

            <div className="card-dashboard p-8" data-testid="feature-analysis">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <Activity className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">AI-Powered Analysis</h3>
              <p className="text-slate-600">
                Our Random Forest ML model analyzes your responses to provide accurate risk predictions and
                personalized recommendations.
              </p>
            </div>

            <div className="card-dashboard p-8" data-testid="feature-tracking">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Blood Test Tracking</h3>
              <p className="text-slate-600">
                Upload and track your blood test results over time. Monitor LDL, HDL, triglycerides, and
                HbA1c levels.
              </p>
            </div>

            <div className="card-dashboard p-8" data-testid="feature-reminders">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <Bell className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Smart Reminders</h3>
              <p className="text-slate-600">
                Get notified every 2 months to take your follow-up blood tests and stay on top of your
                health.
              </p>
            </div>

            <div className="card-dashboard p-8" data-testid="feature-recommendations">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Personalized Guidance</h3>
              <p className="text-slate-600">
                Receive tailored lifestyle and dietary recommendations based on your risk level and health
                data.
              </p>
            </div>

            <div className="card-dashboard p-8" data-testid="feature-history">
              <div className="w-12 h-12 bg-sage-teal/10 rounded-xl flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-sage-teal" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Health History</h3>
              <p className="text-slate-600">
                View your complete health assessment history and track your progress over time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6 gradient-hero" data-testid="how-it-works-section">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4">How It Works</h2>
            <p className="text-lg text-slate-600">Simple steps to better health</p>
          </div>

          <div className="space-y-8">
            <div className="flex items-start space-x-6">
              <div className="w-12 h-12 bg-sage-teal text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
                1
              </div>
              <div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Take the Health Quiz</h3>
                <p className="text-slate-600">
                  Answer 25 questions about your lifestyle, symptoms, and family history. Takes only 5
                  minutes.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-6">
              <div className="w-12 h-12 bg-sage-teal text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
                2
              </div>
              <div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Get Your Risk Score</h3>
                <p className="text-slate-600">
                  Our AI analyzes your responses and provides a comprehensive risk assessment for diabetes
                  and cholesterol.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-6">
              <div className="w-12 h-12 bg-sage-teal text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
                3
              </div>
              <div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Follow Recommendations</h3>
                <p className="text-slate-600">
                  Low risk? Get lifestyle tips. Medium/High risk? We'll guide you to get blood tests and
                  consult a doctor.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-6">
              <div className="w-12 h-12 bg-sage-teal text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">
                4
              </div>
              <div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Track Your Progress</h3>
                <p className="text-slate-600">
                  Upload blood test results, set reminders, and monitor your health journey over time.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-sage-teal" data-testid="cta-section">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Take Control of Your Health?
          </h2>
          <p className="text-lg text-white/90 mb-8">
            Join thousands of people who are taking proactive steps towards better health.
          </p>
          <button
            onClick={() => navigate('/register')}
            className="bg-white text-sage-teal rounded-full px-10 py-4 font-bold text-lg shadow-xl hover:shadow-2xl transition-all transform hover:-translate-y-1"
            data-testid="cta-start-btn"
          >
            Start Your Free Assessment Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Heart className="w-6 h-6" />
            <span className="text-xl font-bold font-manrope">HealthGuard AI</span>
          </div>
          <p className="text-slate-400">
            Empowering people to take control of their health through early detection and prevention.
          </p>
          <p className="text-slate-500 text-sm mt-4">
            © 2024 HealthGuard AI. For informational purposes only. Consult healthcare professionals for
            medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;

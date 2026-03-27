import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Heart, LayoutDashboard, FileText, Activity, History, Bell, LogOut, User } from 'lucide-react';

const DashboardLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const menuItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Overview' },
    { path: '/dashboard/quiz', icon: FileText, label: 'Health Quiz' },
    { path: '/dashboard/blood-test', icon: Activity, label: 'Blood Tests' },
    { path: '/dashboard/history', icon: History, label: 'History' },
    { path: '/dashboard/reminders', icon: Bell, label: 'Reminders' },
  ];

  return (
    <div className="min-h-screen bg-bg-main flex" data-testid="dashboard-layout">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6 border-b border-slate-200">
          <div className="flex items-center space-x-2">
            <Heart className="w-8 h-8 text-sage-teal" />
            <span className="text-xl font-bold font-manrope text-slate-800">HealthGuard</span>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-sage-teal text-white'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
                data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-200">
          <div className="flex items-center space-x-3 px-4 py-3 bg-slate-50 rounded-lg mb-2">
            <div className="w-10 h-10 bg-sage-teal text-white rounded-full flex items-center justify-center font-bold">
              {user?.name?.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1">
              <div className="font-medium text-slate-800 text-sm">{user?.name}</div>
              <div className="text-xs text-slate-500 truncate">{user?.email}</div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
            data-testid="logout-btn"
          >
            <LogOut className="w-5 h-5" />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardLayout;

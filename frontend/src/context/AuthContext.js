import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // 1. Load user on mount or when token changes
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        await loadUser();
      } else {
        setLoading(false);
      }
    };
    initAuth();
  }, [token]);

  const loadUser = async () => {
    try {
      const response = await authAPI.getMe();
      setUser(response.data);
    } catch (error) {
      console.error('Failed to load user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  // 2. Login Function
  const login = async (email, password) => {
    const response = await authAPI.login({ email, password });
    // This handles both 'token' and 'access_token' field names
    const userData = response.data.user;
    const tokenData = response.data.access_token || response.data.token;

    localStorage.setItem('token', tokenData);
    setToken(tokenData);
    setUser(userData);
    return userData;
  };

  // 3. Register Function
  const register = async (data) => {
    const response = await authAPI.register(data);
    const userData = response.data.user;
    const tokenData = response.data.access_token || response.data.token;

    localStorage.setItem('token', tokenData);
    setToken(tokenData);
    setUser(userData);
    return userData;
  };

  // 4. Logout Function
  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook for easy access
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
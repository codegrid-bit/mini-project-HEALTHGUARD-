import axios from 'axios';

// Fallback to localhost:8000 if the .env variable is missing
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Ensure there is only one 'Bearer ' prefix
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Quiz API
export const quizAPI = {
  getQuestions: () => api.get('/quiz/questions'),
  submitQuiz: (data) => api.post('/quiz/submit', data),
};

// Blood Test API
export const bloodTestAPI = {
  submitBloodTest: (data) => api.post('/blood-test/submit', data),
};

// History API
export const historyAPI = {
  getAssessments: () => api.get('/history/assessments'),
  getBloodTests: () => api.get('/history/blood-tests'),
};

// Reminders API
export const remindersAPI = {
  getReminders: () => api.get('/reminders'),
  completeReminder: (id) => api.put(`/reminders/${id}/complete`),
};

export default api;
import axios from 'axios';

// Get backend URL from environment or default to localhost
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

// Log the backend URL for debugging
console.log('Chat widget connecting to backend at:', BACKEND_URL);

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth headers if needed
apiClient.interceptors.request.use(
  (config) => {
    // Add any request modifications here
    // For example, add auth token if available
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

// API methods
export const apiService = {
  // Health check
  checkHealth: () => apiClient.get('/health'),

  // Chat endpoints
  createSession: (userData = {}) =>
    apiClient.post('/chat/new-session', userData),

  sendMessage: (messageData) =>
    apiClient.post('/chat', messageData),

  getSessionHistory: (sessionId) =>
    apiClient.get(`/chat/session/${sessionId}`),

  // Session management
  getSession: (sessionId) =>
    apiClient.get(`/session/${sessionId}`),

  deleteSession: (sessionId) =>
    apiClient.delete(`/session/${sessionId}`),
};

export default apiClient;
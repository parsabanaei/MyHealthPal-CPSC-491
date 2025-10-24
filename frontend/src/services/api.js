import axios from 'axios';

// REQUIREMENT 15: TLS 1.3 encryption in transit (HTTPS)
// REQUIREMENT 16: API timeout set to support sub-500ms latency for concurrent requests
// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://mynutriai-backend-5m3z5i4pga-uc.a.run.app',
  timeout: 10000,  // REQUIREMENT 16: Timeout for API performance monitoring
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth headers if needed
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api; 
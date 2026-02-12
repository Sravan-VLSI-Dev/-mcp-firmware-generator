// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = {
  // Code generation endpoints
  generateCode: `${API_BASE_URL}/api/generate-code`,
  clarifyingQuestions: `${API_BASE_URL}/api/clarifying-questions`,
  
  // Health check
  health: `${API_BASE_URL}/health`,
  
  // Utility function to make API calls
  async post(endpoint, data) {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return response.json();
  },
  
  async get(endpoint) {
    const response = await fetch(endpoint);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return response.json();
  }
};

export default api;
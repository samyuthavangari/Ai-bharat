/**
 * JanSahay AI - API Service
 * Centralized API client for all backend endpoints.
 */

const API_BASE = '/api/v1';

async function request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('jansahay_token');
    if (token) config.headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(url, config);
        const data = await res.json();
        return data;
    } catch (err) {
        console.error('API Error:', err);
        return { success: false, message: 'Network error. Please check your connection.' };
    }
}

const api = {
    // Auth
    register: (data) => request('/users/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data) => request('/users/login', { method: 'POST', body: JSON.stringify(data) }),
    getProfile: () => request('/users/profile'),
    updateProfile: (data) => request('/users/profile', { method: 'PUT', body: JSON.stringify(data) }),

    // Schemes
    searchSchemes: (params) => {
        const qs = new URLSearchParams(params).toString();
        return request(`/schemes/?${qs}`);
    },
    getScheme: (code, lang = 'en') => request(`/schemes/${code}?language=${lang}`),
    getRecommendations: (params) => {
        const qs = new URLSearchParams(params).toString();
        return request(`/schemes/recommend/for-me?${qs}`);
    },

    // Eligibility
    checkEligibility: (data, lang = 'en') => request(`/eligibility/check?language=${lang}`, { method: 'POST', body: JSON.stringify(data) }),
    bulkCheckEligibility: (data, lang = 'en') => request(`/eligibility/bulk-check?language=${lang}`, { method: 'POST', body: JSON.stringify(data) }),

    // Chat
    sendMessage: (data) => request('/chat/message', { method: 'POST', body: JSON.stringify(data) }),
    getSession: (id) => request(`/chat/session/${id}`),

    // Voice
    processVoice: (data) => request('/voice/process', { method: 'POST', body: JSON.stringify(data) }),
    textToSpeech: (text, lang) => request(`/voice/tts?text=${encodeURIComponent(text)}&language=${lang}`, { method: 'POST' }),

    // Documents
    getSchemeDocuments: (code, lang = 'en') => request(`/documents/scheme/${code}?language=${lang}`),
    getDocumentInfo: (id, lang = 'en') => request(`/documents/info/${id}?language=${lang}`),

    // Analytics
    getAnalyticsSummary: () => request('/analytics/summary'),
    getPopularSchemes: () => request('/analytics/schemes/popular'),
    getLanguageStats: () => request('/analytics/languages'),
    getDashboard: () => request('/analytics/dashboard'),

    // Health
    health: () => request('/health'),
    languages: () => request('/languages'),
};

export default api;

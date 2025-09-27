# Authentication Guide for Frontend

This guide explains how to implement authentication in your frontend application to work with the Django REST API.

## Overview

The API now uses JWT (JSON Web Token) authentication. You need to:
1. Register/Login users to get JWT tokens
2. Include the JWT token in requests to protected endpoints
3. Handle token refresh when tokens expire

## Authentication Endpoints

### 1. Register User
**POST** `/api/auth/register/`

```javascript
const response = await fetch('http://localhost:8000/api/auth/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'john_doe',
    email: 'john@example.com',
    password: 'securepassword123',
    first_name: 'John',
    last_name: 'Doe'
  })
});

const data = await response.json();
// Returns: { message, user, tokens: { access, refresh } }
```

### 2. Login User
**POST** `/api/auth/login/`

```javascript
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'john_doe',
    password: 'securepassword123'
  })
});

const data = await response.json();
// Returns: { message, user, tokens: { access, refresh } }
```

### 3. Refresh Token
**POST** `/api/auth/refresh/`

```javascript
const response = await fetch('http://localhost:8000/api/auth/refresh/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh: 'your_refresh_token_here'
  })
});

const data = await response.json();
// Returns: { access: 'new_access_token' }
```

### 4. Logout User
**POST** `/api/auth/logout/`

```javascript
const response = await fetch('http://localhost:8000/api/auth/logout/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    refresh: 'your_refresh_token_here'
  })
});
```

### 5. Get User Profile
**GET** `/api/auth/profile/`

```javascript
const response = await fetch('http://localhost:8000/api/auth/profile/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const data = await response.json();
// Returns: { user: { id, username, email, first_name, last_name, is_staff, ... } }
```

## Making Authenticated Requests

For protected endpoints (admin endpoints), include the JWT token in the Authorization header:

```javascript
const response = await fetch('http://localhost:8000/api/admin/question-stats/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

## Protected Endpoints

These endpoints require authentication (JWT token):

- `POST /api/quiz/config/update/` - Update quiz configuration (staff only)
- `GET /api/admin/attempts/` - Get quiz attempts (staff only)
- `GET /api/admin/stats/` - Get quiz statistics (staff only)
- `GET /api/admin/question-stats/` - Get question statistics (staff only)

## Public Endpoints

These endpoints don't require authentication:

- `GET /api/quiz/config/` - Get quiz configuration
- `GET /api/quiz/` - Get quiz questions
- `POST /api/quiz/submit/` - Submit quiz answers

## Username Support for Admin Panel

The API now supports usernames for better admin panel display. When submitting quiz answers, you can include a username that will be displayed in the admin panel:

### Submit Quiz with Username
```javascript
const response = await fetch('http://localhost:8000/api/quiz/submit/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    answers: {
      "1": 1,  // question_id: choice_id
      "2": 6,
      "3": 9
    },
    time_taken: 300,  // in seconds
    session_id: 'unique_session_id',
    username: 'john_doe'  // Optional: for display in admin panel
  })
});

const data = await response.json();
// Returns: { score, total_points, percentage, time_taken, attempt_id, username, results }
```

### Admin Panel Data Structure
The admin endpoints now return quiz attempts with username information:

```javascript
// GET /api/admin/attempts/ response structure
[
  {
    "id": 1,
    "username": "john_doe",
    "username_display": "john_doe",  // Fallback display name
    "user_session": "session_123",
    "score": 85,
    "total_questions": 30,
    "percentage": 85.0,
    "time_taken": 300,
    "completed_at": "2025-09-27T10:30:00Z",
    "user": null  // User object if authenticated
  }
]
```

### Username Priority
1. **Explicit username** - If provided in the request
2. **Authenticated user** - If user is logged in, uses their username
3. **Anonymous** - If neither is available

## Frontend Implementation Example

### 1. Store Tokens
```javascript
// Store tokens in localStorage or secure storage
localStorage.setItem('accessToken', data.tokens.access);
localStorage.setItem('refreshToken', data.tokens.refresh);
```

### 2. Create API Helper
```javascript
class QuizAPI {
  constructor() {
    this.baseURL = 'http://localhost:8000/api';
  }

  async makeRequest(endpoint, options = {}) {
    const token = localStorage.getItem('accessToken');
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    // Handle token expiration
    if (response.status === 401) {
      await this.refreshToken();
      // Retry request with new token
      config.headers['Authorization'] = `Bearer ${localStorage.getItem('accessToken')}`;
      return fetch(`${this.baseURL}${endpoint}`, config);
    }
    
    return response;
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await fetch(`${this.baseURL}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken })
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('accessToken', data.access);
    } else {
      // Redirect to login
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
  }

  // Authentication methods
  async login(username, password) {
    const response = await this.makeRequest('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    return response.json();
  }

  async register(userData) {
    const response = await this.makeRequest('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
    return response.json();
  }

  // Quiz methods
  async getQuizQuestions() {
    const response = await this.makeRequest('/quiz/');
    return response.json();
  }

  async getQuestionStats() {
    const response = await this.makeRequest('/admin/question-stats/');
    return response.json();
  }
}

export default new QuizAPI();
```

### 3. Usage in Components
```javascript
import QuizAPI from './QuizAPI';

// Login
const handleLogin = async (username, password) => {
  try {
    const data = await QuizAPI.login(username, password);
    localStorage.setItem('accessToken', data.tokens.access);
    localStorage.setItem('refreshToken', data.tokens.refresh);
    // Redirect to dashboard
  } catch (error) {
    console.error('Login failed:', error);
  }
};

// Fetch protected data
const fetchQuestionStats = async () => {
  try {
    const stats = await QuizAPI.getQuestionStats();
    setQuestionStats(stats);
  } catch (error) {
    console.error('Failed to fetch stats:', error);
  }
};
```

## Test Credentials

For testing purposes, you can use:
- **Username**: `adminuser`
- **Password**: `admin123`

This user has staff privileges and can access all admin endpoints.

## Token Expiration

- **Access Token**: Valid for 60 minutes
- **Refresh Token**: Valid for 7 days

The API will return a 401 status when the access token expires. Your frontend should automatically refresh the token and retry the request.

## Error Handling

Common error responses:
- `400` - Bad Request (missing required fields)
- `401` - Unauthorized (invalid credentials or expired token)
- `403` - Forbidden (insufficient permissions)
- `500` - Internal Server Error

Always check the response status and handle errors appropriately in your frontend.

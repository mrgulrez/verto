# 🧠 Verto Quiz API

A comprehensive Django REST API for online quiz applications with JWT authentication, real-time scoring, and detailed analytics. Built with Django 5.2.6 and Django REST Framework, designed for seamless integration with modern frontend applications.

## ✨ Features

### 🔐 Authentication & User Management
- **JWT-based Authentication** with access and refresh tokens
- **User Registration & Login** with email validation
- **Profile Management** - view and update user profiles
- **Password Change** functionality with validation
- **Token Refresh** mechanism for seamless user experience
- **Secure Logout** with token blacklisting
- **Staff-only Admin Access** for quiz management

### 📝 Quiz Management
- **Dynamic Quiz Configuration** - timer, attempts, result display settings
- **Question Management** with categories and difficulty levels
- **Multiple Choice Questions** with correct answer tracking
- **Points System** for scoring questions
- **Active/Inactive Question States** for quiz control
- **Real-time Quiz Submission** with instant scoring

### 📊 Analytics & Statistics
- **Comprehensive Quiz Statistics** - total attempts, average scores, time analysis
- **Score Distribution Analysis** - excellent, good, average, poor performance categories
- **Question-level Analytics** - accuracy rates and attempt statistics
- **User Performance Tracking** with detailed attempt history
- **Admin Dashboard Data** for quiz administrators

### 🚀 Technical Features
- **RESTful API Design** with proper HTTP status codes
- **CORS Support** for cross-origin requests
- **Database Agnostic** - supports PostgreSQL, SQLite, and other databases
- **Environment-based Configuration** for development and production
- **API Documentation** with DRF Spectacular (OpenAPI/Swagger)
- **Vercel Deployment Ready** with optimized settings
- **Static File Serving** with WhiteNoise
- **Security Headers** and production-ready configurations

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (recommended) or SQLite
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/mrgulrez/verto-quiz-api.git
cd verto-quiz-api
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` with your configuration:
```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (REQUIRED)
DATABASE_URL=postgres://username:password@localhost:5432/quiz_db

# Deployment Configuration
VERCEL=False
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Populate with sample data (optional)
python manage.py populate_mock_data
```

### 6. Run the Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Base URL
- **Development**: `http://localhost:8000/api/`
- **Production**: `https://your-domain.com/api/`

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login User
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "johndoe",
    "password": "securepassword123"
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer your-access-token
```

#### Update Profile
```http
POST /api/auth/profile/update/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@example.com"
}
```

#### Change Password
```http
POST /api/auth/change-password/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "old_password": "oldpassword",
    "new_password": "newpassword123"
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

### Quiz Endpoints

#### Get Quiz Configuration
```http
GET /api/quiz/config/
```

#### Get Quiz Questions
```http
GET /api/quiz/
```

#### Submit Quiz Answers
```http
POST /api/quiz/submit/
Content-Type: application/json

{
    "answers": {
        "1": 3,
        "2": 7,
        "3": 12
    },
    "time_taken": 300,
    "session_id": "session_123",
    "username": "johndoe"
}
```

### Admin Endpoints (Require Staff Authentication)

#### Update Quiz Configuration
```http
POST /api/quiz/config/update/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "timer_duration": 15,
    "max_attempts": 3,
    "show_results_immediately": true
}
```

#### Get Quiz Attempts
```http
GET /api/admin/attempts/
Authorization: Bearer your-access-token
```

#### Get Quiz Statistics
```http
GET /api/admin/stats/
Authorization: Bearer your-access-token
```

#### Get Question Statistics
```http
GET /api/admin/question-stats/
Authorization: Bearer your-access-token
```

## 🗄️ Database Models

### QuizConfig
- `timer_duration`: Quiz timer in minutes
- `is_active`: Whether quiz is active
- `max_attempts`: Maximum attempts per user
- `show_results_immediately`: Show results after submission

### Question
- `text`: Question text
- `category`: Question category
- `difficulty`: Easy, Medium, Hard
- `points`: Points for correct answer
- `is_active`: Whether question is active

### Choice
- `question`: Foreign key to Question
- `text`: Choice text
- `is_correct`: Whether this is the correct answer

### QuizAttempt
- `user`: User who attempted (optional)
- `username`: Username for anonymous attempts
- `user_session`: Session identifier
- `score`: Points scored
- `total_questions`: Total questions attempted
- `percentage`: Score percentage
- `time_taken`: Time taken in seconds
- `user_answers`: JSON field storing user answers

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Configure Environment Variables**
Set these in your Vercel dashboard:
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `VERCEL`: `True`
- `ALLOWED_HOSTS`: Your Vercel domain
- `CORS_ALLOWED_ORIGINS`: Your frontend domain

3. **Deploy**
```bash
vercel --prod
```

### Other Platforms
The API is compatible with:
- **Heroku** - Add `Procfile` and configure environment variables
- **Railway** - Connect GitHub repository and set environment variables
- **DigitalOcean App Platform** - Configure build and run commands
- **AWS/GCP/Azure** - Use container deployment or serverless functions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | Yes |
| `DEBUG` | Debug mode | `True` | No |
| `DATABASE_URL` | Database connection string | - | Yes |
| `VERCEL` | Vercel deployment flag | `False` | No |
| `ALLOWED_HOSTS` | Allowed host domains | `localhost,127.0.0.1` | No |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` | No |

### JWT Configuration
- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled
- **Algorithm**: HS256

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### API Testing with cURL
```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get quiz questions
curl -X GET http://localhost:8000/api/quiz/
```

## 📁 Project Structure

```
verto-quiz-api/
├── quiz_project/          # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI application
├── quiz_api/             # Main application
│   ├── models.py         # Database models
│   ├── views.py          # API views
│   ├── auth_views.py     # Authentication views
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # API URL patterns
│   ├── admin.py          # Django admin configuration
│   └── management/       # Custom management commands
│       └── commands/
│           └── populate_mock_data.py
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── env.example          # Environment variables example
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Gulrez Alam**  
Email: [egulrezalam@gmail.com](mailto:egulrezalam@gmail.com)

---

## 🔗 Related Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Vercel Deployment](https://vercel.com/docs)

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/mrgulrez/verto-quiz-api/issues) page
2. Create a new issue with detailed description
3. Contact the developer at [egulrezalam@gmail.com](mailto:egulrezalam@gmail.com)

---

**Happy Quizzing! 🎯**
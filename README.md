# Quiz Backend API

A Django REST Framework backend for an online quiz application, ready for deployment on Vercel.

## Features

- RESTful API for quiz management
- Django REST Framework with DRF Spectacular for API documentation
- CORS support for frontend integration
- Production-ready configuration for Vercel deployment
- PostgreSQL support for production
- Automatic API documentation

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mrgulrez/verto.git
   cd quiz-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv quiz_env
   # On Windows
   quiz_env\Scripts\activate
   # On Mac/Linux
   source quiz_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/schema/

## API Endpoints

- `GET /api/quizzes/` - List all quizzes
- `POST /api/quizzes/` - Create a new quiz
- `GET /api/quizzes/{id}/` - Get quiz details
- `PUT /api/quizzes/{id}/` - Update quiz
- `DELETE /api/quizzes/{id}/` - Delete quiz
- `GET /api/schema/` - API documentation (Swagger/ReDoc)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Vercel deployment instructions.

### Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmrgulrez%2Fverto)

### Environment Variables

Required for production:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `CORS_ALLOWED_ORIGINS` - Comma-separated CORS origins

## Project Structure

```
quiz-backend/
├── quiz_api/              # Main API app
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   └── urls.py           # API URLs
├── quiz_project/          # Project configuration
│   ├── settings.py       # Settings (development & production)
│   ├── urls.py           # Main URLs
│   └── wsgi.py           # WSGI configuration
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── api/                  # Vercel serverless functions
│   └── index.py         # Main entry point
└── manage.py             # Django management script
```

## Technology Stack

- **Backend Framework**: Django 5.2.6
- **API Framework**: Django REST Framework 3.16.1
- **API Documentation**: DRF Spectacular
- **CORS**: Django CORS Headers
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Vercel
- **Static Files**: WhiteNoise

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Gulrez Alam**
- GitHub: [@mrgulrez](https://github.com/mrgulrez)

## Support

For support, email egulrezalam@gmail.com or open an issue on GitHub.

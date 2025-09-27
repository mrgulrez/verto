from django.urls import path
from . import views, auth_views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', auth_views.register),
    path('auth/login/', auth_views.login),
    path('auth/refresh/', auth_views.refresh_token),
    path('auth/logout/', auth_views.logout),
    path('auth/profile/', auth_views.user_profile),
    path('auth/profile/update/', auth_views.update_profile),
    path('auth/change-password/', auth_views.change_password),
    
    # Quiz endpoints (public)
    path('quiz/config/', views.get_quiz_config),
    path('quiz/', views.get_quiz_questions),
    path('quiz/submit/', views.submit_quiz_answers),
    
    # Admin endpoints (require authentication)
    path('quiz/config/update/', views.update_quiz_config),
    path('admin/attempts/', views.get_quiz_attempts),
    path('admin/stats/', views.get_quiz_stats),
    path('admin/question-stats/', views.get_question_stats),
]
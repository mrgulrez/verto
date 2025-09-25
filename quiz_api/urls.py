from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.get_quiz_questions),
    path('quiz/submit/', views.submit_quiz_answers),
]
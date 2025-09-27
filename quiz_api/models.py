from django.db import models
from django.contrib.auth.models import User

class QuizConfig(models.Model):
    timer_duration = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    max_attempts = models.PositiveIntegerField(default=1)
    show_results_immediately = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Quiz Configuration (Timer: {self.timer_duration}min)"

class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="General")
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], default='medium')
    points = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question.text} - {self.text}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    user_session = models.CharField(max_length=100)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0)
    time_taken = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    user_answers = models.JSONField(default=dict)
    
    def __str__(self):
        username_display = self.username or self.user.username if self.user else "Anonymous"
        return f"{username_display} - Score: {self.score}/{self.total_questions}"
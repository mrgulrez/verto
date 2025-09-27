from django.contrib import admin
from .models import QuizConfig, Question, Choice, QuizAttempt

@admin.register(QuizConfig)
class QuizConfigAdmin(admin.ModelAdmin):
    list_display = ['timer_duration', 'is_active', 'max_attempts', 'created_at']
    list_editable = ['is_active', 'max_attempts']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'difficulty', 'points', 'is_active']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['text']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_correct']
    list_filter = ['question', 'is_correct']
    search_fields = ['text', 'question__text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_session', 'score', 'total_questions', 'percentage', 'time_taken', 'completed_at']
    list_filter = ['completed_at', 'user']
    search_fields = ['username', 'user_session', 'user__username']
    readonly_fields = ['completed_at']
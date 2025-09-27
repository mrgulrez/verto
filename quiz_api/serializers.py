from rest_framework import serializers
from .models import Question, Choice, QuizConfig, QuizAttempt

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'choices', 'category', 'difficulty', 'points']

class QuizConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizConfig
        fields = '__all__'

class QuizAttemptSerializer(serializers.ModelSerializer):
    username_display = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizAttempt
        fields = '__all__'
    
    def get_username_display(self, obj):
        return obj.username or (obj.user.username if obj.user else "Anonymous")
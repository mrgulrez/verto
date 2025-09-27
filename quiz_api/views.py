from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from .models import Question, Choice, QuizConfig, QuizAttempt
from .serializers import QuestionSerializer, QuizConfigSerializer, QuizAttemptSerializer
from django.db import models

@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_config(request):
    config = QuizConfig.objects.first()
    if not config:
        config = QuizConfig.objects.create()
    serializer = QuizConfigSerializer(config)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_member_required
def update_quiz_config(request):
    config = QuizConfig.objects.first()
    if not config:
        config = QuizConfig.objects.create()
    
    serializer = QuizConfigSerializer(config, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_questions(request):
    questions = Question.objects.filter(is_active=True)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_quiz_answers(request):
    user_answers = request.data.get('answers', {})
    time_taken = request.data.get('time_taken', 0)
    user_session = request.data.get('session_id', 'anonymous')
    username = request.data.get('username', '')
    
    score = 0
    total_points = 0
    results = []
    questions = Question.objects.filter(is_active=True)
    
    for question in questions:
        choice_id = user_answers.get(str(question.id))
        total_points += question.points
        
        try:
            selected_choice = Choice.objects.get(id=choice_id) if choice_id else None
            correct_choice = Choice.objects.get(question=question, is_correct=True)
            
            is_correct = selected_choice and selected_choice.is_correct
            if is_correct:
                score += question.points
                
            results.append({
                'question_id': question.id,
                'question_text': question.text,
                'user_answer_id': int(choice_id) if choice_id else None,
                'user_answer_text': selected_choice.text if selected_choice else "No answer",
                'correct_answer_id': correct_choice.id,
                'correct_answer_text': correct_choice.text,
                'is_correct': is_correct,
                'points': question.points if is_correct else 0
            })
        except (Choice.DoesNotExist, ValueError):
            results.append({
                'question_id': question.id,
                'question_text': question.text,
                'user_answer_id': None,
                'user_answer_text': "No answer",
                'correct_answer_id': None,
                'correct_answer_text': "Error loading answer",
                'is_correct': False,
                'points': 0
            })
    
    percentage = (score / total_points * 100) if total_points > 0 else 0
    
    # Determine user and username
    user = request.user if request.user.is_authenticated else None
    display_username = username or (user.username if user else "Anonymous")
    
    attempt = QuizAttempt.objects.create(
        user=user,
        username=display_username,
        user_session=user_session,
        score=score,
        total_questions=len(questions),
        percentage=percentage,
        time_taken=time_taken,
        user_answers=user_answers
    )
    
    return Response({
        'score': score,
        'total_points': total_points,
        'percentage': round(percentage, 2),
        'time_taken': time_taken,
        'attempt_id': attempt.id,
        'username': display_username,
        'results': results
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_member_required
def get_quiz_attempts(request):
    attempts = QuizAttempt.objects.all().order_by('-completed_at')
    serializer = QuizAttemptSerializer(attempts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_member_required
def get_quiz_stats(request):
    attempts = QuizAttempt.objects.all()
    total_attempts = attempts.count()
    avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg'] or 0
    avg_time = attempts.aggregate(Avg('time_taken'))['time_taken__avg'] or 0
    
    # Calculate score distribution
    score_distribution = attempts.aggregate(
        excellent=Count('id', filter=models.Q(percentage__gte=90)),
        good=Count('id', filter=models.Q(percentage__gte=70, percentage__lt=90)),
        average=Count('id', filter=models.Q(percentage__gte=50, percentage__lt=70)),
        poor=Count('id', filter=models.Q(percentage__lt=50))
    )
    
    return Response({
        'total_attempts': total_attempts,
        'average_score': round(avg_score, 2),
        'average_time_taken': round(avg_time, 2),
        'total_questions': Question.objects.filter(is_active=True).count(),
        'score_distribution': score_distribution
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_member_required
def get_question_stats(request):
    questions = Question.objects.filter(is_active=True).prefetch_related('choices')
    question_stats = []
    
    # Get total attempts count once
    total_attempts = QuizAttempt.objects.count()
    
    if total_attempts == 0:
        # If no attempts, return empty stats for all questions
        for question in questions:
            question_stats.append({
                'question_id': question.id,
                'question_text': question.text,
                'difficulty': question.difficulty,
                'total_attempts': 0,
                'correct_attempts': 0,
                'accuracy': 0.0
            })
        return Response(question_stats)
    
    # Get all correct choice IDs for all questions
    correct_choices = {}
    for question in questions:
        correct_choice = question.choices.filter(is_correct=True).first()
        if correct_choice:
            correct_choices[question.id] = correct_choice.id
    
    # Get all attempts with their user_answers in one query
    all_attempts = list(QuizAttempt.objects.values('user_answers'))
    
    # Process each question
    for question in questions:
        correct_attempts = 0
        
        if question.id in correct_choices:
            correct_choice_id = correct_choices[question.id]
            
            # Count correct attempts for this question
            for attempt in all_attempts:
                user_answer = attempt['user_answers'].get(str(question.id))
                if user_answer == correct_choice_id:
                    correct_attempts += 1
        
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        question_stats.append({
            'question_id': question.id,
            'question_text': question.text,
            'difficulty': question.difficulty,
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'accuracy': round(accuracy, 2)
        })
    
    return Response(question_stats)
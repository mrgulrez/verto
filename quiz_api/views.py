from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice
from .serializers import QuestionSerializer

@api_view(['GET'])
def get_quiz_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def submit_quiz_answers(request):
    user_answers = request.data
    score = 0
    results = []
    
    for question_id, choice_id in user_answers.items():
        try:
            selected_choice = Choice.objects.get(id=choice_id)
            correct_choice = Choice.objects.get(question_id=question_id, is_correct=True)
            
            is_correct = selected_choice.is_correct
            if is_correct:
                score += 1
                
            results.append({
                'question_id': int(question_id),
                'user_answer_id': int(choice_id),
                'correct_answer_id': correct_choice.id,
                'is_correct': is_correct
            })
        except (Choice.DoesNotExist, ValueError):
            continue
    
    return Response({
        'score': score,
        'results': results
    })
from django.core.management.base import BaseCommand
from django.db import transaction
from quiz_api.models import QuizConfig, Question, Choice, QuizAttempt
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with mock data for frontend testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            QuizAttempt.objects.all().delete()
            Choice.objects.all().delete()
            Question.objects.all().delete()
            QuizConfig.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        with transaction.atomic():
            self.create_quiz_config()
            self.create_questions_and_choices()
            self.create_quiz_attempts()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with mock data!')
        )

    def create_quiz_config(self):
        """Create quiz configuration"""
        config, created = QuizConfig.objects.get_or_create(
            defaults={
                'timer_duration': 15,
                'is_active': True,
                'max_attempts': 3,
                'show_results_immediately': True,
            }
        )
        if created:
            self.stdout.write('Created quiz configuration')
        else:
            self.stdout.write('Quiz configuration already exists')

    def create_questions_and_choices(self):
        """Create questions with multiple choice answers"""
        
        # Programming Questions
        programming_questions = [
            {
                'text': 'What does HTML stand for?',
                'category': 'Programming',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('HyperText Markup Language', True),
                    ('High Tech Modern Language', False),
                    ('Home Tool Markup Language', False),
                    ('Hyperlink and Text Markup Language', False),
                ]
            },
            {
                'text': 'Which programming language is known for its use in web development?',
                'category': 'Programming',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Python', False),
                    ('JavaScript', True),
                    ('C++', False),
                    ('Java', False),
                ]
            },
            {
                'text': 'What is the correct way to declare a variable in JavaScript?',
                'category': 'Programming',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('var name = "John";', True),
                    ('variable name = "John";', False),
                    ('v name = "John";', False),
                    ('declare name = "John";', False),
                ]
            },
            {
                'text': 'Which CSS property is used to change the text color?',
                'category': 'Programming',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('text-color', False),
                    ('color', True),
                    ('font-color', False),
                    ('text-style', False),
                ]
            },
            {
                'text': 'What does API stand for?',
                'category': 'Programming',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Application Programming Interface', True),
                    ('Advanced Programming Integration', False),
                    ('Automated Program Interface', False),
                    ('Application Process Integration', False),
                ]
            },
            {
                'text': 'Which method is used to add an element to the end of an array in JavaScript?',
                'category': 'Programming',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('array.add()', False),
                    ('array.push()', True),
                    ('array.append()', False),
                    ('array.insert()', False),
                ]
            },
            {
                'text': 'What is the purpose of the "use strict" directive in JavaScript?',
                'category': 'Programming',
                'difficulty': 'hard',
                'points': 20,
                'choices': [
                    ('To enable strict mode for better error checking', True),
                    ('To disable all error checking', False),
                    ('To make the code run faster', False),
                    ('To enable experimental features', False),
                ]
            },
            {
                'text': 'Which HTML tag is used to create a hyperlink?',
                'category': 'Programming',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('<link>', False),
                    ('<a>', True),
                    ('<href>', False),
                    ('<url>', False),
                ]
            },
            {
                'text': 'What does SQL stand for?',
                'category': 'Programming',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Structured Query Language', True),
                    ('Simple Query Language', False),
                    ('Standard Query Language', False),
                    ('System Query Language', False),
                ]
            },
            {
                'text': 'Which CSS property is used to control the spacing between elements?',
                'category': 'Programming',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('spacing', False),
                    ('margin', True),
                    ('padding', False),
                    ('gap', False),
                ]
            }
        ]

        # General Knowledge Questions
        general_questions = [
            {
                'text': 'What is the capital of France?',
                'category': 'General Knowledge',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('London', False),
                    ('Berlin', False),
                    ('Paris', True),
                    ('Madrid', False),
                ]
            },
            {
                'text': 'Which planet is known as the Red Planet?',
                'category': 'General Knowledge',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Venus', False),
                    ('Mars', True),
                    ('Jupiter', False),
                    ('Saturn', False),
                ]
            },
            {
                'text': 'Who painted the Mona Lisa?',
                'category': 'General Knowledge',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Vincent van Gogh', False),
                    ('Pablo Picasso', False),
                    ('Leonardo da Vinci', True),
                    ('Michelangelo', False),
                ]
            },
            {
                'text': 'What is the largest ocean on Earth?',
                'category': 'General Knowledge',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Atlantic Ocean', False),
                    ('Indian Ocean', False),
                    ('Pacific Ocean', True),
                    ('Arctic Ocean', False),
                ]
            },
            {
                'text': 'Which year did World War II end?',
                'category': 'General Knowledge',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('1944', False),
                    ('1945', True),
                    ('1946', False),
                    ('1947', False),
                ]
            },
            {
                'text': 'What is the chemical symbol for gold?',
                'category': 'General Knowledge',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Go', False),
                    ('Gd', False),
                    ('Au', True),
                    ('Ag', False),
                ]
            },
            {
                'text': 'Which country is known as the Land of the Rising Sun?',
                'category': 'General Knowledge',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('China', False),
                    ('Japan', True),
                    ('South Korea', False),
                    ('Thailand', False),
                ]
            },
            {
                'text': 'What is the smallest prime number?',
                'category': 'General Knowledge',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('0', False),
                    ('1', False),
                    ('2', True),
                    ('3', False),
                ]
            },
            {
                'text': 'Which gas makes up most of Earth\'s atmosphere?',
                'category': 'General Knowledge',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Oxygen', False),
                    ('Carbon Dioxide', False),
                    ('Nitrogen', True),
                    ('Hydrogen', False),
                ]
            },
            {
                'text': 'What is the fastest land animal?',
                'category': 'General Knowledge',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Lion', False),
                    ('Cheetah', True),
                    ('Leopard', False),
                    ('Tiger', False),
                ]
            }
        ]

        # Science Questions
        science_questions = [
            {
                'text': 'What is the speed of light in vacuum?',
                'category': 'Science',
                'difficulty': 'hard',
                'points': 20,
                'choices': [
                    ('300,000 km/s', True),
                    ('150,000 km/s', False),
                    ('450,000 km/s', False),
                    ('600,000 km/s', False),
                ]
            },
            {
                'text': 'What is the chemical formula for water?',
                'category': 'Science',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('H2O', True),
                    ('CO2', False),
                    ('NaCl', False),
                    ('O2', False),
                ]
            },
            {
                'text': 'Which force keeps planets in orbit around the sun?',
                'category': 'Science',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Magnetic force', False),
                    ('Gravitational force', True),
                    ('Electric force', False),
                    ('Nuclear force', False),
                ]
            },
            {
                'text': 'What is the process by which plants make their food?',
                'category': 'Science',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Respiration', False),
                    ('Photosynthesis', True),
                    ('Digestion', False),
                    ('Fermentation', False),
                ]
            },
            {
                'text': 'What is the atomic number of carbon?',
                'category': 'Science',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('6', True),
                    ('12', False),
                    ('8', False),
                    ('14', False),
                ]
            },
            {
                'text': 'Which type of energy is stored in a battery?',
                'category': 'Science',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Kinetic energy', False),
                    ('Potential energy', False),
                    ('Chemical energy', True),
                    ('Thermal energy', False),
                ]
            },
            {
                'text': 'What is the unit of electric current?',
                'category': 'Science',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Volt', False),
                    ('Ampere', True),
                    ('Watt', False),
                    ('Ohm', False),
                ]
            },
            {
                'text': 'Which gas is responsible for the greenhouse effect?',
                'category': 'Science',
                'difficulty': 'medium',
                'points': 15,
                'choices': [
                    ('Oxygen', False),
                    ('Nitrogen', False),
                    ('Carbon Dioxide', True),
                    ('Hydrogen', False),
                ]
            },
            {
                'text': 'What is the hardest natural substance on Earth?',
                'category': 'Science',
                'difficulty': 'easy',
                'points': 10,
                'choices': [
                    ('Gold', False),
                    ('Iron', False),
                    ('Diamond', True),
                    ('Platinum', False),
                ]
            },
            {
                'text': 'Which particle has no electric charge?',
                'category': 'Science',
                'difficulty': 'hard',
                'points': 20,
                'choices': [
                    ('Proton', False),
                    ('Electron', False),
                    ('Neutron', True),
                    ('Ion', False),
                ]
            }
        ]

        all_questions = programming_questions + general_questions + science_questions

        for question_data in all_questions:
            question, created = Question.objects.get_or_create(
                text=question_data['text'],
                defaults={
                    'category': question_data['category'],
                    'difficulty': question_data['difficulty'],
                    'points': question_data['points'],
                    'is_active': True,
                }
            )
            
            if created:
                # Create choices for the question
                for choice_text, is_correct in question_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                self.stdout.write(f'Created question: {question.text[:50]}...')
            else:
                self.stdout.write(f'Question already exists: {question.text[:50]}...')

    def create_quiz_attempts(self):
        """Create sample quiz attempts for testing"""
        
        # Get all questions for creating realistic attempts
        questions = list(Question.objects.filter(is_active=True))
        if not questions:
            self.stdout.write('No questions found. Skipping quiz attempts creation.')
            return

        # Sample user sessions with usernames
        user_data = [
            ('user_001', 'john_doe'),
            ('user_002', 'jane_smith'),
            ('user_003', 'mike_wilson'),
            ('user_004', 'sarah_jones'),
            ('user_005', 'alex_brown'),
            ('test_user_1', 'test_user_1'),
            ('test_user_2', 'test_user_2'),
            ('demo_user', 'demo_user'),
            ('guest_001', 'Guest User 1'),
            ('guest_002', 'Guest User 2')
        ]

        # Create various quiz attempts with different scores
        for i, (session, username) in enumerate(user_data):
            # Create user answers (simulate different performance levels)
            user_answers = {}
            score = 0
            total_points = 0
            
            for question in questions:
                total_points += question.points
                choices = question.choices.all()
                
                # Simulate different accuracy levels
                if i < 2:  # High performers
                    accuracy = 0.9
                elif i < 5:  # Medium performers
                    accuracy = 0.7
                else:  # Lower performers
                    accuracy = 0.4
                
                # Randomly select correct or incorrect answer based on accuracy
                if random.random() < accuracy:
                    # Select correct answer
                    correct_choice = choices.filter(is_correct=True).first()
                    if correct_choice:
                        user_answers[str(question.id)] = correct_choice.id
                        score += question.points
                else:
                    # Select incorrect answer
                    incorrect_choices = list(choices.filter(is_correct=False))
                    if incorrect_choices:
                        selected_choice = random.choice(incorrect_choices)
                        user_answers[str(question.id)] = selected_choice.id

            percentage = (score / total_points * 100) if total_points > 0 else 0
            time_taken = random.randint(300, 900)  # 5-15 minutes in seconds

            # Create quiz attempt
            QuizAttempt.objects.create(
                username=username,
                user_session=session,
                score=score,
                total_questions=len(questions),
                percentage=round(percentage, 2),
                time_taken=time_taken,
                user_answers=user_answers,
                completed_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )

        self.stdout.write(f'Created {len(user_data)} quiz attempts')

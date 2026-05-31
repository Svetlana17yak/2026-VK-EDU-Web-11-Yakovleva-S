
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from web_vk.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Fills database with fake data. Usage: python manage.py fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()
        
        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        likes_count = ratio * 200

        self.stdout.write(f'Starting generation with ratio {ratio}...')

        # 1. Users & Profiles
        users = []
        for i in range(users_count):
            users.append(User(username=f'{fake.user_name()}_{i}', email=fake.email(), password='password123'))
        User.objects.bulk_create(users, batch_size=1000)
        
        saved_users = list(User.objects.all())
        profiles = [Profile(user=u) for u in saved_users]
        Profile.objects.bulk_create(profiles, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Users created'))

        # 2. Tags
        tags = [Tag(name=f'tag_{fake.word()}_{i}') for i in range(tags_count)]
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        saved_tags = list(Tag.objects.all())
        self.stdout.write(self.style.SUCCESS('Tags created'))

        # 3. Questions
        questions = []
        for i in range(questions_count):
            questions.append(Question(
                title=fake.sentence()[:255],
                text=fake.text(),
                author=random.choice(saved_users),
            ))
        Question.objects.bulk_create(questions, batch_size=1000)
        saved_questions = list(Question.objects.all())
        
        # M2M Tags for questions
        ThroughModel = Question.tags.through
        question_tags = []
        for q in saved_questions:
            q_tags = random.sample(saved_tags, random.randint(1, 4))
            for t in q_tags:
                question_tags.append(ThroughModel(question_id=q.id, tag_id=t.id))
        ThroughModel.objects.bulk_create(question_tags, batch_size=5000)
        self.stdout.write(self.style.SUCCESS('Questions created'))

        # 4. Answers
        answers = []
        for i in range(answers_count):
            answers.append(Answer(
                text=fake.text(),
                author=random.choice(saved_users),
                question=random.choice(saved_questions),
                is_correct=random.choice([True, False, False, False])
            ))
        Answer.objects.bulk_create(answers, batch_size=5000)
        self.stdout.write(self.style.SUCCESS('Answers created'))

        # 5. Likes 
        likes = []
        for i in range(likes_count):
            likes.append(QuestionLike(
                user=random.choice(saved_users),
                question=random.choice(saved_questions),
                is_like=random.choice([True, False])
            ))
        QuestionLike.objects.bulk_create(likes, ignore_conflicts=True, batch_size=5000)
        self.stdout.write(self.style.SUCCESS('Likes created'))
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User



QUESTIONS = [
    {
        'id': 1,
        'title': 'How to build a moon park?',
        'text': 'Guys, I have trouble with a moon park. Can\'t find the black-jack...',
        'tags': ['black-jack', 'bender'],
        'rating': 5,
        'answers_count': 3
    },
    {
        'id': 2,
        'title': 'How to center a div?',
        'text': 'I have tried everything, please help!',
        'tags': ['html', 'css'],
        'rating': 12,
        'answers_count': 5
    },
    {
        'id': 3,
        'title': 'Is Python better than C++?',
        'text': 'Just wondering what should I learn first.',
        'tags': ['python', 'c++'],
        'rating': -2,
        'answers_count': 10
    },

    {
        'id': 4,
        'title': 'How to build a moon park? (4)',
        'text': 'Another question about the park.',
        'tags': ['bender'],
        'rating': 0,
        'answers_count': 0
    },

    {
        'id': 5,
        'title': 'Is Python better than C++?',
        'text': 'Just wondering what should I learn first.',
        'tags': ['python', 'c++'],
        'rating': -2,
        'answers_count': 10
    },

    {
        'id': 6,
        'title': 'Is Python better than C++?',
        'text': 'Just wondering what should I learn first.',
        'tags': ['python', 'c++'],
        'rating': -2,
        'answers_count': 10
    },

    {
        'id': 7,
        'title': 'Is Python better than C++?',
        'text': 'Just wondering what should I learn first.',
        'tags': ['python', 'c++'],
        'rating': -2,
        'answers_count': 10
    },

    {
        'id': 8,
        'title': 'Is Python better than C++?',
        'text': 'Just wondering what should I learn first.',
        'tags': ['python', 'c++'],
        'rating': -2,
        'answers_count': 10
    },
]

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не целое число, возвращаем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем всего страниц, возвращаем последнюю
        page_obj = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    
    return page_obj, page_range
def index(request):
    page_obj, page_range = paginate(QUESTIONS, request, per_page=3)
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'page_range': page_range
    })
def tag_questions(request, tag_name):
    filtered_questions = []
    for q in QUESTIONS:
        if tag_name in q['tags']:
            filtered_questions.append(q)

    page_obj = paginate(filtered_questions, request, per_page=5)
    
    return render(request, 'tag_list.html', {
        'tag_name': tag_name,
        'page_obj': page_obj
    })

def ask(request):
    return render(request, 'ask.html')

def ask_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def register_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            error_message = "Sorry, passwords do not match!"
        elif User.objects.filter(username=username).exists():
            error_message = "Sorry, this login is already taken!"
        elif User.objects.filter(email=email).exists():
            error_message = "Sorry, this email address already registered!"
        else:
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)

            return redirect('index')

    return render(request, 'register.html', {'error_message': error_message})

def setting(request):
    return render(request, 'setting.html')

def question(request, question_id):
    item = {
        'id': question_id,
        'title': f'How to build a moon park? ({question_id})',
        'text': "Guys, I have trouble. Can't find the black-jack...",
        'rating': 5,
    }
    
    answers_list = []
    for i in range(1, 3):
        answers_list.append({
            'id': i,
            'text': f'Это текст ответа номер {i} на вопрос {question_id}. Здесь кто-то очень умный помогает решить проблему.',
            'rating': 5
        })

    return render(request, 'question.html', {'question': item, 'answers': answers_list})

def logout_view(request):
    logout(request) # забываем пользователя
    return redirect('index')

def tag_questions(request, tag_name):
    filtered_questions = []
    for q in QUESTIONS:
        if tag_name in q['tags']:
            filtered_questions.append(q)
            

    paginator = Paginator(filtered_questions, 3)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    

    return render(request, 'tag_list.html', {
        'tag_name': tag_name,
        'page_obj': page_obj, 'page_range': page_range
    })

def hot(request):

    hot = sorted(QUESTIONS, key=lambda x: x['rating'], reverse=True)

    page_obj, page_range = paginate(hot, request, per_page=3)

    return render(request, 'hot.html', {
        'page_obj': page_obj, 
        'page_range': page_range
    })
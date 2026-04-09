from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User

def index(request):

    #questions = [
     #   {'title': 'How to build a moon park?', 'text': 'Guys, i have trouble. Can\'t find th black-jack...', 'rating': -2, 'answers_count': 0},
     #   {'title': 'How to build a moon park?', 'text': 'Guys, i have trouble. Can\'t find th black-jack...'},
 #       {'title': 'How to build a moon park?', 'text': 'Guys, i have trouble. Can\'t find th black-jack...'},
 #   ]
  #  return render(request, 'index.html', {'questions': questions})

    all_questions = []
    for i in range(1,54):
        all_questions.append({
            'id': i,
            'title': f'How to build a moon park? ({i})', 
            'text': "Guys, I have trouble. Can't find th black-jack...",
            'rating': 0, 
            'answers_count': 0 
        })
    paginator = Paginator(all_questions, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return render(request, 'index.html', {'page_obj': page_obj, 'page_range': page_range})
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
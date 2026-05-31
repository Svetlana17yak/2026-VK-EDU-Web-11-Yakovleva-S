from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

from .models import Question, Tag, Answer


def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    
    return page_obj, page_range



def index(request):
 
    questions = Question.objects.get_new()
    page_obj, page_range = paginate(questions, request, per_page=3)
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'page_range': page_range
    })

def hot(request):

    questions = Question.objects.get_hot()
    page_obj, page_range = paginate(questions, request, per_page=3)

    return render(request, 'hot.html', {
        'page_obj': page_obj, 
        'page_range': page_range
    })

def tag_questions(request, tag_name):

    tag = get_object_or_404(Tag, name=tag_name)

    questions = Question.objects.get_by_tag(tag_name)
    page_obj, page_range = paginate(questions, request, per_page=3)
    
    return render(request, 'tag_list.html', {
        'tag_name': tag.name,
        'page_obj': page_obj,
        'page_range': page_range
    })

def question(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)

    answers = question.answers.order_by('-rating', '-created_at').select_related('author', 'author__profile')
    

    page_obj, page_range = paginate(answers, request, per_page=2)

    return render(request, 'question.html', {
        'question': question, 
        'page_obj': page_obj,
        'page_range': page_range
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
            auth_login(request, user) 
            return redirect('index')

    return render(request, 'register.html', {'error_message': error_message})

def setting(request):
    return render(request, 'setting.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index')
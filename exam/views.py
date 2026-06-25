from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Exam, Question, Result

def home(request):
    exams = Exam.objects.all()
    return render(request, 'home.html', {'exams': exams})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer == question.correct_answer:
                score += 1
        result = Result.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total=questions.count()
        )
        return redirect('result', result_id=result.id)
    return render(request, 'take_exam.html', {'exam': exam, 'questions': questions})

@login_required
def result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    return render(request, 'result.html', {'result': result})
@staff_member_required
def students_list(request):
    users = User.objects.filter(is_staff=False)
    return render(request, 'students_list.html', {'users': users})
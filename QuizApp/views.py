from QuizApp.models import Quiz
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from projects.models import Project
# Create your views here.

def home(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    
    projects = Project.objects.all()
    quizes = Quiz.objects.all()
    context = {
        'user':user,
        'projects': projects,
        'quizes': quizes
    }
    return render(request, 'index.html', context=context)
from QuizApp.models import Answer, Quiz, Score
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser
from projects.models import Project
# Create your views here.

def home(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    
    all_projects = Project.objects.all()
    projects=[]
    for project in all_projects:
        if user in project.allocated_to.all():
            projects.append(project)
        
    all_quizes = Quiz.objects.all()
    quizes=[]
    for quiz in all_quizes:
        if user in quiz.assigned_to.all():
            quizes.append(quiz)
    context = {
        'user':user,
        'projects': projects,
        'quizes': quizes
    }
    return render(request, 'index.html', context=context)

def view_quiz(request, url):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    quiz = Quiz.objects.get(user_friendly_url=url)
    try:
        score = Score.objects.get(
                    student = request.user,
                    quiz = quiz
                )
    except:
        score = None
    context = {
        'quiz' : quiz,
        'score': score
    }
    return render(request, 'QuizApp/view.html', context=context)

def start_quiz(request, url):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    quiz = Quiz.objects.get(user_friendly_url=url)
    if request.method!="POST":
        questions = quiz.questions.all()
        all_questions = dict()
        for question in questions:
            all_questions[question] = Answer.objects.filter(question=question)
        context = {
            'quiz' : quiz,
            'questions' : all_questions,
        }
        return render(request, 'QuizApp/start.html', context=context)
    else:
        marks_obtained = 0
        correct_answers = 0
        for key,value in request.POST.items():
            if key.find("answer")!=-1:
                answer = Answer.objects.get(id=value[0])
                if answer.correct_answer:
                    marks_obtained+=answer.question.marks
                    correct_answers+=1
            

        percentage_obtained = (marks_obtained/quiz.marks)*100
        try:
            score = Score.objects.get(
                student = request.user,
                quiz = quiz
            )
            score.marks = marks_obtained
            score.total_attempts += 1
            if score.max_marks < marks_obtained:
                score.max_marks = marks_obtained
            score.save()
        except:
            score = Score.objects.create(
                student = request.user,
                quiz = quiz,
                marks = marks_obtained,
                total_attempts = 1,
                max_marks = marks_obtained
            )
            score.save()

        if percentage_obtained >= quiz.passing_marks:
            score.passed=True
            message = "You have passed the quiz!"
        else:
            score.passed=False
            message = "You have failed the quiz!"
        score.save()
        context = {
            'correct_answers': correct_answers,
            'marks_obtained': marks_obtained,
            'total_marks': quiz.marks,
            'percentage_obtained': percentage_obtained,
            'passing_percentage': quiz.passing_marks,
            'message': message,
            'quiz': quiz
        }
        return render(request, 'QuizApp/result.html', context=context)
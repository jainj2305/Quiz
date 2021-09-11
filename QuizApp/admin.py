from QuizApp.models import Option, Question, Quiz, Score
from django.contrib import admin

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'title', "total_questions"]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'que_text', 'marks']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'quiz', 'max_marks', 'total_attempts']
    list_filter = ['max_marks', 'quiz', 'student']
    search_fields = ['quiz__title', 'student__email','student__username', 'max_marks']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Score, ScoreAdmin)
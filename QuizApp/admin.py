from QuizApp.models import Answer, Question, Quiz, Score
from django.contrib import admin

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator','user_friendly_url', 'title', "total_questions"]
    prepopulated_fields = {'user_friendly_url': ('title', 'creator')}

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'que_text', 'marks']
    inlines = [AnswerInline]

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'quiz', 'max_marks', 'total_attempts', 'passed']
    list_filter = ['max_marks', 'quiz', 'student', 'passed']
    search_fields = ['quiz__title', 'student__email','student__username', 'max_marks']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Score, ScoreAdmin)
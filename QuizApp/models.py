from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Option(models.Model):
    text = RichTextUploadingField()

    def __str__(self) -> str:
        return self.text

class Question(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    que_text = RichTextUploadingField()
    options = models.ManyToManyField(Option, related_name="all_options")
    answer = models.ForeignKey(Option, on_delete=models.DO_NOTHING, related_name="correct_option")
    marks = models.IntegerField(default=5)

    def __str__(self) -> str:
        return self.que_text


class Quiz(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="creator")
    title = models.TextField()
    questions = models.ManyToManyField(Question)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="students")

    def __str__(self) -> str:
        return self.title

    @property
    def marks(self):
        total_marks = 0
        for que in self.questions.all():
            total_marks+=que.marks
        return total_marks

    @property
    def total_questions(self):
        return self.questions.count()



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            instance.groups.add(Group.objects.get(name='Student'))
        except:
            pass

class Score(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    marks = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now_add=True)
    total_attempts = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.quiz.title + ' ' + self.student.email
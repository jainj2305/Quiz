from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Question(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    que_text = RichTextUploadingField()
    marks = models.IntegerField(default=5)

    def __str__(self) -> str:
        return self.que_text

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='Question', on_delete=models.CASCADE)

    text = RichTextUploadingField(blank=False,
                                help_text="Enter the answer text that you want displayed",
                                verbose_name="Content")

    correct_answer = models.BooleanField( default=False, 
                                        help_text="Is this a correct answer?", 
                                        verbose_name="Correct")

    def __str__(self):
        return self.text



class Quiz(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(Question)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="students")
    passing_marks = models.IntegerField(default=1,
                                        validators=[
                                        MaxValueValidator(100),
                                        MinValueValidator(0)
                                        ],
                                        help_text="Enter passing percentage")
    user_friendly_url = models.SlugField(null=False, unique=True)

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
    last_attempt = models.DateTimeField(auto_now=True)
    total_attempts = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.quiz.title + ' ' + self.student.email
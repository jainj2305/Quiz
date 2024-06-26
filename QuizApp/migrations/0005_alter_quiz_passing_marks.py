# Generated by Django 3.2.7 on 2021-09-24 11:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0004_alter_quiz_passing_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='passing_marks',
            field=models.IntegerField(default=0, help_text='Enter passing percentage', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]

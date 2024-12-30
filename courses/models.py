from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

class Module(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
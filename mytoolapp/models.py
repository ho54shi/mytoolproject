from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomeUser(AbstractUser):
    expert = models.BooleanField(default=False)


class ProjectModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    text_file = models.FileField(upload_to='', validators=[
                                 FileExtensionValidator(['txt', ])])

    def __str__(self):
        return self.title


class LabelModel(models.Model):
    name = models.CharField(max_length=50)
    keybind = models.CharField(max_length=1)
    color = models.CharField(max_length=10)
    projects = models.ForeignKey(
        ProjectModel, verbose_name='プロジェクト',  on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AnnotationModel(models.Model):
    text = models.TextField()
    anns = models.TextField()
    projects = models.ForeignKey(
        ProjectModel, verbose_name='プロジェクト',  on_delete=models.DO_NOTHING, null=True)
    annotator = models.ForeignKey(CustomeUser, on_delete=models.DO_NOTHING)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)

    def __str__(self):
        return self.text

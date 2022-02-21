from django.conf import settings
from django.db import models


class Project(models.Model):

    BACKEND = 'BACKEND'
    FRONTEND = 'FRONTEND'
    IOS = 'IOS'
    ANDRIOD = 'ANDROID'

    TYPE_CHOICES = [
        (BACKEND, 'back-end'),
        (FRONTEND, 'front-end'),
        (IOS, 'iOS'),
        (ANDRIOD, 'Android'),
    ]

    title = models.CharField(max_length=150, verbose_name='Titre')
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Type')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Issue(models.Model):

    BUG = 'BUG'
    IMPROVEMENT = 'IMPROVEMENT'
    TASK = 'TASK'
    WEAK = 'WEAK'
    AVERAGE = 'AVERAGE'
    HIGH = 'HIGH'
    TO_DO = 'TO_DO'
    IN_PROGRESS = ' IN_PROGRESS'
    DONE = 'DONE'

    TAG_CHOICES = [
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Amélioration'),
        (TASK, 'Tâche'),
    ]

    PRIORITY_CHOICES = [
        (WEAK, 'Faible'),
        (AVERAGE, 'Moyenne'),
        (HIGH, 'Elevée'),
    ]

    STATUS_CHOICES = [
        (TO_DO, 'A faire'),
        (IN_PROGRESS, 'En cours'),
        (DONE, 'Terminé')
    ]
    title = models.CharField(max_length=150, verbose_name='Titre')
    description = models.TextField(max_length=2048)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, verbose_name='Tag')
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, verbose_name='Priorité')
    project_id = models.IntegerField
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Status')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auteur')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigné')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issues_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.description

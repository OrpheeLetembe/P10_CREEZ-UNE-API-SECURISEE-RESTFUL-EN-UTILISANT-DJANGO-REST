from django.conf import settings
from django.db import models


class Project(models.Model):

    TYPE_CHOICES = (
        ('back-end', 'Back-end'),
        ('front-end', 'front-end'),
        ('Ios', 'Ios'),
        ('android', 'Android')

    )

    title = models.CharField(max_length=255, verbose_name='Titre')
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Type')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                       verbose_name='Auteur')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création",)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='users')

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.title


class Issue(models.Model):

    TAG_CHOICES = (
        ('bug', 'Bug'),
        ('improvement', 'Amélioration'),
        ('task', 'Tâche'),
    )

    PRIORITY_CHOICES = (
        ('weak', 'Faible'),
        ('average', 'Moyenne'),
        ('high', 'Elevée'),
    )

    STATUS_CHOICES = (
        ('to do', 'A faire'),
        ('in progress', 'En cours'),
        ('done', 'Terminée'),
    )

    title = models.CharField(max_length=255, verbose_name='Titre')
    description = models.TextField(max_length=2048)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, verbose_name='Tag')
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, verbose_name='Priorité')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Statut')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author',
                                       verbose_name='auteur')

    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asssigned',
                                         verbose_name='utilisateur assigné')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = 'Problème'
        verbose_name_plural = 'Problèmes'

    def __str__(self):
        return "id:{}, titre:{}".format(self.id, self.title)


class Comment(models.Model):
    description = models.TextField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user',
                                       verbose_name='Auteur')
    issues_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'

    def __str__(self):
        return self.description


class Contributor(models.Model):

    RESPONSABILE = 'RESPONSABILE'
    CONTRIBUTOR = 'CONTRIBUTOR'

    ROLE_CHOICES = (
        (RESPONSABILE, 'Responsable'),
        (CONTRIBUTOR, 'Contibuteur')
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Utilisateur',
                                related_name='user')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Projet', related_name='projet')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Role')

    class Meta:
        unique_together = ('user_id', 'project_id')
        verbose_name = 'Contributeur'
        verbose_name_plural = 'contributeurs'







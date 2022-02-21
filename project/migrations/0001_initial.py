# Generated by Django 4.0.2 on 2022-02-21 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Titre')),
                ('description', models.TextField(max_length=2048)),
                ('type', models.CharField(choices=[('BACKEND', 'back-end'), ('FRONTEND', 'front-end'), ('IOS', 'iOS'), ('ANDROID', 'Android')], max_length=100, verbose_name='Type')),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Titre')),
                ('description', models.TextField(max_length=2048)),
                ('tag', models.CharField(choices=[('BUG', 'Bug'), ('IMPROVEMENT', 'Amélioration'), ('TASK', 'Tâche')], max_length=100, verbose_name='Tag')),
                ('priority', models.CharField(choices=[('WEAK', 'Faible'), ('AVERAGE', 'Moyenne'), ('HIGH', 'Elevée')], max_length=100, verbose_name='Priorité')),
                ('status', models.CharField(choices=[('TO_DO', 'A faire'), (' IN_PROGRESS', 'En cours'), ('DONE', 'Terminé')], max_length=100, verbose_name='Status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('assignee_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigné', to=settings.AUTH_USER_MODEL)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auteur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=2048)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('issues_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.issues')),
            ],
        ),
    ]

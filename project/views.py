from django.http import request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from project.models import Project, Issue, Comment
from project.serializers import ProjectListSerializer, ProjectDetailSerializer,  IssueListSerializer, \
    IssueDetailSerializer, CommentSerializer


class MultipleSerializerMixim:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixim, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)


class IssueViewset(MultipleSerializerMixim, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get(' project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        issues_id = self.request.GET.get('issues_id')
        if issues_id:
            queryset = queryset.filter(issues_id=issues_id)
        return queryset


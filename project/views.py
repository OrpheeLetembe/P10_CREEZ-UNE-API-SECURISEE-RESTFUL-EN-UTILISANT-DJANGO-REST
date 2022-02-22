from rest_framework.viewsets import ModelViewSet

from project.models import Project, Issue, Comment
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()







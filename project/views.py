
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q


from authentication.models import User
from authentication.serializers import UserSerializer
from project.models import Project, Issue, Comment
from project.serializers import ProjectListSerializer, ProjectDetailSerializer,  IssueListSerializer, \
    IssueDetailSerializer, CommentSerializer
from project.permissions import IsCurrentUserOwner


class MultipleSerializerMixim:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixim, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = (IsCurrentUserOwner,)

    def get_queryset(self):
        # filter projects related to the connected user
        user = self.request.user
        return Project.objects.filter(Q(users=user) | Q(author_user_id=user))

    def create(self, request, *args, **kwargs):
        project_data = request.data

        new_project = Project.objects.create(
            title=project_data["title"],
            description=project_data["description"],
            type=project_data["type"],
            author_user_id=request.user,
        )
        new_project.save()
        serializer = ProjectListSerializer(new_project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        project_data = request.data
        project.title = project_data["title"]
        project.description = project_data["description"]
        project.type = project_data["type"]
        project.author_user_id = request.user

        project.save()
        serializer = ProjectListSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return Response()

    @action(detail=True, methods=['post'], url_path='users')
    def add_users(self, request, *args, **kwargs):
        data = request.data
        project = self.get_object()
        project_users = project.users.all()
        user = User.objects.get(id=data['user_id'])
        if user in project_users:
            return Response({"message": user.username + "" + " est déjà membre de " + "" + project.title})
        else:
            project.users.add(user, through_defaults={'role': data['role']})
            project.save()
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data)

    @action(detail=True, url_path='users')
    def get_users(self, request, *args, **kwargs):
        project = self.get_object()
        project_users = project.users.all()
        serializer = UserSerializer(project_users, many=True)
        return Response(serializer.data)


class IssueViewset(MultipleSerializerMixim, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
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


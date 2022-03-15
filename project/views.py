from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from project.permissions import IsProjectAuthor
#from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.serializers import UserSerializer
from project.models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer


@api_view(['GET', 'POST'])
def project_list(request):

    if request.method == 'GET':
        projects = Project.objects.filter(users=request.user)
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectListSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user_id=request.user)
            project.users.add(request.user, through_defaults={'role': 'responsable'})
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsProjectAuthor])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def add_user(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data
        project_users = project.users.all()
        user = User.objects.get(id=data['user_id'])
        if user in project_users:
            return Response({"message": user.username + "" + " est déjà membre de " + "" + project.title},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            project.users.add(user, through_defaults={'role': data['role']})
            project.save()
            return Response({"message": user.username + "" + " a été ajouté au projet " + "" + project.title},
                            status=status.HTTP_200_OK)

    elif request.method == 'GET':
        project_users = project.users.all()
        serializer = UserSerializer(project_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, project_id, user_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        contributor = Contributor.objects.get(Q(user_id=user_id) & Q(project_id=project_id))
        contributor.delete()
        return Response({"message": 'test' + "" + " a été supprimé de " + "" + project.title},
                        status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def add_issue(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            issue = serializer.save(author_user_id=request.user, project_id=project, assignee_user_id=request.user)
            issue.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        issues = Issue.objects.filter(project_id=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def delete_issue(request, project_id, issue_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        issues = Issue.objects.filter(project_id=project)
        issue = issues.get(id=issue_id)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        issues = Issue.objects.filter(project_id=project)
        issue = issues.get(id=issue_id)
        issue.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def add_comment(request, project_id, issue_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author_user_id=request.user, issues_id=issue)
            comment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        comments = Comment.objects.filter(issues_id=issue_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def delete_comment(request, project_id, issue_id, comment_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    issues = Issue.objects.filter(project_id=project)
    issue = issues.get(id=issue_id)
    comments = Comment.objects.filter(issues_id=issue)
    comment = comments.get(id=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)









"""
class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = (IsProjectAuthor,)

    def get_serializer_class(self):
        if self.action == 'retrieve':  # and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        # filter projects related to the connected user
        return Project.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author_user_id=self.request.user)
        project.users.add(self.request.user, through_defaults={'role': 'responsable'})
        project.save()

    @action(detail=True, methods=['post'], url_path='users', url_name='add user')
    def add_project_user(self, request, pk=None):
        data = request.data
        project = self.get_object()
        project_users = project.users.all()
        user = User.objects.get(id=data['user_id'])
        if user in project_users:
            return Response({"message": user.username + "" + " est déjà membre de " + "" + project.title})
        else:
            project.users.add(user, through_defaults={'role': data['role']})
            project.save()
            return Response({"message": user.username + "" + " a été ajouté au projet " + "" + project.title})

    @action(detail=True, methods=['get'], url_path='users', url_name='get users')
    def get(self, request, pk=None):
        project = self.get_object()
        project_users = project.users.all()
        serializer = UserSerializer(project_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='users/(?P<user_pk>[^/.]+)')
    def delete_user(self, request, pk=None, user_pk=None):
        project = self.get_object()
        user = project.users.all().get(id=user_pk)
        contributor = Contributor.objects.get(user_id=user)
        contributor.delete()
        return Response({"message": user.username + "" + " a été supprimé de " + "" + project.title})


    def add_issue(self, request, pk):
        pass


class IssueViewset(ModelViewSet):

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

"""
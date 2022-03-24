from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from project.permissions import IsAuthor
from rest_framework.views import APIView

from authentication.models import User
from project.models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer, \
    ContributorSerializer


class GetObjectMixin:
    """
    mixin that provides the different view classes with permissions and methods for managing
    projects, problems and comments.

    """
    permission_classes = [IsAuthor]

    def get_project(self, request, id):
        """
        Method to retrieve projects related to the connected user.
        It takes as parameter the id of the project and returns it if it exists
        """
        related_projects = Project.objects.filter(users=request.user)
        project = get_object_or_404(related_projects, id=id)
        return project

    def get_issue(self, request, project_id, issue_id):
        """
        Method to retrieve a problem from a project related to the connected user.
        It takes the project id and the problem id as parameters and returns the latter if it exists.
        """
        project = self.get_project(request, project_id)
        issues = Issue.objects.filter(project_id=project)
        issue = get_object_or_404(issues, id=issue_id)
        return issue

    def get_comment(self, request, project_id, issue_id, comment_id):
        """
        method to retrieve a comment of a problem related to the connected user.
        It takes as parameters the id of the project, the id of the problem and the id of the comment
        and returns the latter if it exists.

        """
        project = self.get_project(request, project_id)
        issues = Issue.objects.filter(project_id=project)
        issue = get_object_or_404(issues, id=issue_id)
        comments = Comment.objects.filter(issues_id=issue)
        comment = get_object_or_404(comments, id=comment_id)
        return comment


class ProjectListView(APIView, GetObjectMixin):
    """
    Class intended for the management of the display of the list of projects related to the connected user
    and the creation of new projects.
    """

    def get(self, request):
        related_projects = Project.objects.filter(users=request.user)
        serializer = ProjectListSerializer(related_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectListSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user_id=request.user)
            project.users.add(request.user, through_defaults={'role': 'RESPONSABILE'})
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(GetObjectMixin, APIView):
    """
    Class that provides methods to :
        - get the details of a project with respect to the logged-in user
        - update a project
        - and delete a project.
    """

    def get(self, request, id):
        project = self.get_project(request, id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        project = self.get_project(request, id)
        self.check_object_permissions(request, project)
        serializer = ProjectListSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        project = self.get_project(request, id)
        self.check_object_permissions(request, project)
        project.delete()
        return Response({"message": "projet supprimé "}, status=status.HTTP_404_NOT_FOUND)


class GetAddContributorView(GetObjectMixin, APIView):

    # Class that provides methods to add a contributor to a project and to get the list of contributors of a project.

    def post(self, request, id):
        data = request.data
        project = self.get_project(request, id)
        self.check_object_permissions(request, project)
        contributors = project.users.all()
        user = get_object_or_404(User, username=data['username'])
        if user in contributors:
            return Response({"message": user.username + "" + " est déjà membre de " + "" + project.title},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            project.users.add(user, through_defaults={'role': 'CONTRIBUTOR'})
            project.save()
            return Response({"message": user.username + "" + " a été ajouté au projet " + "" + project.title},
                            status=status.HTTP_200_OK)

    def get(self, request, id):
        project = self.get_project(request, id)
        contributors = Contributor.objects.filter(project_id=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteContributorView(GetObjectMixin, APIView):

    def delete(self, request, project_id, user_id):
        project = self.get_project(request, project_id)
        self.check_object_permissions(request, project)
        contributors = project.users.all()
        user = get_object_or_404(contributors, id=user_id)
        contributor = Contributor.objects.get(Q(user_id=user) & Q(project_id=project.id))
        contributor.delete()
        return Response({"message": user.username + "" + " a été supprimé de " + "" + project.title},
                        status=status.HTTP_404_NOT_FOUND)


class GetAddIssueView(GetObjectMixin, APIView):

    # Class that provides methods to add a issue to a project and to display issues related to a project.

    def post(self, request, id):
        project = self.get_project(request, id)
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user, project_id=project, assignee_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        project = self.get_project(request, id)
        issues = Issue.objects.filter(project_id=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PutDeleteIssueView(GetObjectMixin, APIView):

    # Class that provides methods to update and remove a problem.

    def put(self, request, project_id, issue_id):
        issue = self.get_issue(request, project_id, issue_id)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):
        issue = self.get_issue(request, project_id, issue_id)
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response({"message": "Problème supprimé "}, status=status.HTTP_404_NOT_FOUND)


class GetAddCommentView(GetObjectMixin, APIView):

    # Class that provides methods to add a comment to a problem and to get the comments related to a problem.

    def post(self, request, project_id, issue_id):
        issue = self.get_issue(request, project_id, issue_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user, issues_id=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id):
        issue = self.get_issue(request, project_id, issue_id)
        comments = Comment.objects.filter(issues_id=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PutDeleteCommentView(GetObjectMixin, APIView):
    """
    Class that provides methods to :
        - obtaining a comment
        - updating a comment
        - and deleting a comment.

    """
    def get(self, request, project_id, issue_id, comment_id):
        comment = self.get_comment(request, project_id, issue_id, comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id, issue_id, comment_id):
        comment = self.get_comment(request, project_id, issue_id, comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):
        comment = self.get_comment(request, project_id, issue_id, comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

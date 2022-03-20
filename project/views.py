
#from django.core.paginator import Paginator

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from project.permissions import IsAuthor
from rest_framework.views import APIView


from authentication.models import User
from authentication.serializers import UserSerializer
from project.models import Project, Issue, Comment, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer


class GetObjectMixin:
    """

    """
    permission_classes = [IsAuthor]

    def get_object(self, obj, id):
        try:
            return obj.objects.get(id=id)
        except obj.DoesNotExist:
            return None

    def get_project(self, request, id):
        related_projects = Project.objects.filter(users=request.user)
        try:
            return related_projects.get(id=id)
        except Project.DoesNotExist:
            return None


class ProjectListView(APIView, GetObjectMixin):
    """

    """

    def get(self, request):
        related_projects = Project.objects.filter(users=request.user)
        serializer = ProjectListSerializer(related_projects, many=True)
        #paginator = Paginator(serializer, 2)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectListSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user_id=request.user)
            project.users.add(request.user, through_defaults={'role': 'responsable'})
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(GetObjectMixin, APIView):
    """

    """

    def get(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, project)
            serializer = ProjectListSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, project)
            project.delete()
            return Response({"message": "projet supprimé "}, status=status.HTTP_404_NOT_FOUND)


class GetAddUserView(GetObjectMixin, APIView):
    """

    """

    def post(self, request, id):
        data = request.data
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, project)
            project_users = project.users.all()
            user = self.get_object(User, data['user_id'])
            if user is None:
                return Response({"message": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            elif user in project_users:
                return Response({"message": user.username + "" + " est déjà membre de " + "" + project.title},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                project.users.add(user, through_defaults={'role': data['role']})
                project.save()
                return Response({"message": user.username + "" + " a été ajouté au projet " + "" + project.title},
                                status=status.HTTP_200_OK)

    def get(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            project_users = project.users.all()
            serializer = UserSerializer(project_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserView(GetObjectMixin, APIView):
    """

    """

    def delete(self, request, project_id, user_id):

        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, project)
            project_users = project.users.all()
            try:
                user = project_users.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                contributor = Contributor.objects.get(Q(user_id=user) & Q(project_id=project.id))
                contributor.delete()
                return Response({"message": user.username + "" + " a été supprimé de " + "" + project.title},
                                status=status.HTTP_404_NOT_FOUND)


class GetAddIssueView(GetObjectMixin, APIView):
    """

    """

    def post(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_user_id=request.user, project_id=project, assignee_user_id=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        project = self.get_project(request, id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class PutDeleteIssueView(GetObjectMixin, APIView):
    """

    """

    def put(self, request, project_id, issue_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project_id)
            try:
                issue = issues.get(id=issue_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                self.check_object_permissions(request, issue)
                serializer = IssueSerializer(issue, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                self.check_object_permissions(request, issue)
                issue.delete()
                return Response({"message": "Problème supprimé "}, status=status.HTTP_404_NOT_FOUND)


class GetAddCommentView(GetObjectMixin, APIView):
    """

    """

    def post(self, request, project_id, issue_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(author_user_id=request.user, issues_id=issue)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                comments = Comment.objects.filter(issues_id=issue)
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCommentView(GetObjectMixin, APIView):
    """

    """

    def get(self, request, project_id, issue_id, comment_id):

        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
                comments = Comment.objects.filter(issues_id=issue)
                comment = comments.get(id=comment_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            except Comment.DoesNotExist:
                return Response({"message": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id, issue_id, comment_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
                comments = Comment.objects.filter(issues_id=issue)
                comment = comments.get(id=comment_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            except Comment.DoesNotExist:
                return Response({"message": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                self.check_object_permissions(request, comment)
                serializer = CommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response({"message": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            issues = Issue.objects.filter(project_id=project)
            try:
                issue = issues.get(id=issue_id)
                comments = Comment.objects.filter(issues_id=issue)
                comment = comments.get(id=comment_id)
            except Issue.DoesNotExist:
                return Response({"message": "Problème non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            except Comment.DoesNotExist:
                return Response({"message": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            else:
                self.check_object_permissions(request, comment)
                comment.delete()
                return Response(status=status.HTTP_404_NOT_FOUND)









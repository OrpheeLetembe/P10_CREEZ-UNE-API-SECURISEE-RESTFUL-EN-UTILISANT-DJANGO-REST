from rest_framework.serializers import ModelSerializer, SerializerMethodField

from authentication.serializers import UserSerializer
from project.models import Project, Issue, Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id', 'status', 'author_user_id',
                  'assignee_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id', 'status', 'author_user_id',
                  'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()
    #users = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'issues', 'users']

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueDetailSerializer(queryset, many=True)
        return serializer.data
"""
    def get_users(self, instance):
        queryset = instance.users.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data

"""
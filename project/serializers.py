from rest_framework.serializers import ModelSerializer

from project.models import Project, Issue, Comment


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'users']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'created_time', 'author_user_id', 'issues', 'users']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id', 'status', 'author_user_id',
                  'assignee_user_id', 'created_time', 'comments']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

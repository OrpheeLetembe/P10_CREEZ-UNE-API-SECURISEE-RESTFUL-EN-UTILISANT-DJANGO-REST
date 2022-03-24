from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from project.models import Project, Issue, Comment, Contributor


class ProjectListSerializer(ModelSerializer):
    author_user_id = StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'created_time', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    author_user_id = StringRelatedField()
    issues = StringRelatedField(many=True)
    users = StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'created_time', 'author_user_id', 'issues', 'users']


class IssueSerializer(ModelSerializer):
    author_user_id = StringRelatedField()
    assignee_user_id = StringRelatedField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id', 'status', 'author_user_id',
                  'assignee_user_id', 'created_time', 'comments']


class CommentSerializer(ModelSerializer):
    author_user_id = StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorSerializer(ModelSerializer):
    user_id = StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['user_id', 'role']

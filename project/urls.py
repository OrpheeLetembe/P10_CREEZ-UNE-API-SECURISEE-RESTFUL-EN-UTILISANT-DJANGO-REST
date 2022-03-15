from django.urls import path

from .views import project_list, project_detail, add_user, delete_user, add_issue, delete_issue, add_comment, \
    delete_comment

urlpatterns = [
    path('projects/', project_list, name='projects list'),
    path('projects/<int:pk>/', project_detail, name='projects detail'),
    path('projects/<int:pk>/users/', add_user, name='add user'),
    path('projects/<int:project_id>/users/<int:user_id>', delete_user, name='delete user'),
    path('projects/<int:pk>/issues/', add_issue, name='add issues'),
    path('projects/<int:project_id>/issues/<int:issue_id>', delete_issue, name='delete issues'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', add_comment, name='add comment'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', delete_comment,
         name='delete comment')
    ]

"""
from rest_framework import routers
from project.views import ProjectViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()

router.register('projects', ProjectViewset, basename='projects')
router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')


"""



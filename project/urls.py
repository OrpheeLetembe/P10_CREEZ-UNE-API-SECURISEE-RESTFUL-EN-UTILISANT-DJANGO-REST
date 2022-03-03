from rest_framework import routers

from project.views import ProjectViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()

router.register('projects', ProjectViewset, basename='projects')
router.register('issues', IssueViewset, basename='issues')
router.register('comments', CommentViewset, basename='comments')


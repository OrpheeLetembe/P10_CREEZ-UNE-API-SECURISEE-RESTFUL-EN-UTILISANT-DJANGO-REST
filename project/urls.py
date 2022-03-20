from django.urls import path

from .views import ProjectListView, ProjectDetailView, GetAddUserView, DeleteUserView, GetAddIssueView, \
    PutDeleteIssueView, GetAddCommentView, DeleteCommentView

urlpatterns = [

    path('projects/', ProjectListView.as_view()),
    path('projects/', ProjectDetailView.as_view()),
    path('projects/<int:id>/', ProjectDetailView.as_view()),
    path('projects/<int:id>/users/', GetAddUserView.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>', DeleteUserView.as_view()),
    path('projects/<int:id>/issues/', GetAddIssueView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>', PutDeleteIssueView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', GetAddCommentView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', DeleteCommentView.as_view()),

    ]





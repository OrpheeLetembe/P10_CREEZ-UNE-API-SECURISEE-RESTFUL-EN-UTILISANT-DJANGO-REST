from django.urls import path

from .views import ProjectListView, ProjectDetailView, GetAddContributorView, DeleteContributorView, GetAddIssueView, \
    PutDeleteIssueView, GetAddCommentView, PutDeleteCommentView

urlpatterns = [

    path('projects/', ProjectListView.as_view()),
    path('projects/', ProjectDetailView.as_view()),
    path('projects/<int:id>/', ProjectDetailView.as_view()),
    path('projects/<int:id>/users/', GetAddContributorView.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>', DeleteContributorView.as_view()),
    path('projects/<int:id>/issues/', GetAddIssueView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>', PutDeleteIssueView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', GetAddCommentView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', PutDeleteCommentView.as_view()),

    ]

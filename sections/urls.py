from django.urls import path
from . import views
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('subforum/<int:pk>/createtopic/',views.CreateTopicView.as_view(),name='createtopic'),
    path("subforum/<int:pk>/",views.SubForumView.as_view(),name="subforum"),
    path("theme/<int:pk>/",views.TopicView.as_view(),name="topic"),
]
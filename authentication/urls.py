from django.urls import path,include
from . import views
from django.views.generic.base import TemplateView
app_name="auth"
urlpatterns=[
    path('', include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
    path('user/<int:pk>/',views.UserProfile.as_view(),name='userpage'),
    # path('loggedout',TemplateView.as_view(template_name='registration/logout.html'),name='logout')
    path('loggedout',views.userlogout,name='logout')
]
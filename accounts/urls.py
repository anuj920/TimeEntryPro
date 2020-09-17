from django.urls import path
from accounts import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    path('password-done/',views.Password_DoneView.as_view(),name='password_done'),
]
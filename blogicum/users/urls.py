from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('auth/registration/', views.SignUp.as_view(), name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'profile/<str:username>/edit/',
        views.edit_profile,
        name='edit_profile'),
]

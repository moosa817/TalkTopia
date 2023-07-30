from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('register/', views.RegisterPage, name='register'),
    path('delete-msg/<str:pk>', views.deleteMessage, name='delete-msg'),
    path('edit-msg/<str:pk>', views.EditMessage, name='edit-msg'),
    path('profile/<str:user>', views.UserProfile, name='profile')

]

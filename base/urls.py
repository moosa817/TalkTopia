from django.urls import path
# views folder
from .views import home, profile, room_messages, register_login, profile, rooms
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home.home, name='home'),
    path('room/<str:pk>', room_messages.room, name='room'),
    path('create-room/', rooms.createRoom, name='create-room'),
    path('update-room/<str:pk>', rooms.updateRoom, name='update-room'),
    path('delete-room', rooms.deleteRoom, name='delete-room'),
    path('login/', register_login.LoginPage, name='login'),
    path('logout/', register_login.LogoutPage, name='logout'),
    path('register/', register_login.RegisterPage, name='register'),
    path('delete-msg/<str:pk>', room_messages.deleteMessage, name='delete-msg'),
    path('edit-msg/<str:pk>', room_messages.EditMessage, name='edit-msg'),
    path('profile/<str:pk>', profile.Profile, name='profile'),
    path('joined-rooms', profile.JoinedRooms, name='joined-rooms'),
    path('account', profile.AccountSettings, name='account'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

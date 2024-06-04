from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('signup', views.signup, name="signup"),

    path('login', views.login_user, name="login_user"),

    path('logout', views.logout_page, name="logout_page"),

    path('upload', views.upload, name="upload"),

    path('edit/<int:media_id>/', views.edit_media, name='edit_media'),

    path('delete/<int:media_id>/', views.delete_media, name='delete_media'),

    path('search_media', views.search_media, name="search_media"),

    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),

    path('audio', views.audio, name="audio"),

    path('images', views.images, name="images"),

    path('documents', views.documents, name="documents"),

    path('play_video/<int:video_id>/', views.play_video, name='play_video')

]

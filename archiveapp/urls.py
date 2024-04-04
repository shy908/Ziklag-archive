from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('signup', views.signup, name="signup"),

    path('login', views.login_user, name="login_user"),

    path('logout', views.logout_page, name="logout_page"),

    path('upload', views.upload, name="upload"),

    path('audio', views.audio, name="audio"),

    path('images', views.images, name="images"),

    path('documents', views.documents, name="documents"),


]
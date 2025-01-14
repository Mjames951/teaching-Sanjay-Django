from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('blogpost/<id>/', views.blogPost, name="blogpost"),
    path('about/', views.about, name="about"),
    path('userpage/<username>/', views.userPage, name='userpage'),

    path('addpost/', views.addPost, name="addpost"),
    path('editpost/<id>/', views.editPost, name="editpost"),
    path('deletepost/<id>/', views.deletePost, name="deletepost"),

    path('register/', views.register, name="register"),
]
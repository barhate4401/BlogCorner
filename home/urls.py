from django.contrib import admin
from django.urls import path, include
from home import views
# from froala_editor import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'), 
    path("signup", views.handlesignup, name='handlesignup'), 
    path("login", views.handlelogin, name='handlelogin'), 
    path("logout", views.handlelogout, name='handlelogout'), 
    path('search', views.search, name="search"),
    path('blog', views.blog, name="blog"),
    path('<str:slug>/', views.blogPost, name="blogpost"),
    # API to postComment
    path('postComment', views.postComment, name="PostComment"),
    # Flora Edito
    # path('froala_editor/',include('froala_editor.urls')),
]
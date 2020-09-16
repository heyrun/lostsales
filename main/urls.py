from django.contrib import admin
from django.urls import path
from . import views

name = 'main'
urlpatterns = [
    path('', views.allcaptures, name="home"),
    path('capture_item', views.item_select, name="capture_item"),
    path('additem', views.additem, name='additem'),
    path('capture', views.capture, name='capture'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
]

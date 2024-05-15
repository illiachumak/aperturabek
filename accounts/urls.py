from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    re_path('login/',  views.login),
    re_path('signup/',  views.signup),
]

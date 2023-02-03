# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import login_view, register_user, Profile, CustomLogoutView, ProfileUpdateView, LihatUser


urlpatterns = [
    path('lihatuser/', LihatUser.as_view(), name='lihatuser'),
    path('profile2/', ProfileUpdateView.as_view(), name='profile2'),
    path('profile/', Profile.as_view(), name='profile'),
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('social_login/', include('allauth.urls')),
]

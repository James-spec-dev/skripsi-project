# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.tiket import models

class UserForm(forms.ModelForm): #baru bisa update data user
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

JURUSAN = [
    ('Informatika', 'Informatika'),
    ('Ilmu Komunikasi', 'Ilmu Komunikasi'),
    ('Tekanik', 'Tekanik'),
    ('Psikologi', 'Psikologi'),]

class MahasiswaForm(forms.ModelForm):
    nim = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    jurusan = forms.ChoiceField(choices=JURUSAN, widget=forms.Select(attrs={'class':'form-control'}))
    no_hp = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    foto = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'})) #Note that we didn't mention user field here.
    class Meta:
        model = models.Mahasiswa
        fields = ['nim', 'jurusan', 'no_hp', 'foto',]



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

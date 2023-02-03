# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, UserForm, MahasiswaForm
from core.settings import GITHUB_AUTH
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.tiket.models import Mahasiswa
from .forms import UserForm, MahasiswaForm
from django.contrib import messages
from django.http import HttpResponseRedirect

class LihatUser(TemplateView):
    template_name='accounts/user.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    mahasiswa_form = MahasiswaForm
    template_name = 'accounts/profile2.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        mahasiswa_form = MahasiswaForm(post_data, file_data, instance=request.user.mahasiswa)

        if user_form.is_valid() and mahasiswa_form.is_valid():
            user_form.save()
            mahasiswa_form.save()
            print(user_form)
            print(mahasiswa_form)
            messages.success(request, 'Your Profile was Succesfully Updated')
            return HttpResponseRedirect(reverse_lazy('profile2'))

        context = self.get_context_data(user_form=user_form, mahasiswa_form=mahasiswa_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class Profile(UpdateView):
    form_class = UserForm
    template_name = "accounts/Profile.html"
    # context_object_name = 'form'
    # queryset = models.Mahasiswa.objects.all()
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg, "GITHUB_AUTH": GITHUB_AUTH})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

class CustomLogoutView(LogoutView):
    template_name = 'accounts/login.html'
    next_page = 'login'
# -*- coding: utf-8 -*-


# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from .models import Profile, Version, Application

from .core.create_uid import create_uid



@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    user_id = request.user.id
    profile_id = Profile.objects.get(user=user_id)
    _app = Application.objects.filter(user=profile_id)
    return render(request,
                  'account/all_app.html',
                  {'applications':_app},)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )

            #Create the user profile

            new_user.save()

            profile = Profile.objects.create(user=new_user)
            _date_joined = str(profile.date_joined)
            profile.unique_id = create_uid(profile.id, profile.user.username, _date_joined)

            # Save the User object
            profile.save()

            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

def show_version(request):
    if request.method == 'GET':
        # например
        # account/version/?app_id=1&ver_type=W
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)

        _ver_small = request.GET.get('ver_type')
        _ver_type = Version.LOOKUP_CHOISE[_ver_small] # получаем полное имя ОС


        _versions = Version.objects.filter(application=_app, ver_type=_ver_small)
        return render(request, 'account/versions.html', {
                                                        'versions': _versions,
                                                        'app_name': _app.name,
                                                        'os_type': _ver_type,
                                                        })
    else:
        dashboard(request) # если не get, отправляем в личный кабинет

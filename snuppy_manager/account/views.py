# -*- coding: utf-8 -*-


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .core.create_uid import create_uid
from .forms import LoginForm, UserRegistrationForm
from .models import Profile

from group.models import Invite, Rule, Group


#login
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


#logout
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'account/user_logout.html')


#register
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
            uid = create_uid(profile.id, profile.user.username, _date_joined)
            profile.unique_id = uid

            # Save the User object
            profile.save()

            group = Group(name = uid)
            group.save()

            rule = Rule(group=group, profile=profile, rule='U')
            rule.save()


            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
        else:
            print('wrong registration parametrs')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

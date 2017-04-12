# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required


# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect


from .models import User, Version, Application


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
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def show_all_app(request, user_id):
    _user = User.objects.get(pk=user_id)
    _app = Application.objects.filter(user=_user)
    return render(request, 'account/all_app.html', {'user': _user, 'applications':_app})

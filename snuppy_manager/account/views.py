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


#user's personal room
@login_required
def dashboard(request):
    if request.method == 'GET':
        user_id = request.user.id
        profile = Profile.objects.get(user=user_id)

        invites = Invite.objects.filter(profile=profile)

        # _group = Group.objects.filter(profile__id =profile.id)
        # for get rule, group[0].rule_set.all(),
        # or group[0].rule_set.get()
        #g[0].profile.get().unique_id = profile id
        # g[1].application_set.all() = все application для группы. При обратной связи используется _set
        # или related_name="имя" в models, manytomany
        # g[0].rule_set.get().get_rule_display() показать полное имя
        #group[0].profile.get().unique_id - получаемя uid профайла через группу
        # _app = Application.objects.filter(id__in=_group)
        # id__in == "a in (1,2,3)"(который queryset и результатов может быть несколько)

        users_rule = Rule.objects.filter(profile__id =profile.id)

        return render(
            request,
            'account/all_app.html',
            {'rules':users_rule, 'invites':invites}
        )
    else:
        return HttpResponseBadRequest()


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

# -*- coding: utf-8 -*-


# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from .models import Profile, Version, Application, Group, Rule, Invite

from .core.create_uid import create_uid
from .core.get_changes import get_changes
from .core.ApiConnect import ApiConnect
from django.db.models import Q


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
def user_logout(request):
    logout(request)
    return render(request, 'account/user_logout.html')


@login_required
def dashboard(request):
    user_id = request.user.id
    profile = Profile.objects.get(user=user_id)

    invites = Invite.objects.filter(profile=profile)

    _group = Group.objects.filter(profile__id =profile.id)
    # for get rule, group[0].rule_set.all(),
    # or group[0].rule_set.get()
    #g[0].profile.get().unique_id = profile id
    # g[1].application_set.all() = все application для группы. При обратной связи используется _set
    # или related_name="имя" в models, manytomany
    # g[0].rule_set.get().get_rule_display() показать полное имя

    #group[0].profile.get().unique_id - получаемя uid профайла через группу

    _app = Application.objects.filter(id__in=_group)
    # id__in == "a in (1,2,3)"(который queryset и результатов может быть несколько)

    users_rule = Rule.objects.filter(profile__id =profile.id)


    return render(
        request,
        'account/all_app.html',
        {'rules':users_rule, 'invites':invites}
    )


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


@login_required
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
                                                        'app': _app,
                                                        'os_type': _ver_type,
                                                        })
    else:
        dashboard(request) # если не get, отправляем в личный кабинет

@login_required
def add_version(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)
        _os_type = request.GET.get('os_type')
        return render(request, 'account/add_version.html', {'app': _app, 'os_type':_os_type})


@login_required
def compile_ver(request):
    if request.method == 'POST':
        _app_id = request.POST.get('app_id')
        _os_type_f = request.POST.get('os_type')
        _os_type_s = _os_type_f[0] # Берем первую букву, она равна сокращениям
        _ver_number = request.POST.get('ver_number')

        app = Application.objects.get(id=_app_id)

        _ver_changes = get_changes(app.source_code)

        api_con = ApiConnect()
        api_con.send_compile_request(
            'uuid',
            app.id,
            _ver_number,
            app.source_code,
            _os_type_f,
        )

        v = Version(
            number=_ver_number,
            application=app,
            path=api_con.file,
            ver_type=_os_type_s,
            status = api_con.status,
            changes = _ver_changes,
        )
        v.save()
        api_con.remove_file()

        return render(
            request,
            'account/add_version_success.html',
            {'app_id':app.id, 'ver_type':v.ver_type},
        )


@login_required
def modify_ver(request): #not used now
    _ver_id = request.GET.get('id')
    ver = Version.objects.get(id=_ver_id)
    return render(request, 'account/version_modify.html', {'ver':ver})


@login_required
def change_ver(request): #not used now
    _ver_id = request.POST.get('ver_id')
    _ver_name = request.POST.get('ver_name')


    ver = Version.objects.get(id=_ver_id)

    if ver.name != _ver_name:
        ver.name = _ver_name
    ver.save()

    return render(request, 'account/version_modify_success.html')


@login_required
def delete_ver(request):
    _ver_id = request.GET.get('ver_id')
    _ver_type = request.GET.get('ver_type')
    _app_id = request.GET.get('app_id')
    ver = Version.objects.get(id=_ver_id)
    ver.delete()

    print('ver_type = {} and app_id = {}'.format(_ver_type, _app_id))
    return render(
        request,
        'account/version_delete_success.html',
        {'ver_type':_ver_type, 'app_id':_app_id})


@login_required
def add_app(request):
    user_id = request.user.id
    profile = Profile.objects.get(user=user_id)
    group = Group.objects.filter(profile__id=profile.id)

    return render(
                   request,
                  'account/app_add.html',
                  {'profile':profile, 'group':group},
    )


@login_required
def add_app_check(request):
    _app_name = request.POST.get('app_name')
    _app_description = request.POST.get('app_description')
    _app_source = request.POST.get('app_source')
    _group_id = request.POST.get('group_id')

    group = Group.objects.get(id=_group_id)

    app = Application(
        name = _app_name,
        description = _app_description,
        source_code = _app_source,
        group = group
    )
    app.save()

    return render(request, 'account/app_add_success.html')


@login_required
def delete_app(request):
    _app_id = request.GET.get('app_id')
    app = Application.objects.get(id=_app_id)
    app.delete()

    return render(request, 'account/app_delete_success.html')


@login_required
def change_app(request):
    _app_id = request.GET.get('app_id')
    _app = Application.objects.get(id=_app_id)

    user_id = request.user.id
    profile = Profile.objects.get(id=user_id)
    group = Group.objects.filter(profile__id=profile.id)

    return render(
        request,
        'account/app_change.html',
        {'app':_app,'group':group}
    )


@login_required
def change_app_check(request):
    _app_id = request.POST.get('app_id')
    _app_name = request.POST.get('app_name')
    _app_descr = request.POST.get('app_description')
    _app_source = request.POST.get('app_source')
    _gr = request.POST.get('group_id')

    group = Group.objects.get(id=_gr)

    app = Application.objects.get(id=_app_id)
    app.name = _app_name
    app.description = _app_descr
    app.source_code = _app_source
    app.group = group

    app.save()

    return render(request, 'account/app_change_success.html')


@login_required
def show_groups(request):
    user_id = request.user.id
    profile = Profile.objects.get(user=user_id)

    groups = Group.objects.filter(profile=profile, rule__rule='A')

    return render(request, 'account/show_groups.html', {'groups':groups})


@login_required
def group_add(request):
    return render(request, 'account/group_add.html')


@login_required
def group_check_add(request):
    group_name = request.POST.get('group_name')
    user_id = request.user.id
    profile = Profile.objects.get(id=user_id)


    new_group = Group(name=group_name)
    new_group.save()
    rule = Rule(group=new_group, profile=profile, rule='U')
    rule.save()

    return render(request, 'account/group_add_success.html')

@login_required
def group_edit(request):

    group_id = request.GET.get('group_id')
    group = Group.objects.get(id=group_id)
    rules = group.rule_set.all()

    return render(request, 'account/group_edit.html', {'rules':rules, 'group':group})


@login_required
def group_add_user(request):
    # code block must contain login for add "invite" for user
    # also, mb it is need to add in return answer like "send user invite"
    username = request.GET.get('new_user')
    profile = Profile.check_profile(username)
    if profile:
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        invite = Invite(group=group, profile=profile)
        invite.save()
    return group_edit(request)


@login_required
def group_delete(request):
    group_id = request.GET.get('group_id')
    group = Group.objects.get(id=group_id)
    group.delete()
    group_name = group.name
    # ВАЖНО!!!
    # group.delete() удалит вообще все: группу, все приложения в этой группе,
    # все версии удаленных приложений (ну, кроме файлов, конечно, но это только пока...)
    return render(request, 'account/group_delete_success.html', {'group_name':group_name})


@login_required
def decline_invite(request):
    group_id = request.GET.get('group_id')
    group = Group.objects.get(id=group_id)
    profile = Profile.objects.get(user=request.user.id)

    invite = Invite.objects.get(group=group, profile=profile)
    invite.delete()
    #не делаем ни чего, просто удаляем приглашение.
    # Возможно нужно добавить информирование приглащающего,
    # что его приглашение отклонили?

    return dashboard(request)


@login_required
def accept_invite(request):
    group_id = request.GET.get('group_id')
    group = Group.objects.get(id=group_id)
    profile = Profile.objects.get(user=request.user.id)

    invite = Invite.objects.get(group=group, profile=profile)
    invite.delete()

    rule = Rule(group=group, profile=profile, rule='G')
    # новые пользователи добавляются с правами Guest
    rule.save()

    return dashboard(request)


@login_required
def group_modify(request):
    for key in request.POST:
        print('key = {}, value = {}'.format(key, request.POST[key]))
        if key.find('rule_new_') != -1 and request.POST[key] != 'None':
            print('key = {} and value = {}'.format(key, request.POST[key]))
            group_id = key.split('_')[-1]
            new_privilege = request.POST[key].split('_')[1]
            profile_id = request.POST[key].split('_')[0]
            profile = Profile.objects.get(id=profile_id)
            group = Group.objects.get(id=group_id)
            rule = Rule.objects.get(profile=profile, group=group)
            rule.rule = new_privilege
            rule.save()
    return dashboard(request)
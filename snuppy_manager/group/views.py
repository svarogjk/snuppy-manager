# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render

from account.models import Profile
from .models import Group, Rule, Invite


#GROUPS

@login_required
def show_groups(request):
    if request.method == 'GET':
        user_id = request.user.id
        profile = Profile.objects.get(user=user_id)

        groups = Group.objects.filter(profile=profile, rule__rule='A')

        return render(request, 'group/show_all.html', {'groups':groups})
    else:
        return HttpResponseBadRequest()


@login_required
def group_add(request):
    if request.method == 'GET':
        return render(request, 'group/add.html')
    else:
        return HttpResponseBadRequest


@login_required
def group_check_add(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        user_id = request.user.id
        profile = Profile.objects.get(id=user_id)

        new_group = Group(name=group_name)
        new_group.save()
        rule = Rule(group=new_group, profile=profile, rule='A')
        rule.save()

        return render(request, 'group/add_success.html')
    else:
        return HttpResponseBadRequest()


@login_required
def group_edit(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        rules = group.rule_set.all()

        return render(request, 'group/edit.html', {'rules':rules, 'group':group})
    else:
        return HttpResponseBadRequest()


@login_required
def group_add_user(request):
    if request.method == 'GET':
        # mb it is need to add in return answer like "send user invite"
        username = request.GET.get('new_user')
        profile = Profile.check_profile(username)
        group_id = request.GET.get('group_id')
        if profile:
            group = Group.objects.get(id=group_id)
            invite = Invite(group=group, profile=profile)
            invite.save()
        return redirect('group/edit?group_id={}'.format(group_id))

    else:
        return HttpResponseBadRequest()


@login_required
def group_delete(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        group.delete()
        group_name = group.name
        # ВАЖНО!!!
        # group.delete() удалит вообще все: группу, все приложения в этой группе,
        # все версии удаленных приложений (ну, кроме файлов, конечно, но это только пока...)
        return render(request, 'group/delete_success.html', {'group_name':group_name})
    else:
        return HttpResponseBadRequest()


@login_required
def decline_invite(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        profile = Profile.objects.get(user=request.user.id)

        invite = Invite.objects.get(group=group, profile=profile)
        invite.delete()
        #не делаем ни чего, просто удаляем приглашение.
        # Возможно нужно добавить информирование приглащающего,
        # что его приглашение отклонили?

        return redirect('account/templates/all_app')
    else:
        return HttpResponseBadRequest()


@login_required
def accept_invite(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        profile = Profile.objects.get(user=request.user.id)

        invite = Invite.objects.get(group=group, profile=profile)
        invite.delete()

        rule = Rule(group=group, profile=profile, rule='G')
        # новые пользователи добавляются с правами Guest
        rule.save()

        return redirect('account/templates/all_app')
    else:
        return HttpResponseBadRequest()


@login_required
def group_modify(request):
    if request.method == 'POST':
        group_id = request.POST['group_id']
        for key in request.POST:
            if key.find('rule_new_') != -1 and request.POST[key] != 'None':
                profile_id = key.split('_')[-1]
                new_privilege = request.POST[key].split('_')[1]

                profile = Profile.objects.get(id=profile_id)
                group = Group.objects.get(id=group_id)
                rule = Rule.objects.get(profile=profile, group=group)

                if new_privilege == 'remove':
                    rule.delete()
                else:
                    rule.rule = new_privilege
                    rule.save()
        return redirect('group/edit?group_id={}'.format(group_id))
    else:
        return HttpResponseBadRequest()

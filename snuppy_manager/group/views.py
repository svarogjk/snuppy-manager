# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from account.models import Profile
from .models import Group, Rule, Invite


#GROUPS

@login_required
@require_GET
def show_groups(request):
    user_id = request.user.id
    profile = Profile.objects.get(user=user_id)

    groups = Group.objects.filter(profile=profile, rule__rule='A')

    return render(request, 'group/show_all.html', {'groups':groups})


@csrf_protect
@login_required
@require_POST
def group_add(request):
    try:
        group_name = request.POST.get('group_name')
    except KeyError:
        return HttpResponseBadRequest # нету параментра group_name, форму подделали

    if Group.objects.filter(name=group_name).count() > 0: # группа с таким именем существуюет
        return JsonResponse({
            'error': 'Ошибка!',
            'error_text': 'Группа с именем {} уже существует!'.format(group_name)
        })

    user_id = request.user.id
    profile = Profile.objects.get(id=user_id)

    new_group = Group(name=group_name)
    new_group.save()
    rule = Rule(group=new_group, profile=profile, rule='A')
    rule.save()

    html = render_to_string('group/add_new.html', {'group': new_group})
    return HttpResponse(html)


@login_required
@require_http_methods(["GET", "POST"])
def group_edit(request):
    if request.method == 'GET':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
        rules = group.rule_set.all()

        return render(request, 'group/edit.html', {'rules':rules, 'group':group})
    elif request.method == 'POST':
        try:
            group_id = int(request.POST['group_id'])
        except (KeyError, ValueError):
            return HttpResponseBadRequest() # Если нет group_id значит форму подделали
        if not Group.is_user_admin_in_group(request.user.profile, group_id):
            return HttpResponseBadRequest() # Если отправитель не админ значит форму подделали

        for key in request.POST:
            try:
                _profile_id = int(key)
                profile = Profile.objects.get(id=_profile_id)
            except (ObjectDoesNotExist, ValueError):
                continue #в POST будут не только user_id - все не нужные пропускаем
            if not Group.is_user_in_group(profile, group_id):
                return HttpResponseBadRequest() #Если хотя бы один не в группе или не верное Rule значит форму подделали
            if not Rule.is_rule_exist(request.POST[key]): # Если указанного rule не существует, значит форму подделали
                return HttpResponseBadRequest()
            #.... all check done here
            if request.POST[key] == 'remove':
                pass #remove user
            elif request.POST[key] == 'stay':
                pass # do nothing
            else:
                pass #change to request.POST[key] value
            print(request.POST[key])
        print(Rule.other_choices)


        return HttpResponse('qweqwe')

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
        return redirect('/group/edit?group_id={}'.format(group_id))


#adds the user as a response to invite
@login_required
@csrf_protect
@require_POST
def group_add_user(request):
    admin_profile = request.user.profile
    group_id_arr = []
    try:
        invitations_arr = request.POST.get('invitations_arr')
        for invitation in invitations_arr:
            new_user = request.POST.get('_new_user')
            group_id = int(invitation)
            group_id_arr.append(group_id)

            # group_id = int(request.POST.get('_group_id_val'))
    except (KeyError, ValueError):
        return HttpResponseBadRequest() # если нет аргументов или group_id не число, значит форму подделали

    #verification procedures
    profile = Profile.check_profile(new_user)
    if not profile: # Проверяем, что введенный пользователь существует
        return JsonResponse({
            'error': 'Ошибка!',
            'error_text': 'Пользователя {} не существует'.format(new_user)
        })
    if not Group.is_user_admin_in_group(admin_profile, group_id): # Отправитель является админом группы
        return HttpResponseBadRequest  # Если не админ, значит форму подделали
    if Group.is_user_in_group(profile, group_id): # пользователь уже в группе
        return JsonResponse({
            'error': 'Ошибка!',
            'error_text': 'Пользователь {} уже в группе!'.format(new_user)
        })
    if Invite.is_user_have_invite(profile, group_id): # уже есть приглашение в группу
        return JsonResponse({
            'error': 'Ошибка!',
            'error_text': 'Пользователю {} уже отправленно приглашение!'.format(new_user)
        })

    #invitation itself
    for group_id in group_id_arr:
        group = Group.objects.get(id=group_id)
        invite = Invite(group=group, profile=profile)
        invite.save()
    return HttpResponse('success')


@login_required
@require_POST
def group_delete(request):
    try:
        group_id = int(request.POST.get('group_id'))
    except (KeyError, ValueError):
        return HttpResponseBadRequest # если не число или нет параметра, значит форму подделали
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest # группы не существует, форму подделали

    if not Group.is_user_admin_in_group(request.user.profile, group_id):
        return HttpResponseBadRequest # если не админ, значит форму подделали

    group.delete()
    # ВАЖНО!!!
    # group.delete() удалит вообще все: группу, все приложения в этой группе,
    # все версии удаленных приложений (кроме файлов!)
    return HttpResponse('Success')


@login_required
def decline_invite(request):
    if request.method == 'POST':
        group_id = request.POST.get('_group_id')
        group = Group.objects.get(id=group_id)
        profile = Profile.objects.get(user=request.user.id)

        invite = Invite.objects.get(group=group, profile=profile)
        invite.delete()
        #не делаем ни чего, просто удаляем приглашение.
        # Возможно нужно добавить информирование приглащающего,
        # что его приглашение отклонили?

        return redirect('/application/')
    else:
        return HttpResponseBadRequest()


@login_required
def accept_invite(request):
    if request.method == 'POST':

        group_id = request.POST.get('_group_id')
        group = Group.objects.get(id=group_id)
        profile = Profile.objects.get(user=request.user.id)

        invite = Invite.objects.get(group=group, profile=profile)
        invite.delete()

        rule = Rule(group=group, profile=profile, rule='G')
        # новые пользователи добавляются с правами Guest
        rule.save()

        return redirect('/application/')
    else:
        return HttpResponseBadRequest()




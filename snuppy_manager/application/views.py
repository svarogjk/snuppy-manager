from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from account.models import Profile
from group.models import Group, Invite, Rule
from .models import Application


@login_required
@require_http_methods(["GET"])
def show(request):
    if request.method == 'GET':
        user_id = request.user.id

        profile = Profile.objects.get(user=user_id)
        invites = Invite.objects.filter(profile=profile)
        users_rule = Rule.objects.filter(profile__id =profile.id)

        return render(
            request,
            'application/all_app.html',
            {'rules':users_rule, 'invites':invites}
        )


@login_required
@require_http_methods(["GET", "POST"])
def add_app(request):
    if request.method == 'GET':
        user_id = request.user.id
        profile = Profile.objects.get(user=user_id)
        group = Group.objects.filter(profile__id=profile.id)

        return render(
            request,
            'application/app_add.html',
            {'profile': profile, 'group': group},
        )
    elif request.method == 'POST':
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

        return render(request, 'application/app_success.html', {'status':'добавлено'})


@login_required
@require_http_methods(["GET"])
def delete_app(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        app = Application.objects.get(id=_app_id)
        app.delete()

        return render(request, 'application/app_success.html', {'status':'удалено'})


@login_required
@require_http_methods(["GET", "POST"])
def change_app(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)

        groups = Group.get_user_groups(request.user.id)

        return render(
            request,
            'application/app_change.html',
            {'app':_app,'group':groups}
        )
    elif request.method == 'POST':
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

        return render(request, 'application/app_success.html', {'status':'изменено'})


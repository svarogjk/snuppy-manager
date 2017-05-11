from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from account.models import Profile
from group.models import Group
from .models import Application


#APPS

@login_required
def add_app(request):
    if request.method == 'GET':
        user_id = request.user.id
        profile = Profile.objects.get(user=user_id)
        group = Group.objects.filter(profile__id=profile.id)

        return render(
                       request,
                      'application/app_add.html',
                      {'profile':profile, 'group':group},
        )
    else:
        return HttpResponseBadRequest()


@login_required
def add_app_check(request):
    if request.method == 'POST':
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

        return render(request, 'application/app_add_success.html')
    else:
        return HttpResponseBadRequest()


@login_required
def delete_app(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        app = Application.objects.get(id=_app_id)
        app.delete()

        return render(request, 'application/app_delete_success.html')
    else:
        return HttpResponseBadRequest()


@login_required
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
    else:
        return HttpResponseBadRequest()


@login_required
def change_app_check(request):
    if request.method == 'POST':
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

        return render(request, 'application/app_change_success.html')
    else:
        return HttpResponseBadRequest()

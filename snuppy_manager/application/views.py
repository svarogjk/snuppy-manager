from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from account.models import Profile, Group
from .models import Application, Version
from .core.get_changes import get_changes
from .core.ApiConnect import ApiConnect


# Create your views here.

@login_required
def show_version(request):
    if request.method == 'GET':
        # например
        # account/version/?app_id=1&ver_type=W
        profile = Profile.objects.get(user=request.user)
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)

        _ver_small = request.GET.get('ver_type')
        _ver_type = Version.LOOKUP_CHOISE[_ver_small] # получаем полное имя ОС

        _versions = Version.objects.filter(application=_app, ver_type=_ver_small)

        privilege = _app.group.rule_set.get(profile=profile).rule

        return render(request, 'application/version/show.html', {
                                                        'versions': _versions,
                                                        'app': _app,
                                                        'os_type': _ver_type,
                                                        'privilege':privilege,
                                                        })
    else:
        return HttpResponseBadRequest()


@login_required
def add_version(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)
        _os_type = request.GET.get('os_type')
        return render(request, 'application/version/add.html', {'app': _app, 'os_type':_os_type})
    else:
        return HttpResponseBadRequest()


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
            'application/version/add_success.html',
            {'app_id':app.id, 'ver_type':v.ver_type},
        )
    else:
        return HttpResponseBadRequest()


@login_required
def modify_ver(request): #not used now
    if request.method == 'GET':
        _ver_id = request.GET.get('id')
        ver = Version.objects.get(id=_ver_id)
        return render(request, 'application/version/edit.html', {'ver':ver})
    else:
        return HttpResponseBadRequest()


@login_required
def change_ver(request): #not used now
    if request.method == 'POST':
        _ver_id = request.POST.get('ver_id')
        _ver_name = request.POST.get('ver_name')

        ver = Version.objects.get(id=_ver_id)

        if ver.name != _ver_name:
            ver.name = _ver_name
        ver.save()

        return render(request, 'application/version/edit_success.html')
    else:
        return HttpResponseBadRequest()


@login_required
def delete_ver(request):
    if request.method == 'GET':
        _ver_id = request.GET.get('ver_id')
        _ver_type = request.GET.get('ver_type')
        _app_id = request.GET.get('app_id')
        ver = Version.objects.get(id=_ver_id)
        ver.delete()

        return render(
            request,
            'application/version/delete_success.html',
            {'ver_type':_ver_type, 'app_id':_app_id})
    else:
        return HttpResponseBadRequest()


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

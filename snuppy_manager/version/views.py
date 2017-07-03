from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic.list import View
from django.utils.decorators import method_decorator

from account.models import Profile
from application.models import Application
from .models import Version

from .core.ApiConnect import ApiConnect
from .core.get_changes import get_changes

import json


#VERSIONS
class ShowVersion(View):

    @method_decorator(login_required)
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)

        _ver_small = request.GET.get('ver_type')
        _ver_type = Version.LOOKUP_CHOISE[_ver_small]  # получаем полное имя ОС

        _versions = Version.objects.filter(application=_app, ver_type=_ver_small)

        privilege = _app.group.rule_set.get(profile=profile).rule

        return render(request, 'version/show.html', {
            'versions': _versions,
            'app': _app,
            'os_type': _ver_type,
            'privilege': privilege,
        })

    @method_decorator(login_required)
    def post(self, request):
        _app_id = request.POST.get('app_id')
        _os_type_f = request.POST.get('os_type')
        _os_type_s = _os_type_f[0]  # Берем первую букву, она равна сокращениям
        _ver_number = request.POST.get('ver_number')

        app = Application.objects.get(id=_app_id)

        # Апи не используется, нет смысла...
        # _ver_changes = get_changes(app.source_code)
        # api_con = ApiConnect()
        # api_con.send_compile_request(
        #     'uuid',
        #     app.id,
        #     _ver_number,
        #     app.source_code,
        #     _os_type_f,
        # )

        v = Version(
            number=_ver_number,
            application=app,
            # path=api_con.file,
            path='NotImplemented',
            ver_type=_os_type_s,
            status='NotImplemented',
            # status = api_con.status,
            # changes = _ver_changes,
            changes='NotImplemented',
        )

        v.save()
        # api_con.remove_file()

        return HttpResponse('ok')


@login_required
def add_version(request):
    if request.method == 'GET':
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)
        _os_type = request.GET.get('os_type')
        return render(request, 'version/add.html', {'app': _app, 'os_type':_os_type})


@login_required
def edit(request):
    if request.method == 'GET':
        _ver_id = request.GET.get('id')
        ver = Version.objects.get(id=_ver_id)
        return render(request, 'version/edit.html', {'ver': ver})

    elif request.method == 'POST': #not used now...
        _ver_id = request.POST.get('ver_id')
        _ver_name = request.POST.get('ver_name')

        ver = Version.objects.get(id=_ver_id)

        if ver.name != _ver_name:
            ver.name = _ver_name
        ver.save()

        return render(request, 'version/edit_success.html')
    else:
        return HttpResponseBadRequest()


@login_required
def delete_ver(request):
    if request.method == 'POST':
        _ver_ids = json.loads(request.POST.get('ver_id'))
        _app_id = request.POST.get('app_id')

        for version_id in _ver_ids:
            ver = Version.objects.get(id=int(version_id))
            ver.delete()

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest()
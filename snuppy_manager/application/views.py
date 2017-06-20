from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.template.loader import render_to_string

from django.views.generic.list import View
from django.utils.decorators import method_decorator

from account.models import Profile
from group.models import Group, Invite, Rule
from .models import Application
from account.core.decorators import ajax_required


class ShowApp(View):

    @method_decorator(login_required)
    def get(self, request):
        user_id = request.user.id

        profile = Profile.objects.get(user=user_id)
        group = Group.objects.filter(profile__id=profile.id)
        invites = Invite.objects.filter(profile=profile)
        users_rule = Rule.objects.filter(profile__id=profile.id)
        return render(
            request,
            'application/all_app.html',
            {'rules': users_rule, 'invites': invites, 'profile':profile, 'group': group}
        )


    @method_decorator(require_POST)
    @method_decorator(csrf_protect)
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(ajax_required)
    @method_decorator(login_required)
    def post(self, request):
        _group_id = request.POST.get('_group_id')
        _app_name = request.POST.get('_app_name')
        _app_description = request.POST.get('_app_description')
        _app_source = request.POST.get('_app_source')

        group = Group.objects.get(id=_group_id)

        app = Application(
            name=_app_name,
            description=_app_description,
            source_code=_app_source,
            group=group
        )
        app.save()

        html = render_to_string('application/app_new.html', {'app': app})
        return HttpResponse(html)

class DeleteApp(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def get(self, request):
        _app_id = request.GET.get('app_id')
        app = Application.objects.get(id=_app_id)
        app.delete()

        return render(request, 'application/app_success.html', {'status': 'удалено'})


class ChangeApp(View):

    @method_decorator(login_required)
    @method_decorator(require_GET)
    def get(self, request):
        _app_id = request.GET.get('app_id')
        _app = Application.objects.get(id=_app_id)

        groups = Group.get_user_groups(request.user.id)

        return render(
            request,
            'application/app_change.html',
            {'app': _app, 'group': groups}
        )

    @method_decorator(require_POST)
    @method_decorator(csrf_protect)
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(ajax_required)
    @method_decorator(login_required)
    def post(self, request):
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

        # return render(request, 'application/app_success.html', {'status': 'изменено'})
        return redirect('application/all_app.html')


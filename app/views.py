from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from pdc.helpers.login import auth
from pdc import settings
import docker
from services_api.models import Service

# Create your views here.

def index(request):
    installedServices = Service.objects.all()
    session_token = request.COOKIES.get('authorizator_session')
    if auth.Api.pdcLoginCheck(session_token):
        services = '{ "service" : ['
        for i in range(0, len(installedServices)):
            service = '{"name": "' + installedServices[i].name + '" , "docker_id": "' + installedServices[i].docker_id + '", "super": "' + str(installedServices[i].super) + '", "is_required":"' + str(installedServices[i].is_required) + '", "path":"' + installedServices[i].path + '", "icon":"' + installedServices[i].icon + '"},'
            services = services + service
        services = services[:-1] + "]}"
        return HttpResponse(services)
    else:
        return HttpResponseRedirect(settings.PDC_LOGIN_URL + "?next=/system")

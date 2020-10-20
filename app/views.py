from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from pdc.helpers.login import auth
from pdc import settings
import docker

# Create your views here.

def index(request):
    session_token = request.COOKIES.get('authorizator_session')
    client = docker.from_env()
    services = client.services.list()
    services_names = "Installed Services: "
    for i in range(0, len(services)):
        services_names = services_names + services[i].name + ", "
    if auth.Api.pdcLoginCheck(session_token):
        user = auth.Api.pdcGetUser(session_token)
        return HttpResponse("system is logged in - username:" + user.getName()+ "   " + services_names)
    else:
        return HttpResponseRedirect(settings.PDC_LOGIN_URL + "?next=/system")

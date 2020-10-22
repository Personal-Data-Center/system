from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from pdc.helpers.login import auth
from pdc import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import Service
import docker
import secrets
import json
import ast

# Create your views here.

class List(APIView):

    def get(self, request):
        installedServices = Service.objects.all()
        session_token = request.GET.get('token', False)
        if auth.Api.pdcLoginCheck(session_token):
            services = '{ "service" : ['
            for i in range(0, len(installedServices)):
                service = '{"name": "' + installedServices[i].name + '" , "docker_id": "' + installedServices[i].docker_id + '", "super": "' + str(installedServices[i].super) + '", "is_required":"' + str(installedServices[i].is_required) + '", "path":"' + installedServices[i].path + '", "icon":"' + installedServices[i].icon + '"},'
                services = services + service
            services = services[:-1] + "]}"
            content = json.loads(services)
        else:
            content = {'error': 'auth failed'}
        return Response(content)


class Install(APIView):

    def post(self, request, format=None):
        session_token = request.GET.get('token', False)
        service_name = request.GET.get('service_name', False)
        service_image = request.GET.get('service_image', False)
        service_super = request.GET.get('service_super', False)
        #first check if super user pdcGetUser
        if ( auth.Api.pdcLoginCheck(session_token)):
            user = auth.Api.pdcGetUser(session_token)
            if (user.isAdmin and service_name and service_image and service_super):
                #check if service is already installed
                django_installed_services = Service.objects.filter(image=service_image)
                if(len(django_installed_services)==0):
                    docker_service = None
                    client = docker.from_env()
                    try:
                        #first tries to create service
                        #generate a random name based on the service name
                        hex  = secrets.token_hex(2)
                        name_hex = service_name + "_" + hex
                        #create service
                        docker_service = client.services.create(
                        name=name_hex,image="traefik/whoami",
                        hostname=name_hex,networks=["pdc_pdc"],
                        container_labels={"traefik.enable": "true", "traefik.http.routers."+ name_hex +".entrypoints": "web", "traefik.http.routers."+ name_hex +".rule": "PathPrefix(`/"+ name_hex +"`)", "traefik.http.services."+ name_hex +".loadbalancer.server.port": "80"})
                    except Exception as e:
                        content = {'status' : "error",'message' : str(e)}
                    try:
                        #add to database
                        service_path = "/" + name_hex
                        service_icon = "/" + name_hex + "/static/icon.png"
                        django_service_model = Service(name=service_name, docker_id=docker_service.id, image=service_image, super=ast.literal_eval(service_super), is_required=False, path=service_path, icon=service_icon )
                        django_service_model.save()
                        content = {'status' : "success", "message": "Service installed"}
                    except Exception as e:
                        docker_service.remove()
                        content = {'status' : "error",'message' : str(e)}
                else:
                    content = {'status': 'error', 'message' : 'Service already installed'}
            else:
                content = {'status': 'error', 'message' : 'Bad Parameters'}
        else:
            content = {'status': 'error', 'message' : 'Not Authorized'}

        return Response(content)

class Remove(APIView):

    def post(self, request, format=None):
        session_token = request.GET.get('token', False)
        service_id = request.GET.get('service_id', False)
        #first check if super user pdcGetUser
        if ( auth.Api.pdcLoginCheck(session_token)):
            user = auth.Api.pdcGetUser(session_token)
            if (user.isAdmin and service_id):
                serviceToRemove_Django = Service.objects.filter(docker_id=service_id)
                if len(serviceToRemove_Django)>0:
                    if(not serviceToRemove_Django[0].is_required):
                        try:
                            client = docker.from_env()
                            serviceToRemove_Docker = client.services.get(service_id)
                            serviceToRemove_Docker.remove()
                            serviceToRemove_Django.delete()
                            content = {'status' : "success", "message": "Service removed"}
                        except Exception as e:
                            content = {'status' : "error",'message' : str(e)}
                    else:
                        content = {'status' : "error", "message": 'Can`t delete required service'}
                else:
                    content = {'status' : "error", "message": 'Service Don`t exist in database'}
            else:
                content = {'status': 'error', 'message' : 'bad parameters'}
        else:
            content = {'status': 'error', 'message' : 'not authorized'}

        return Response(content)

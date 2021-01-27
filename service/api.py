from django.http import JsonResponse
from django.conf import settings
from pdc.service.apiKeyManagement.models import GrantedKey

import docker
import os
import psutil
import json
import requests
import socket

# Service Management
def getServices(request):
    if request.method == 'GET':
        if request.user.admin or request.isApi == e:
            client = docker.from_env()
            installedServices = client.services.list()
            serviceMain = []
            stichedServices = {}
            for service in installedServices:
                attrs = service.attrs
                if attrs['Spec']['Labels']['pdc_backend'] != 'true':
                    dockerid = attrs['ID']
                    name = attrs['Spec']['Labels']['pdc_name']
                    createdAt = attrs['CreatedAt']
                    updatedAt = attrs['UpdatedAt']
                    path = attrs['Spec']['Labels']['pdc_path']
                    essential = attrs['Spec']['Labels']['pdc_essential']
                    image = attrs['Spec']['TaskTemplate']['ContainerSpec']['Image']
                    serviceInfo = {
                    'dockerid' : dockerid,
                    'name' : name,
                    'image': image,
                    'createdAt' : createdAt,
                    'updatedAt' : updatedAt,
                    'essential' : essential,
                    'path' : path,
                    }
                    serviceMain.append(serviceInfo)
                    stichedServices = {'service' : serviceMain}
            content ={ **{'Success' : True}, **stichedServices}
        else:
            content = {'Success' : False, 'Error' : 'no permission'}
    else:
        content = {'Success' : False, 'Error' : 'not GET method'}
    return JsonResponse(content)

def installService(request):
    if request.method == 'POST':
        if request.user.admin or request.isApi == True:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'Error' : 'no permission'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def removeService(request):
    if request.method == 'POST':
        if request.user.admin or request.isApi == True:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'Error' : 'no permission'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

#User Management

def getUsers(request):
    if request.method == 'GET':
        if request.user.admin and request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/getusers/?apiKey=" + authorizatorKey + "&"
            authorizatorResponse = requests.get(url).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not GET method'}
    return JsonResponse(content)


def createUser(request):
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)
    admin = request.GET.get('admin', None)
    email = request.GET.get('email', None)
    firstName = request.GET.get('firstName', None)
    lastName = request.GET.get('lastName', None)
    if request.method == 'POST':
        if request.user.admin and request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/createuser/?apiKey=" + authorizatorKey + "&"
            username = 'username=' + username + '&'
            password = 'password=' + password + '&'
            admin = 'admin=' + admin + '&'
            email = 'email=' + email + '&'
            firstName = 'firstName=' + firstName + '&'
            lastName = 'lastName=' + lastName + '&'
            authorizatorResponse = requests.post(url+username+password+admin+email+firstName+lastName).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def deleteUser(request):
    username = request.GET.get('username', None)
    if request.method == 'POST':
        if request.user.admin and request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/deleteuser/?apiKey=" + authorizatorKey + "&"
            username = 'username=' + username + '&'
            authorizatorResponse = requests.post(url+username).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)
def resetUserPassword(request):
    if request.method == 'POST':
        if request.user.admin and request.isApi is False:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

#Profile Management

def changePicture(request):
    username = request.GET.get('username', False)
    profilePic = {'profilePic' : request.FILES['profilePic']}
    if request.method == 'POST':
        if request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/changeprofilepic/?apiKey=" + authorizatorKey + "&"
            username = 'username=' + username + '&'
            authorizatorResponse = requests.post(url+username, files=profilePic).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def deletePicture(request):
    username = request.GET.get('username', False)
    if request.method == 'POST':
        if request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/deleteprofilepic/?apiKey=" + authorizatorKey + "&"
            username = 'username=' + username + '&'
            authorizatorResponse = requests.post(url+username).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def changePassword(request):
    username = request.GET.get('username', False)
    password = request.GET.get('password', False)
    if request.method == 'POST':
        if request.isApi is False:
            authorizatorKey = GrantedKey.objects.get(serviceName='authorizator').apiKey
            url = "http://authorizator/authorizator/api/changeuserpassword/?apiKey=" + authorizatorKey + "&"
            username = 'username=' + username + '&'
            password = 'password=' + password + '&'
            authorizatorResponse = requests.post(url+username).text
            authorizatorJson = json.loads(authorizatorResponse)
            content = authorizatorJson
        else:
            content = {'Success' : False, 'error' : 'only user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

def changeProfileInfo(request):
    if request.method == 'POST':
        if request.isApi is False:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'error' : 'only user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}

#Network Management

def getHostname(request):
    if request.method == 'GET':
        if request.user.admin and request.isApi is False:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not GET method'}

def changeHostName(request):
    if request.user.admin and request.method == 'POST':
        if request.isApi is False:
            content = {'Success' : True}
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not POST method'}
    return JsonResponse(content)

#System Management

def getNodes(request):
    if request.method == 'GET':
        if request.user.admin and request.isApi is False:
            client = docker.from_env()
            nodes = client.nodes.list()
            nodeMain = []
            for node in nodes:
                attrs = node.attrs
                del attrs['Description']['Engine']
                del attrs['Description']['TLSInfo']
                del attrs['Description']['Resources']
                del attrs['Description']['Hostname']
                nodeMain.append(attrs)
                stichedNodes = {'node' : nodeMain}
            content ={ **{'Success' : True},**stichedNodes}
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not GET method'}
    return JsonResponse(content)


def getNodeResources(request):
    if request.method == 'GET':
        ip_list = list({addr[-1][0] for addr in socket.getaddrinfo("tasks.pdc_resource_monitor", 0, 0, 0, 0)})
        if request.user.admin and request.isApi is False:
            ip_list = list({addr[-1][0] for addr in socket.getaddrinfo("tasks.pdc_resource_monitor", 0, 0, 0, 0)})
            resourceMonitorKey = GrantedKey.objects.get(serviceName='resourceMonitor').apiKey
            nodeMain = []
            for ip in ip_list:
                url = "http://" + ip + "/api/getresources/?apiKey=" + resourceMonitorKey + "&"
                resourceMonitorResponse = requests.get(url).text
                resourceMonitorJson = json.loads(resourceMonitorResponse)
                node = {
                'nodeId' : resourceMonitorJson['node']['nodeId'],
                'cpuUsage': resourceMonitorJson['node']['cpuUsage'],
                'cpuCount': resourceMonitorJson['node']['cpuCount'],
                'cpuFreq': resourceMonitorJson['node']['cpuFreq'],
                'ramTotal': resourceMonitorJson['node']['ramTotal'],
                'ramUsed': resourceMonitorJson['node']['ramUsed'],
                'diskTotal': resourceMonitorJson['node']['diskTotal'],
                'diskUsed': resourceMonitorJson['node']['diskUsed'],
                'diskFree': resourceMonitorJson['node']['diskFree'],
                }
                nodeMain.append(node)
                stichedNodes = {'node' : nodeMain}
            content ={ **{'Success' : True},**stichedNodes}
        else:
            content = {'Success' : False, 'error' : 'only admin user allowed'}
    else:
        content = {'Success' : False, 'Error' : 'not GET method'}
    return JsonResponse(content)

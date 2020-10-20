from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from pdc.helpers.login import auth
from pdc import settings
import docker

# Create your views here.

class List(APIView):

    def get(self, request):
        pass

class Install(APIView):

    def get(self, request):
        pass

class Remove(APIView):

    def get(self, request):
        pass

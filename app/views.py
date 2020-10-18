from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponse("is logged in - username:" + request.user.username)
    else:
         return HttpResponseRedirect("/cas/login")

from django.urls import path, include
from . import api

urlpatterns = [
    path('getservices/', api.getServices, name='getservices'),
    path('changepicture/', api.changePicture, name='changepicture'),
    path('changeuserpassword/', api.changePassword, name='changeuserpassword'),
    path('changeuserinfo/', api.changeProfileInfo, name='changeuserinfo'),
    path('deleteprofilepicture/', api.deletePicture, name='deleteprofilepic'),
    path('getnodes/', api.getNodes, name='getnodes'),
    path('getnoderesources/', api.getNodeResources, name='getnoderesource'),
    path('getusers/', api.getUsers, name='getusers'),
    path('createuser/', api.createUser, name='createuser'),
    path('deleteuser/', api.deleteUser, name='deleteuser'),
]

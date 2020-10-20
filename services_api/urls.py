from django.urls import path

from . import api

urlpatterns = [
    path('list/', api.List.as_view(), name='service_list'),
    path('install/', api.Install.as_view(), name='service_install'),
    path('remove/', api.Remove.as_view(), name='service_remove'),
]

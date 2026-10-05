from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render


def dashboard(request):

    return render(
        request,
        'patients/dashboard.html'
    )


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'patients/',
        include('patients.urls')
    ),

    path(
        '',
        dashboard,
        name='dashboard'
    ),
]


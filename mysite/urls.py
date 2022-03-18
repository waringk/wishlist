# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://tutorial.djangogirls.org


"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('home/', include('home.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# for every URL that starts with admin/, Django will find the corresponding view
from home.forms import UserSettingsForm
from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]


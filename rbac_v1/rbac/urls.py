"""rbac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.routers import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.routers'))
"""
from django.urls import path, include


urlpatterns = [
    path('v1/rbac/', include([
        # path('other/', include('v1.rbac_app.routers.other_urls')),
        path('user/', include('v1.rbac_app.routers.user_urls')),
        path('role/', include('v1.rbac_app.routers.role_urls')),
        path('privilege/', include('v1.rbac_app.routers.privilege_urls'))
    ])),
]
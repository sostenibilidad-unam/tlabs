"""fobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^ego/(?P<ego_id>[0-9]+)/$', views.ego_nets, name='ego_nets'),
    url(r'^ego_json/(?P<ego_id>[0-9]+)/$', views.ego_net_json, name='ego_net'),
    url(r'^mm/(?P<ego_id>[0-9]+)/$', views.mm, name='mm'),
    url(r'^mm_json/(?P<ego_id>[0-9]+)/$', views.mm_json, name='mm_json'),

]

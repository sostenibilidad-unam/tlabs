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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from mm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$',
        views.index, name='index'),

    url(r'^setup$',
        views.AnaSetup.as_view(),
        name="ana_setup"),

    url(r'^ana$',
        views.Ana.as_view(),
        name="ana_view"),

    url(r'^ana_json/$',
        views.ana_json, name='ana_json'),

    url(r'^alter/(?P<alter_id>[0-9]+)/$',
        views.view_alter,
        name='view_alter'),

    url(r'^action/(?P<action_id>[0-9]+)/$',
        views.view_action,
        name='view_action'),

    url(r'^mm$',
        views.MMView.as_view(),
        name="mm_view"),

    url(r'^mm_json/$',
        views.mm_json, name='mm_json'),

    url(r'^power_json/$',
        views.power_json, name='power_json'),

    url(r'^power$',
        views.Power.as_view(),
        name="power_view"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

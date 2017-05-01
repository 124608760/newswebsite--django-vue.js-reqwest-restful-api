"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from newswebsite.views import *
from newswebsite.api import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', index, name='index'),
    url(r'^category/(?P<cate_id>\d+)/$', category, name='category'),
    url(r'^detail/(?P<article_id>\d+)/$', detail, name='detail'),
    url(r'^login/', login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^logout/', logout, name='logout'),
    url(r'^profile/', profile, name='profile'),

    #api
    url(r'^api/index/', api_index, name='api_index'),
    url(r'^api/category/(?P<cate_id>\d+)/$', api_category, name='api_category'),
    url(r'^api/detail/(?P<article_id>\d+)/$', api_detail, name='api_detail'),
    url(r'^api/token-auth/$', views.obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

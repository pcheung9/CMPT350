from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.explore, name='explore'),
    url(r'^load/$', views.load, name='load'),
]

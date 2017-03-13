from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.indexView, name='explore'),
    url(r'^load/', views.load, name='load'),
    url(r'^search/', views.search, name='search'),
]

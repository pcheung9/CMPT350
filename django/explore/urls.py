from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^view/', views.results, name='view'),
]

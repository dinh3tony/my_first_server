from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'create$', views.create),
	url(r'success$', views.login),
	url(r'show$', views.show),
	url(r'clear$', views.clear)
]
from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns = [
	url(r'^$', views.home),
	url(r'^login/$', views.login, name="login"),
	url(r'^logout/$', views.logout_view),
	url(r'^register/$', views.register, name="register"),
	url(r'^groups/$', views.groups, name="groups"),
	url(r'^groups/(?P<group_id>[?=@\w+]+)/$', views.photos_list),
	url(r'^photos/(?P<photo_id>[\w+]+)/$', views.photos_display),
	url(r'^photos/$', views.photos),
]
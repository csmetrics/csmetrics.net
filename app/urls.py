from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^select', views.selectKeyword, name='select'),
    url(r'^admin/', admin.site.urls),
]

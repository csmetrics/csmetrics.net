from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^admin/', admin.site.urls),
]

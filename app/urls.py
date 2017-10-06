from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^update', views.updateTable, name='update'),
    url(r'^select', views.selectKeyword, name='select'),
    url(r'^overview/', views.overview, name='overview'),
    url(r'^acks/', views.acks, name='acks'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^network/', views.citingflow, name='citingflow'),
    url(r'^admin/', admin.site.urls),
]

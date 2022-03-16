from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('update', views.updateTable, name='update'),
    path('select', views.selectKeyword, name='select'),
    path('shareable/', views.shareable, name='shareable'),
    path('overview/', views.overview, name='overview'),
    path('acks/', views.acks, name='acks'),
    path('faq/', views.faq, name='faq'),
    path('admin/', admin.site.urls),
]

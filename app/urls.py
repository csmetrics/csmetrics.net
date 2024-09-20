from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('update', views.update_table, name='update'),
    path('venue', views.venue_list, name='venue'),
    path('shareable/', views.shareable, name='shareable'),
    path('overview/', views.overview, name='overview'),
    path('acks/', views.acks, name='acks'),
    path('faq/', views.faq, name='faq'),
    path('admin/', admin.site.urls),
]

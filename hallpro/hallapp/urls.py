from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('avhalls/', views.avhalls, name='avhalls'),
    path('landing/', views.landing, name='landing'),
]

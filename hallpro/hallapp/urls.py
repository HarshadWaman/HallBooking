from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('avhalls/', views.avhalls, name='avhalls'),
    path('index/', views.index, name='index'),
]

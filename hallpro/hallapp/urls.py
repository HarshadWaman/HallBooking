from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('avhalls/', views.avhalls, name='avhalls'),
    path('index/', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('api/login/', views.login, name='api-login'),
    path('api/register/', views.register, name='api-register'),
    path('logout/', views.logout, name='logout'),
]

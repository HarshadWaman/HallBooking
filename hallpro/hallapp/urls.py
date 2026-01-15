from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('admin-login/', views.admin_login_view, name='admin-login-view'),
    path('api/admin-login/', views.admin_login_api, name='admin-login-api'),
    path('index/', views.index, name='index'),
    path('booking/', views.booking_view, name='booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('api/login/', views.api_login, name='api-login'),
    path('api/register/', views.api_register, name='api-register'),
    path('api/add-user/', views.api_add_user, name='api-add-user'),
    path('api/update-user/<int:user_id>/', views.api_update_user, name='api-update-user'),
    path('api/delete-user/<int:user_id>/', views.api_delete_user, name='api-delete-user'),
    path('api/booking-details/<int:booking_id>/', views.api_booking_details, name='api-booking-details'),
    path('api/booking-status/<int:booking_id>/', views.api_booking_status, name='api-booking-status'),
    path('api/cancel-booking/<int:booking_id>/', views.api_cancel_booking, name='api-cancel-booking'),
    path('api/add-hall/', views.api_add_hall, name='api-add-hall'),
    path('api/update-hall/<int:hall_id>/', views.api_update_hall, name='api-update-hall'),
    path('api/delete-hall/<int:hall_id>/', views.api_delete_hall, name='api-delete-hall'),
    path('api/delete-booking/<int:booking_id>/', views.api_delete_booking, name='api-delete-booking'),
    path('api/update-booking/<int:booking_id>/', views.api_update_booking_status, name='api-update-booking'),
    path('api/ceo-approval/<int:booking_id>/', views.api_ceo_approval, name='api-ceo-approval'),
    path('api/principal-approval/<int:booking_id>/', views.api_principal_approval, name='api-principal-approval'),
    # Profile URLs
    path('api/get-profile/', views.api_get_profile, name='api-get-profile'),
    path('api/update-profile/', views.api_update_profile, name='api-update-profile'),
    path('api/upload-profile-image/', views.api_upload_profile_image, name='api-upload-profile-image'),
    path('logout/', views.logout_view, name='logout'),
    path('mybooking/', views.my_bookings, name='mybooking'),
    path('booking-details/<int:booking_id>/', views.booking_details_view, name='booking-details'),
]

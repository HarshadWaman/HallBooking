from django.contrib import admin
from .models import User, Hall, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Hall)
admin.site.register(Booking)
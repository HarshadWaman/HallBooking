from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# 1. Custom User Model
# Matches login/register logic in 'landing.html' and user management in 'admin.html'
class User(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

# 2. Hall Model
# Stores data for halls shown in 'index.html' and managed in 'admin.html'
class Hall(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Main Auditorium"
    capacity = models.IntegerField()         # e.g., 500
    location = models.CharField(max_length=100) # e.g., "Block A"
    description = models.TextField(blank=True)
    facilities = models.CharField(max_length=255, help_text="e.g., AC, Sound System, WiFi")
    # image = models.ImageField(upload_to='halls/', blank=True, null=True)  # Temporarily commented
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 3. Booking Model
# The core model connecting Users, Halls, and form data from 'booking.html'
class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    STAGE_CHOICES = (
        ('Large', 'Large'),
        ('Small', 'Small'),
    )

    CHAIR_CHOICES = (
        ('Wheel', 'Wheel'),
        ('Fiber', 'Fiber'),
    )

    # Relationship Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='bookings')

    # Basic Event Details (from booking.html)
    event_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    coordinator_name = models.CharField(max_length=100, verbose_name="Program Head / Coordinator")
    coordinator_mobile = models.CharField(max_length=15)
    
    # Date and Time
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Event Requirements (from booking.html)
    stage_size = models.CharField(max_length=10, choices=STAGE_CHOICES, blank=True)
    audience_count = models.PositiveIntegerField(default=0)
    chair_type = models.CharField(max_length=10, choices=CHAIR_CHOICES, blank=True)
    chair_count = models.PositiveIntegerField(default=0)

    # Equipment Counts (from "Materials & Facilities" section)
    mic_count = models.PositiveIntegerField(default=0)
    speaker_count = models.PositiveIntegerField(default=0)
    projector_count = models.PositiveIntegerField(default=0)
    laptop_count = models.PositiveIntegerField(default=0)

    # Boolean Checkboxes (The "checkbox-grid" in booking.html)
    req_agarbatti = models.BooleanField(default=False, verbose_name="Incense Sticks (Agarbatti)")
    req_matchbox = models.BooleanField(default=False, verbose_name="Matchbox")
    req_oil = models.BooleanField(default=False, verbose_name="Oil")
    req_wati = models.BooleanField(default=False, verbose_name="Cotton Wicks (Wati)")
    req_kapur = models.BooleanField(default=False, verbose_name="Camphor (Kapur)")
    req_satarangi = models.CharField(max_length=100, blank=True, verbose_name="Satarangi/Mat")
    req_carpet = models.BooleanField(default=False, verbose_name="Red Carpet")
    req_mandap = models.BooleanField(default=False, verbose_name="Mandap")
    req_saraswati_photo = models.BooleanField(default=False, verbose_name="Saraswati Photo")
    req_samai = models.BooleanField(default=False, verbose_name="Traditional Lamp (Samai)")

    # Status Tracking (for admin dashboard and mybooking.html)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_bookings')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_bookings')
    rejected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_name} on {self.booking_date} ({self.status})"

    class Meta:
        ordering = ['-booking_date', '-start_time']

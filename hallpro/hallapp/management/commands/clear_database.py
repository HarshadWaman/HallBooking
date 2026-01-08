import os
import django
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Clear all data from database safely'

    def handle(self, *args, **options):
        # Close existing connections
        connection.close()
        
        # Import models after setting up Django
        from hallapp.models import Booking, Hall, User
        from django.contrib.admin.models import LogEntry
        from django.contrib.sessions.models import Session
        
        # Clear all data
        try:
            Booking.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all bookings'))
            
            Hall.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all halls'))
            
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all users'))
            
            LogEntry.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared admin logs'))
            
            Session.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared sessions'))
            
            self.stdout.write(self.style.SUCCESS('All data cleared successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing data: {e}'))

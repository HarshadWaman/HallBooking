from django.core.management.base import BaseCommand
from hallapp.models import Hall

class Command(BaseCommand):
    help = 'Create sample halls for the booking system'

    def handle(self, *args, **options):
        # Clear existing halls
        Hall.objects.all().delete()
        
        # Create sample halls
        halls_data = [
            {'name': 'Sai Baba Hall', 'capacity': 500, 'location': 'Main Building', 'is_active': True},
            {'name': 'New Seminar Hall', 'capacity': 150, 'location': 'Academic Block', 'is_active': True},
            {'name': 'Auditorium', 'capacity': 1000, 'location': 'Campus Center', 'is_active': True},
        ]

        for hall_data in halls_data:
            hall = Hall.objects.create(**hall_data)
            self.stdout.write(self.style.SUCCESS(f'Created hall: {hall.name} (ID: {hall.id})'))

        self.stdout.write(self.style.SUCCESS(f'Total halls created: {Hall.objects.count()}'))

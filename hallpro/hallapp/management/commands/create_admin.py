from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hallapp.models import User

class Command(BaseCommand):
    help = 'Create an admin user for the system'

    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(user_type='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists!'))
            return

        # Create admin user
        admin_user = User.objects.create_user(
            username='admin@sangamnercollege.edu.in',
            email='admin@sangamnercollege.edu.in',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            user_type='admin'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Admin user created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Email: {admin_user.email}'))
        self.stdout.write(self.style.SUCCESS('Password: admin123'))
        self.stdout.write(self.style.WARNING('Please change the password after first login!'))

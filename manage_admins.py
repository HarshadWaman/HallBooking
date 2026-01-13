#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallpro.settings')
django.setup()

from hallapp.models import User, Admin

def create_default_admins():
    """Create default admin users"""
    print("\n=== Creating Default Admin Users ===")
    
    default_admins = [
        {
            'username': 'harshadwaman4@gmail.com',
            'email': 'harshadwaman4@gmail.com',
            'password': '9011818144',
            'first_name': 'Harshad',
            'user_type': 'admin'
        },
        {
            'username': 'nayanpatilnp11@gmail.com',
            'email': 'nayanpatilnp11@gmail.com', 
            'password': 'nayan2105',
            'first_name': 'Nayan',
            'user_type': 'admin'
        }
    ]
    
    for admin_data in default_admins:
        email = admin_data['email']
        
        # Check if admin user already exists
        if User.objects.filter(email=email).exists():
            print(f"Admin user {email} already exists")
            user = User.objects.get(email=email)
        else:
            # Create admin user
            user = User.objects.create_user(
                username=admin_data['username'],
                email=admin_data['email'],
                password=admin_data['password'],
                first_name=admin_data['first_name']
            )
            user.user_type = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"Created admin user: {email}")
        
        # Create Admin profile if it doesn't exist
        if not Admin.objects.filter(user=user).exists():
            Admin.objects.create(
                user=user,
                admin_code=f"ADMIN_{user.id}",
                department="Administration"
            )
            print(f"Created admin profile for: {email}")
    
    print("=== Default Admin Users Created ===\n")

if __name__ == '__main__':
    create_default_admins()

#!/usr/bin/env python
"""
Admin Management Script for Hall Booking System
Usage: python manage_admins.py
"""

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallpro.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

def create_admin_user(username, email, password, first_name="", user_type="admin"):
    """Create or update an admin user"""
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'user_type': user_type,
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"[CREATED] Admin user '{username}' created successfully!")
        else:
            # Update existing user
            user.email = email
            user.first_name = first_name
            user.user_type = user_type
            user.set_password(password)
            user.save()
            print(f"[UPDATED] Admin user '{username}' updated successfully!")
            
        return user
        
    except Exception as e:
        print(f"[ERROR] Failed to create/update user '{username}': {e}")
        return None

def list_admin_users():
    """List all admin users"""
    print("\n=== Admin Users ===")
    admins = User.objects.filter(user_type='admin')
    if admins:
        for admin in admins:
            status = "Active" if admin.is_active else "Inactive"
            print(f"- {admin.username} ({admin.email}) - {status}")
    else:
        print("No admin users found.")

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
        create_admin_user(**admin_data)

def create_custom_admin():
    """Create a custom admin user"""
    print("\n=== Create Custom Admin ===")
    
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
        
    email = input("Enter email: ").strip()
    if not email:
        print("Email cannot be empty!")
        return
        
    first_name = input("Enter first name: ").strip()
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return
    
    create_admin_user(username, email, password, first_name)

def delete_admin_user():
    """Delete an admin user"""
    print("\n=== Delete Admin User ===")
    username = input("Enter username to delete: ").strip()
    
    try:
        user = User.objects.get(username=username, user_type='admin')
        confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
        if confirm == 'y':
            user.delete()
            print(f"[DELETED] Admin user '{username}' deleted successfully!")
        else:
            print("Deletion cancelled.")
    except User.DoesNotExist:
        print(f"[ERROR] Admin user '{username}' not found!")
    except Exception as e:
        print(f"[ERROR] Failed to delete user: {e}")

def migrate_database():
    """Run Django migrations"""
    print("\n=== Running Database Migrations ===")
    try:
        call_command('makemigrations')
        call_command('migrate')
        print("[SUCCESS] Database migrations completed!")
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")

def create_superuser():
    """Create Django superuser"""
    print("\n=== Create Django Superuser ===")
    try:
        call_command('createsuperuser', interactive=True)
        print("[SUCCESS] Superuser created!")
    except Exception as e:
        print(f"[ERROR] Failed to create superuser: {e}")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("HALL BOOKING - ADMIN MANAGEMENT SYSTEM")
        print("="*50)
        print("1. List Admin Users")
        print("2. Create Default Admins")
        print("3. Create Custom Admin")
        print("4. Delete Admin User")
        print("5. Run Database Migrations")
        print("6. Create Django Superuser")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            list_admin_users()
        elif choice == '2':
            create_default_admins()
        elif choice == '3':
            create_custom_admin()
        elif choice == '4':
            delete_admin_user()
        elif choice == '5':
            migrate_database()
        elif choice == '6':
            create_superuser()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

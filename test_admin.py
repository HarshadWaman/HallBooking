import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallpro.settings')
import django
django.setup()

from django.contrib.auth import authenticate
from hallapp.models import User

print("=== Testing Admin Login ===")

# Test credentials
test_credentials = [
    {'email': 'harshadwaman4@gmail.com', 'password': '9011818144'},
    {'email': 'nayanpatilnp11@gmail.com', 'password': 'nayan2105'},
    {'email': 'hallbooking@gmail.com', 'password': 'hallbooking'},
]

for cred in test_credentials:
    print(f"\nTesting: {cred['email']}")
    
    # Find user
    try:
        user = User.objects.get(email=cred['email'])
        print(f"  User found: {user.username}")
        print(f"  User type: {getattr(user, 'user_type', 'NOT_SET')}")
        print(f"  Is staff: {user.is_staff}")
        print(f"  Is active: {user.is_active}")
        
        # Test authentication
        auth_user = authenticate(username=user.username, password=cred['password'])
        if auth_user:
            print(f"  ✓ Authentication successful")
        else:
            print(f"  ✗ Authentication failed")
            
    except User.DoesNotExist:
        print(f"  ✗ User not found")

print("\n=== All Users ===")
for user in User.objects.all():
    print(f"{user.email} - {getattr(user, 'user_type', 'NO_TYPE')} - Staff: {user.is_staff}")

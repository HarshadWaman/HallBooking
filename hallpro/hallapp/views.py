from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Admin
import json

# Create your views here.
def index(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('landing')
    return render(request, 'index.html')

def avhalls(request):
    return render(request, 'avhalls.html')

def landing(request):
    return render(request, 'landing.html')

def booking(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('landing')
    return render(request, 'booking.html')

def admin_dashboard(request):
    # Check if admin is logged in
    if 'admin_id' not in request.session:
        return redirect('landing')
    admin = Admin.objects.get(id=request.session['admin_id'])
    return render(request, 'admin.html', {'admin': admin})

@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        user_type = data.get('userType')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm = data.get('confirm')
        
        # Validation
        if not all([user_type, name, email, password, confirm]):
            return JsonResponse({'success': False, 'message': 'All fields are required'})
        
        if password != confirm:
            return JsonResponse({'success': False, 'message': 'Passwords do not match'})
        
        if len(password) < 6:
            return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters'})
        
        if user_type == 'user':
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})
            
            hashed_password = make_password(password)
            user = User.objects.create(name=name, email=email, password=hashed_password)
            return JsonResponse({'success': True, 'message': 'Registration successful! Please login.'})
        
        elif user_type == 'admin':
            if Admin.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})
            
            hashed_password = make_password(password)
            admin = Admin.objects.create(name=name, email=email, password=hashed_password)
            return JsonResponse({'success': True, 'message': 'Registration successful! Please login.'})
        
        return JsonResponse({'success': False, 'message': 'Invalid user type'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        user_type = data.get('userType')
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not all([user_type, email, password]):
            return JsonResponse({'success': False, 'message': 'All fields are required'})
        
        if user_type == 'user':
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return JsonResponse({'success': True, 'message': 'Login successful!', 'redirect': '/index/'})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid credentials'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        
        elif user_type == 'admin':
            try:
                admin = Admin.objects.get(email=email)
                if check_password(password, admin.password):
                    request.session['admin_id'] = admin.id
                    request.session['admin_name'] = admin.name
                    return JsonResponse({'success': True, 'message': 'Login successful!', 'redirect': '/admin-dashboard/'})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid credentials'})
            except Admin.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        
        return JsonResponse({'success': False, 'message': 'Invalid user type'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def logout(request):
    request.session.flush()
    return redirect('landing')
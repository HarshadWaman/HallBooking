import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from django.db.models import Q, Case, When, Value
from django.utils import timezone
from .models import User, Hall, Booking

# Hardcoded admin credentials
HARDCODED_ADMINS = [
    {'username': 'harshad', 'password': '9011818144', 'email': 'harshadwaman4@gmail.com', 'name': 'Harshad'},
    {'username': 'nayan', 'password': 'nayan2105', 'email': 'nayanpatilnp11@gmail.com', 'name': 'Nayan'},
]

# ===========================
# Public Pages
# ===========================

def index(request):
    # Fetch active halls to display on homepage
    halls = Hall.objects.filter(is_active=True)
    return render(request, 'index.html', {'halls': halls})

# ===========================
# Authentication (Login/Register)
# ===========================

def landing_page(request):
    """Renders Login/Register page"""
    if request.user.is_authenticated:
        # Check if it's a hardcoded admin
        if request.session.get('is_admin') or (hasattr(request.user, 'user_type') and request.user.user_type == 'admin'):
            return redirect('admin-dashboard')
        return redirect('index')
    return render(request, 'landing.html')

@ensure_csrf_cookie
def api_login(request):
    """Handles AJAX login requests from landing.html"""
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('userType') # 'admin' or 'user'

        # Check hardcoded admin credentials first
        if user_type == 'admin':
            for admin in HARDCODED_ADMINS:
                if admin['email'] == email and admin['password'] == password:
                    # Create a temporary user object for session
                    from django.contrib.auth.models import AnonymousUser
                    user = AnonymousUser()
                    user.username = admin['username']
                    user.email = admin['email']
                    user.first_name = admin['name']
                    user.user_type = 'admin'
                    user.is_authenticated = True
                    
                    # Store admin info in session
                    request.session['admin_user'] = admin
                    request.session['is_admin'] = True
                    
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect': reverse('admin-dashboard')})
            
            return JsonResponse({'success': False, 'message': 'Invalid admin credentials.'})
        
        # Handle regular user login
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect': reverse('index')})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid password.'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_register(request):
    """Handles AJAX register requests from landing.html"""
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered.'})

        # Create user
        # Note: We use email as username or generate a unique one if you prefer
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.user_type = 'user'  # Set default user type
        user.save()

        return JsonResponse({'success': True, 'message': 'Registration successful!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def logout_view(request):
    logout(request)
    return redirect('landing')

@ensure_csrf_cookie
def admin_login_api(request):
    """Handle admin login via API"""
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        # Check hardcoded admin credentials
        for admin in HARDCODED_ADMINS:
            if admin['email'] == email and admin['password'] == password:
                # Create session for admin
                request.session['admin_user'] = admin
                request.session['is_admin'] = True
                
                return JsonResponse({'success': True, 'redirect': reverse('admin-dashboard')})
        
        return JsonResponse({'success': False, 'message': 'Invalid admin credentials.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def admin_login_view(request):
    """Renders admin login page"""
    if request.user.is_authenticated and request.session.get('is_admin'):
        return redirect('admin-dashboard')
    # Only allow access to admin login page if user is not authenticated
    # or if user is authenticated but not an admin (regular user)
    if request.user.is_authenticated and not request.session.get('is_admin'):
        return redirect('index')
    return render(request, 'admin_login.html')

@ensure_csrf_cookie
def api_add_user(request):
    """Handle adding new user by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('userType', 'user')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered.'})

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.user_type = user_type  # Set the user type from form
            user.save()
            return JsonResponse({'success': True, 'message': 'User created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error creating user: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_update_user(request, user_id):
    """Handle updating user by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'})
    
    if request.method == "POST":
        data = json.loads(request.body)
        
        if 'name' in data:
            user.first_name = data['name']
        if 'email' in data and data['email'] != user.email:
            if User.objects.filter(email=data['email']).exclude(id=user_id).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists.'})
            user.email = data['email']
            user.username = data['email']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'user_type' in data:
            user.user_type = data['user_type']
        
        user.save()
        return JsonResponse({'success': True, 'message': 'User updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_cancel_booking(request, booking_id):
    """Handle booking cancellation by user"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'})
    
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        # Only allow cancellation of PENDING bookings
        if booking.status != 'PENDING':
            return JsonResponse({'success': False, 'message': 'Only pending bookings can be cancelled'})
        
        # Update booking status to CANCELLED
        booking.status = 'CANCELLED'
        booking.save()
        
        return JsonResponse({'success': True, 'message': 'Booking cancelled successfully!'})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error cancelling booking: {str(e)}'})

@ensure_csrf_cookie
def api_booking_status(request, booking_id):
    """Handle real-time booking status updates"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'})
    
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        current_time = timezone.now()
        
        status_data = {
            'id': booking.id,
            'status': booking.status,
            'event_name': booking.event_name,
            'hall_name': booking.hall.name,
            'start_time': booking.start_time.strftime('%H:%M'),
            'end_time': booking.end_time.strftime('%H:%M'),
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'current_time': current_time.strftime('%H:%M'),
            'current_date': current_time.strftime('%Y-%m-%d'),
            'event_started': False,
            'event_completed': False
        }
        
        # Check if event has started
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(booking.booking_date, booking.start_time),
            timezone.get_current_timezone()
        )
        
        if current_time >= booking_datetime and booking.status == 'APPROVED':
            status_data['event_started'] = True
            # Update status to IN_PROGRESS if not already set
            if booking.status != 'IN_PROGRESS' and booking.status != 'COMPLETED':
                booking.status = 'IN_PROGRESS'
                booking.save()
                status_data['status'] = 'IN_PROGRESS'
        
        # Check if event has completed
        end_datetime = timezone.make_aware(
            timezone.datetime.combine(booking.booking_date, booking.end_time),
            timezone.get_current_timezone()
        )
        
        if current_time >= end_datetime and booking.status == 'IN_PROGRESS':
            status_data['event_completed'] = True
            booking.status = 'COMPLETED'
            booking.save()
            status_data['status'] = 'COMPLETED'
        
        return JsonResponse({'success': True, 'booking': status_data})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error checking booking status: {str(e)}'})

@ensure_csrf_cookie
def api_add_hall(request):
    """Handle adding new hall by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        capacity = data.get('capacity')
        location = data.get('location')
        is_active = data.get('is_active', True)
        
        if not name or not capacity or not location:
            return JsonResponse({'success': False, 'message': 'All required fields must be provided'})
        
        try:
            hall = Hall.objects.create(
                name=name,
                capacity=int(capacity),
                location=location,
                is_active=is_active
            )
            return JsonResponse({'success': True, 'message': 'Hall added successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error adding hall: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_delete_hall(request, hall_id):
    """Handle hall deletion by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == "POST":
        try:
            hall = Hall.objects.get(id=hall_id)
            hall.delete()
            return JsonResponse({'success': True, 'message': 'Hall deleted successfully!'})
        except Hall.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Hall not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error deleting hall: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_update_hall(request, hall_id):
    """Handle hall updates by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    try:
        hall = Hall.objects.get(id=hall_id)
    except Hall.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Hall not found.'})
    
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        capacity = data.get('capacity')
        location = data.get('location')
        is_active = data.get('is_active')
        
        if not name or not capacity or not location:
            return JsonResponse({'success': False, 'message': 'All required fields must be provided'})
        
        try:
            hall.name = name
            hall.capacity = int(capacity)
            hall.location = location
            if is_active is not None:
                hall.is_active = is_active
            hall.save()
            return JsonResponse({'success': True, 'message': 'Hall updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error updating hall: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@ensure_csrf_cookie
def api_delete_booking(request, booking_id):
    """Handle permanent booking deletion by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return JsonResponse({'success': True, 'message': 'Booking deleted permanently!'})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error deleting booking: {str(e)}'})

@ensure_csrf_cookie
def api_booking_details(request, booking_id):
    """Handle booking details retrieval by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    try:
        booking = Booking.objects.select_related('user', 'hall').get(id=booking_id)
        booking_data = {
            'id': booking.id,
            'event_name': booking.event_name,
            'hall_name': booking.hall.name,
            'user_name': booking.user.get_full_name() or booking.user.username,
            'department': booking.department,
            'coordinator_name': booking.coordinator_name,
            'coordinator_mobile': booking.coordinator_mobile,
            'booking_date': booking.booking_date.strftime('%d %b %Y'),
            'start_time': booking.start_time.strftime('%H:%M'),
            'end_time': booking.end_time.strftime('%H:%M'),
            'status': booking.status,
            'rejection_reason': booking.rejection_reason or ''
        }
        return JsonResponse({'success': True, 'booking': booking_data})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found.'})

@ensure_csrf_cookie
def api_update_booking_status(request, booking_id):
    """Handle booking approval/rejection by admin"""
    if not request.session.get('is_admin'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found.'})
    
    if request.method == "POST":
        data = json.loads(request.body)
        status = data.get('status')
        
        if status in ['APPROVED', 'REJECTED']:
            booking.status = status
            if status == 'APPROVED':
                booking.approved_at = timezone.now()
            elif status == 'REJECTED':
                booking.rejected_at = timezone.now()
                booking.rejection_reason = data.get('reason', '')
            booking.save()
            
            action = 'approved' if status == 'APPROVED' else 'rejected'
            return JsonResponse({'success': True, 'message': f'Booking {action} successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# ===========================
# Booking Logic
# ===========================

def booking_view(request):
    if request.method == "POST":
        # Extract data from form
        event_name = request.POST.get('event_name')
        date = request.POST.get('date')
        time_from = request.POST.get('time_from')
        time_to = request.POST.get('time_to')
        venue_id = request.POST.get('venue') # ID of Hall
        
        # Save Booking
        # Note: Ensure you have Halls created in Admin panel first!
        try:
            hall = Hall.objects.get(id=venue_id) if venue_id else Hall.objects.first()
            
            booking = Booking(
                user=request.user,
                hall=hall,
                event_name=event_name,
                booking_date=date,
                start_time=time_from,
                end_time=time_to,
                department=request.POST.get('department'),
                coordinator_name=request.POST.get('coordinator'),
                coordinator_mobile=request.POST.get('mobile'),
                # Event Requirements
                stage_size=request.POST.get('stage_size'),
                audience_count=int(request.POST.get('audience_count', 0)),
                chair_type=request.POST.get('chair_type'),
                chair_count=int(request.POST.get('chairs_count', 0)),
                # Equipment Counts
                mic_count=int(request.POST.get('mic_count', 0)),
                speaker_count=int(request.POST.get('speaker_count', 0)),
                projector_count=int(request.POST.get('projector_count', 0)),
                laptop_count=int(request.POST.get('laptop_count', 0)),
                # Traditional Items (checkboxes)
                req_agarbatti=request.POST.get('agarbatti') == 'on',
                req_matchbox=request.POST.get('matchbox') == 'on',
                req_oil=request.POST.get('oil') == 'on',
                req_wati=request.POST.get('wati') == 'on',
                req_kapur=request.POST.get('kapur') == 'on',
                req_satarangi=request.POST.get('satarangi', ''),
                req_carpet=request.POST.get('carpet') == 'on',
                req_mandap=request.POST.get('mandap') == 'on',
                req_saraswati_photo=request.POST.get('saraswati') == 'on',
                req_samai=request.POST.get('samai') == 'on',
            )
            booking.save()
            return JsonResponse({'success': True, 'message': 'Application Submitted Successfully'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'message': f'Error submitting form: {str(e)}'})

    # GET request - Handle query parameters from index.html
    hall_name = request.GET.get('hall', '')
    selected_date = request.GET.get('date', '')
    
    # Get the hall object if hall name is provided
    selected_hall = None
    if hall_name:
        try:
            selected_hall = Hall.objects.get(name=hall_name)
        except Hall.DoesNotExist:
            selected_hall = None
    
    halls = Hall.objects.filter(is_active=True)
    context = {
        'halls': halls,
        'selected_hall': selected_hall,
        'selected_date': selected_date,
        'hall_name': hall_name
    }
    return render(request, 'booking.html', context)

@login_required
def my_bookings(request):
    # Get bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'mybooking.html', {'bookings': bookings})

# ===========================
# Admin Dashboard
# ===========================

@login_required
def booking_details_view(request, booking_id):
    """Display detailed booking information"""
    try:
        booking = Booking.objects.select_related('user', 'hall').get(id=booking_id)
        
        # Check if user is admin or the booking owner
        is_admin = request.session.get('is_admin')
        is_owner = booking.user == request.user
        
        if not (is_admin or is_owner):
            return redirect('index')  # Unauthorized access
        
        context = {'booking': booking}
        return render(request, 'booking_details.html', context)
    except Booking.DoesNotExist:
        return redirect('index')  # Booking not found

def admin_dashboard(request):
    # Security check: Ensure only admins can access
    if not request.session.get('is_admin'):
        return redirect('admin-login-view')

    # Get admin info from session
    admin_info = request.session.get('admin_user', {})
    admin_name = admin_info.get('name', 'Admin')
    
    context = {
        'admin': admin_info,
        'admin_name': admin_name,
        'total_halls': Hall.objects.count(),
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='PENDING').count(),
        'users_count': User.objects.count(),
        'halls': Hall.objects.all().order_by('-id'),
        'recent_bookings': Booking.objects.select_related('user', 'hall').exclude(status='CANCELLED').annotate(
            status_order=Case(
                When(status='PENDING', then=Value(1)),
                When(status='REJECTED', then=Value(2)),
                When(status='APPROVED', then=Value(3)),
                default=Value(4)
            )
        ).order_by('status_order', '-created_at')[:5],
        'all_bookings': Booking.objects.select_related('user', 'hall').exclude(status='CANCELLED').annotate(
            status_order=Case(
                When(status='PENDING', then=Value(1)),
                When(status='REJECTED', then=Value(2)),
                When(status='APPROVED', then=Value(3)),
                default=Value(4)
            )
        ).order_by('status_order', '-booking_date', '-start_time'),
        'users': User.objects.all().order_by('-date_joined')
    }
    return render(request, 'admin.html', context)
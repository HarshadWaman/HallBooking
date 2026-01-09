# Hardcoded Admin System - Hall Booking

## Overview

Admin users are now hardcoded in the application instead of being stored in the database. The User table is now used only for regular users.

## Hardcoded Admin Credentials

| Username | Email                   | Password   | Name    |
| -------- | ----------------------- | ---------- | ------- |
| harshad  | harshadwaman4@gmail.com | 9011818144 | Harshad |
| nayan    | nayanpatilnp11.com      | nayan2105  | Nayan   |

## How It Works

1. **Admin Login**: When user selects "Admin" login type, the system checks against hardcoded credentials
2. **Session Management**: Admin info is stored in session for the duration of the login
3. **Regular Users**: Normal users register and login through the database as before

## Database Changes

- ✅ Removed `user_type` field from User model
- ✅ Deleted all admin users from database
- ✅ Applied database migrations
- ✅ User table now stores only regular users

## Security Features

- Admin credentials are hardcoded in `views.py`
- Session-based admin authentication
- Separate admin and user login flows
- Admin access protected by session checks

## Login Process

### Admin Login:

1. Select "Admin" as user type
2. Enter email and password from hardcoded list
3. System validates against `HARDCODED_ADMINS` array
4. Creates session and redirects to admin dashboard

### User Registration/Login:

1. Select "User" as user type
2. Register/login through database
3. No access to admin features

## Files Modified

- `models.py` - Removed user_type field
- `views.py` - Added hardcoded admin authentication
- Database migrations applied

## Admin Dashboard Access

**URL**: http://127.0.0.1:8000/admin-dashboard/

Admin dashboard now works with hardcoded credentials and session management.

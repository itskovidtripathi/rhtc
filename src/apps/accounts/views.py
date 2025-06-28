from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import CareGiverProfile, UserRole

# Create your views here.

def is_strong_password(password):
    # At least 8 chars, one uppercase, one lowercase, one digit, one special char
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[\W_]', password):
        return False, "Password must contain at least one special character."
    return True, ""

def is_valid_mobile(number):
    return re.fullmatch(r'[6-9]\d{9}', number) is not None

def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        whatsapp = request.POST.get("whatsapp", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        accept_terms = request.POST.get("accept_terms")
        # Basic validation
        if not full_name:
            messages.error(request, "Full name is required.")
        elif not whatsapp or not is_valid_mobile(whatsapp):
            messages.error(request, "Enter a valid 10-digit WhatsApp number starting with 6-9.")
        elif not accept_terms:
            messages.error(request, "You must accept the Terms & Conditions and Privacy Policy.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            strong, msg = is_strong_password(password)
            if not strong:
                messages.error(request, msg)
            elif User.objects.filter(username=whatsapp).exists():
                messages.error(request, "A user with this WhatsApp number already exists.")
            else:
                user = User.objects.create_user(username=whatsapp, password=password, first_name=full_name)
                UserRole.objects.create(user=user, role='patient')
                login(request, user)
                return redirect('core:home')
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember_me")
        if not is_valid_mobile(mobile):
            messages.error(request, "Enter a valid 10-digit mobile number starting with 6-9.")
        elif not password:
            messages.error(request, "Password is required.")
        else:
            user = authenticate(request, username=mobile, password=password)
            if user is not None:
                # Ensure user is a patient
                if hasattr(user, 'role') and user.role.role == 'patient':
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('core:home')
                else:
                    messages.error(request, "You are not authorized to login as a patient.")
            else:
                messages.error(request, "Invalid mobile number or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:home')

def caregiver_signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        whatsapp = request.POST.get("whatsapp", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        designation = request.POST.get("designation", "").strip()
        specialty = request.POST.get("specialty", "").strip()
        profile_image = request.FILES.get("profile_image")  # <-- handle file upload
        accept_terms = request.POST.get("accept_terms")
        # Basic validation
        if not full_name:
            messages.error(request, "Full name is required.")
        elif not whatsapp or not is_valid_mobile(whatsapp):
            messages.error(request, "Enter a valid 10-digit WhatsApp number starting with 6-9.")
        elif not email:
            messages.error(request, "Email is required.")
        elif not designation:
            messages.error(request, "Designation is required.")
        elif not specialty:
            messages.error(request, "Area of specialty is required.")
        elif not accept_terms:
            messages.error(request, "You must accept the Terms & Conditions and Privacy Policy.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            strong, msg = is_strong_password(password)
            if not strong:
                messages.error(request, msg)
            elif User.objects.filter(username=whatsapp).exists():
                messages.error(request, "A user with this WhatsApp number already exists.")
            elif CareGiverProfile.objects.filter(email=email).exists():
                messages.error(request, "A caregiver with this email already exists.")
            else:
                user = User.objects.create_user(username=whatsapp, password=password, first_name=full_name, email=email)
                caregiver_profile = CareGiverProfile.objects.create(
                    user=user,
                    full_name=full_name,
                    email=email,
                    designation=designation,
                    specialty=specialty,
                    profile_image=profile_image,  # <-- save uploaded image
                    contact_number=whatsapp,  # Set contact_number to WhatsApp/mobile
                )
                UserRole.objects.create(user=user, role='caregiver')
                login(request, user)
                return redirect('human_interface:care_giver_detail', pk=caregiver_profile.pk)
    return render(request, 'accounts/caregiver-signup.html')

def caregiver_login_view(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember_me")
        if not is_valid_mobile(mobile):
            messages.error(request, "Enter a valid 10-digit mobile number starting with 6-9.")
        elif not password:
            messages.error(request, "Password is required.")
        else:
            user = authenticate(request, username=mobile, password=password)
            if user is not None and hasattr(user, 'caregiver_profile'):
                # Ensure user is a caregiver
                if hasattr(user, 'role') and user.role.role == 'caregiver':
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return redirect('human_interface:care_giver_detail', pk=user.caregiver_profile.pk)
                else:
                    messages.error(request, "You are not authorized to login as a caregiver.")
            else:
                messages.error(request, "Invalid caregiver mobile number or password.")
    return render(request, 'accounts/caregiver-login.html')


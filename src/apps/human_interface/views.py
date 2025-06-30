from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import CareGiverProfile, UserRole
from .models import AppointmentRequest
from django.utils import timezone
from datetime import timedelta, date, datetime

# Create your views here.

def list_care_givers(request):
    caregivers = CareGiverProfile.objects.all()
    return render(request, 'human-interface/list_care_givers.html', {'caregivers': caregivers})

def care_giver_profile(request, pk):
    caregiver = get_object_or_404(CareGiverProfile, pk=pk)
    return render(request, 'human-interface/care-giver-profile.html', {'caregiver': caregiver})

@login_required
def edit_care_giver_profile(request):
    user = request.user
    # Only caregivers can access
    if not hasattr(user, 'role') or user.role.role != 'caregiver':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('core:home')
    caregiver = get_object_or_404(CareGiverProfile, user=user)
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        designation = request.POST.get("designation", "").strip()
        specialty = request.POST.get("specialty", "").strip()
        bio = request.POST.get("bio", "").strip()
        profile_image = request.FILES.get("profile_image")
        social_linked_in = request.POST.get("social_linked_in", "").strip()
        social_twitter = request.POST.get("social_twitter", "").strip()
        social_facebook = request.POST.get("social_facebook", "").strip()
        # Basic validation (add more as needed)
        if not full_name or not email or not designation or not specialty:
            messages.error(request, "Please fill all required fields.")
        else:
            caregiver.full_name = full_name
            caregiver.email = email
            caregiver.designation = designation
            caregiver.specialty = specialty
            caregiver.bio = bio
            caregiver.social_linked_in = social_linked_in
            caregiver.social_twitter = social_twitter
            caregiver.social_facebook = social_facebook
            if profile_image:
                caregiver.profile_image = profile_image
            caregiver.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('human_interface:care_giver_detail', pk=caregiver.pk)
    return render(request, 'human-interface/edit-profile-care-giver.html', {'caregiver': caregiver})

@login_required
def schedule_appointment(request, caregiver_id):
    caregiver = get_object_or_404(CareGiverProfile, pk=caregiver_id)
    # Prevent duplicate pending requests
    existing = AppointmentRequest.objects.filter(
        caregiver=caregiver,
        requester=request.user,
        status='pending'
    ).exists()
    if existing:
        messages.error(request, "You already have a pending appointment request with this caregiver. Please wait for approval or rejection before submitting another request.")
        return redirect('human_interface:list_care_givers')
    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        # Server-side validation for duplicate approved date
        if not date_from or not date_to:
            messages.error(request, "Please select both start and end dates.")
        else:
            # Check for overlap with already approved appointments for this caregiver
            overlap = AppointmentRequest.objects.filter(
                caregiver=caregiver,
                status='approved',
                approved_date__range=[date_from, date_to]
            ).exists()
            if overlap:
                messages.error(request, "There is already an approved appointment for this caregiver in the selected date range. Please choose a different range.")
            else:
                AppointmentRequest.objects.create(
                    caregiver=caregiver,
                    requester=request.user,
                    date_from=date_from,
                    date_to=date_to,
                )
                messages.success(request, "Appointment request submitted! Approval takes approximately 24 hours. You will be informed after approval.")
                return redirect('human_interface:list_care_givers')
    return render(request, 'human-interface/schedule-appointment.html', {'caregiver': caregiver})

@login_required
def check_appointment_requests(request):
    user = request.user
    if not hasattr(user, 'role') or user.role.role != 'caregiver':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('core:home')
    caregiver = getattr(user, 'caregiver_profile', None)
    if not caregiver:
        messages.error(request, "Caregiver profile not found.")
        return redirect('core:home')

    # Handle approve/reject POST
    if request.method == "POST":
        req_id = request.POST.get("request_id")
        action = request.POST.get("action")
        selected_date = request.POST.get("approved_date")
        appointment = AppointmentRequest.objects.filter(pk=req_id, caregiver=caregiver, status='pending').first()
        if not appointment:
            messages.error(request, "Invalid appointment request.")
        elif action == "approve":
            # Standardize date format: always expect YYYY-MM-DD from frontend
            if not selected_date:
                messages.error(request, "Please select a date to approve.")
            else:
                try:
                    # Debug: print the value received from the frontend
                    print("DEBUG: selected_date value from frontend:", selected_date)
                    selected_date_obj = date.fromisoformat(selected_date)
                except Exception:
                    messages.error(request, f"Invalid date format: '{selected_date}'. Please select a valid date.")
                    selected_date_obj = None
                if selected_date_obj:
                    conflict = AppointmentRequest.objects.filter(
                        caregiver=caregiver,
                        approved_date=selected_date_obj,
                        status='approved'
                    ).exclude(pk=appointment.pk).exists()
                    if conflict:
                        messages.error(request, f"Already have an approved appointment on {selected_date_obj}.")
                    elif not (appointment.date_from <= selected_date_obj <= appointment.date_to):
                        messages.error(request, "Selected date is not within the requested range.")
                    else:
                        appointment.status = 'approved'
                        appointment.approved_date = selected_date_obj
                        appointment.save()
                        messages.success(request, f"Appointment approved for {selected_date_obj}.")
        elif action == "reject":
            appointment.status = 'rejected'
            appointment.approved_date = None
            appointment.save()
            messages.success(request, "Appointment request rejected.")

    # List all appointment requests for this caregiver
    appointments = AppointmentRequest.objects.filter(caregiver=caregiver).order_by('-created_at')
    approved_dates = set(
        AppointmentRequest.objects.filter(
            caregiver=caregiver,
            status='approved'
        ).values_list('approved_date', flat=True)
    )
    pending_appointments = []
    for appt in appointments:
        if appt.status == 'pending':
            available_dates = []
            d = appt.date_from
            while d <= appt.date_to:
                if d not in approved_dates:
                    available_dates.append(d)
                d += timedelta(days=1)
            appt.available_dates = available_dates
        pending_appointments.append(appt)

    return render(request, 'human-interface/check-appointment-request.html', {
        'appointments': appointments,
    })

@login_required
def appointment_status_view(request):
    # Only allow patients to view their own appointment status
    user = request.user
    if not hasattr(user, 'role') or user.role.role != 'patient':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('core:home')
    # Show only this user's appointment requests
    appointments = AppointmentRequest.objects.filter(requester=user).order_by('-created_at')
    return render(request, 'human-interface/appointments-status.html', {
        'appointments': appointments,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def patient_profile_view(request):
    user = request.user
    # Only allow patients to view their own profile
    if not hasattr(user, 'role') or user.role.role != 'patient':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('core:home')
    return render(request, 'patient/patient-profile.html', {'user': user})

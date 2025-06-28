from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import CareGiverProfile

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
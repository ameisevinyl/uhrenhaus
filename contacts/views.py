from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UnifiedProfileForm

@login_required
def user_dashboard(request):
    return render(request, "contacts/dashboard.html")

@login_required
def profile_settings(request):
    """Allows users to update all profile data (Contact, Address, BankAccount) in one form."""
    
    user = request.user

    if request.method == "POST":
        form = UnifiedProfileForm(request.POST, instance=user, user=user)
        if form.is_valid():
            form.save(user=user)
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

    else:
        form = UnifiedProfileForm(instance=user, user=user)

    return render(request, "contacts/profile.html", {"form": form})

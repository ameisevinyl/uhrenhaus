from django.urls import path
from .views import user_dashboard, profile_settings

urlpatterns = [
    path("dashboard/", user_dashboard, name="dashboard"),
    path("profile/", profile_settings, name="profile"),  # ✅ Profile page
]

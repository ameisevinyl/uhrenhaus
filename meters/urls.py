from django.urls import path
from . import views  # Import views from meters app

urlpatterns = [
    # Example route (add actual views later)
    path("", views.home, name="home"),
]

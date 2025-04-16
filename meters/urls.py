from django.urls import include, path
from . import views  # Import views from meters app

urlpatterns = [
    # Example route (add actual views later)
    path("", views.home, name="home"),
    path("api/", include("meters.api_urls")),
]

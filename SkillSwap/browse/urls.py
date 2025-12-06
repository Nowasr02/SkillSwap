from django.urls import path
from . import views

app_name = "browse"

urlpatterns = [
    path("", views.browse_view, name="browse_view"),
]
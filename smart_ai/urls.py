__author__ = "Mohit Thakkar"

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Don't need the admin app, might add later
    path('admin/', admin.site.urls),
]

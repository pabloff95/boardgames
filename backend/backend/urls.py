from django.contrib import admin
from django.urls import include, path
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path(os.getenv("API_NAMESPACE"), include("game.urls")),
]

from django.contrib import admin
from django.urls import include, path
import os

API_NAMESPACE = os.getenv("API_NAMESPACE", "/api/v1/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_NAMESPACE, include("game.urls")),
    path(API_NAMESPACE, include("users.urls")),
]

from django.contrib import admin
from django.urls import include, path
import os
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

API_NAMESPACE = os.getenv("API_NAMESPACE", "/api/v1/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_NAMESPACE, include("game.urls")),
    path(API_NAMESPACE, include("users.urls")),
    path(
        f"{API_NAMESPACE}token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        f"{API_NAMESPACE}token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

from django.contrib import admin
from django.urls import include, path

namespace = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(namespace, include("game.urls")),
]

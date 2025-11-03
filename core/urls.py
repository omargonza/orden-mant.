from django.contrib import admin
from django.urls import path, include
from .views import health_check

urlpatterns = [
    path("", health_check),  # 👈 Render usará esto para el “check de puerto”
    path("admin/", admin.site.urls),
    path("api/", include("orders.urls")),
]



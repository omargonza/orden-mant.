from django.urls import path
from .views import OrdenPDFView

urlpatterns = [
    path("ordenes/pdf", OrdenPDFView.as_view(), name="orden-pdf"),
]

# core/orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf
import logging

logger = logging.getLogger(__name__)

class OrdenPDFView(APIView):
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    def post(self, request):
        logger.info("📩 Datos recibidos: %s", request.data)
        serializer = OrdenTrabajoSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error("❌ Errores de validación: %s", serializer.errors)
            return Response({"errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)
        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename=\"{nombre_archivo}\"'
        logger.info("✅ PDF generado exitosamente: %s", nombre_archivo)
        return resp
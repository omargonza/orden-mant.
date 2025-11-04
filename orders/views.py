from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf
import logging

logger = logging.getLogger(__name__)

class OrdenPDFView(APIView):
    def post(self, request):
        # 👀 Log de lo que llega
        logger.info("📩 Datos recibidos: %s", request.data)

        serializer = OrdenTrabajoSerializer(data=request.data)

        if not serializer.is_valid():
            # 🔎 Mostrar los errores exactos (y enviarlos en la respuesta)
            logger.error("❌ Errores de validación: %s", serializer.errors)
            return Response(
                {"errores": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Generar el PDF con datos validados
        pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
        return resp


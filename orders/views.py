from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf

class OrdenPDFView(APIView):
    def post(self, request):
        # 👀 Log de lo que llega
        print("📩 Datos recibidos:", request.data)

        serializer = OrdenTrabajoSerializer(data=request.data)

        if not serializer.is_valid():
            # 🔎 DEVOLVÉ el detalle del 400 para saber qué campo rompe
            print("❌ Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
        return resp

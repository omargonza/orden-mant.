from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf

class OrdenPDFView(APIView):
    # 🔸 Maneja el preflight request (CORS)
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    def post(self, request):
        print("📩 Datos recibidos:", request.data)

        serializer = OrdenTrabajoSerializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 🧾 Generación del PDF
        try:
            pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)
            resp = HttpResponse(pdf_bytes, content_type="application/pdf")
            resp["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
            # Encabezado CORS para el PDF
            resp["Access-Control-Allow-Origin"] = "*"
            return resp

        except Exception as e:
            print("💥 Error generando PDF:", e)
            return Response(
                {"error": "Error al generar el PDF", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

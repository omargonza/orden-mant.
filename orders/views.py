from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import traceback

from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf


@method_decorator(csrf_exempt, name='dispatch')
class OrdenPDFView(APIView):
    def post(self, request):
        print("📩 REQUEST BODY RAW:", request.body[:500])

        try:
            data = json.loads(request.body)
            print("✅ JSON Decodificado:", data)
        except json.JSONDecodeError:
            print("❌ Error decodificando JSON")
            return Response({"error": "JSON inválido"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrdenTrabajoSerializer(data=data)
        if not serializer.is_valid():
            print("❌ Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("🧩 Datos validados:", serializer.validated_data)
            pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)
            print("✅ PDF generado correctamente:", nombre_archivo)

            resp = HttpResponse(pdf_bytes, content_type="application/pdf")
            resp["Content-Disposition"] = f'attachment; filename=\"{nombre_archivo}\"'
            return resp

        except Exception as e:
            print("💥 Error generando PDF:", str(e))
            traceback.print_exc()
            return Response(
                {"error": str(e), "trace": traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

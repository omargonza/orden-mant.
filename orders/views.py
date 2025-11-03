from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf


class OrdenPDFView(APIView):
    def post(self, request):
        print("📩 Datos recibidos en el servidor:", request.data) 
        serializer = OrdenTrabajoSerializer(data=request.data)

        # 🔍 Agregamos este bloque para ver qué está fallando en Render
        if not serializer.is_valid():
            print("❌ Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=400)

        # ✅ Si está todo bien, generamos el PDF
        pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
        return resp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import OrdenTrabajoSerializer
from .pdf import build_pdf


class OrdenPDFView(APIView):
    def post(self, request):
        serializer = OrdenTrabajoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pdf_bytes, nombre_archivo = build_pdf(serializer.validated_data)

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
        return resp

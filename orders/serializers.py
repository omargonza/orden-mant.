# backend/orders/serializers.py
from rest_framework import serializers

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField()
    cant = serializers.FloatField(required=False, allow_null=True)
    unidad = serializers.CharField(allow_blank=True, required=False)

class LegajoSerializer(serializers.Serializer):
    id = serializers.CharField()
    nombre = serializers.CharField()

class OrdenTrabajoSerializer(serializers.Serializer):
    fecha = serializers.DateField(input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    centro_costos = serializers.CharField(allow_blank=True, required=False)
    ubicacion = serializers.CharField(allow_blank=True, required=False)
    tipo_mantenimiento = serializers.ChoiceField(choices=["Preventivo", "Correctivo", "Obras nuevas"])
    prioridad = serializers.ChoiceField(choices=["Normal", "Urgente"])
    tarea = serializers.CharField(allow_blank=True, required=False)
    observaciones = serializers.CharField(allow_blank=True, required=False)
    tableros = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    circuitos = serializers.CharField(allow_blank=True, required=False)
    hora_inicio = serializers.CharField(allow_blank=True, required=False)
    hora_fin = serializers.CharField(allow_blank=True, required=False)
    legajos = LegajoSerializer(many=True, required=False)
    materiales = MaterialSerializer(many=True, required=False)

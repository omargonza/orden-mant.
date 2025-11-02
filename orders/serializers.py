# backend/orders/serializers.py
from rest_framework import serializers

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField()
    cant = serializers.FloatField()
    unidad = serializers.CharField()

class LegajoSerializer(serializers.Serializer):
    id = serializers.CharField()
    nombre = serializers.CharField()

class OrdenTrabajoSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    centro_costos = serializers.CharField(allow_blank=True, required=False)
    ubicacion = serializers.CharField(allow_blank=True, required=False)

    # campos principales
    tipo_mantenimiento = serializers.ChoiceField(choices=["Preventivo", "Correctivo", "Obras nuevas"])
    prioridad = serializers.ChoiceField(choices=["Normal", "Urgente"])

    # 🟢 título corto y descripción larga
    tarea = serializers.CharField(allow_blank=True, required=False)            # título
    observaciones = serializers.CharField(allow_blank=True, required=False)    # descripción larga

    # 🟢 nuevos
    tableros = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    circuitos = serializers.CharField(allow_blank=True, required=False)

    # horarios y personas
    hora_inicio = serializers.CharField()
    hora_fin = serializers.CharField()
    legajos = LegajoSerializer(many=True)

    # materiales
    materiales = MaterialSerializer(many=True, required=False)

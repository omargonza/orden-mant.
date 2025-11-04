from rest_framework import serializers

class MaterialSerializer(serializers.Serializer):
    nombre = serializers.CharField()  # 👈 en lugar de "material"
    cant = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False, allow_null=True
    )
    unidad = serializers.CharField(allow_blank=True, required=False)

class LegajoSerializer(serializers.Serializer):
    id = serializers.CharField()
    nombre = serializers.CharField()

class OrdenTrabajoSerializer(serializers.Serializer):
    # 📌 Acepta "2025-11-03" y "03/11/2025"
    fecha = serializers.DateField(input_formats=["%Y-%m-%d", "%d/%m/%Y"])

    centro_costos = serializers.CharField(allow_blank=True, required=False)
    ubicacion = serializers.CharField(allow_blank=True, required=False)

    tipo_mantenimiento = serializers.ChoiceField(
        choices=["Preventivo", "Correctivo", "Obras nuevas"]
    )
    prioridad = serializers.ChoiceField(choices=["Normal", "Urgente"])

    # título y descripción
    tarea = serializers.CharField(allow_blank=True, required=False)
    observaciones = serializers.CharField(allow_blank=True, required=False)

    # listas/strings opcionales
    tableros = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    circuitos = serializers.CharField(allow_blank=True, required=False)

    # horarios y personas (opcionales para no romper si vienen vacíos)
    hora_inicio = serializers.CharField(allow_blank=True, required=False)
    hora_fin = serializers.CharField(allow_blank=True, required=False)
    legajos = LegajoSerializer(many=True, required=False)

    # materiales opcional
    materiales = MaterialSerializer(many=True, required=False)

from rest_framework import serializers

VEHICULOS = [
    ("AB101RS", "AB101RS"),
    ("AE026TH", "AE026TH"),
    ("AE026VN", "AE026VN"),
    ("AF836WI", "AF836WI"),
    ("AF078KP", "AF078KP"),
    ("AH223LS", "AH223LS"),
    ("AA801TV", "AA801TV"),
]

TABLEROS = [
    "TI 1400","TI 1300","TI 1200","TI 1100","TI 1000","TI 900",
    "Tablero Cámara 1","Tablero Cámara 2","TI 800","TI 700","TI 600",
    "TI 500","TI 400","TI 300","TI 200","TI 100","TI 47 Provincias Unidas",
    "Tuyuti","Ibarrola","Amadeo Jacques","Madrid","San Cayetano","J.J. Paso",
    "San Ignacio","Croacia","TI 40 Superi","TI 41 Zapiola","TI 42 Cabildo",
    "TI 43 11 de Septiembre","Tab Grecia","TI 34 Marquez I","TI 35 Marquez II",
    "TI 32 Rolon I","TI 33 Rolon II","Tab Sucre","TG 093 Gardel",
    "TG 099 Carlos Tejedor","TG 111 Camino Moron","TGBA03 Buen Aire",
    "TGBA05 Ezequiel","TG147 Boulogne","TG165 Pacheco","TG177 Reconquista",
    "TG195 Bifurcación","TC02 Gutiérrez","TC04 Constituyentes","TC06 Alvear",
    "TC10 Ruta 9","TC24 Escobar II","TC39 Río Luján","TC42 Los Cardales",
    "TC58 Campana","TP02 Carnot","TP06 Constituyentes","TP09 Ruta 26",
    "TP14 Los Lagartos","TP21 Ricchieri","TP27 J.J. Paso","TP30 Pilar",
    "TT1 Blanco Encalada","TT3 Guido","TT6 Avellaneda","TT9 Carupá",
    "TT12 Tigre Centro","Peaje Debenedetti ASC","Peaje Debenedetti DESC",
    "Peaje Márquez ASC","Peaje Márquez DESC","Peaje Tigre Troncal",
    "Peaje Pilar Troncal","Peaje Campana Troncal",
]

class TecnicoSerializer(serializers.Serializer):
    legajo = serializers.CharField(required=False, allow_blank=True)
    nombre = serializers.CharField(required=False, allow_blank=True)

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField(required=False, allow_blank=True)
    cant = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    unidad = serializers.CharField(required=False, allow_blank=True)

class OrdenTrabajoSerializer(serializers.Serializer):
    fecha = serializers.DateField(input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    ubicacion = serializers.CharField()
    tablero = serializers.ChoiceField(choices=[(t, t) for t in TABLEROS], required=False, allow_blank=True)
    circuito = serializers.CharField(required=False, allow_blank=True)

    vehiculo = serializers.ChoiceField(choices=VEHICULOS, required=False, allow_blank=True)
    km_inicial = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    km_final = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)

    tecnicos = TecnicoSerializer(many=True, required=False)
    tarea_pedida = serializers.CharField(max_length=255, allow_blank=True, required=False)
    tarea_realizada = serializers.CharField(allow_blank=True, required=False)
    tarea_pendiente = serializers.CharField(allow_blank=True, required=False)
    luminaria_equipos = serializers.CharField(allow_blank=True, required=False)
    materiales = MaterialSerializer(many=True, required=False)

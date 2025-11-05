# core/orders/serializers.py
from rest_framework import serializers

# --- Choices ---
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
    # Gral. Paz – Acceso Norte / La Noria
    "TI 1400","TI 1300","TI 1200","TI 1100","TI 1000","TI 900",
    "Tablero Cámara 1","Tablero Cámara 2","TI 800","TI 700","TI 600",
    "TI 500","TI 400","TI 300","TI 200","TI 100","TI 47 Provincias Unidas",
    "Tuyuti","Ibarrola","Amadeo Jacques","Madrid","San Cayetano","J.J. Paso",
    "San Ignacio","Croacia",
    # Acceso Norte – General Paz / Lugones
    "TI 40 Superi","TI 41 Zapiola","TI 42 Cabildo","TI 43 11 de Septiembre","Tab Grecia",
    # Acceso Norte – Marquez / Bifurcación
    "TI 34 Marquez I","TI 35 Marquez II","TI 32 Rolon I","TI 33 Rolon II",
    "Tab Sucre","TG 093 Gardel","TG 099 Carlos Tejedor","TG 111 Camino Moron",
    "TGBA03 Buen Aire","TGBA05 Ezequiel","TG147 Boulogne","TG165 Pacheco",
    "TG177 Reconquista","TG195 Bifurcación",
    # Ramal Campana
    "TC02 Gutiérrez","TC04 Constituyentes","TC06 Alvear","TC10 Ruta 9",
    "TC24 Escobar II","TC39 Río Luján","TC42 Los Cardales","TC58 Campana",
    # Ramal Pilar
    "TP02 Carnot","TP06 Constituyentes","TP09 Ruta 26","TP14 Los Lagartos",
    "TP21 Ricchieri","TP27 J.J. Paso","TP30 Pilar",
    # Ramal Tigre
    "TT1 Blanco Encalada","TT3 Guido","TT6 Avellaneda","TT9 Carupá","TT12 Tigre Centro",
    # Estaciones de Peaje
    "Peaje Debenedetti ASC","Peaje Debenedetti DESC",
    "Peaje Márquez ASC","Peaje Márquez DESC",
    "Peaje Tigre Troncal","Peaje Pilar Troncal","Peaje Campana Troncal",
]

class TecnicoSerializer(serializers.Serializer):
    legajo = serializers.CharField()
    nombre = serializers.CharField()

class MaterialSerializer(serializers.Serializer):
    material = serializers.CharField()
    cant = serializers.DecimalField(max_digits=10, decimal_places=2)
    unidad = serializers.ChoiceField(choices=[("unidad","unidad"),("mtrs","mtrs")])

class OrdenTrabajoSerializer(serializers.Serializer):
    # encabezado / metadatos
    fecha = serializers.DateField(input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    ubicacion = serializers.CharField()
    tablero = serializers.ChoiceField(choices=[(t, t) for t in TABLEROS])
    circuito = serializers.CharField()

    # vehículo y kms
    vehiculo = serializers.ChoiceField(choices=VEHICULOS)
    km_inicial = serializers.DecimalField(max_digits=8, decimal_places=2)
    km_final = serializers.DecimalField(max_digits=8, decimal_places=2)

    # equipo humano
    tecnicos = TecnicoSerializer(many=True)

    # tareas
    tarea_pedida = serializers.CharField(max_length=255)
    tarea_realizada = serializers.CharField(allow_blank=True, required=False)
    tarea_pendiente = serializers.CharField(allow_blank=True, required=False)

    # luminarias / equipos
    luminaria_equipos = serializers.CharField(allow_blank=True, required=False)

    # materiales
    materiales = MaterialSerializer(many=True, required=False)

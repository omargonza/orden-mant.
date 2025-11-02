# Backend (Django + ReportLab)

## Setup rápido
```bash
cd backend
python -m venv venv
# Windows PowerShell:
./venv/Scripts/Activate.ps1
pip install -r requirements.txt

# Migraciones mínimas
python manage.py migrate

# Run
python manage.py runserver 0.0.0.0:8000
```
### Endpoint
- `POST /api/ordenes/pdf` -> recibe JSON y devuelve PDF.

Ejemplo de payload:
```json
{
  "fecha": "2025-11-01",
  "centro_costos": "CC-101",
  "ubicacion": "Planta 3 - Línea A",
  "tipo_mantenimiento": "Correctivo",
  "prioridad": "Urgente",
  "tarea": "Cambio de válvula",
  "observaciones": "Sin incidentes",
  "hora_inicio": "08:00",
  "hora_fin": "11:30",
  "legajos": [{"id":"7023","nombre":"F. Lagréade"}],
  "equipos": [{"codigo":"AB101RS","horas":"3","km_inicial":"1200","km_final":"1210"}],
  "materiales": [{"material":"Válvula 1/2","cant":1,"unidad":"un"}]
}
```

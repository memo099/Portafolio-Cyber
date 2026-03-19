# Fase 1 — Inventario de Tags

Registro de todos los tags NFC escaneados durante la fase de reconocimiento.
Todas las tarjetas son de propiedad personal.

---

## Metodología

Cada tag fue escaneado usando la funcion NFC > Read del Flipper Zero.
Se registró el tipo de chip, UID, tecnologia, ATQA, SAK y estado inicial.
Las fotos de evidencia se encuentran en la carpeta assets/.

---

## Registro de Tags

| # | Chip | UID | Tech | ATQA | SAK | Estado | Evidencia |
|---|------|-----|------|------|-----|--------|-----------|
| 1 | NTAG215 | 04:AA:F2:3F:C8:2A:81 | ISO 14443-3 (NFC-A) | 00:44 | 00 | Virgen | [foto](../assets/tag-01.jpg) |
| 2 | NTAG215 | 04:D1:5B:30:C9:2A:81 | ISO 14443-3 (NFC-A) | 00:44 | 00 | Virgen | [foto](../assets/tag-02.jpg) |
| 3 | NTAG215 | 04:5B:A1:3D:C8:2A:81 | ISO 14443-3 (NFC-A) | 00:44 | 00 | Virgen | [foto](../assets/tag-03.jpg) |

---

## Observaciones

- Todos los tags son del mismo fabricante: NXP Semiconductors (identificador 04)
- Los ultimos bytes del UID (2A:81) son identicos en los tres tags, patron comun en lotes del mismo proveedor
- Ninguno tiene proteccion de escritura activa
- Ninguno tiene datos NDEF inicializados (M1: Empty)
- El Flipper Zero los detecta correctamente como NTAG215 en todos los casos

---

## Herramienta utilizada

Flipper Zero — Firmware oficial
Ruta: NFC > Read > More

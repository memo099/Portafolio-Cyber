# NFC Security Research

Investigación práctica de seguridad en tecnología NFC mediante análisis de tags y lectores usando un Flipper Zero. Todas las pruebas fueron realizadas sobre dispositivos y tarjetas de propiedad personal en un entorno de laboratorio controlado.

---

## Objetivo

Este proyecto documenta una evaluación de seguridad estructurada sobre tecnología NFC — abarcando enumeración de tags, análisis de protocolos, identificación de vulnerabilidades, construcción de payloads y recomendaciones defensivas. El objetivo es comprender las superficies de ataque reales presentes en entornos cotidianos con NFC.

---

## Herramientas y Hardware

| Herramienta | Propósito |
|-------------|-----------|
| Flipper Zero | Lectura/escritura NFC, emulación de tags, detección de protocolos |
| NFC Tools (Android) | Inspección y verificación de payloads NDEF |
| nfcpy (Python) | Interacción automatizada con tags mediante scripts |
| 20x tarjetas NTAG215 | Tags objetivo del laboratorio (propiedad personal) |

---

## Estructura del Proyecto

```
nfc-security-research/
├── phase-1-recon/
│   └── tags-inventory.md          # Enumeración de tags e identificación de chips
├── phase-2-analysis/
│   └── vulnerability-findings.md  # Debilidades de protocolo y superficie de ataque
├── phase-3-payloads/
│   └── payload-demos.md           # Construcción y demostración de payloads NDEF
├── phase-4-mitigations/
│   └── recommendations.md         # Medidas defensivas y recomendaciones
└── assets/                        # Capturas de pantalla y material de apoyo
```

---

## Fases de Investigación

### Fase 1 — Reconocimiento
Enumeración de tags NFC en el entorno del laboratorio personal. Identificación de tipos de chip, UIDs, distribución de memoria y postura de seguridad inicial (bloqueado, escribible, NDEF inicializado).

### Fase 2 — Análisis de Vulnerabilidades
Evaluación de los tags identificados contra vectores de ataque conocidos:
- Clonación y suplantación de UID
- Acceso de escritura no autorizado (sin protección de escritura)
- Manipulación de NDEF (inyección de URI maliciosa, sustitución de payload)
- Mecanismos de autenticación débiles o ausentes

### Fase 3 — Demostración de Payloads
Construcción y despliegue de payloads NDEF sobre tarjetas NTAG215 de propiedad personal para demostrar escenarios de ataque reales:
- Payload de URI de phishing
- Simulación de captura de credenciales WiFi
- Redirección de aplicación mediante Android Application Record (AAR)
- Payload oculto (sin registro NDEF visible, datos en páginas reservadas)

### Fase 4 — Mitigaciones
Documentación de contramedidas defensivas:
- Tipos de chip recomendados para control de acceso (NTAG424 DNA, DESFire EV2+)
- Estrategias de bloqueo de escritura
- Detección de tags manipulados
- Opciones de blindaje NFC

---

## Aviso Legal

Toda la investigación contenida en este repositorio fue realizada exclusivamente sobre hardware y tarjetas de propiedad personal en un entorno de laboratorio privado. En ningún momento se accedió, clonó o modificó ningún sistema de terceros, infraestructura pública ni dispositivos ajenos. Este proyecto tiene fines exclusivamente educativos y de seguridad defensiva.

---

## Autor

Memo — Estudiante de Ingeniería en Ciberseguridad, competidor de CTF
Querétaro, México
GitHub Portfolio: https://github.com/memo099/Portafolio-Cyber

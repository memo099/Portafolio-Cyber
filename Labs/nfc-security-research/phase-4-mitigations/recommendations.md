# Fase 4 — Mitigaciones y Recomendaciones

Contramedidas defensivas basadas en los hallazgos de las fases anteriores.
El objetivo es documentar como mitigar las vulnerabilidades identificadas en
tags NFC de uso cotidiano.

---

## Contexto

Las vulnerabilidades documentadas en este proyecto no son exclusivas de los tags
utilizados en el laboratorio. Afectan a cualquier tag NFC sin configuracion de
seguridad, incluyendo los que se encuentran en carteles publicitarios, menus de
restaurantes, credenciales de acceso y productos comerciales.

---

## Mitigaciones por Vulnerabilidad

### VUL-01 — Ausencia de proteccion de escritura

**Mitigacion recomendada: Activar proteccion de escritura con contrasena**

El estandar NTAG215 soporta proteccion de escritura mediante contrasena de 32 bits.
Una vez activada, cualquier intento de escritura requiere autenticacion previa.

Implementacion en NFC Tools:
```
Otro → Seguridad → Proteger con contrasena
```

Limitaciones:
- La contrasena tiene solo 32 bits, lo que la hace vulnerable a fuerza bruta
- No protege contra lectura del contenido
- Para casos de uso criticos se recomienda migrar a chips mas seguros

**Alternativa: Usar chips con mejor seguridad**

Para aplicaciones que requieren mayor seguridad se recomienda:

| Chip | Caracteristicas de seguridad |
|------|------------------------------|
| NTAG424 DNA | Autenticacion criptografica AES-128, firma dinamica |
| MIFARE DESFire EV2 | Cifrado AES, autenticacion mutua, diversificacion de claves |
| MIFARE DESFire EV3 | Todo lo anterior mas proteccion contra ataques de repeticion |

---

### VUL-02 — Ausencia de autenticacion de lectura

**Mitigacion recomendada: No almacenar datos sensibles en tags NFC estandar**

Los tags NTAG215 no ofrecen cifrado de contenido. Cualquier dato almacenado
es legible por cualquier dispositivo NFC. Por lo tanto:

- No almacenar contrasenas, tokens de acceso ni datos personales en tags NTAG
- Si se requiere confidencialidad usar chips con cifrado nativo como DESFire EV2
- Para control de acceso usar sistemas que validen en el backend, no en el tag

**Mitigacion complementaria: Proteccion fisica**

- Usar fundas con blindaje NFC (materiales RFID-blocking) para tarjetas sensibles
- Limitar la exposicion del tag a distancias de lectura innecesarias

---

### VUL-03 — Firma NXP invalida

**Mitigacion recomendada: Verificar autenticidad del tag antes de confiar en su contenido**

La firma NXP permite verificar que un tag es genuino y no fue clonado. Para
sistemas que dependen de tags NFC como mecanismo de autenticacion:

- Implementar verificacion de firma en el backend antes de procesar el contenido
- Rechazar tags con firma invalida en aplicaciones criticas
- Considerar el uso de NTAG424 DNA que incluye firmas dinamicas imposibles de clonar

---

## Recomendaciones Generales

**Para usuarios finales:**
- Instalar una aplicacion NFC de analisis (como NFC Tools) para inspeccionar
  tags desconocidos antes de interactuar con ellos
- Desactivar NFC cuando no se este usando activamente
- No conectarse automaticamente a redes WiFi sugeridas por tags NFC en lugares publicos
- Ser escéptico ante tags NFC en lugares poco convencionales

**Para desarrolladores e implementadores:**
- Nunca usar NTAG215 o chips similares para control de acceso critico
- Implementar validacion en el backend, no confiar unicamente en el contenido del tag
- Usar chips con autenticacion criptografica para aplicaciones de seguridad
- Registrar y auditar todos los accesos a sistemas basados en NFC

**Para organizaciones:**
- Realizar auditorias periodicas de tags NFC desplegados en instalaciones
- Implementar deteccion de tags no autorizados en areas criticas
- Capacitar a usuarios sobre los riesgos de interactuar con tags NFC desconocidos

---

## Comparativa de Chips NFC por Nivel de Seguridad

| Chip | Proteccion escritura | Cifrado | Firma de autenticidad | Uso recomendado |
|------|---------------------|---------|----------------------|-----------------|
| NTAG215 | Contrasena 32 bits | No | Si (invalida por defecto) | Marketing, demos, lab |
| NTAG424 DNA | Si | AES-128 | Si (dinamica) | Autenticacion, anti-falsificacion |
| MIFARE Classic 1K | Clave 48 bits (vulnerable) | Propietario (roto) | No | No recomendado para seguridad |
| MIFARE DESFire EV2 | Si | AES-128 | Si | Control de acceso empresarial |
| MIFARE DESFire EV3 | Si | AES-128 | Si | Aplicaciones criticas |

---

## Conclusion

Las vulnerabilidades documentadas en este proyecto son inherentes al diseno del
estandar NTAG215 y no pueden ser completamente eliminadas en este tipo de chip.
La mitigacion mas efectiva es seleccionar el chip adecuado segun el nivel de
seguridad requerido por la aplicacion, y nunca asumir que un tag NFC es seguro
sin verificar sus capacidades criptograficas.

# Fase 3 — Demostracion de Payloads

Construccion y despliegue de payloads NDEF sobre tarjetas NTAG215 de propiedad personal.
El objetivo es demostrar escenarios de ataque reales que son posibles debido a las
vulnerabilidades identificadas en la Fase 2.

Todas las pruebas fueron realizadas en un entorno de laboratorio controlado sobre
tarjetas y dispositivos de propiedad personal.

---

## Herramientas utilizadas

- NFC Tools (Wakdev, Android) — escritura de payloads NDEF
- Flipper Zero — verificacion de contenido escrito
- 3x tarjetas NTAG215 (propiedad personal)

---

## PAYLOAD-01 — URL de portafolio

**Tag utilizado:** Tag #1 (UID: 04:AA:F2:3F:C8:2A:81)
**Tipo de record NDEF:** URI
**Tamano:** 23 bytes

**Descripcion:**
Se escribio una URL apuntando al perfil de GitHub del investigador. Al acercar cualquier
dispositivo Android al tag, el navegador se abre automaticamente sin ninguna interaccion
del usuario.

**Contenido escrito:**
```
https://github.com/memo099
```

**Resultado:**
El tag activo redirige automaticamente al navegador del dispositivo que lo lee.
Ningun tipo de autenticacion fue requerida para escribir ni para leer el contenido.

**Relevancia para seguridad:**
Un atacante podria sustituir esta URL por cualquier sitio de phishing o malware.
El usuario final no tendria forma de distinguir un tag legitimo de uno malicioso
sin una herramienta de analisis NFC.

**Evidencia:**
- payload-01-configurado.jpg — URL configurada en NFC Tools
- payload-01-escritura.jpg — Escritura exitosa
- payload-01-flipper.jpg — Flipper confirmando M1-R1: URL
- payload-01-activo.jpg — Navegador abriendo la URL automaticamente

---

## PAYLOAD-02 — URL de repositorio (simulacion de phishing)

**Tag utilizado:** Tag #2 (UID: 04:D1:5B:30:C9:2A:81)
**Tipo de record NDEF:** URI
**Tamano:** 45 bytes

**Descripcion:**
Se escribio una URL apuntando directamente al repositorio de esta investigacion.
Este payload simula el escenario donde un atacante coloca un tag NFC en un lugar
publico con una URL que aparenta ser legitima pero redirige a un sitio malicioso.

**Contenido escrito:**
```
https://github.com/memo099/nfc-security-research
```

**Resultado:**
El navegador se abrio automaticamente al acercar el dispositivo al tag.
La URL mostrada en la barra del navegador podria facilmente pasar desapercibida
para un usuario sin conocimientos tecnicos.

**Relevancia para seguridad:**
Este vector de ataque es especialmente efectivo en entornos publicos como
aeropuertos, centros comerciales o transporte publico, donde los usuarios
podrian confiar en tags NFC aparentemente oficiales.

**Evidencia:**
- payload-02-tag-info.jpg — Informacion del tag #2
- payload-02-configurado.jpg — URL del repositorio configurada
- payload-02-escritura.jpg — Escritura exitosa
- payload-02-activo.jpg — Navegador abriendo la URL automaticamente

---

## PAYLOAD-03 — Credenciales WiFi

**Tag utilizado:** Tag #3 (UID: 04:5B:A1:3D:C8:2A:81)
**Tipo de record NDEF:** WiFi
**Autenticacion:** WPA/WPA2 Personal

**Descripcion:**
Se escribieron credenciales de una red WiFi de laboratorio en el tag. Al acercar
un dispositivo Android al tag, el sistema operativo muestra automaticamente un
dialogo solicitando confirmacion para conectarse a la red, sin necesidad de
ingresar la contrasena manualmente.

**Contenido escrito:**
```
SSID: [redacted - red de laboratorio]
AUTH: WPA/WPA2 Personal
Contrasena: [redacted]
```

**Resultado:**
El dispositivo Android mostro automaticamente el dialogo "Conectar a la red"
con el nombre de la red pre-cargado. El usuario solo necesita presionar "Conectar".

**Relevancia para seguridad:**
Un atacante podria desplegar tags WiFi en lugares publicos con credenciales de
una red controlada por el atacante (Evil Twin). El usuario creeria estar
conectandose a una red legitima (por ejemplo, "AeropuertoWiFi") cuando en
realidad se conecta a una red maliciosa que intercepta su trafico.

**Evidencia:**
- payload-03-tag-info.jpg — Informacion del tag #3
- payload-03-configurado.jpg — Formulario WiFi configurado (datos redactados)
- payload-03-escritura.jpg — Escritura exitosa
- payload-03-flipper.jpg — Flipper confirmando M1-R1: WiFi con AUTH WPA/WPA2
- payload-03-activo.jpg — Dialogo automatico de conexion a red

---

## Resumen de Payloads

| ID | Tipo | Tag | Tamano | Resultado |
|----|------|-----|--------|-----------|
| PAYLOAD-01 | URI — URL de portafolio | Tag #1 | 23 bytes | Navegador abre URL automaticamente |
| PAYLOAD-02 | URI — Simulacion phishing | Tag #2 | 45 bytes | Navegador abre URL automaticamente |
| PAYLOAD-03 | WiFi — Credenciales de red | Tag #3 | N/A | Dialogo de conexion automatico |

---

## Conclusion

Los tres payloads fueron escritos y ejecutados exitosamente sin ningun tipo de
autenticacion o restriccion. Esto confirma las vulnerabilidades documentadas en
la Fase 2 y demuestra que cualquier dispositivo NFC puede modificar y explotar
estos tags de forma trivial.

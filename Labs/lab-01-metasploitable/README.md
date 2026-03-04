/*
# Lab 01 — Intrusion Analysis (Metasploitable2)

## Contexto

Este laboratorio consiste en un ejercicio de análisis de intrusión realizado en un entorno controlado utilizando una máquina vulnerable (Metasploitable2) y una máquina atacante (Parrot OS). Ambas máquinas se encontraban en una red virtual aislada diseñada específicamente para pruebas de seguridad.

El objetivo del laboratorio fue simular el proceso que seguiría un atacante al identificar servicios expuestos, investigar vulnerabilidades conocidas y explotar una debilidad del sistema para evaluar el impacto de una intrusión.

Este ejercicio fue realizado únicamente con fines educativos.

---

# Objetivo

Identificar servicios expuestos en una máquina vulnerable, analizar posibles vectores de ataque, explotar una vulnerabilidad conocida y evaluar el impacto que tendría un compromiso del sistema.

---

# Entorno del laboratorio

Componente: Máquina atacante  
Descripción: Parrot OS

Componente: Máquina objetivo  
Descripción: Metasploitable2

Componente: Red  
Descripción: Red virtual aislada

IP atacante: 192.168.124.35  
IP objetivo: 192.168.124.136

---

# Metodología

El laboratorio se desarrolló siguiendo las siguientes fases:

- Reconocimiento de red
- Escaneo de puertos
- Enumeración de servicios
- Investigación de vulnerabilidades
- Explotación
- Obtención de acceso
- Verificación de impacto
- Análisis post-intrusión
- Evaluación de impacto de seguridad

---

# 1. Reconocimiento de red

En la primera fase del laboratorio se identificaron los dispositivos disponibles dentro de la red del entorno virtual.

Se verificó la conectividad entre la máquina atacante (Parrot OS) y la máquina objetivo (Metasploitable2) para confirmar que ambas podían comunicarse correctamente dentro de la red.

Este paso es importante ya que permite confirmar que el objetivo es accesible antes de iniciar el análisis de servicios expuestos.

---

# 2. Escaneo de puertos

Una vez identificada la máquina objetivo se realizó un escaneo de puertos utilizando Nmap con el objetivo de identificar qué servicios estaban disponibles en el sistema.

Comando utilizado:

nmap -sV 192.168.124.136

Este escaneo permitió identificar múltiples puertos abiertos y servicios activos en la máquina vulnerable.

Entre los servicios detectados se encontraban:

FTP (21)  
SSH (22)  
Telnet  
HTTP  
MySQL  
Samba  
PostgreSQL  
VNC  
IRC  
Tomcat

La presencia de múltiples servicios expuestos indica una superficie de ataque amplia, lo que aumenta el riesgo de compromiso del sistema.

---

# 3. Enumeración de servicios

Después del escaneo de puertos se analizaron las versiones de los servicios detectados.

Uno de los servicios identificados fue:

vsftpd 2.3.4

Esta versión del servidor FTP es conocida por contener un backdoor introducido en una versión comprometida del software en 2011.

Este hallazgo fue clave para identificar un posible vector de ataque.

---

# 4. Investigación de vulnerabilidades

Para confirmar si existían exploits disponibles para esta versión del servicio FTP se utilizó Metasploit Framework.

Dentro de Metasploit se ejecutó el siguiente comando:

search vsftpd

El resultado mostró varios módulos relacionados con el servicio FTP, incluyendo el módulo:

exploit/unix/ftp/vsftpd_234_backdoor

Este módulo explota la vulnerabilidad presente en la versión vulnerable del servidor FTP.

---

# 5. Configuración del exploit

Se seleccionó el módulo de explotación dentro de Metasploit:

use exploit/unix/ftp/vsftpd_234_backdoor

Posteriormente se configuró la dirección IP de la máquina objetivo:

set RHOSTS 192.168.124.136

El puerto utilizado por el servicio FTP es el puerto 21, que ya se encontraba configurado dentro del módulo.

---

# 6. Ejecución del exploit

Una vez configurado el exploit se ejecutó el módulo dentro de Metasploit.

run

El exploit aprovechó el backdoor presente en el servicio FTP vulnerable y permitió abrir una sesión remota en la máquina objetivo.

Esto proporcionó acceso al sistema comprometido.

---

# 7. Obtención de acceso al sistema

Después de ejecutar el exploit se obtuvo acceso a una shell dentro de la máquina Metasploitable.

Para confirmar el nivel de privilegio se ejecutó el siguiente comando:

whoami

Resultado:

root

Esto confirmó que se había obtenido acceso con privilegios administrativos, lo que representa el control total del sistema.

---

# 8. Verificación de impacto

Para demostrar el impacto del compromiso se ejecutaron comandos dentro del sistema comprometido.

Por ejemplo, se creó un nuevo directorio dentro del sistema:

mkdir Hola

Posteriormente se verificó su existencia:

ls

La creación del directorio confirmó que el atacante tenía capacidad para modificar el sistema objetivo.

Esto representa una pérdida de integridad del sistema.

---

# 9. Análisis post-intrusión

Una vez obtenido acceso root se revisaron archivos sensibles del sistema para evaluar el alcance del compromiso.

Por ejemplo:

cat /etc/passwd

y

cat /etc/shadow

Estos archivos contienen información sobre las cuentas del sistema y los hashes de contraseñas.

El acceso a estos archivos demuestra que el atacante posee privilegios suficientes para comprometer completamente el sistema.

---

# 10. Impacto de seguridad

El compromiso del sistema permitió:

- Acceso completo al sistema
- Lectura de archivos sensibles
- Modificación de archivos del sistema
- Creación de nuevos archivos o directorios
- Posible instalación de software malicioso
- Uso del sistema comprometido como punto de ataque hacia otros sistemas

Esto representa una pérdida total de confidencialidad, integridad y disponibilidad.

---

# Conclusión

Este laboratorio demostró cómo una vulnerabilidad conocida en un servicio expuesto puede permitir el compromiso total de un sistema.

A través de las fases de reconocimiento, enumeración, explotación y análisis post-intrusión se pudo observar el impacto real que una mala configuración de seguridad puede tener en un sistema.

Este tipo de ejercicios permite comprender la importancia de mantener los sistemas actualizados, minimizar la superficie de ataque y aplicar buenas prácticas de seguridad en los servicios expuestos a la red.
*/


Network Lab Topology

                Virtual Lab Network
        ------------------------------------

        Attacker Machine
        Parrot OS
        IP: 192.168.124.35
               |
               |   (Network Scan / Exploitation)
               |
               v
        -------------------------
        Metasploitable2 Target
        IP: 192.168.124.136
        -------------------------

        Exposed Services Discovered

        - FTP (vsftpd 2.3.4)
        - SSH
        - Telnet
        - HTTP
        - MySQL
        - Samba
        - PostgreSQL
        - VNC
        - IRC
        - Tomcat

        Exploited Service

        vsftpd 2.3.4 Backdoor
        exploit/unix/ftp/vsftpd_234_backdoor

        Result

        Root Shell Obtained
        Full System Compromise

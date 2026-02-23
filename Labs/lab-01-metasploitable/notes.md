## Preparación del entorno
- Host: Fedora Linux
- VM atacante: Parrot Security
- VM objetivo: Metasploitable2
- Red: NAT (GNOME Boxes)

## Observaciones iniciales
## Paso 2 — Escaneo de puertos y servicios
**Acción:** Se realizó un escaneo de puertos TCP con detección de versiones sobre el sistema objetivo utilizando Nmap (-sV).  
**Resultado:** Se identificaron múltiples servicios activos, incluyendo servicios de red, administración remota, bases de datos y aplicaciones web.  
**Análisis:** El sistema presenta una superficie de ataque extremadamente amplia, con numerosos servicios expuestos y versiones antiguas, lo que incrementa significativamente el riesgo de compromiso.

## Servicios relevantes identificados
Durante el escaneo se detectaron servicios que destacan por su criticidad:

- FTP (vsftpd 2.3.4)
- SSH (OpenSSH 4.7p1)
- Telnet
- HTTP (Apache 2.2.8)
- Samba (NetBIOS / SMB)
- MySQL y PostgreSQL
- VNC
- Tomcat (8180)
- Servicios RPC y NFS
- Shell remota expuesta (bindshell en el puerto 1524)

## Observaciones preliminares
- Se observan múltiples servicios obsoletos conocidos por presentar vulnerabilidades públicas.
- Existen servicios de acceso remoto sin cifrado (Telnet, FTP).
- La presencia de una shell expuesta sugiere una configuración deliberadamente insegura.
- El número de servicios activos indica ausencia total de hardening.

## Próximo paso
Priorizar servicios para enumeración detallada y selección de un vector de ataque inicial.


## Selección del vector de ataque inicial
Tras analizar los servicios expuestos, se prioriza el servicio FTP (vsftpd 2.3.4)
como vector de ataque inicial debido a:

- Uso de un protocolo sin cifrado.
- Versión conocida por vulnerabilidades públicas.
- Alta probabilidad de compromiso remoto.
- Menor necesidad de credenciales válidas en comparación con SSH.

El servicio SSH se considera un posible vector secundario para persistencia
o escalamiento de privilegios una vez obtenido acceso inicial.


## Paso 4 — Confirmación de versión del servicio FTP
**Acción:** Se estableció una conexión directa al puerto 21 utilizando Netcat para obtener el banner del servicio.  
**Resultado:** El servidor respondió con el banner `vsFTPd 2.3.4`, confirmando la versión del servicio FTP expuesto.  
**Análisis:** La divulgación explícita de la versión del servicio permite identificar vulnerabilidades conocidas asociadas a esta implementación. El cierre posterior de la conexión corresponde a un timeout por inactividad y no afecta la validez de la enumeración.

## Paso 5 — Confirmación de vulnerabilidad (vsftpd 2.3.4)
**Descripción:** El servicio FTP identificado corresponde a la versión vsftpd 2.3.4, una implementación históricamente comprometida que contiene un backdoor conocido.  
**Impacto:** Esta vulnerabilidad permite la ejecución remota de comandos y potencialmente el acceso no autorizado al sistema objetivo.  
**Riesgo:** Crítico. La explotación de este servicio podría resultar en el compromiso total del sistema sin necesidad de credenciales válidas.  
**Conclusión:** El servicio FTP representa un vector de ataque prioritario y viable para obtener acceso inicial al sistema.


## Paso 6A — Selección del exploit
Tras la investigación de vulnerabilidades para el servicio FTP, se identificaron
múltiples módulos relacionados con vsftpd. Se seleccionó el módulo
`exploit/unix/ftp/vsftpd_234_backdoor` debido a:

- Coincidencia exacta con la versión detectada (vsftpd 2.3.4).
- Capacidad de ejecución remota de comandos.
- Ausencia de requerimiento de credenciales.
- Clasificación de riesgo alta (Rank: excellent).

Este exploit se considera adecuado como vector de acceso inicial al sistema.

## Paso 6B — Validación del exploit seleccionado
**Acción:** Se revisó la información detallada del módulo `exploit/unix/ftp/vsftpd_234_backdoor` mediante el comando `info` en Metasploit.  
**Resultado:** El módulo describe un backdoor malicioso insertado directamente en la versión vsftpd 2.3.4, permitiendo ejecución remota de comandos sin autenticación.  
**Análisis:** La descripción del exploit confirma que el servicio FTP identificado en el sistema objetivo corresponde a una versión comprometida, validando la viabilidad del ataque como vector de acceso inicial.

## Concepto — Bind shell
Una bind shell ocurre cuando el sistema objetivo abre un puerto de red que queda
escuchando conexiones entrantes y proporciona acceso directo a una shell.
En este escenario, el exploit `vsftpd_234_backdoor` activa un backdoor que
provoca la apertura de un puerto adicional en el sistema comprometido,
permitiendo al atacante conectarse y ejecutar comandos de forma remota.

## Paso 6D — Verificación de compromiso del sistema
**Acción:** Se ejecutaron comandos remotos desde la shell obtenida para interactuar con el sistema de archivos del usuario `msfadmin`.  
**Resultado:** Se creó un directorio (`Hola`) en el sistema objetivo y se confirmó su existencia mediante la ejecución de comandos remotos.  
**Impacto:** La creación y visualización de archivos/directorios confirma el control efectivo del sistema comprometido.  
**Conclusión:** El acceso obtenido permite la ejecución arbitraria de comandos, validando el compromiso inicial del sistema.

## Paso 7B — Confirmación de privilegios elevados
**Acción:** Se verificaron los privilegios del usuario tras el escalamiento.  
**Resultado:** El usuario actual corresponde a `root` (UID 0).  
**Impacto:** Acceso con privilegios máximos, permitiendo control total del sistema.  
**Conclusión:** El escalamiento de privilegios fue exitoso debido a una configuración insegura de sudo.

## Resumen Ejecutivo
Durante este laboratorio de pruebas se identificó y explotó un servicio FTP vulnerable
(vsftpd 2.3.4) que permitió obtener acceso remoto no autorizado al sistema objetivo.
La explotación condujo a la ejecución de comandos remotos, verificación de impacto
mediante modificación del sistema y posterior escalamiento de privilegios hasta
obtener control total (root).

El compromiso fue posible debido a la exposición de múltiples servicios inseguros,
uso de software obsoleto y configuraciones deficientes de control de privilegios.
Una vez obtenido acceso con privilegios elevados, se confirmó la pérdida total de
confidencialidad, integridad y disponibilidad del sistema.

Este escenario demuestra cómo una única vulnerabilidad crítica puede derivar en
el compromiso completo de un activo si no existen controles de seguridad adecuados.

## Área de Mejora y Mitigación
El compromiso del sistema pudo haberse evitado mediante la aplicación de controles
básicos de seguridad y buenas prácticas de hardening. A continuación se describen
las principales medidas de mitigación:

### Gestión de Servicios
- Eliminar servicios innecesarios expuestos a la red, especialmente protocolos
  inseguros como FTP y Telnet.
- Sustituir servicios legacy por alternativas seguras (por ejemplo, SFTP en lugar de FTP).
- Limitar el acceso a servicios críticos mediante firewalls y listas de control de acceso.

### Actualización y Parches
- Mantener todos los servicios actualizados y evitar el uso de versiones obsoletas
  conocidas por contener vulnerabilidades críticas.
- Implementar un proceso de gestión de parches periódico.

### Control de Privilegios
- Aplicar el principio de mínimo privilegio para todos los usuarios.
- Evitar configuraciones de sudo sin autenticación.
- Revisar periódicamente permisos y roles de los usuarios del sistema.

### Gestión de Credenciales
- No almacenar credenciales en texto plano dentro de archivos de configuración.
- Utilizar credenciales fuertes y únicas por servicio.
- Implementar mecanismos de rotación de contraseñas.

### Monitoreo y Detección
- Habilitar registros de auditoría y monitoreo de accesos.
- Detectar comportamientos anómalos como apertura de puertos inesperados o ejecución
  de comandos no autorizados.

La aplicación de estas medidas habría reducido significativamente la superficie de
ataque y mitigado el impacto de una posible explotación.

> Este laboratorio fue realizado en un entorno controlado con fines educativos,
> demostrando la importancia de la prevención, detección y respuesta ante incidentes
> de seguridad.

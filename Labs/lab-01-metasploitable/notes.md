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


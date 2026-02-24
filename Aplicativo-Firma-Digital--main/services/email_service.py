"""
email_service.py

Módulo encargado del envío de documentos firmados por correo electrónico.

Este servicio:
- Carga variables de entorno desde el archivo .env
- Autentica contra el servidor SMTP de Gmail
- Adjunta el PDF firmado y la foto capturada
- Envía el correo al destinatario indicado

Autor: Equipo Aplicativo Firma Digital
"""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from pathlib import Path


# ==========================================================
# CARGA DE VARIABLES DE ENTORNO
# ==========================================================

# Se construye la ruta absoluta hacia el archivo .env
# ubicado en la raíz del proyecto.
env_path = Path(__file__).resolve().parent.parent / ".env"

# Carga las variables definidas en el archivo .env
load_dotenv(dotenv_path=env_path)

# Obtiene las credenciales desde las variables de entorno
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


# ==========================================================
# FUNCIÓN PRINCIPAL DE ENVÍO
# ==========================================================

def enviar_documento(destino: str, ruta_pdf: str, ruta_foto: str) -> None:
    """
    Envía por correo electrónico el documento firmado y la foto de evidencia.

    Parámetros:
        destino (str): Correo electrónico del destinatario.
        ruta_pdf (str): Ruta del archivo PDF firmado.
        ruta_foto (str): Ruta de la imagen capturada como evidencia.

    Excepciones:
        ValueError: Si las variables de entorno no están configuradas.
        Exception: Si ocurre un error durante el envío SMTP.
    """

    # Validación de credenciales
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("Faltan variables de entorno del correo")

    # Creación del mensaje
    msg = EmailMessage()
    msg["Subject"] = "Documento firmado digitalmente"
    msg["From"] = EMAIL_USER
    msg["To"] = destino
    msg.set_content(
        "Adjunto encontrarás el documento firmado electrónicamente "
        "junto con la evidencia fotográfica del firmante."
    )

    # ==========================================================
    # ADJUNTAR PDF FIRMADO
    # ==========================================================
    with open(ruta_pdf, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(ruta_pdf),
        )

    # ==========================================================
    # ADJUNTAR IMAGEN DE EVIDENCIA
    # ==========================================================
    with open(ruta_foto, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="jpeg",
            filename=os.path.basename(ruta_foto),
        )

    # ==========================================================
    # CONEXIÓN Y ENVÍO SMTP
    # ==========================================================
    # Se utiliza SMTP_SSL en el puerto 465 (conexión segura)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print("Correo enviado correctamente ✅")

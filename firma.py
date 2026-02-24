import os
# os.system("cls")  # limpiar consola Windows

# ==========================================================
# CONFIGURACIÓN DE CARPETAS PRINCIPALES
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DOCS_DIR = os.path.join(BASE_DIR, "docs_salida")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==========================================================
# LIBRERÍAS
# ==========================================================

# Librería para abrir explorador de archivos
import tkinter as tk
from tkinter import filedialog

# Librerías para copiar archivos y generar hash
import shutil
import hashlib

# Librería para manejar cámara y procesamiento de imagen
import cv2

# 🔥 Librería biométrica
from deepface import DeepFace

# Librerías para leer y escribir PDFs
from pypdf import PdfReader, PdfWriter, Transformation

# Librería para generar contenido dentro del PDF
from reportlab.pdfgen import canvas

# Librería para obtener fecha y hora actual
from datetime import datetime

# Librerías para formato y diseño del PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# Servicio para enviar documentos por correo
from services.email_service import enviar_documento


# ==========================================================
# VALIDACIÓN BIOMÉTRICA (INTEGRADA EN EL CÓDIGO MADRE)
# ==========================================================

def validar_identidad(ruta_imagen_documento, ruta_foto):
    """
    Compara la imagen del documento con la selfie usando DeepFace.
    Si la distancia es menor o igual al threshold → identidad validada.
    """

    try:
        resultado = DeepFace.verify(
            img1_path=ruta_imagen_documento,
            img2_path=ruta_foto,
            model_name="ArcFace",
            distance_metric="cosine",
            detector_backend="retinaface",
            enforce_detection=True
        )

        distancia = resultado["distance"]
        print("Distancia facial:", distancia)

        # 🔐 Threshold empresarial (ajústalo según tus pruebas)
        THRESHOLD = 0.90

        if distancia <= THRESHOLD:
            print("✅ Identidad validada")
            return True
        else:
            print("❌ Identidad NO coincide")
            return False

    except Exception as e:
        print("Error en validación biométrica:", e)
        return False


# ==========================================================
# SELECCIÓN DE PDF
# ==========================================================

def seleccionar_pdf_desde_explorador():
    """
    Abre explorador y permite seleccionar un PDF.
    """

    root = tk.Tk()
    root.withdraw()

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccione un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    return ruta_archivo if ruta_archivo else None


# ==========================================================
# GENERACIÓN DE HASH PARA EVITAR DUPLICADOS
# ==========================================================

def generar_hash_archivo(ruta_archivo):
    """
    Genera hash SHA256 del archivo.
    """

    hash_sha256 = hashlib.sha256()

    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)

    return hash_sha256.hexdigest()


def construir_nombre_por_hash(hash_archivo, extension):
    """
    Construye nombre usando hash.
    """

    return f"{hash_archivo}{extension}"


# ==========================================================
# FUNCIÓN PARA TOMAR FOTO (SELFIE)
# ==========================================================

def tomar_foto():
    """
    Abre cámara y guarda imagen como foto_capturada.jpg
    """

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo abrir la camara")
        exit()

    print("Presiona 's' para capturar la foto")

    ruta_imagen = os.path.join(UPLOAD_DIR, "foto_capturada.jpg")

    while True:
        ret, frame = camara.read()
        if not ret:
            break

        cv2.imshow("Camara", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            cv2.imwrite(ruta_imagen, frame)
            print("Foto guardada")
            break

        if key == ord('q'):
            ruta_imagen = None
            break

    camara.release()
    cv2.destroyAllWindows()

    return ruta_imagen


# ==========================================================
# SUBIDA Y VALIDACIÓN DE PDF
# ==========================================================

def subir_pdf(ruta_origen):
    """
    Valida y copia PDF a uploads usando hash.
    """

    if not os.path.isfile(ruta_origen):
        raise FileNotFoundError("El archivo no existe")

    if not ruta_origen.lower().endswith(".pdf"):
        raise ValueError("Solo se permiten archivos PDF")

    hash_archivo = generar_hash_archivo(ruta_origen)
    extension = os.path.splitext(ruta_origen)[1]
    nombre_hash = construir_nombre_por_hash(hash_archivo, extension)

    ruta_destino = os.path.join(UPLOAD_DIR, nombre_hash)

    if os.path.exists(ruta_destino):
        raise ValueError("⚠️ Este documento ya existe")

    shutil.copy2(ruta_origen, ruta_destino)

    return ruta_destino


def seleccionar_y_subir_pdf():
    """
    Permite seleccionar y subir PDF.
    """

    while True:
        ruta = seleccionar_pdf_desde_explorador()

        if not ruta:
            print("⚠️ Selección cancelada")
            return None

        try:
            destino = subir_pdf(ruta)
            print("✅ PDF subido correctamente")
            return destino

        except ValueError as e:
            print("❌", e)


# ==========================================================
# DATOS DEL FIRMANTE
# ==========================================================

def ingresar_datos_firmante():
    """
    Solicita datos por consola.
    """

    try:
        nombre = input("Ingrese su nombre: ")
        documento = int(input("Ingrese su documento: "))
        edad = int(input("Ingrese su edad: "))
        cargo = input("Ingrese su cargo: ")

    except Exception as e:
        print("Error en los datos:", e)
        return ingresar_datos_firmante()

    return nombre, documento, edad, cargo


def obtener_tiempo():
    """
    Retorna fecha actual.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ==========================================================
# CREACIÓN DEL PDF DE FIRMA
# ==========================================================

def crear_pdf_texto(ruta, nombre, cargo, fecha, edad, documento, ruta_imagen):
    """
    Genera hoja de firma electrónica.
    """

    c = canvas.Canvas(ruta, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 26)
    c.drawString(80, height - 80, "Firmas Electrónicas")

    # Línea decorativa
    c.setFillColor(colors.blue)
    c.rect(50, height - 120, 10, 80, fill=1)
    c.setFillColor(colors.black)

    c.setFont("Helvetica", 12)
    c.drawString(80, height - 150, "Firmado electrónicamente por:")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, height - 170, nombre)

    c.setFont("Helvetica", 11)
    c.drawString(80, height - 200, f"Documento: {documento}")
    c.drawString(80, height - 220, f"Fecha: {fecha}")

    # Agregar foto capturada al PDF
    if ruta_imagen:
        c.drawImage(
            ruta_imagen,
            80,
            520,
            width=120,
            height=90
        )

    c.save()


# ==========================================================
# ===================== FLUJO PRINCIPAL =====================
# ==========================================================

print("Suba su Documento PDF a firmar")

ruta_doc_uploads = seleccionar_y_subir_pdf()

nombre, documento, edad, cargo = ingresar_datos_firmante()
fecha = obtener_tiempo()

# 📷 Tomar foto (SELFIE)
ruta_foto = tomar_foto()

if not ruta_foto:
    print("Proceso cancelado")
    exit()


# ==========================================================
# VALIDACIÓN BIOMÉTRICA INTEGRADA
# ==========================================================

print("Seleccione la imagen del documento para validar identidad")

root = tk.Tk()
root.withdraw()

ruta_imagen_documento = filedialog.askopenfilename(
    title="Seleccione imagen del documento",
    filetypes=[("Imagenes", "*.jpg *.jpeg *.png")]
)

if not ruta_imagen_documento:
    print("No se seleccionó imagen del documento")
    exit()

# Aquí se ejecuta la validación biométrica
if not validar_identidad(ruta_imagen_documento, ruta_foto):
    print("Validación fallida. No se firma.")
    exit()

print("✅ Validación exitosa. Continuando firma...")


# ==========================================================
# GENERAR PDF TEMPORAL
# ==========================================================

ruta_temp = os.path.join(UPLOAD_DIR, "temporal2.pdf")
crear_pdf_texto(ruta_temp, nombre, cargo, fecha, edad, documento, ruta_foto)


# ==========================================================
# UNIR PDF ORIGINAL + HOJA DE FIRMA
# ==========================================================

lector_pdf = PdfReader(ruta_doc_uploads)
lector_datos_firmante = PdfReader(ruta_temp)

escritor_pdf = PdfWriter()

# Copiar páginas originales
for pagina in lector_pdf.pages:
    escritor_pdf.add_page(pagina)

# Agregar hoja de firma
escritor_pdf.add_page(lector_datos_firmante.pages[0])

nombre_salida = os.path.join(DOCS_DIR, "pdf_firmado.pdf")

with open(nombre_salida, "wb") as salida:
    escritor_pdf.write(salida)

print("PDF Firmado Exitosamente")


# ==========================================================
# ENVÍO POR CORREO
# ==========================================================

try:
    correo_destino = input("Ingrese el correo al cual enviar el documento firmado: ")

    enviar_documento(
        correo_destino,
        nombre_salida,
        ruta_foto
    )

except Exception as e:
    print("Error al enviar el correo:", e)


print("Proceso Finalizado")
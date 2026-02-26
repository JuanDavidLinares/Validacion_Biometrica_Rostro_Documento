import os
# os.system("cls")

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

import tkinter as tk
from tkinter import filedialog
import shutil
import hashlib
import cv2
import pytesseract
import re
from deepface import DeepFace
from datetime import datetime

# RUTA TESSERACT (WINDOWS)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ==========================================================
# VALIDACIÓN BIOMÉTRICA
# ==========================================================

def validar_identidad(ruta_imagen_documento, ruta_foto):

    print("Entrando a validación biométrica...")

    try:
        resultado = DeepFace.verify(
            img1_path=ruta_imagen_documento,
            img2_path=ruta_foto,
            model_name="ArcFace",
            distance_metric="cosine",
            detector_backend="retinaface",
            enforce_detection=True
        )

        print("Verified:", resultado.get("verified"))
        print("Distance:", resultado.get("distance"))

        distancia = resultado["distance"]
        THRESHOLD = 0.65
        print("Threshold:", THRESHOLD)

        if distancia <= THRESHOLD:
            print("✅ VALIDACIÓN FACIAL: APROBADA")
            return True
        else:
            print("VALIDACIÓN FACIAL: RECHAZADA")
            return False

    except Exception as e:
        print("ERROR en validación biométrica:", e)
        return False


# ==========================================================
# EXTRAER NÚMERO DESDE IMAGEN (OCR)
# ==========================================================

def extraer_numero_desde_imagen(ruta_imagen):

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return None

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gris)

    numeros = re.findall(r"\d[\d\.]{6,20}\d", texto)

    if not numeros:
        return None

    return max(numeros, key=len)



# ==========================================================
# HASH
# ==========================================================

def generar_hash_archivo(ruta_archivo):

    hash_sha256 = hashlib.sha256()

    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)

    return hash_sha256.hexdigest()


def construir_nombre_por_hash(hash_archivo, extension):
    return f"{hash_archivo}{extension}"


# ==========================================================
# TOMAR FOTO
# ==========================================================

def tomar_foto():

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo abrir la camara")
        return None

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
# DATOS DEL FIRMANTE
# ==========================================================

def ingresar_datos_firmante():

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
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ==========================================================
# ===================== FLUJO PRINCIPAL =====================
# ==========================================================


nombre, documento, edad, cargo = ingresar_datos_firmante()
fecha = obtener_tiempo()

ruta_foto = tomar_foto()

if not ruta_foto:
    print("Proceso cancelado")
    exit()

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

# ==========================================================
# VALIDACIÓN NÚMERO DOCUMENTO (OCR)
# ==========================================================

numero_detectado = extraer_numero_desde_imagen(ruta_imagen_documento)

if not numero_detectado:
    print(" No se pudo extraer número del documento.")
    exit()

numero_detectado_limpio = numero_detectado.replace(".", "").replace(" ", "")

if str(documento) != numero_detectado_limpio:
    print("❌El número del documento NO coincide.")
    exit()

print("Número de documento validado correctamente.")

# ==========================================================
# VALIDACIÓN BIOMÉTRICA
# ==========================================================

if not validar_identidad(ruta_imagen_documento, ruta_foto):
    print("Validación facial fallida. No se firma.")
    exit()

print(" Validación facial exitosa. Continuando...")

print(" Proceso Finalizado")
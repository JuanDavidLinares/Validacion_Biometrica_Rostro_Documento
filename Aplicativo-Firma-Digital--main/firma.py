import os
#os.system("cls") limpiar consola Windows
#Funcion Para devolver la ruta de la carpeta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DOCS_DIR= os.path.join(BASE_DIR, "docs_salida")
os.makedirs(DOCS_DIR, exist_ok=True)

os.makedirs(UPLOAD_DIR, exist_ok=True)
#Librerias para abrir el explorador de Archivos y manipular pdfs 
import tkinter as tk
from tkinter import filedialog
import shutil
import hashlib
#Libreria Para el manejo de la camara y las imagenes 
import cv2


#Libreria para poder leer , escribir pdf
from pypdf import PdfReader, PdfWriter, Transformation
#Libreria para generar texto pdf 
from reportlab.pdfgen import canvas 
#Libreria para obtener la fecha actual
from datetime import datetime
#librerias para el diseño y tamaño
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from services.email_service import enviar_documento

#
def seleccionar_pdf_desde_explorador() -> str | None:
   
    """
    Abre el explorador del sistema y permite seleccionar un PDF.

    Retorna:
        str | None: ruta del archivo seleccionado o None si cancela
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccione un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    return ruta_archivo if ruta_archivo else None

# Funcion Para Generar un hash asociado al archivo subido para evitar que se suba el mismo archivo dos veces
def generar_hash_archivo(ruta_archivo: str) -> str:
    """
    Genera un hash SHA-256 del archivo para validar duplicados.
    """
    hash_sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)

    return hash_sha256.hexdigest()

def construir_nombre_por_hash(hash_archivo: str, extension: str) -> str:
    """
    Construye el nombre del archivo usando su hash.
    """
    return f"{hash_archivo}{extension}"

#Funcion Para tomar fotos des del sistema de 
def tomar_foto()   -> str | None:
 camara = cv2.VideoCapture(0)

 if not camara.isOpened():
    print("No se pudo abrir la camara")
    exit()

 print("Presiona 's' para tomar una foto o 'q' para salir.")
 ruta_imagen = os.path.join(UPLOAD_DIR, "foto_capturada.jpg")
 while True:
    ret, frame = camara.read()
    if not ret:
        break

    cv2.imshow("Camara - Presiona S para capturar", frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    # SI PRESIONAS 's' GUARDA LA IMAGEN
    if key == ord('s'):
        cv2.imwrite(ruta_imagen, frame)
        print("¡Foto guardada como foto_capturada.jpg!")
        break
    # SI PRESIONAS 'q' CIERRA EL PROGRAMA
    if key == ord('q'):
        break

 camara.release()
 cv2.destroyAllWindows()
 return ruta_imagen

 
 # Permite subir los archivos y retorna la ruta de destino 
 
 #

#Funcion Para Seleccinar Y subir el pdf desde el exploradir de archivos
def seleccionar_y_subir_pdf():
    """
    Permite seleccionar y subir un PDF.
    Si el archivo ya existe, solicita otro.
    """
    while True:
        ruta = seleccionar_pdf_desde_explorador()

        if not ruta:
            print("⚠️ Selección cancelada")
            return None

        try:
            destino = subir_pdf(ruta)
            print("✅ PDF subido correctamente")
            print("📁 Guardado en:", destino)
            return destino   # ← SALE DEL BUCLE CORRECTAMENTE

        except ValueError as e:
            print("❌", e)
            print("Seleccione un archivo diferente.\n")

 #
def subir_pdf(ruta_origen: str) -> str:

#Valida  la subida y la subida del pdf en la ruta de destino  
    if not os.path.isfile(ruta_origen):
        raise FileNotFoundError("El archivo no existe")

    if not ruta_origen.lower().endswith(".pdf"):
        raise ValueError("Solo se permiten archivos PDF")
        
         
    hash_archivo = generar_hash_archivo(ruta_origen)
     
    # 4️⃣ Construir nombre destino basado en hash
    extension = os.path.splitext(ruta_origen)[1]
    nombre_hash = construir_nombre_por_hash(hash_archivo, extension)

    ruta_destino = os.path.join(UPLOAD_DIR, nombre_hash)
      
    if os.path.exists(ruta_destino):
        print("Ya Existe Archivo en el Sistema")
        ###seleccionar_y_subir_pdf()
        raise ValueError("⚠️ Este documento ya existe en el sistema.")
         
    shutil.copy2(ruta_origen, ruta_destino)

    return ruta_destino   
#funcion solicitar datos al usuario    
def ingresar_datos_firmante():
    try:    
     nombre=input("Ingrese su nombre : ")
     documento=int(input("Ingrese su documento : "))
     edad=int(input("Ingrese su edad (numero)"))
     cargo=input("Ingrese su cargo")
    except Exception as e:
        print("Ingrese el tipo de dato solicitado:", e)
        ingresar_datos_firmante()
    return nombre,documento,edad,cargo
    
  #Funcion obtener tiempo del sistema  
#Funcion Para Obtener la fecha actual del sistema
def obtener_tiempo():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return timestamp   
#Funcion  para Crear pdf con los datos del ingresados
def crear_pdf_texto(ruta, nombre, cargo, fecha,edad,documento,ruta_imagen):
   
  c = canvas.Canvas(ruta, pagesize=A4)
#controlar altura y ancho
  width, height = A4

   
     # TÍTULO
 
  c.setFont("Helvetica-Bold", 26)
  c.drawString(80, height - 80, "Firmas Electrónicas")

    # Línea decorativa amarilla
  c.setFillColor(colors.blue)
  c.rect(50, height - 120, 10, 80, fill=1)
  c.setFillColor(colors.black)

    
    # TEXTO INFORMATIVO
  
  c.setFont("Helvetica", 12)

  c.drawString(80, height - 150, "Firmado electrónicamente por:")
  c.setFont("Helvetica-Bold", 14)
  c.drawString(80, height - 170, nombre)

  c.setFont("Helvetica", 11)
  c.drawString(80, height - 200, f"Documento: {documento}")
  c.drawString(80, height - 220, f"Fecha: {fecha}")

     #  Foto y colocacion

  if ruta_imagen:
     c.drawImage(
            ruta_imagen,
            80,            # X
            520,           # Y
            width=120,
            height=90
        )

  c.save()
print("Creando pdf")
    
    
    
print("Suba su Documento PDF A firmar ")

ruta_doc_uploads=seleccionar_y_subir_pdf()

nombre,documento,edad,cargo=ingresar_datos_firmante()
fecha=obtener_tiempo()
ruta_foto=tomar_foto()  
  
ruta=os.path.join(UPLOAD_DIR, "temporal2.pdf")
crear_pdf_texto(ruta,nombre,cargo,fecha,edad,documento,ruta_foto)

 # Metodos para leer el pdf y escribir 
lector_pdf = PdfReader(ruta_doc_uploads)
lector_datos_firmante=PdfReader(ruta)
escritor_pdf = PdfWriter()

#  Copiar todas las páginas originales
for pagina in lector_pdf.pages:
    escritor_pdf.add_page(pagina)

#  Agregar la nueva página al final
escritor_pdf.add_page(lector_datos_firmante.pages[0])

#Genera la salida del pdf original firmado
nombre_salida = os.path.join(DOCS_DIR,"pdf_firmado.pdf")
with open(nombre_salida, "wb") as salida:
        escritor_pdf.write(salida)
        print("PDF Firmado Exitosamente")


try:
    correo_destino = input("Ingrese el correo al cual enviar el documento firmado: ")

    enviar_documento(
        correo_destino,
        nombre_salida,
        ruta_foto
    )

except Exception as e:
    print("Error al enviar el correo:", e)






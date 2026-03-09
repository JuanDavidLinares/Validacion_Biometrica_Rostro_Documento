# ==============================================
# OCR + VALIDACIÓN DE DOCUMENTO
# ==============================================

import pytesseract
import cv2
import re
from tkinter import Tk, filedialog


# 🔥 FORZAR RUTA TESSERACT (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ==============================================
# SELECCIONAR IMAGEN
# ==============================================

def seleccionar_imagen():
    root = Tk()
    root.withdraw()

    ruta = filedialog.askopenfilename(
        title="Selecciona la imagen del documento",
        filetypes=[("Imagen", "*.jpg *.jpeg *.png")]
    )

    return ruta


# ==============================================
# EXTRAER NÚMERO DEL DOCUMENTO
# ==============================================

def extraer_numero_desde_imagen(ruta_imagen):

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        print("No se pudo cargar la imagen")
        return None, None

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    texto = pytesseract.image_to_string(gris)

    print("\nTexto detectado:\n")
    # print(texto)

    # Buscar números largos con puntos (ej: 1.022.639.266)
    numeros = re.findall(r"\d[\d\.]{6,20}\d", texto)

    if not numeros:
        return None, None

    numero_original = max(numeros, key=len)  # Con puntos
    numero_limpio = numero_original.replace(".", "")  # Sin puntos

    return numero_original, numero_limpio


# ==============================================
# VALIDACIÓN DEL DOCUMENTO (FUNCIÓN PRINCIPAL)
# ==============================================

def validar_documento(ruta_imagen, numero_usuario):
    """
    Valida si el número del documento coincide con el OCR.

    Returns:
        bool
    """

    numero_original, numero_documento = extraer_numero_desde_imagen(ruta_imagen)

    if not numero_documento:
        print("\nNo se pudo extraer ningún número del documento.")
        return False

    print("\nNúmero detectado en documento (con puntos):", numero_original)
    print("Número detectado en documento (sin puntos):", numero_documento)

    numero_usuario = numero_usuario.replace(".", "").replace(" ", "")

    if numero_usuario == numero_documento:
        print("\nDOCUMENTO VÁLIDO - Los números coinciden.")
        return True
    else:
        print("\nDOCUMENTO NO VÁLIDO - Los números NO coinciden.")
        return False


# ==============================================
# PROGRAMA PRINCIPAL (PARA PRUEBAS)
# ==============================================

if __name__ == "__main__":

    print("VALIDACIÓN DE DOCUMENTO CON OCR\n")

    # 1️⃣ Usuario selecciona imagen
    ruta = seleccionar_imagen()

    if not ruta:
        print("No seleccionaste imagen.")
        exit()

    # 2️⃣ Usuario ingresa su número manualmente
    numero_usuario = input("\nEscribe tu número de documento: ")

    # 3️⃣ Validar documento
    resultado = validar_documento(ruta, numero_usuario)

    print("\nResultado final OCR:", resultado)
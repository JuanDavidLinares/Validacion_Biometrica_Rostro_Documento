"""from deepface import DeepFace

resultado = DeepFace.verify(
    img1_path="cedula.jpeg",
    img2_path="uploads/foto_capturada.jpg",
    model_name="ArcFace"
)

print(resultado)"""

"""
import cv2
from deepface import DeepFace

# ==========================
# 1. Detectar rostro en documento
# ==========================

def detectar_y_recortar_rostro(ruta_imagen):
    image = cv2.imread(ruta_imagen)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) == 0:
        print("❌ No se detectó rostro en:", ruta_imagen)
        return None

    # Tomamos el primer rostro detectado
    x, y, w, h = faces[0]
    rostro = image[y:y+h, x:x+w]

    # Guardar rostro recortado
    ruta_rostro = "rostro_recortado.jpg"
    cv2.imwrite(ruta_rostro, rostro)

    print("✅ Rostro detectado y recortado:", ruta_rostro)

    return ruta_rostro


# ==========================
# 2. Flujo completo
# ==========================

# Detectar rostro en la cédula
ruta_rostro_cedula = detectar_y_recortar_rostro("cedula.jpeg")

if ruta_rostro_cedula is not None:

    resultado = DeepFace.verify(
        img1_path=ruta_rostro_cedula,
        img2_path="uploads/foto_capturada.jpg",
        model_name="ArcFace",
        enforce_detection=False
    )

    print("\n🔎 Resultado comparación:")
    print("Match:", resultado["verified"])
    print("Distancia:", resultado["distance"])
    print("Umbral:", resultado["threshold"])
    """

"""
from deepface import DeepFace

# ==============================
# CONFIGURACIÓN
# ==============================

ruta_documento = "cedula.jpeg"
ruta_selfie = "uploads/foto_capturada.jpg"

# Umbral adaptado a tus pruebas
UMBRAL_PERSONALIZADO = 0.90  # 🔥 Ajustado según tus resultados

# ==============================
# VERIFICACIÓN FACIAL
# ==============================

try:
    resultado = DeepFace.verify(
        img1_path=ruta_documento,
        img2_path=ruta_selfie,
        model_name="Facenet512",
        distance_metric="cosine",
        enforce_detection=True  # Detecta rostro automáticamente
    )

    distancia = resultado["distance"]
    umbral_modelo = resultado["threshold"]

    # ==============================
    # RESULTADOS
    # ==============================

    print("\n🔎 Resultado comparación:")
    print("Distancia:", distancia)
    print("Umbral del modelo:", umbral_modelo)
    print("Umbral personalizado:", UMBRAL_PERSONALIZADO)

    # 🔥 Decisión basada en tu umbral personalizado
    if distancia < UMBRAL_PERSONALIZADO:
        print("✅ IDENTIDAD VALIDADA")
        print("Resultado Final: TRUE")
    else:
        print("❌ IDENTIDAD NO COINCIDE")
        print("Resultado Final: FALSE")

except Exception as e:
    print("❌ Error durante la verificación:")
    print(str(e))
    """


"""
=============================================================
VERIFICACIÓN BIOMÉTRICA FACIAL - ENTORNO EMPRESARIAL
=============================================================

Descripción:
Este script realiza verificación biométrica facial comparando:
1. La foto de un documento de identidad
2. Una selfie capturada del usuario

Flujo:
- Detecta y extrae el rostro en ambas imágenes.
- Alinea los rostros automáticamente.
- Genera embeddings faciales usando FaceNet512.
- Calcula distancia coseno entre embeddings.
- Aplica reglas empresariales de decisión.

Tecnologías:
- DeepFace
- RetinaFace (detección y alineación)
- FaceNet512 (modelo de embeddings)
- Métrica: cosine distance

"""

from deepface import DeepFace
import cv2
import tkinter as tk
from tkinter import filedialog


# ==========================================
# SELECCIONAR DOCUMENTO
# ==========================================

def pedir_ruta_documento():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    ruta = filedialog.askopenfilename(
        title="Seleccione el DOCUMENTO",
        filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
    )

    root.destroy()
    return ruta


# ==========================================
# CAPTURAR SELFIE
# ==========================================

def capturar_selfie():

    print("\nAbriendo cámara... Presiona 'S' para tomar la foto o 'ESC' para salir.")

    cam = cv2.VideoCapture(0)

    selfie = None

    while True:

        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("Captura tu Selfie - Presiona S", frame)

        key = cv2.waitKey(1)

        if key == 115:  # tecla S
            selfie = frame.copy()
            break

        elif key == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()

    return selfie


# ==========================================
# VALIDACIÓN FACIAL
# ==========================================

def validar_rostro():

    ruta_documento = pedir_ruta_documento()

    if not ruta_documento:
        print("No se seleccionó documento.")
        return False

    selfie_capturada = capturar_selfie()

    if selfie_capturada is None:
        print("Captura cancelada.")
        return False

    print("\nVerificando identidad...")

    try:

        resultado = DeepFace.verify(
            img1_path=ruta_documento,
            img2_path=selfie_capturada,
            model_name="Facenet512",
            detector_backend="retinaface",
            distance_metric="cosine",
            enforce_detection=True
        )

        distancia = resultado["distance"]
        threshold = resultado["threshold"]

        print(f"\nDistancia: {distancia:.4f}")
        print(f"Threshold: {threshold:.4f}")

        if distancia <= threshold:
            print("IDENTIDAD VALIDADA")
            return True
        else:
            print("IDENTIDAD NO COINCIDE")
            return False

    except Exception as e:
        print(f"Error en DeepFace: {e}")
        return False


# ==========================================
# EJECUCIÓN DIRECTA
# ==========================================

if __name__ == "__main__":

    resultado = validar_rostro()

    print("\nResultado final DeepFace:", resultado)
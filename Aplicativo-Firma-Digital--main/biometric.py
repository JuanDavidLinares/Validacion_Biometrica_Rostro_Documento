import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)


def generar_vector(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        return None

    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    resultados = face_mesh.process(imagen_rgb)

    if not resultados.multi_face_landmarks:
        return None

    landmarks = resultados.multi_face_landmarks[0]

    vector = []
    for punto in landmarks.landmark:
        vector.append(punto.x)
        vector.append(punto.y)

    return vector


def comparar_vectores(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    distancia = np.linalg.norm(v1 - v2)

    # Este threshold lo ajustamos luego con pruebas reales
    if distancia < 5:
        return True, float(distancia)
    else:
        return False, float(distancia)
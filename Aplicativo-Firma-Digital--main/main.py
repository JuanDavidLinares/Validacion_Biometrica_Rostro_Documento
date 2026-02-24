from fastapi import FastAPI, UploadFile, File, Form
import tempfile
from biometric import generar_vector, comparar_vectores

app = FastAPI()

base_datos_temporal = {}


@app.post("/register-document")
async def register_document(
    numero_documento: str = Form(...),
    imagen: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        contenido = await imagen.read()
        temp.write(contenido)
        temp_path = temp.name

    vector = generar_vector(temp_path)

    if vector is None:
        return {"error": "No se detectó un rostro válido en la cédula"}

    base_datos_temporal[numero_documento] = vector

    return {"mensaje": "Documento registrado correctamente"}


@app.post("/validate-identity")
async def validate_identity(
    numero_documento: str = Form(...),
    selfie: UploadFile = File(...)
):
    if numero_documento not in base_datos_temporal:
        return {"error": "Documento no registrado"}

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        contenido = await selfie.read()
        temp.write(contenido)
        temp_path = temp.name

    vector_selfie = generar_vector(temp_path)

    if vector_selfie is None:
        return {"error": "No se detectó un rostro en la selfie"}

    vector_guardado = base_datos_temporal[numero_documento]

    resultado, distancia = comparar_vectores(
        vector_guardado,
        vector_selfie
    )

    if resultado:
        return {"resultado": "OK", "distancia": distancia}
    else:
        return {"resultado": "FALLO", "distancia": distancia}
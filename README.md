# 🖊️ Aplicativo Validacion Biometria Rostro/Documento

Sistema desarrollado en Python que permite validar la identidad de una persona mediante la carga de su documento
extrayendo numero de documento y rostro, comparandolo con la toma de datos en tiempo real.

---

## 🚀 Funcionalidades

- 📂 Cargue del documento de identidad  desde el explorador de archivos
- 🔐 Validación de documentos duplicados mediante hash SHA-256
- 📸 Captura de fotografía del firmante como evidencia
- 📝 Generación de  la validacion correcta de identidad




---



## ▶️ Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python firma.py
```

**Flujo del sistema:**

1. Ingresar los datos del firmante
2. Cargue de foto del documento
3. Capturar la fotografía del rostro
4. Validacion Numero de documento
5. Validacion del Rostro
 

---

## 🔒 Seguridad Implementada

- **Hash SHA-256** para evitar el procesamiento de documentos duplicados

---



## 👨‍💻 Equipo de Desarrollo

## 🔐 Persistencia de datos

Se usa la libreria psycopg2. Instalacion:
```bash
pip install psycopg2 
```

## 🔐 Validación Biométrica con DeepFace

El sistema implementa autenticación biométrica mediante reconocimiento facial utilizando la librería **DeepFace**.

Antes de permitir la firma del documento, el sistema verifica que la persona que toma la selfie coincide con la persona presente en la imagen del documento de identidad.

---

## 🤖 ¿Qué es DeepFace?

DeepFace es una librería de reconocimiento facial basada en Deep Learning desarrollada en Python.

Permite:

- 📷 Detectar rostros en imágenes
- 🔍 Extraer características faciales (embeddings)
- 🧠 Comparar rostros matemáticamente
- ⚖ Calcular la similitud entre dos caras

Repositorio oficial:
https://github.com/serengil/deepface

---

## ⚙ ¿Cómo Funciona la Validación?

El proceso interno funciona así:

### 1️⃣ Detección del Rostro

DeepFace usa un detector como:

- RetinaFace (utilizado en este proyecto)

Este detector:

- Encuentra la ubicación del rostro en la imagen
- Recorta el rostro automáticamente
- Lo alinea para mejorar precisión

---

### 2️⃣ Generación de Embeddings

Una vez detectado el rostro:

- El modelo ArcFace convierte la imagen facial en un vector numérico
- Ese vector representa características únicas del rostro

Ejemplo:

Imagen → Modelo → Vector matemático de 512 dimensiones

Ese vector es llamado **embedding facial**.

---

### 3️⃣ Cálculo de Distancia

El sistema compara los dos embeddings usando distancia coseno:


Distancia = qué tan diferentes son los vectores


Si los vectores son muy parecidos → distancia pequeña  
Si son diferentes → distancia grande  

---

### 4️⃣ Comparación con Threshold

En el código encontrarás:

```python
THRESHOLD = 0.90

Regla:

Si distancia ≤ threshold → Identidad validada ✅

Si distancia > threshold → Identidad rechazada ❌

📊 Interpretación de Valores
Distancia	Significado
0.4 – 0.7	Mismo rostro con alta confianza
0.7 – 0.9	Posible coincidencia
> 0.9	Probablemente persona diferente

El threshold puede ajustarse según pruebas reales.

🧠 Modelos Utilizados

El proyecto utiliza los siguientes modelos internos:

✅ ArcFace

Modelo principal para generación de embeddings

Alta precisión

Ideal para verificación biométrica

✅ RetinaFace

Detector de rostros

Encuentra y alinea la cara antes de comparar

Estos modelos son descargados automáticamente por DeepFace.

📦 Dependencias Necesarias

Para que la validación biométrica funcione, se requieren:

deepface

tensorflow

tf-keras

opencv-python

numpy

Instalación:

pip install deepface tensorflow tf-keras opencv-python numpy
💾 Model Weights

Los modelos pre-entrenados (weights) se descargan automáticamente la primera vez que se ejecuta el sistema.

Se almacenan en:

Windows:

C:\Users\TU_USUARIO\.deepface\

Linux / Mac:

~/.deepface/
🌍 Descarga Manual de Modelos

Si deseas descargarlos manualmente:

Repositorio oficial:
https://github.com/serengil/deepface

Modelos y weights:
https://github.com/serengil/deepface/tree/master/deepface/weights

⚡ Los weights NO deben subirse al repositorio porque:

Son archivos pesados

Se descargan automáticamente

DeepFace los gestiona internamente

🚀 Flujo Técnico Completo

Usuario toma selfie

Usuario selecciona imagen del documento

DeepFace detecta rostro en ambas imágenes

Se generan embeddings

Se calcula distancia coseno

Se compara con threshold

Si pasa → Se permite firmar

Si falla → Se bloquea el proceso

# 📄 OCR + Validación de Documento

Sistema en Python que utiliza **OCR (Tesseract + OpenCV)** para extraer el número de un documento desde una imagen y compararlo con el número ingresado por el usuario.

---

## 🚀 Funcionalidades

✅ Selección de imagen mediante explorador de archivos  
✅ Procesamiento de imagen con OpenCV  
✅ Extracción de texto con Tesseract OCR  
✅ Búsqueda automática de números de documento  
✅ Limpieza de formato (elimina puntos)  
✅ Comparación entre número extraído y número ingresado  
✅ Validación automática del documento  

---

## 🛠 Tecnologías Utilizadas

- 🐍 Python
- 👁 OpenCV
- 🧠 Tesseract OCR
- 🔍 Regex (Expresiones regulares)
- 🖥 Tkinter (Selector de archivos)

---

## 📦 Requisitos

### 🔥 Instalar dependencias

```bash
pip install opencv-python pytesseract
🔥 Instalar Tesseract OCR (OBLIGATORIO)

Descargar e instalar desde:

👉 https://github.com/UB-Mannheim/tesseract/wiki

Luego verificar que esta ruta exista:

C:\Program Files\Tesseract-OCR\tesseract.exe

Si está en otra ruta, modificar esta línea en el código:

pytesseract.pytesseract.tesseract_cmd = r"TU_RUTA_AQUI\tesseract.exe"
▶️ Cómo Ejecutar

Ejecutar el script con:

python nombre_archivo.py
Flujo del programa:

Se abre una ventana para seleccionar la imagen del documento.

El sistema extrae automáticamente los números del documento.

Se muestra el número detectado (con y sin puntos).

El usuario ingresa manualmente su número de documento.

El sistema compara ambos valores.

Se imprime si el documento es válido o no.

🔎 Cómo Funciona el OCR

El sistema:

Convierte la imagen a escala de grises.

Aplica reconocimiento de texto con Tesseract.

Usa una expresión regular para detectar números largos con puntos.

Limpia el formato eliminando puntos.

Compara con el número ingresado por el usuario.

📌 Expresión Regular Utilizada
r"\d[\d\.]{6,20}\d"

Busca números largos con formato tipo:

1.234.567.890
1023456789
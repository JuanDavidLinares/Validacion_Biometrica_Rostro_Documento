# 🖊️ Aplicativo Firma Digital

Sistema desarrollado en Python que permite firmar electrónicamente documentos PDF, generando evidencia fotográfica del firmante y enviando automáticamente el documento firmado por correo electrónico.

---

## 🚀 Funcionalidades

- 📂 Selección de documento PDF desde el explorador de archivos
- 🔐 Validación de documentos duplicados mediante hash SHA-256
- 📸 Captura de fotografía del firmante como evidencia
- 📝 Generación de página de firma con nombre, documento de identidad, fecha/hora e imagen capturada
- 📎 Unión del documento original con la página de firma
- 📧 Envío automático del documento firmado por correo electrónico
- 🔒 Uso de variables de entorno para proteger credenciales SMTP

---

## 🏗️ Estructura del Proyecto

```
APLICATIVO-FIRMA-DIGITAL/
│
├── uploads/                  # PDFs originales y foto capturada
├── docs_salida/              # PDFs firmados generados
├── services/
│   └── email_service.py     # Módulo de envío de correos
├── camera.py                # Captura de imagen con OpenCV
├── firma.py                 # Flujo principal de firma
├── .env                     # Variables de entorno (NO subir a Git)
└── README.md
```

---

## ⚙️ Requisitos

Instala las dependencias con:

```bash
pip install opencv-python pypdf reportlab python-dotenv
```

---

## 🔐 Configuración de Correo (Gmail)

1. Activa la verificación en dos pasos en tu cuenta de Google.
2. Crea una [contraseña de aplicación](https://myaccount.google.com/apppasswords).
3. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASS=tu_app_password
```

> ⚠️ **Nunca subas el archivo `.env` a tu repositorio.** Asegúrate de incluirlo en `.gitignore`.

---

## ▶️ Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python firma.py
```

**Flujo del sistema:**

1. Seleccionar el PDF a firmar
2. Ingresar los datos del firmante
3. Capturar la fotografía de evidencia
4. Generar el documento firmado
5. Enviar automáticamente por correo electrónico

---

## 🔒 Seguridad Implementada

- **Hash SHA-256** para evitar el procesamiento de documentos duplicados
- **Variables de entorno** para proteger las credenciales SMTP
- **Conexión SMTP segura** mediante SSL (puerto 465)

---

## 🧠 Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| OpenCV | Captura de fotografía |
| PyPDF | Manipulación de PDFs |
| ReportLab | Generación de la página de firma |
| SMTP / Gmail | Envío de correo electrónico |
| python-dotenv | Gestión de variables de entorno |

---

## 👨‍💻 Equipo de Desarrollo


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
Sistema de Verificación de Identidad Biométrica

Este proyecto implementa un sistema de verificación de identidad que combina dos mecanismos de validación:

Verificación biométrica facial utilizando DeepFace.

Validación de documento mediante OCR utilizando Tesseract.

El objetivo es confirmar que la persona que presenta el documento es realmente su titular mediante la comparación de:

La foto del documento de identidad.

Una selfie capturada en tiempo real.

El número de documento extraído automáticamente mediante OCR.

Arquitectura del Proyecto

El sistema está compuesto por dos módulos independientes:

proyecto/
│
├── test_deepface.py   # Validación biométrica facial
├── test_ocr.py        # Validación de número de documento con OCR
└── validacion.py      # (Opcional) Integración de resultados

Cada módulo puede ejecutarse de manera independiente.

1. Verificación Biométrica Facial (test_deepface.py)

Este módulo valida que el rostro del documento coincida con la selfie capturada por la cámara.

Flujo de funcionamiento

El usuario selecciona una imagen del documento de identidad.

Se abre la cámara del computador.

El usuario captura una selfie presionando la tecla S.

El sistema utiliza DeepFace para comparar ambos rostros.

Se calcula la distancia entre embeddings faciales.

Se determina si la identidad es válida.

Tecnologías utilizadas

DeepFace

RetinaFace (detección y alineación facial)

FaceNet512 (modelo de embeddings faciales)

OpenCV (captura de cámara)

Tkinter (selección de archivos)

Ejecución
python test_deepface.py
Resultado esperado
Distancia: 0.42
Threshold: 0.68
IDENTIDAD VALIDADA

Resultado final DeepFace: True
2. Validación de Documento con OCR (test_ocr.py)

Este módulo valida que el número de documento ingresado por el usuario coincida con el número detectado en la imagen del documento.

Flujo de funcionamiento

El usuario selecciona una imagen del documento.

El sistema convierte la imagen a escala de grises.

Se aplica OCR con Tesseract para extraer el texto.

Se identifica el número de documento usando expresiones regulares.

El usuario ingresa su número manualmente.

El sistema compara ambos valores.

Tecnologías utilizadas

Tesseract OCR

pytesseract

OpenCV

Expresiones regulares (regex)

Ejecución
python test_ocr.py
Resultado esperado
Número detectado en documento (con puntos): 1.022.639.266
Número detectado en documento (sin puntos): 1022639266

DOCUMENTO VÁLIDO - Los números coinciden.

Resultado final OCR: True
Instalación de Dependencias
1. Instalar Python

Se recomienda Python 3.9 o superior.

2. Instalar librerías necesarias
pip install deepface
pip install opencv-python
pip install pytesseract
pip install numpy
3. Instalar Tesseract OCR

Descargar desde:

https://github.com/tesseract-ocr/tesseract

Instalar en Windows en:

C:\Program Files\Tesseract-OCR\

El script ya incluye la ruta:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
Flujo General del Sistema

El sistema puede integrarse en un flujo de validación completo:

Documento de identidad
        │
        ├── OCR (test_ocr.py)
        │       │
        │       └── True / False
        │
Selfie capturada
        │
        └── DeepFace (test_deepface.py)
                │
                └── True / False
                       │
                       ▼
             Validación final
             (AND lógico)

La identidad se considera válida únicamente si ambas validaciones son verdaderas.

resultado_final = facial AND ocr
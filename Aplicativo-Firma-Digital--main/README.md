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
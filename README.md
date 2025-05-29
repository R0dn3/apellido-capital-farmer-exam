# Sistema de Cotizaciones Legales - Capital & Farmer Abogados 

Este sistema permite generar cotizaciones legales automatizadas a partir de un formulario web. Incluye una simulación de análisis de complejidad con IA y guarda los datos en una base de datos SQLite.

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/R0dn3/apellido-capital-farmer-exam.git
   cd apellido-capital-farmer-exam

2. Crea un entorno virtual y actívalo:

   
   `python -m venv venv`
   `venv\Scripts\actívate`
   
4. Instala las dependencias:

   `pip install -r requirements.txt`

5. Ejecuta la aplicación:

   `python app.py`

6. Abre tu navegador en:

   `http://localhost:5000`
   
## 🧾 Uso
Llena el formulario con tus datos y una descripción del caso.

Haz clic en “Generar Cotización”.

Recibirás una cotización completa que incluye:

💰 Precio base

🧠 Nivel de complejidad (simulado)

📈 Ajuste de precio recomendado

📌 Servicios adicionales sugeridos

📝 Propuesta profesional simulada

## 🤖 API de IA utilizada
Simulación de IA:
Debido a limitaciones de presupuesto, la lógica de IA fue simulada usando reglas simples en el backend. No se realizó una integración real con servicios como OpenAI, Claude o Groq.

## 🛠️ Requisitos

Python 3.8+

Flask

SQLAlchemy

## ✨ Bonus no implementados

❌ Autenticación básica (login/logout)

❌ Validaciones frontend

❌ Tests automatizados

❌ Deploy en plataforma externa

# PARTE 3 – RESPUESTAS TÉCNICAS SOBRE ARQUITECTURA 

## 1. Arquitectura Modular
Modularizaría el sistema separando cada componente (cotizaciones, tickets, expedientes) en blueprints o módulos independientes dentro de Flask. Cada uno tendría sus propias rutas, modelos y controladores, pero compartirían recursos comunes como la base de datos o la autenticación.

## 2. Escalabilidad
Al escalar a 100 usuarios o más, migraría la base de datos de SQLite a PostgreSQL. También implementaría índices en columnas frecuentes, migraciones con Alembic y un sistema de caché para reducir consultas innecesarias.

## 3. Integraciones
Utilizaría las APIs oficiales de Google Drive o Dropbox con OAuth 2.0. Configuraría una ruta que genere el documento legal (PDF o Word) y lo suba automáticamente a la nube, guardando el enlace en la base de datos.

## 4. Deployment
Desplegaría la aplicación en Railway o Render, por su bajo costo y facilidad de uso. Usaría Gunicorn para producción y configuraría el dominio para acceso interno desde computadoras y celulares del estudio.

## 5. Seguridad
Implementaría validaciones en backend, sanitización de entradas y HTTPS en producción. También ocultaría las claves y configuraciones sensibles usando variables de entorno (.env) y evitaría exponer datos personales en logs.

## 📷 Capturas de Funcionamiento

Ejecucion valida ejecutando el codigo: python app.py:

![{65B10E0C-43CC-4556-84E1-2E9119841B7D}](https://github.com/user-attachments/assets/7c376698-4291-4e3c-befc-69acdcbe2103)

Captura del formulario con sus respectivos secciones de llenado: 

![{BF5AB2A2-6AB9-450B-A33D-D509DED8DED2}](https://github.com/user-attachments/assets/2d7dd567-94da-4736-861a-a520f59342f1)

Devolucion de la cotizacion:

![{0E8FA87B-BC95-4D34-9771-28A9DB41A325}](https://github.com/user-attachments/assets/2a85bc67-4000-4cdb-88e4-49c39c328747)

Datos guardados en la base de datos elegida SQLite

![{4AC22031-2B01-47E1-968D-DA9018B0FE06}](https://github.com/user-attachments/assets/b63217a0-56b4-43c6-8ada-c6ff88b51ac3)

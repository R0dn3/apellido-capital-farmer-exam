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
   
🧾 Uso
Llena el formulario con tus datos y una descripción del caso.

Haz clic en “Generar Cotización”.

Recibirás una cotización completa que incluye:

💰 Precio base

🧠 Nivel de complejidad (simulado)

📈 Ajuste de precio recomendado

📌 Servicios adicionales sugeridos

📝 Propuesta profesional simulada

🤖 API de IA utilizada
Simulación de IA:
Debido a limitaciones de presupuesto, la lógica de IA fue simulada usando reglas simples en el backend. No se realizó una integración real con servicios como OpenAI, Claude o Groq.

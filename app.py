from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os
import re

# Crear la aplicación Flask
app = Flask(__name__)

# Definir ruta absoluta para la base de datos SQLite dentro de la carpeta 'instance'
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')

# Si la carpeta 'instance' no existe, crearla para almacenar la base de datos
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Configurar SQLAlchemy para usar SQLite con la ruta definida
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path.replace('\\', '/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar para mejorar rendimiento

# Crear objeto SQLAlchemy para manejar la base de datos
db = SQLAlchemy(app)

# Definir el modelo 'Cotizacion' que representa una tabla en la base de datos
class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID autoincremental único
    numero = db.Column(db.String(20), unique=True, nullable=False)  # Número único de cotización
    nombre = db.Column(db.String(100), nullable=False)  # Nombre del cliente
    email = db.Column(db.String(100), nullable=False)  # Email del cliente
    tipo_servicio = db.Column(db.String(50), nullable=False)  # Tipo de servicio solicitado
    descripcion = db.Column(db.Text, nullable=False)  # Descripción del caso o solicitud
    precio = db.Column(db.Integer, nullable=False)  # Precio final calculado
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación automática

# Función para validar formato básico de email usando expresiones regulares
def es_email_valido(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

# Función para evaluar la complejidad del caso y ajustar el precio según el tipo de servicio y descripción
def evaluar_complejidad_ajuste_servicios(tipo_servicio, descripcion):
    # Convertir a minúsculas para comparaciones más fáciles
    tipo_servicio = tipo_servicio.lower()
    descripcion = descripcion.lower()
    
    complejidad = "Baja"  # Valor inicial por defecto
    ajuste = 0  # Sin ajuste inicial
    servicios_adicionales = []  # Lista vacía de servicios extra

    # Evaluar según palabras clave para Defensa laboral
    if "defensa laboral" in tipo_servicio:
        if any(p in descripcion for p in ["despido arbitrario", "acusación criminal", "falta grave"]):
            complejidad, ajuste = "Alta", 50
            servicios_adicionales = ["Análisis de pruebas", "Representación en juicio"]
        elif any(p in descripcion for p in ["disputa", "conflicto"]):
            complejidad, ajuste = "Media", 25
            servicios_adicionales = ["Análisis de pruebas"]

    # Evaluar según palabras clave para Consultoría tributaria
    elif "consultoría tributaria" in tipo_servicio:
        if any(p in descripcion for p in ["auditoría", "multinacional", "contratos complejos"]):
            complejidad, ajuste = "Alta", 50
            servicios_adicionales = ["Revisión de declaraciones anteriores", "Planeamiento tributario", "Revisión de contratos"]
        elif any(p in descripcion for p in ["declaración", "impuestos", "consultoría básica"]):
            complejidad, ajuste = "Media", 25
            servicios_adicionales = ["Revisión de declaraciones anteriores", "Planeamiento tributario"]

    # Evaluar según palabras clave para Constitución de empresa
    elif "constitución de empresa" in tipo_servicio:
        if any(p in descripcion for p in ["multisucursal", "socios internacionales"]):
            complejidad, ajuste = "Alta", 50
            servicios_adicionales = [
                "Revisión de contratos internacionales",
                "Consultoría en regulación internacional",
                "Asesoría en estructuras societarias complejas"
            ]
        else:
            servicios_adicionales = []

    return complejidad, ajuste, servicios_adicionales

# Generar texto formal de propuesta profesional para el cliente
def generar_propuesta_texto(nombre_cliente, tipo_servicio, complejidad, ajuste, servicios_adicionales):
    servicios_texto = (
        "Para una gestión completa y eficiente, recomendamos considerar los siguientes servicios adicionales: "
        + ", ".join(servicios_adicionales) + "."
        if servicios_adicionales else ""
    )
    return (
        f"Estimado/a {nombre_cliente},\n\n"
        f"Gracias por confiar en Capital & Farmer Abogados para su solicitud de {tipo_servicio}. "
        f"Tras una revisión inicial, hemos determinado que el caso presenta una complejidad de nivel {complejidad.lower()}, "
        f"lo que implica un ajuste en el precio base del {ajuste}%.\n\n"
        f"{servicios_texto}\n\n"
        f"Nuestro equipo se compromete a brindarle asesoría especializada, atención personalizada y un seguimiento detallado "
        f"para asegurar la mejor resolución de su caso.\n"
        f"El plazo estimado para la entrega del servicio es de 5 a 10 días hábiles, sujeto a la complejidad del caso.\n\n"
        f"Quedamos a su disposición para cualquier consulta adicional.\n\n"
        f"Atentamente,\nCapital & Farmer Abogados"
    )

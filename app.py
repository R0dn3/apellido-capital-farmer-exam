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

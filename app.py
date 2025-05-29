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

# Ruta principal para mostrar el formulario HTML al usuario
@app.route('/')
def form():
    return render_template('form.html')

# Ruta que procesa el formulario, genera la cotización y responde con JSON
@app.route('/generar', methods=['POST'])
def generar():
    try:
        # Obtener los datos enviados por POST desde el formulario
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        tipo = request.form.get('tipo_servicio', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        # Validaciones para asegurar que no falten datos obligatorios
        if not nombre or not email or not tipo or not descripcion:
            return jsonify({"error": "Todos los campos son obligatorios."}), 400

        # Validar formato del email
        if not es_email_valido(email):
            return jsonify({"error": "Email inválido."}), 400

        # Precios base para cada tipo de servicio
        precios = {
            "Constitución de empresa": 1500,
            "Defensa laboral": 2000,
            "Consultoría tributaria": 800
        }

        # Obtener el precio base según el tipo de servicio; error si no existe
        precio_base = precios.get(tipo)
        if precio_base is None:
            return jsonify({"error": "Tipo de servicio inválido."}), 400

        # Evaluar la complejidad, ajuste y servicios adicionales para la cotización
        complejidad, ajuste_porcentaje, servicios_adicionales = evaluar_complejidad_ajuste_servicios(tipo, descripcion)

        # Calcular precio final aplicando el porcentaje de ajuste
        precio_final = int(precio_base * (1 + ajuste_porcentaje / 100))

        # Generar número único para la cotización
        numero = f"COT-2025-{str(uuid.uuid4())[:8].upper()}"

        # Crear el objeto Cotizacion y guardarlo en la base de datos
        cotizacion = Cotizacion(
            numero=numero,
            nombre=nombre,
            email=email,
            tipo_servicio=tipo,
            descripcion=descripcion,
            precio=precio_final
        )
        db.session.add(cotizacion)
        db.session.commit()

        # Generar el texto de propuesta para mostrar al cliente
        propuesta = generar_propuesta_texto(nombre, tipo, complejidad, ajuste_porcentaje, servicios_adicionales)

        # Retornar toda la información en formato JSON para que el frontend la muestre
        return jsonify({
            "numero": numero,
            "precio_base": precio_base,
            "precio_final": precio_final,
            "fecha": datetime.utcnow().isoformat(),
            "cliente": nombre,
            "email": email,
            "tipo_servicio": tipo,
            "descripcion": descripcion,
            "complejidad": complejidad,
            "ajuste": f"{ajuste_porcentaje}%",
            "servicios_adicionales": servicios_adicionales,
            "propuesta": propuesta
        })

    except Exception as e:
        # Registrar error inesperado en el log y devolver mensaje genérico
        app.logger.error(f"Error inesperado: {e}")
        return jsonify({"error": "Ocurrió un error inesperado. Intente nuevamente."}), 500

# Ejecutar la aplicación solo si se corre directamente este archivo
if __name__ == '__main__':
    # Crear tablas en la base de datos si no existen antes de iniciar el servidor
    with app.app_context():
        db.create_all()

    app.run(debug=True)  # Ejecutar en modo debug para facilitar desarrollo

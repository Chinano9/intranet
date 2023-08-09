from jinja2 import Template, Environment, FileSystemLoader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Cargar el directorio que contiene las plantillas
template_loader = FileSystemLoader(searchpath="./templates")
env = Environment(loader=template_loader)

# Cargar la plantilla
template = env.get_template("kardex.html")

# Datos para rellenar la plantilla (tus datos_empleado aquí)
datos_empleado = {
    "id": 5,
    "antiguedad_dias": 1025,
    "nombre": "Juanito",
    "apellido_paterno": "Lopez",
    "apellido_materno": "Marquez",
    "fecha_nacimiento": "2000-08-16",
    "fecha_contratacion": "2020-10-12",
    "foto": None,
    "ciudad": "Ciudad del empleado",
    "estado": "Estado del empleado",
    "codigo_postal": "72656",
    "email": "correo@example.com",
    "puesto": "Puesto del empleado",
    "tel_casa": "1232123123",
    "tel_cel": "5637368728",
    "rfc": "RFC del empleado",
    "seguro_social": "Número de seguro social del empleado",
    "curp": "CURP del empleado",
    "sueldo_dia": 318,
    "sueldo_texto": "Trescientos dieciocho pesos"
}

# Renderizar la plantilla con los datos
rendered_template = template.render(datos_empleado=datos_empleado)

# Crear el archivo PDF
pdf_filename = "empleado.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
styles = getSampleStyleSheet()
content = []

# Agregar el contenido a la página PDF
paragraph = Paragraph(rendered_template, style=styles["Normal"])
content.append(paragraph)

# Construir el PDF
doc.build(content)

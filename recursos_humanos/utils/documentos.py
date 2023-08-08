from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generar_kardex(datos_empleado, nombre_archivo):
    # Crear un documento PDF
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)

    # Crear una lista con los datos del empleado
    data = [
        ['NUM. de empleado:', str(datos_empleado['id'])],
        ['Nombre:', datos_empleado['nombre']],
        ['Apellido Paterno:', datos_empleado['apellido_paterno']],
        ['Apellido Materno:', datos_empleado['apellido_materno']],
        ['Fecha de Nacimiento:', datos_empleado['fecha_nacimiento']],
        ['Fecha de Contratación:', datos_empleado['fecha_contratacion']],
        ['Ciudad:', datos_empleado['ciudad']],
        ['Estado:', datos_empleado['estado']],
        ['Código Postal:', datos_empleado['codigo_postal']],
        ['Email:', datos_empleado['email']],
        ['Puesto:', datos_empleado['puesto']],
        ['Teléfono de Casa:', datos_empleado['tel_casa']],
        ['Teléfono Celular:', datos_empleado['tel_cel']],
        ['RFC:', datos_empleado['rfc']],
        ['Número de Seguro Social:', datos_empleado['seguro_social']],
        ['CURP:', datos_empleado['curp']],
        ['Sueldo por Día:', f"${datos_empleado['sueldo_dia']}"],
        ['Sueldo en Texto:', datos_empleado['sueldo_texto']],
        ]

    # Crear una tabla para mostrar los datos
    table = Table(data, colWidths=[150, 300])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    # Se aplica el estilo a la tabla
    table.setStyle(style)

    styles = getSampleStyleSheet()
    estilo_normal = styles['Normal']
    estilo_titulo = styles['Heading1']

    spacer = Spacer(1, 40)
    
    empleado_path = "./res/photo_placeholder.png"
    if datos_empleado['foto'] is not None:
        empleado_path = datos_empleado['foto']
    empleado = Image(empleado_path)
    empleado.drawHeight = 2*inch
    empleado.drawWidth = 2*inch

    
    # Se hace el logo de la empresa
    logo_path = "./res/gpe_logo_light.png"
    logo = Image(logo_path)
    logo.drawHeight = 1.5*inch
    logo.drawWidth = 1.5*inch

    img_paragraph = Paragraph(f'<img src="{logo_path}" width="80" height="80" valign="middle"/> <h1>Kardex</h1> <img src="{empleado_path}" width="90" height="90" valign="middle"/>', estilo_titulo)

    # Agregamos todo el contenido a una lista
    content = [img_paragraph,spacer,table] # Insertar la imagen al inicio del contenido

    doc.build(content)
#

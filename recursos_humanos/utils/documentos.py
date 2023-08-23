from jinja2 import Template, Environment, FileSystemLoader
from xhtml2pdf import pisa
import os
import locale

from .decorators import formato_local

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FOTO_PLACEHOLDER = '/home/chinano/Programming/gpe_servers/intranet/recursos_humanos/utils/res/photo_placeholder.png'


template_loader = FileSystemLoader(searchpath= os.path.join(BASE_DIR, 'templates'))
env = Environment(loader=template_loader)

@formato_local
def generar_kardex(datos_empleado, documento):
    template =env.get_template("kardex.html")

        # Convertir las fechas en el formato localizado (dd-mmm-aaaa)
    if not datos_empleado['foto']:
        datos_empleado['foto'] = FOTO_PLACEHOLDER

    # Renderizar la plantilla con los datos
    rendered_template = template.render(datos_empleado=datos_empleado)# Crear el archivo PDF
    with open(documento, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_template, dest=pdf_file)

        if not pisa_status.err:
            print("PDF generado correctamente.")
        else:
            raise Exception("Ocurrió un error al generar el PDF:", pisa_status.err)


def generar_gafete(datos_empleado, documento):
    template = env.get_template("gafete.html")

    if datos_empleado['foto'] is None:
        datos_empleado['foto'] = FOTO_PLACEHOLDER

    # Renderizar la plantilla con los datos
    rendered_template = template.render(datos_empleado=datos_empleado)

    # Crear el archivo PDF
    with open(documento, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_template, dest=pdf_file, pagesize=(612, 792), orientation='landscape')

        if not pisa_status.err:
            print("PDF generado correctamente.")
        else:
            raise Exception("Ocurrió un error al generar el PDF:", pisa_status.err)

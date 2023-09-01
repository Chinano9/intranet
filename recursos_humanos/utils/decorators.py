from datetime import datetime
import locale

def establecer_localizacion():
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            print("No se pudo establecer una localización en español válida.")

# Decorador para manejar la localización y el cambio de formato de fecha
def formato_local(func):
    def wrapper(datos_empleado, *args, **kwargs):
        establecer_localizacion()

        # Convertir las fechas en el formato localizado (dd-mmm-aaaa)
        for campo_fecha in ['fecha_nacimiento', 'fecha_contratacion']:
            if datos_empleado.get(campo_fecha):
                fecha_formateada = datos_empleado[campo_fecha].strftime("%d/%b/%Y")
                datos_empleado[campo_fecha] = fecha_formateada

        return func(datos_empleado, *args, **kwargs)

    return wrapper

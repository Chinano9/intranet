from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Empleado, Puesto

class EmpleadosListaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        puesto = Puesto(nombre='puesto de prueba', responsabilidad = 'responsabilidad del puesto de prueba')
        puesto.save()
        empleado = {
            "nombre": "Juanito",
            "apellido_paterno": "Lopez",
            "apellido_materno": "Marquez",
            "fecha_nacimiento": "2000-08-16",
            "fecha_contratacion": "2020-10-12",
            "ciudad_residencia": "Ciudad del empleado",
            "estado_residencia": "Estado del empleado",
            "calle": "calle",
            "num_casa": "2",
            "codigo_postal": "78656",
            "email": "correo@example.com",
            "puesto": puesto,
            "tel_casa": "1232123123",
            "tel_cel": "5637368728",
            "rfc": "RFC del empleado",
            "seguro_social": "Número de seguro social del empleado",
            "curp": "CURP del empleado",
            "sueldo_texto": "Trescientos dieciocho pesos"
        }

        self.empleado_1 = Empleado.objects.create(**empleado)
        self.empleado_2 = Empleado.objects.create(nombre="María", apellido_paterno="López", fecha_nacimiento="1985-05-10", fecha_contratacion="2019-02-15", ciudad_residencia="Otra Ciudad")

    def test_lista_empleados(self):
        url = reverse("empleados-lista")  # Asegúrate de usar el nombre correcto de la URL
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # Verifica que hay dos empleados en la respuesta

    def test_filtrado_empleados(self):
        url = reverse("empleados-lista")
        query_params = {"query": "Juan"}  # Puedes ajustar el término de búsqueda aquí
        response = self.client.get(url, query_params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)  # Debe haber un empleado en la respuesta
        self.assertEqual(response.data["results"][0]["nombre"], "Juan")

    # Agrega más pruebas según sea necesario para otros casos de uso y situaciones



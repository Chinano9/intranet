from recursos_humanos.models import Puesto
import csv


def run():
    with open('scripts/res/puestos.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        #Puesto.objects.all()

        for row in reader:
            print(row)
            puesto = Puesto(nombre=row[0],
                        responsabilidad=row[1])
            puesto.save()

        print('Importacion exitosa')

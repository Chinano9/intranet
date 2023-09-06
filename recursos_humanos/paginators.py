from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class EmpleadoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def __init__(self):
        # Agrega una variable para almacenar el parámetro de búsqueda
        self.query = None
        super().__init__()

    def get_paginated_response(self, data):
        #serializer = EmpleadoPaginadoSerializer(data, many=True)
        return Response({
            'pagina_actual': self.page.number,
            'total_paginas': self.page.paginator.num_pages,
            'total_empleados': self.page.paginator.count,
            'next': self.page.number + 1 if (self.page.number + 1) <= self.page.paginator.num_pages else None,
            'prev': self.page.number - 1,
            'results': data,
        })



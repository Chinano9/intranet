# Intranet - Documentacion para Nitzia
Requisitos previos:
- Tener Python 3.11 instalado, ya sea en la maquina fisica, docker, etc.

1. Instalar por medio de pip el modulo venv.
    - Windows:  
    `pip install venv`
    - Linux:
    `pip3 install venv` o `pip install venv`

2. Crear un entorno virtual con venv.
    - Windows:
    `python -m venv venv`
    - Linux:
    `python3 -m venv venv` o `python -m venv venv`

3. Activar el entorno virtual:
    - Windows:
    `./venv/Scripts/activate`
    - Linux:
    `source venv/bin/activate`

4. Instalar las dependencias:
    - Ambas plataformas:
    `pip install -r requirements.txt`

5. Correr el programa, se abrira el puerto 8000.
    - Windows: 
    (PENDIENTE)
    - Linux:
    Servidor de pruebas:
    `python manage.py runserver`
    Servidor dedicado:
    `gunicorn intranet.wsgi`

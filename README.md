# BOGATOURS-INT2

Una aplicación para gestionar rutas turísticas en Bogotá, proporcionando información detallada sobre paradas, niveles de riesgo y sitios de interés.

## 📌 Descripción General

BOGATOURS-INT2 es una aplicación desarrollada en **Django** que permite la administración y consulta de rutas turísticas. Ofrece una interfaz intuitiva para explorar sitios de interés, ver detalles sobre paradas y aplicar filtros avanzados para facilitar la navegación.  

## 🎯 Objetivo del Proyecto

- **Facilitar la exploración turística** en Bogotá con información organizada.
- **Ofrecer una herramienta de consulta** sobre sitios turísticos, horarios y niveles de riesgo.
- **Implementar una solución escalable** que pueda ser mejorada en el futuro con nuevas funciones.

## 🌍 Público Objetivo

Está dirigido a:
- **Turistas** interesados en descubrir rutas seguras y sitios emblemáticos.
- **Agencias de viajes** que necesitan una plataforma estructurada para visualizar rutas.
- **Desarrolladores** que buscan aprender sobre integración de bases de datos y desarrollo web con Django.

---

## ⚡ Funcionalidades Principales

- **Gestión de rutas turísticas** con opciones para agregar, editar y eliminar registros.
- **Visualización de paradas y sitios de interés** con detalles relevantes.
- **Filtrado avanzado** por tipo de sitio turístico y nivel de seguridad.
- **Interfaz basada en Django** con soporte para HTML, CSS y JavaScript.
- **Soporte para recursos gráficos** en la carpeta `pro_lle/img/`.

---

## 🛠 Tecnologías y Dependencias

### 🔹 Tecnologías utilizadas
- **Django** → Framework para desarrollo web.
- **SQLite/MySQL** → Bases de datos (SQLite por defecto, con posibilidad de migración a MySQL).
- **HTML, CSS, JavaScript** → Para la interfaz web.
- **Python** → Lenguaje principal para la lógica de backend.

### 🔹 Dependencias principales (`requirements.txt`)
```plaintext
asgiref
Django
Flask
Flask-SQLAlchemy
mysql-connector-python
numpy
pandas
PyJWT
PyQt6
PyQt6-Qt6
requests
SQLAlchemy
Werkzeug```

Para instalar todas las dependencias, usa:
```
pip install -r requirements.txt

```
🚀 Instalación y Configuración

🔹 Clonar el Proyecto
```
git clone https://github.com/Jacobsame/BOGATOURS-INT2.git
cd BOGATOURS-INT2
```


🔹 Configurar el Entorno Virtual
```
python -m venv env
source env/Scripts/activate  # En Windows
source env/bin/activate      # En Linux/MacOS
pip install -r requirements.txt
```
🔹 Configuración de la Base de Datos
Por defecto, el proyecto usa SQLite, pero puedes migrarlo a MySQL modificando settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_basedatos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Luego, ejecuta las migraciones:

```
python manage.py migrate
🔹 Ejecutar el Servidor de Django
bash
python manage.py runserver
```
Accede a la aplicación en http://127.0.0.1:8000/.

📂 Estructura del Proyecto
```
/BOGATOURS-INT2
├── app/               # Contiene el punto de entrada de la aplicación
│   ├── main.py        # Archivo principal que ejecuta la lógica central
├── env/               # Entorno virtual donde se encuentran las librerías
│   ├── Lib/site-packages/  # Dependencias instaladas con pip
│   ├── Scripts/       # Archivos de activación y ejecución
│   ├── pyvenv.cfg     # Configuración del entorno virtual
├── pro_lle/img/       # Almacena imágenes esenciales para la aplicación
│   ├── cinemateca-de-bogota.jpg
│   ├── Figura-3-Mapa-de-Bogota-de-l...
│   ├── descarga (1).jpg
│   ├── descarga.png
│   ├── images.jpg
│   ├── page_1_thumb_large.webp
│   ├── ... (Otros archivos de imagen)
├── turismo_bogota/     # Carpeta principal del proyecto Django
│   ├── __init__.py     # Inicialización del módulo
│   ├── asgi.py         # Configuración para ASGI (usado en servidores asíncronos)
│   ├── settings.py     # Archivo de configuración global de Django
│   ├── urls.py         # Mapeo de rutas principales del proyecto
│   ├── wsgi.py         # Configuración WSGI para despliegue del servidor
│   ├── db.sqlite3      # Base de datos en SQLite (puede migrarse a MySQL)
│   ├── manage.py       # Comando administrativo de Django
│   ├── .env            # Variables de entorno y credenciales
│   ├── turismo_bogota/ # Subcarpeta interna con lógica de la aplicación
│   │   ├── __init__.py  # Inicialización del módulo
│   │   ├── views.py     # Lógica para el manejo de vistas dentro de la app
│   │   ├── models.py    # Definición de las tablas y estructura ORM
│   │   ├── urls.py      # Rutas específicas de la app
│   │   ├── static/      # Recursos estáticos específicos de esta sub-aplicación
│   │   ├── templates/   # Templates HTML internos de la aplicación
│   │   ├── migrations/  # Archivos de migración de Django
│   │   ├── admin.py     # Configuración del panel de administración
│   │   └── tests.py     # Pruebas unitarias del módulo
├── requirements.txt   # Listado de dependencias necesarias
└── DOCUMENTACION.md   # Documentación detallada del proyecto
```
📖 Uso de la Aplicación
Accede al servidor local: Ingresa a ```http://127.0.0.1:8000/``` en el navegador.

Explora las rutas disponibles: Usa los filtros para encontrar sitios turísticos relevantes.

Consulta detalles: Haz clic en una ruta para ver información de paradas y niveles de riesgo.

🤝 Contribuciones
Si deseas colaborar en el desarrollo:

Realiza un fork del repositorio.

Crea una nueva rama:
```
git checkout -b feature/nueva-funcionalidad
```
Agrega tus modificaciones y haz un commit.

Envía un Pull Request para revisión.

🔖 Licencia y Otros Detalles
Licencia
Este proyecto se distribuye bajo la licencia MIT, lo que permite su uso, modificación y distribución libremente bajo los términos especificados en LICENSE.

Información Adicional
Posibles Mejoras Futuras: Se considera la posibilidad de agregar funciones de personalización y tours virtuales en versiones posteriores, dependiendo de la evolución del proyecto.

Bugs Conocidos: Se documentan en la sección Issues del repositorio.

Documentación Adicional: Se podrían incluir diagramas ER y UML en futuras versiones para mejorar la comprensión de la arquitectura del proyecto.












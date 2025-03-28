# Conexión Gourmet 🍽️

## Descripción
Conexión Gourmet es una plataforma de marketplace gastronómico que conecta a vendedores de servicios gastronómicos con clientes. La plataforma permite la gestión de menús, pedidos y servicios gastronómicos de manera eficiente y segura.

## Características Principales
- 🛍️ Marketplace gastronómico completo
- 👥 Sistema de gestión de usuarios (clientes y vendedores)
- 📱 Interfaz responsiva
- 🗺️ Integración con Google Maps
- 💳 Integración con PayPal
- 📦 Sistema de gestión de pedidos
- 📋 Gestión de menús
- 📧 Sistema de notificaciones por correo

## Requisitos Previos
- Python 3.8 o superior
- PostgreSQL con PostGIS
- GDAL 3.9.2
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/conexiongourmet.git
cd conexiongourmet
```

2. Crear y activar entorno virtual:
```bash
python -m venv .venv
# En Windows
.venv\Scripts\activate
# En Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env-sample .env
# Editar .env con tus configuraciones
```

5. Instalar GDAL:
- Windows: Usar el archivo GDAL-3.9.2-cp312-cp312-win_amd64.whl proporcionado
- Linux: `sudo apt-get install python3-gdal`
- Mac: `brew install gdal`

6. Realizar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Crear superusuario:
```bash
python manage.py createsuperuser
```

8. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto
```
conexiongourmet/
├── accounts/          # Gestión de usuarios
├── vendor/           # Gestión de vendedores
├── menu/             # Gestión de menús
├── marketplace/      # Funcionalidad principal
├── customers/        # Gestión de clientes
├── orders/          # Gestión de pedidos
├── static/          # Archivos estáticos
├── templates/       # Plantillas HTML
├── media/           # Archivos multimedia
└── congourmet_main/ # Configuración principal
```

## Configuración de Variables de Entorno
Crear un archivo `.env` con las siguientes variables:
```
DEBUG=True
SECRET_KEY=tu-clave-secreta
DB_NAME=nombre_db
DB_USER=usuario_db
DB_PASSWORD=contraseña_db
DB_HOST=localhost
DB_PORT=5432
GOOGLE_API_KEY=tu-api-key
PAYPAL_CLIENT_ID=tu-client-id
```

## Tecnologías Utilizadas
- Django 3.2.5
- PostgreSQL con PostGIS
- GDAL 3.9.2
- Python 3.8+
- HTML5/CSS3
- JavaScript
- Bootstrap

## Contribución
1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Link del Proyecto: [https://github.com/JeffCode2022/ConexionGourmet](https://github.com/JeffCode2022/conexionGourmet) 

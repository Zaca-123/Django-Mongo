🗄️ Django-Mongo
Proyecto académico para el práctico de Bases de Datos (Ingeniería en Sistemas, UTN FRVM). Basado en el trabajo del profe fábrica de pastasEsta versión utiliza Django con MongoDB como base de datos, todo orquestado con Docker.

🚀 Puesta en marcha
1. Clona el repositorio
git clone https://github.com/Zaca-123/Django-Mongo.git
cd Django-Mongo
2. Genera la estructura del proyecto y levanta el backend
docker compose run --rm generate
sudo chown $USER:$USER -R .
docker compose up -d backend
3. Crea un superusuario para el admin
docker compose run --rm manage createsuperuser
4. Carga datos iniciales
docker compose run --rm manage loaddata datos.json
🔄 Migración a MongoDB
Este repositorio muestra cómo migrar tu proyecto Django para que utilice MongoDB como base de datos principal, usando Docker, djongo y las mejores prácticas para un entorno de desarrollo moderno.

1. Agregar MongoDB al docker-compose.yml
Incorporá el servicio de MongoDB al archivo docker-compose.yml:

mongo:
  image: mongo:latest
  container_name: mongo
  environment:
    - MONGO_INITDB_ROOT_USERNAME=mongo
    - MONGO_INITDB_ROOT_PASSWORD=mongo
    - MONGO_INITDB_DATABASE=mongo
  volumes:
    - mongo-data:/data/db
  ports:
    - "27017:27017"
  networks:
    - net

volumes:
  mongo-data:
2. Modificar el models.py
Reemplazá la importación de models de Django tradicional por:

from djongo import models
Haz este cambio en todos los archivos models.py de tus apps.

3. Configurar MongoDB en settings.py
Ajustá la configuración de base de datos para que apunte a MongoDB:

DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "mongo",
        "CLIENT": {
            "host": "mongo",
            "port": 27017,
            "username": "mongo",
            "password": "mongo",
            "authSource": "admin",  # Importante
        },
    },
    # (Opcional) Base de datos anterior, por si necesitas migrar datos
    "old_db": {
        "ENGINE": "django.db.backends.postgresql",  # O la que uses
        "NAME": "nombre_db_anterior",
        "USER": "usuario_anterior",
        "PASSWORD": "contraseña_anterior",
        "HOST": "host_anterior",
        "PORT": "puerto_anterior",
    },
}
4. Limpiar migraciones anteriores
Eliminá todos los archivos dentro del directorio app/migrations/, excepto init.py, para evitar conflictos con las migraciones antiguas.

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
5. Reconstruir la imagen Docker
Ejecutá el siguiente comando para reconstruir los servicios:

docker compose build
6. Levantar servicios con MongoDB
Iniciá todos los contenedores:

docker compose up -d
7. Migrar modelos a MongoDB
Creá y aplicá las nuevas migraciones:

docker compose run manage makemigrations
docker compose run manage migrate
8. Crear nuevamente el superusuario
Generá un nuevo superusuario para acceder al admin:

docker compose run --rm manage createsuperuser
9. Ejecutar comando personalizado de migración
Si creaste un comando personalizado para migrar datos de PostgreSQL a MongoDB, ejecutalo:

docker compose run --rm manage migrate_to_mongo
✅ ¡Listo! Ahora tus datos y modelos están migrados a MongoDB. Puedes acceder al panel de administración en http://localhost:8000/admin usando las credenciales creadas en el paso anterior.

🤝 Créditos y Licencia
Mantenido por: Grupo 12
Basado en el repositorio: fábrica de pastas
El código se entrega "tal cual", sin garantías. Si te es útil, considera dar feedback.


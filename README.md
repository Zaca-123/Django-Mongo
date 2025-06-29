# 🗄️ Django-Mongo
Proyecto académico para el práctico de Bases de Datos (Ingeniería en Sistemas, UTN FRVM).
Basado en el trabajo del profe fábrica de pastas
Esta versión utiliza Django con MongoDB como base de datos, todo orquestado con Docker.

# 🚀 Puesta en marcha rápida

## 1. Clona el repositorio
````bash
git clone https://github.com/Zaca-123/Django-Mongo.git
cd Django-Mongo
````
## 2. Genera la estructura del proyecto y levanta el backend
````bash
docker compose run --rm generate
sudo chown $USER:$USER -R .
docker compose up -d backend
````
## 3. (Opcional) Crea un superusuario para el admin
````bash
docker compose run --rm manage createsuperuser
````
## 4. (Opcional) Carga datos iniciales
````bash
docker compose run --rm manage loaddata datos.json
````
👉 Accede a http://localhost:8000/admin para gestionar la app con el usuario creado.


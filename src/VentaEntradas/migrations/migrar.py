import psycopg2
from pymongo import MongoClient

# Conexión a PostgreSQL
pg_conn = psycopg2.connect(
    dbname='tu_basedatos',
    user='tu_usuario',
    password='tu_contraseña',
    host='localhost',
    port=5432
)
pg_cursor = pg_conn.cursor()

# Conexión a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['miBase']
mongo_col = mongo_db['clientes']

# Consulta para obtener datos
pg_cursor.execute("SELECT id, nombre, email FROM clientes;")
rows = pg_cursor.fetchall()

# Insertar datos en MongoDB
for row in rows:
    doc = {
        "_id": row[0],
        "nombre": row[1],
        "email": row[2]
    }
    mongo_col.insert_one(doc)

pg_cursor.close()
pg_conn.close()

print("Migración finalizada")

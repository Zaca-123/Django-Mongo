import psycopg2
from pymongo import MongoClient

# 📌 1. Conexión a PostgreSQL
pg_conn = psycopg2.connect(
    dbname='VentaEntrada',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
pg_cursor = pg_conn.cursor()

# 📌 2. Conexión a MongoDB
mongo_client = MongoClient("localhost", 27017)
mongo_db = mongo_client["VentaEntrada"]

# Función utilitaria para migrar una tabla
def migrar_tabla(nombre_tabla, query_sql, transformador):
    print(f"Migrando {nombre_tabla}...")
    pg_cursor.execute(query_sql)
    rows = pg_cursor.fetchall()
    docs = [transformador(row) for row in rows]
    if docs:
        mongo_db[nombre_tabla].insert_many(docs)
    print(f"{len(docs)} documentos insertados en {nombre_tabla}.")

# Transformadores para cada tabla
migrar_tabla("tipo_dni", "SELECT id, descripcion FROM tipo_dni", lambda r: {
    "_id": r[0],
    "descripcion": r[1]
})

migrar_tabla("cliente", "SELECT id, nombre, apellido, dni, tipo_dni_id FROM cliente", lambda r: {
    "_id": r[0],
    "nombre": r[1],
    "apellido": r[2],
    "dni": r[3],
    "tipo_dni_id": r[4]
})

migrar_tabla("evento", "SELECT id, nombre, fecha, lugar FROM evento", lambda r: {
    "_id": r[0],
    "nombre": r[1],
    "fecha": str(r[2]),
    "lugar": r[3]
})

migrar_tabla("entrada", "SELECT id, evento_id, precio FROM entrada", lambda r: {
    "_id": r[0],
    "evento_id": r[1],
    "precio": float(r[2])
})

migrar_tabla("medio_de_pago", "SELECT id, nombre FROM medio_de_pago", lambda r: {
    "_id": r[0],
    "nombre": r[1]
})

migrar_tabla("venta", "SELECT id, cliente_id, medio_pago_id, fecha FROM venta", lambda r: {
    "_id": r[0],
    "cliente_id": r[1],
    "medio_pago_id": r[2],
    "fecha": str(r[3])
})

migrar_tabla("detalle_de_venta", "SELECT id, venta_id, entrada_id, cantidad FROM detalle_de_venta", lambda r: {
    "_id": r[0],
    "venta_id": r[1],
    "entrada_id": r[2],
    "cantidad": r[3]
})

# Cerrar conexiones
pg_cursor.close()
pg_conn.close()
mongo_client.close()

print("✅ Migración finalizada.")

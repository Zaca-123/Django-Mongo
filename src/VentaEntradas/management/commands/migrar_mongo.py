import time # Importar time para los delays
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import connections, OperationalError # Importar OperationalError

class Command(BaseCommand):
    help = "Migra todos los datos de old_db (PostgreSQL) a default (MongoDB)"

    def handle(self, *args, **kwargs):
        app_label = "VentaEntradas"
        models = apps.get_app_config(app_label).get_models()
        self.stdout.write(self.style.SUCCESS("Iniciando migración de datos..."))

        # --- SECCIÓN DE ESPERA Y RETRY PARA LA CONEXIÓN old_db ---
        self.stdout.write(self.style.WARNING("\n--- Verificando conexión a old_db ---"))
        max_retries = 10
        retry_delay = 5 # segundos
        connected_to_old_db = False

        for i in range(max_retries):
            try:
                conn = connections['old_db']
                if not conn.is_usable():
                    conn.close_if_unusable_connection() # Cierra la conexión si está rota
                    conn.connect() # Intenta reconectar
                
                # Intentar una consulta simple para asegurar que la DB esté lista
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS(f"Conexión a old_db establecida en intento {i+1}."))
                connected_to_old_db = True
                break # Salir del bucle si la conexión es exitosa
            except OperationalError as e: # Capturar el error específico de la DB
                self.stdout.write(self.style.WARNING(f"Intento {i+1}/{max_retries}: old_db aún no lista o no accesible ({e}). Esperando {retry_delay} segundos..."))
                time.sleep(retry_delay)
            except Exception as e: # Capturar cualquier otro error inesperado
                self.stdout.write(self.style.ERROR(f"Intento {i+1}/{max_retries}: Error inesperado al conectar a old_db: {e}. Esperando {retry_delay} segundos..."))
                time.sleep(retry_delay)

        if not connected_to_old_db:
            self.stdout.write(self.style.ERROR("¡Error crítico! No se pudo conectar a old_db después de varios intentos. Abortando migración."))
            return # Salir si no se puede conectar

        self.stdout.write(self.style.WARNING("----------------------------------\n"))
        # --- FIN SECCIÓN DE ESPERA Y RETRY ---


        # Opcional: ordena los modelos para primero migrar los que no tienen FKs
        models = sorted(models, key=lambda m: len(m._meta.fields))

        for model in models:
            model_name = model.__name__
            table_name = model._meta.db_table # Obtiene el nombre de la tabla en la DB
            self.stdout.write(f"Migrando modelo: {model_name} (Tabla en DB: {table_name})")

            # Obtiene todos los objetos de old_db
            try:
                # Ya que la conexión ha sido verificada, esta línea debería funcionar
                objs = list(model.objects.using("old_db").all())
                total = len(objs)
                self.stdout.write(f"   Filas encontradas en {model_name}: {total}") # <--- Verificando las filas

                if total == 0:
                    self.stdout.write(f"   No hay datos para migrar en {model_name}.")
                    continue

                migrated = 0
                # ... (resto de tu lógica de migración, que se mantiene igual) ...
                for obj in objs:
                    # Clona el objeto
                    obj.pk = obj.pk
                    obj._state.db = "default"
                    try:
                        obj.save(using="default", force_insert=True)
                        migrated += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"   Error migrando {obj}: {e}"))
                self.stdout.write(
                    self.style.SUCCESS(
                        f"   Migrados {migrated}/{total} objetos de {model_name}"
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error al leer datos del modelo {model_name} desde old_db: {e}"))


        self.stdout.write(self.style.SUCCESS("¡Migración completa!"))
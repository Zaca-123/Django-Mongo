import os
import json
import mongoengine
from VentaEntradas.models import Cliente, TipoDNI, MedioDePago, Evento, Entrada, Venta, DetalleDeVenta  


mongoengine.connect(
    db='VentaEntrada',  
    host='localhost',         
    port=27017                
)

def exportar_modelo(modelo, nombre_archivo):
    print(f"Exportando {modelo.__name__}...")
    datos = [doc.to_mongo().to_dict() for doc in modelo.objects()]
    for d in datos:
        d.pop("_id", None)  
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, default=str)
    print(f"{len(datos)} documentos exportados a {nombre_archivo}")

if __name__ == "__main__":
    exportar_modelo(Cliente, "clientes.json")
    exportar_modelo(TipoDNI, "tipos_dni.json")
    exportar_modelo(MedioDePago, "medios_de_pago.json")
    exportar_modelo(Evento, "eventos.json")
    exportar_modelo(Entrada, "entradas.json")
    exportar_modelo(Venta, "ventas.json")
    exportar_modelo(DetalleDeVenta, "detalles_de_venta.json")

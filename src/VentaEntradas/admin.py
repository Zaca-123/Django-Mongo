from django.contrib import admin
from .models import (
    TipoDNI,
    Cliente,
    MedioDePago,
    Evento,
    Entrada,
    Venta,
    DetalleDeVenta,
)

@admin.register(TipoDNI)
class TipoDNIAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'nro_dni', 'tipo_dni')
    search_fields = ('nombre', 'apellido', 'nro_dni')
    list_filter = ('tipo_dni',)

@admin.register(MedioDePago)
class MedioDePagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion')
    search_fields = ('descripcion',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha', 'hora', 'capacidad')
    search_fields = ('nombre',)
    list_filter = ('fecha',)

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'precio', 'evento')
    search_fields = ('descripcion',)
    list_filter = ('evento',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'importe', 'medio_de_pago', 'cliente')
    search_fields = ('cliente__nombre', 'cliente__apellido')
    list_filter = ('medio_de_pago', 'fecha')

@admin.register(DetalleDeVenta)
class DetalleDeVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'cant_entradas', 'importe_unitario', 'venta', 'entrada')
    search_fields = ('descripcion',)
    list_filter = ('venta', 'entrada')

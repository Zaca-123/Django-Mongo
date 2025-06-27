from mongoengine import (
    Document, StringField, IntField, ReferenceField,
    DateField, DateTimeField, DecimalField
)

class TipoDNI(Document):
    nombre = StringField(max_length=50, required=True)

    def __str__(self):
        return self.nombre

class Cliente(Document):
    nombre = StringField(max_length=100, required=True)
    apellido = StringField(max_length=100, required=True)
    nro_dni = IntField(required=True)
    tipo_dni = ReferenceField(TipoDNI, required=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class MedioDePago(Document):
    descripcion = StringField(max_length=100, required=True)

    def __str__(self):
        return self.descripcion

class Evento(Document):
    nombre = StringField(max_length=100, required=True)
    descripcion = StringField()
    fecha = DateField(required=True)
    hora = DateTimeField(required=True)
    capacidad = IntField(required=True)

    def __str__(self):
        return self.nombre

class Entrada(Document):
    descripcion = StringField(max_length=100, required=True)
    precio = DecimalField(precision=2, required=True)
    evento = ReferenceField(Evento, required=True)

    def __str__(self):
        return self.descripcion

class Venta(Document):
    fecha = DateField(required=True)
    hora = DateTimeField(required=True)
    importe = DecimalField(precision=2, required=True)
    medio_de_pago = ReferenceField(MedioDePago, required=True)
    cliente = ReferenceField(Cliente, required=True)

    def __str__(self):
        return f"Venta {str(self.id)} - {self.fecha}"

class DetalleDeVenta(Document):
    descripcion = StringField(max_length=100, required=True)
    cant_entradas = IntField(required=True)
    importe_unitario = DecimalField(precision=2, required=True)
    venta = ReferenceField(Venta, required=True)
    entrada = ReferenceField(Entrada, required=True)

    def __str__(self):
        return self.descripcion

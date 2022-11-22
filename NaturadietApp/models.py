from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from ckeditor.fields import RichTextField
from .choices import *


class Caloria(models.Model):
    id_caloria = models.AutoField(db_column='ID_CALORIA', primary_key=True)  
    persona = models.CharField(db_column='PERSONA', max_length=30, choices=PERSONA_CHOICES, default=PERSONA_CHOICES[0], null=True)  
    genero = models.CharField(db_column='GENERO', max_length=30, choices=GENERO_CHOICES, default=GENERO_CHOICES[0], null=True)  
    edad_min = models.IntegerField(db_column='EDAD_MIN', blank=True, null=True)  
    edad_max = models.IntegerField(db_column='EDAD_MAX', blank=True, null=True)  
    calorias = models.IntegerField(db_column='CALORIAS', blank=True, null=True) 

    class Meta:
        db_table = 'CALORIA'

    def __str__(self):
        return 'ID: %s, %s, %s, Edad(%s-%s) KCAL: %s' % (self.id_caloria, self.persona, self.genero, self.edad_min, self.edad_max, self.calorias)


class Dieta(models.Model):
    id_dieta = models.AutoField(db_column='ID_DIETA', primary_key=True)  
    lunes = RichTextField(db_column='LUNES')  
    martes = RichTextField(db_column='MARTES')  
    miercoles = RichTextField(db_column='MIERCOLES')  
    jueves = RichTextField(db_column='JUEVES')  
    viernes = RichTextField(db_column='VIERNES')  
    sabado = RichTextField(db_column='SABADO')  
    domingo = RichTextField(db_column='DOMINGO')  
    kcal = models.ForeignKey(Caloria, db_column='KCAL', on_delete=models.CASCADE)  

    class Meta:
        db_table = 'DIETA'

    def __str__(self):
        return 'ID: %s, kcal: %s' % (self.id_dieta, self.kcal)


class Estado(models.Model):
    id_estado = models.AutoField(db_column='ID_ESTADO', primary_key=True)  
    minimo = models.DecimalField(db_column='MINIMO', max_digits=3, decimal_places=1) 
    maximo = models.DecimalField(db_column='MAXIMO', max_digits=3, decimal_places=1)  
    tipo = models.CharField(db_column='TIPO', max_length=45)  
    descripcion = RichTextField(db_column='DESCRIPCION', null=True)  

    class Meta:
        db_table = 'ESTADO'
    
    def __str__(self):
        return 'ID: %s, Mínimo: %s, Máximo: %s, Tipo: %s' % (self.id_estado, self.minimo, self.maximo, self.tipo)




class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='ID_CATEGORIA', primary_key=True)
    nombre = models.CharField(db_column='NOMBRE', max_length=50)

    class Meta:
        db_table = 'CATEGORIA'

    def __str__(self):
        return '%s' % (self.nombre)



class Noticia(models.Model):
    id_noticia = models.AutoField(db_column='ID_NOTICIA', primary_key=True)  
    titulo = models.CharField(db_column='TITULO', max_length=255)  
    subtitulo = models.CharField(db_column='SUBTITULO', max_length=255)  
    imagen = models.ImageField(db_column='IMAGEN', upload_to='Noticias')
    contenido = RichTextField(db_column='CONTENIDO', max_length=1000)  
    usuario = models.ForeignKey('Usuario', db_column='USUARIO', on_delete=models.CASCADE)  
    categoria = models.ForeignKey('Categoria', db_column='CATEGORIA', on_delete=models.CASCADE)
    created = models.DateTimeField(db_column='CREATED', auto_now_add=True)
    
    class Meta:
        db_table = 'NOTICIA'

    def __str__(self):
        return 'ID:%s, Título:%s, Usuario:%s' % (self.id_noticia, self.titulo, self.usuario)


class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(db_column='ID_CATEGORIA', primary_key=True)
    nombre = models.CharField(db_column='NOMBRE', max_length=50)

    class Meta:
        db_table = 'CATEGORIA_PRODUCTO'

    def __str__(self):
        return '%s' % (self.nombre)


class Producto(models.Model):
    id_producto = models.AutoField(db_column='ID_PRODUCTO', primary_key=True)  
    nombre = models.CharField(db_column='NOMBRE', max_length=255)  
    imagen = models.ImageField(db_column='IMAGEN', upload_to='Productos')
    descripcion = RichTextField(db_column='DESCRIPCION', max_length=255, blank=True, null=True) 
    categoria = models.ForeignKey('CategoriaProducto', db_column='CATEGORIA', on_delete=models.CASCADE)
    precio = models.DecimalField(db_column='PRECIO', max_digits=5, decimal_places=2)  
    disponibilidad = models.BooleanField(db_column='DISPONIBILIDAD', default=True)

    class Meta:
        db_table = 'PRODUCTO'

    def __str__(self):
        return '%s' % (self.nombre)



class Rol(models.Model):
    id_rol = models.AutoField(db_column='ID_ROL', primary_key=True)  
    nombre = models.CharField(db_column='NOMBRE', max_length=45) 

    class Meta:
        db_table = 'ROL'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    edad = models.IntegerField(db_column='EDAD')  
    dni = models.CharField(db_column='DNI', max_length=11, null=True)  
    telefono = models.CharField(db_column='TELEFONO', max_length=12, null=True)  
    direccion = models.CharField(db_column='DIRECCION', max_length=50, null=True)  
    localidad = models.CharField(db_column='LOCALIDAD', max_length=50, null=True)  
    provincia = models.CharField(db_column='PROVINCIA', max_length=30, choices=PROVINCIA_CHOICES, null=True)  
    cp = models.CharField(db_column='CP', max_length=5, null=True)  
    peso = models.IntegerField(db_column='PESO')  
    altura = models.DecimalField(db_column='ALTURA', max_digits=3, decimal_places=2) 
    imc = models.DecimalField(db_column='IMC', max_digits=3, decimal_places=1, blank=True, null=True)  
    genero = models.CharField(db_column='GENERO', max_length=30, choices=GENERO_CHOICES, default=GENERO_CHOICES[0])  
    rol = models.ForeignKey('Rol', db_column='ROL', on_delete=models.CASCADE, default=2, null=True)  
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=500, blank=True, null=True)
    estado = models.ForeignKey('Estado', db_column='ESTADO', on_delete=models.CASCADE, blank=True, null=True)  
    dieta = models.ManyToManyField('Dieta', db_column='DIETA', blank=True)  

    

    class Meta:
        db_table = 'USUARIO'
    
    

class Pedido(models.Model):
    id_pedido = models.AutoField(db_column='ID_PEDIDO', primary_key=True)  
    usuario = models.ForeignKey('Usuario', db_column='USUARIO', on_delete=models.CASCADE)  
    fecha = models.DateTimeField(auto_now_add=True, db_column='FECHA')  
    total = models.DecimalField(db_column='IMPORTE', max_digits=5, decimal_places=2, blank=True, null=True)
    entregado = models.BooleanField(db_column='ENTREGADO', default=False)


    class Meta:
        db_table = 'PEDIDO'

    def __str__(self):
        return '%s' % (self.id_pedido)



class Factura(models.Model):
    pedido = models.ForeignKey('Pedido', db_column='PEDIDO', on_delete=models.CASCADE)  
    producto = models.ForeignKey('Producto', db_column='PRODUCTO', on_delete=models.CASCADE) 
    importe = models.DecimalField(db_column='IMPORTE', max_digits=5, decimal_places=2, blank=True, null=True) 
    cantidad = models.IntegerField(db_column='CANTIDAD', blank=True, null=True) 

    class Meta:
        db_table = 'FACTURA'
        unique_together = (('pedido', 'producto'))


    def __str__(self):
        return '%s,%s,%s,%s' % (self.pedido, self.producto, self.importe, self.cantidad)

from django.contrib import admin

from .models import *
from .forms import UsuarioCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Usuario
    add_form = UsuarioCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Más datos',
            {
                'fields': (
                    'edad',
                    'dni',
                    'telefono',
                    'direccion',
                    'localidad',
                    'provincia',
                    'cp',
                    'peso',
                    'altura',
                    'imc',
                    'genero',
                    'rol',
                    'estado',
                    'dieta',
                    'descripcion',
                )
            }
        )
    )

class UsuarioAdmin(admin.ModelAdmin):
    list_display=("id", "username", "first_name", "last_name", "email", "is_staff", "is_active")

class EstadoAdmin(admin.ModelAdmin):
    list_display=("id_estado", "minimo", "maximo", "tipo")

class NoticiaAdmin(admin.ModelAdmin):
    list_display=("id_noticia", "titulo", "usuario")

class ProductoAdmin(admin.ModelAdmin):
    list_display=("id_producto", "nombre", "categoria", "precio", "disponibilidad")

class CategoriaAdmin(admin.ModelAdmin):
    list_display=("id_categoria", "nombre")

class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display=("id_categoria", "nombre")

class CaloriaAdmin(admin.ModelAdmin):
    list_display=("id_caloria", "persona", "genero", "edad_min", "edad_max", "calorias")

class DietaAdmin(admin.ModelAdmin):
    list_display=("id_dieta", "kcal")

class PedidoAdmin(admin.ModelAdmin):
    list_display=("id_pedido", "usuario", "fecha", "total")

class FacturaAdmin(admin.ModelAdmin):
    list_display=("pedido", "producto", "cantidad", "importe")

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Rol)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Dieta, DietaAdmin)
admin.site.register(Caloria, CaloriaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(CategoriaProducto, CategoriaProductoAdmin)



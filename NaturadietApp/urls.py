from django.urls import path, include
from NaturadietApp import views
from django.conf import settings
from django.conf.urls.static import static


 
urlpatterns = [
    path('', views.Home, name="Home"),
    
    #Usuario
    path('perfil/actualizar', views.ActualizarUsuarioView, name="Actualizar"),
    path('eliminar', views.EliminarUsuarioView, name="Eliminar"),
    path('perfil', views.PerfilUsuarioView, name="Perfil"),
    
    #Noticias
    path('noticias', views.NoticiasView, name="Noticias"),
    path('noticias/<id_noticia>', views.NoticiaView, name="Noticia"),
    path('noticias/categoria/<nombre>', views.CategoriaView, name="Categoria"),
    
    #Productos
    path('productos', views.ProductosView, name="Productos"),
    path('productos/<nombre>', views.CategoriaProductoView, name="CategoriaProducto"),
    
    #Dieta
    path('dieta', views.DietaView, name="Dieta"),

    #Login
    path('login', views.Login, name="Login"),
    path('logout', views.salir, name="Logout"),
    path('recovery', views.RecuperarPass, name="RecuperarPass"),

    #Contacto
    path('contacto', views.Contacto, name="Contacto"),

    #Registro
    path('registro', views.Registro, name="Registro"),

    #Carrito
    path('carro', views.CarroView, name="Carro"),
    path('productos/agregar/<int:id_producto>', views.Agregar_producto, name="Agregar"),
    path('carro/aumentar/<int:id_producto>', views.Aumentar_producto, name="Aumentar"),
    path('carro/restar/<int:id_producto>', views.Restar_producto, name="Restar"),
    path('carro/eliminar/<int:id_producto>', views.Eliminar_producto, name="Eliminar"),
    path('carro/limpiar', views.Limpiar_carro, name="Limpiar"),
    path('carro/pagado', views.ComprarView, name="Comprar"),

    #Pedidos
    path('perfil/pedidos', views.PedidosView, name="Pedidos"),

    #Sobre MI
    path('sobreMi', views.SobreMiView, name="SobreMi"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


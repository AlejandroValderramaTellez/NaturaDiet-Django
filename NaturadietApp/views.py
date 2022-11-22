from django.contrib import messages
from NaturadietApp.forms import CustomUserCreationForm, DietaForm
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .carro import Carro
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator

# Create your views here.


#----------------------------------------------------------------


#home
def Home(request):
    total = Noticia.objects.all().count()
    noticias1 = Noticia.objects.filter(id_noticia__gte=total-2, id_noticia__lte=total).order_by('-id_noticia')
    noticias2 = Noticia.objects.filter(id_noticia__gte=total-5, id_noticia__lte=total-3).order_by('-id_noticia')
    noticias3 = Noticia.objects.filter(id_noticia__gte=total-8, id_noticia__lte=total-6).order_by('-id_noticia')
    
    return render(request, "NaturadietApp/home.html", {"noticias1": noticias1, "noticias2": noticias2, "noticias3": noticias3})



#----------------------------------------------------------------


#usuario
@login_required(login_url='Login')
def ActualizarUsuarioView(request):
    usuario = Usuario.objects.get(id=request.user.id)
    form = CustomUserCreationForm(instance=usuario)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            if usuario.id != form.cleaned_data['password1']:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, user)

            messages.success(request, f'Usuario actualizado')

    data = {'form': form}
    
    return render(request, "NaturadietApp/actualizar.html", data)




#----------------------------------------------------------------

#Vista de toda las noticias
def NoticiasView(request):
    categorias = Categoria.objects.all()
    lista = Noticia.objects.all().order_by('-id_noticia')
    
    paginator = Paginator(lista, 6)
    pagina = request.GET.get("page") or 1
    noticias = paginator.get_page(pagina)
    pagina_actual = int(pagina)
    paginas = range(1, noticias.paginator.num_pages + 1)

    return render(request, "NaturadietApp/noticias.html", {"categorias": categorias,"noticias": noticias, "paginas": paginas, "pagina_actual": pagina_actual})




#----------------------------------------------------------------

#Vista de una noticia
def NoticiaView(request, id_noticia):
    categorias = Categoria.objects.all()
    noticia = Noticia.objects.get(id_noticia = id_noticia)
    noticias = Noticia.objects.all().order_by('-id_noticia')[:5]
    return render(request, "NaturadietApp/noticia.html", {"noticia": noticia, "noticias": noticias, "categorias": categorias})



#----------------------------------------------------------------


#Vista de toda las noticias de una categoría
def CategoriaView(request, nombre):
    categorias = Categoria.objects.all()
    categoria = Categoria.objects.get(nombre = nombre)
    noticias = Noticia.objects.filter(categoria = categoria.id_categoria).order_by('-id_noticia')
    
    return render(request, "NaturadietApp/categoria.html", {"noticias": noticias, "categoria": categoria, "categorias": categorias})




#----------------------------------------------------------------


#Vista de todos los productos (Requiere estar logueado)
@login_required(login_url='Login')
def ProductosView(request):
    categorias = CategoriaProducto.objects.all()
    lista = Producto.objects.all().order_by('-id_producto')

    paginator = Paginator(lista, 9)
    pagina = request.GET.get("page") or 1
    productos = paginator.get_page(pagina)
    pagina_actual = int(pagina)

    paginas = range(1, productos.paginator.num_pages + 1)
    
    return render(request, "NaturadietApp/productos.html", {"productos": productos, "categorias": categorias, "paginas": paginas, "pagina_actual": pagina_actual})



#----------------------------------------------------------------



#Vista de todos los productos de una categoría (Requiere estar logueado)
@login_required(login_url='Login')
def CategoriaProductoView(request, nombre):
    categorias = CategoriaProducto.objects.all()
    categoria = CategoriaProducto.objects.get(nombre = nombre)
    productos = Producto.objects.filter(categoria = categoria.id_categoria).order_by('-id_producto')
    
    return render(request, "NaturadietApp/categoriaProductos.html", {"productos": productos, "categorias": categorias ,"categoria": categoria})




#----------------------------------------------------------------



#Vista del carro de la compra (Requiere estar logueado)
@login_required(login_url='Login')
def CarroView(request):
    return render(request, "NaturadietApp/carro.html")




#Agrega producto desde la tienda (Requiere estar logueado)
@login_required(login_url='Login')
def Agregar_producto(request, id_producto):
    carro = Carro(request)
    producto = Producto.objects.get(id_producto = id_producto)
    carro.agregar(producto=producto)
    messages.success(request, "Producto agregado al carrito")
    return redirect("Productos")




#Elimina producto desde el carrito de la compra (Requiere estar logueado)
@login_required(login_url='Login')
def Eliminar_producto(request, id_producto):
    carro = Carro(request)
    producto = Producto.objects.get(id_producto = id_producto)
    carro.eliminar(producto=producto)
    return redirect("Carro")




#Aumenta und cantidad de producto desde el carrito de compra (Requiere estar logueado)
@login_required(login_url='Login')
def Aumentar_producto(request, id_producto):
    carro = Carro(request)
    producto = Producto.objects.get(id_producto = id_producto)
    carro.aumentar_producto(producto=producto)
    return redirect("Carro")





#Quita und cantidad de producto desde el carrito de compra (Requiere estar logueado)
@login_required(login_url='Login')
def Restar_producto(request, id_producto):
    carro = Carro(request)
    producto = Producto.objects.get(id_producto = id_producto)
    carro.restar_producto(producto=producto)
    return redirect("Carro")





#Vacia el carrito de la compra (Requiere estar logueado)
@login_required(login_url='Login')
def Limpiar_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    return redirect("Carro")




#----------------------------------------------------------------




#Calcula el IMC, asigna dietas, IMC, estado y actualiza datos del usuario (peso, altura y edad)
@login_required(login_url='Login')
def DietaView(request):
    usuario = Usuario.objects.get(id=request.user.id)
    form = DietaForm(instance=usuario)

    estado = ''
    dietas = ''
    imc = ''
    alerta = ''

    if request.method == 'POST':
        form = DietaForm(request.POST)
        peso = float(request.POST['peso'])
        altura = float(request.POST['altura'])
        edad = request.POST['edad']

        if peso != usuario.peso or altura != usuario.altura or edad != usuario.edad:
            usuario.peso = peso
            usuario.altura = altura
            usuario.edad = edad
            

        imc = round(peso / (altura*altura),1)
        estado = Estado.objects.filter(minimo__lte=imc, maximo__gte=imc)
        tipo = estado.values()[0]['tipo']
        caloria = Caloria.objects.filter(edad_min__lte=edad, edad_max__gte=edad, genero=usuario.genero)
        dietas = Dieta.objects.filter(kcal__in=caloria)
        
        usuario.imc = imc
        usuario.estado = Estado.objects.get(tipo = tipo)
        usuario.dieta.set(dietas)

        usuario.save()

        if tipo == "Bajopeso" or tipo == "Obesidad 1" or tipo == "Obesidad 2" or tipo == "Obesidad Morbida" or tipo == "Obesidad Extrema":
            alerta = "alert-danger"
        if tipo == "Normopeso":
            alerta = "alert-success"
        if tipo == "Sobrepeso 1" or tipo == "Sobrepeso 2":
            alerta = "alert-warning"


    return render(request, "NaturadietApp/dieta.html", {"form": form, "estado": estado, "dietas": dietas, "imc": imc, "alerta": alerta})



#----------------------------------------------------------------




#Vista del login 
def Login(request):
    if request.method == "POST":
        name = request.POST['usuario']
        password = request.POST['password']
        usuario = authenticate(username=name, password=password)

        if usuario is not None:
            login(request, usuario)
            messages.success(request, f"Bienvenid@ {name}")
            request.session["carro"] = {}
            return redirect(to="Home")
        else:
            messages.error(request, "Los datos son incorrectos")

    return render(request, "NaturadietApp/login.html")



#----------------------------------------------------------------


#Vista para desloguearse
def salir(request):
    usuario = request.user.username
    logout(request)
    messages.success(request, f"Hasta pronto {usuario} ")
    return redirect(to="Home")



#----------------------------------------------------------------



#Vista del formulario de contacto
def Contacto(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        asunto = request.POST['asunto']
        email = request.POST['email']
        mensaje = request.POST['mensaje'] + "\n\n\n" + nombre + ":  " + email

        #Si los imputs están vacios muestra aviso 
        if not nombre or not asunto or not mensaje or not email:
            messages.error(request, f"No puede haber campos vacíos.")
            return render(request, "NaturadietApp/contacto.html")


        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['Naturadiet2021@gmail.com']
        send_mail(asunto, mensaje, email_from, recipient_list)
        messages.success(request, f"Su mensaje ha sido enviado. Gracias!")

    return render(request, "NaturadietApp/contacto.html")




#----------------------------------------------------------------



#Vista del registro de usuario
def Registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            name = formulario.cleaned_data['username']
            user = authenticate(username=name, password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, f"Bienvenid@ {name}")
            return redirect(to="Home")

        data["form"] = formulario
        
    return render(request, "NaturadietApp/registro.html", data)




#----------------------------------------------------------------




def EliminarUsuarioView(request):
    usuario = Usuario.objects.get(id=request.user.id)
    usuario.delete()
    messages.success(request, f'Usuario Eliminado')

    return redirect(to="Home")





#----------------------------------------------------------------



#Vista para comprar el carrito, creando un pedido y una factura de ese pedido
def ComprarView(request):

    if not request.session["carro"]:
        messages.success(request, f'El carrito está vacío')
        return render(request, "NaturadietApp/carro.html")
    
    usuario = Usuario.objects.get(id=request.user.id) #Creo y guardo en BD un pedido del usuario logueado
    pedido = Pedido(usuario = usuario) 
    pedido.save()

    total = 0

    #Creo y guardo en BD una factura del pedido y almaceno los productos del carro, caculando el importe segun su cantidad
    for key, value in request.session["carro"].items(): 
        importe = 0
        id = int(value["id_producto"])
        producto = Producto.objects.get(id_producto = id)
        precio = float(value["precio"])
        cantidad = float(value["cantidad"])
        importe = round(importe + precio * cantidad,2)
        total += importe

        factura = Factura(pedido = pedido, producto = producto, cantidad = cantidad, importe = importe)
        factura.save()

    #Obtengo el total del carro y actualizo el pedido
    pedido.total = total
    pedido.save()

    #Vacio la sesion del carro
    request.session["carro"] = {}
    messages.success(request, f'Pedido realizado')

    return render(request, "NaturadietApp/carro.html")




#----------------------------------------------------------------




def PedidosView(request):
    usuario = Usuario.objects.get(id=request.user.id)
    pedidos = Pedido.objects.filter(usuario = usuario)
    facturas = []

    for pedido in pedidos:
        factura = Factura.objects.filter(pedido = pedido)
        facturas.append(factura)

    p = tuple(zip(pedidos, facturas))
    
    return render(request, "NaturadietApp/pedidos.html", {'pedidos': p})




#----------------------------------------------------------------


def SobreMiView(request):
    return render(request, "NaturadietApp/sobreMi.html")




#----------------------------------------------------------------



def RecuperarPass(request):

    if request.method == "POST":
        usuario = request.POST['usuario']
        email = request.POST['email']
        asunto = "Recuperación Contraseña"

        try:
            #Si los imputs están vacios muestra aviso 
            if (not email) and (not usuario):
                messages.error(request, f"No puede haber campos vacíos.")

            #Si el usuario no existe salta la excepción 
            user = Usuario.objects.get(username = usuario, email = email)

            if user:
                password = ''+BaseUserManager().make_random_password(45)
                user.set_password(password)
                user.save()
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                mensaje = "Hola "+ user.first_name + " "+ user.last_name +".\nTu nueva contraseña es: \n" + password
                send_mail(asunto, mensaje, email_from, recipient_list)
                messages.success(request, f"Se le ha enviado una nueva contraseña a su correo.")
                return redirect(to="Home")

        except:
            messages.error(request, f"El usuario o Email no coinciden.")
            return render(request, "NaturadietApp/recovery.html")

    return render(request, "NaturadietApp/recovery.html")



#----------------------------------------------------------------



def PerfilUsuarioView(request):
    usuario = request.user
    
    return render(request, "NaturadietApp/perfil.html", {'usuario': usuario})


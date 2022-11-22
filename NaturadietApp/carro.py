class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")

        if not carro:
            carro = self.session["carro"] = {}
        

        self.carro = carro



    def agregar(self, producto):
        if(str(producto.id_producto) not in self.carro.keys()):
            self.carro[producto.id_producto] = {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url
            }
        else:
            for key, value in self.carro.items():
                if key == str(producto.id_producto):
                    value["cantidad"] = value["cantidad"]+1
                    break
        
        self.guardar_carro()



    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True



    def eliminar(self, producto):
        id_producto = str(producto.id_producto)

        if id_producto in self.carro:
            del self.carro[id_producto]
            self.guardar_carro()



    def aumentar_producto(self, producto):
        for key, value in self.carro.items():
            if key == str(producto.id_producto):
                value["cantidad"] = value["cantidad"]+1
                self.guardar_carro()
                break
                

    def restar_producto(self, producto):
        for key, value in self.carro.items():
            if key == str(producto.id_producto):
                value["cantidad"] = value["cantidad"]-1
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                
                self.guardar_carro()
                break

        



    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True


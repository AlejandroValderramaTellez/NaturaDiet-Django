from .carro import Carro

def importe_total_carro(request):
    total = 0
    unidades = 0

    if request.user.is_authenticated:
        carro = request.session.get("carro")
        if not carro:
            carro = request.session["carro"] = {}
        for key, value in request.session["carro"].items():
            precio = float(value["precio"])
            cantidad = float(value["cantidad"])
            unidades += int(cantidad)
            total = round(total + precio * cantidad,2)
    

    return {"importe_total_carro": total, "unidades": unidades}
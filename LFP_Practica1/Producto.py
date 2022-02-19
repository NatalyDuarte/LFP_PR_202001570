class Producto:
    def __init__(self, producto, preciouni, cantidad, ganancia):
        self.producto = producto
        self.preciouni = preciouni
        self.cantidad = cantidad
        self.ganancia = ganancia

    def __repr__(self):
        return "Producto:"+ self.producto +" Precio por unidad:" + self.preciouni + " Cantidad vendida al mes:" + self.cantidad + " Cantidad generada:" + self.ganancia
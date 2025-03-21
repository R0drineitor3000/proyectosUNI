import database

class Product:
    def __init__(self, ID, ordered):
        product = database.products.getProduct(ID)
        if product:
            self.ID = ID
            self.name = product['name']
            self.details = product['details']
            self.price = product['price']
            self.stock = product['stock']
            if ordered >= product['stock']:
                self.ordered = product['stock']
            else:
                self.ordered = ordered
            self.picture = product['picture']
            self.idPoster = product['idPoster']

    def imprimir_valores(self):
        keys = self.__dict__.keys()
        for key in keys:
            print(f"{key}: {getattr(self, key)}")
        



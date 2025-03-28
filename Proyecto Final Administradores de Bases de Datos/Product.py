import database

class Product:
    def __init__(self, ID, ordered):
        product = database.products.getProduct(ID)
        if product:
            self.ID = ID
            self.name = product['name']
            self.details = product['details']
            self.price = float(product['price'])
            self.stock = int(product['stock'])
            self.ordered = min(int(ordered), self.stock)
            self.picture = product['picture']
            self.idPoster = product['idPoster']
            self.Poster = database.login.getUser(product.get("idPoster")).get("username")

    def imprimir_valores(self):
        keys = self.__dict__.keys()
        for key in keys:
            print(f"{key}: {getattr(self, key)}")
        
    def to_dict(self):
        return {
            'ID': self.ID,
            'name': self.name,
            'details': self.details,
            'price': self.price,
            'stock': self.stock,
            'ordered': self.ordered,
            'ordered': self.ordered,
            'picture': self.picture,
            'idPoster': self.idPoster,
            'Poster': self.Poster
        }

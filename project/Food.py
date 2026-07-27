from Product import Product
from datetime import date 

class Food(Product):

    def __init__(self, id, name, price, stock, expired_by:date):
        super().__init__(id, name, price, stock) # Product
        self.expired_by = expired_by

    

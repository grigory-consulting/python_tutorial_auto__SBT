from Product import Product



class ShoppingCart:
    def __init__(self):
        self.items = {} # Dictionary 

    def __repr__(self):
        return f"ShoppingCart({self.items})"

    def add(self, product, quantity=1):
        if quantity <= product.stock and quantity>0:
            self.items[product] = self.items.get(product,0) + quantity 
        
        # Two cases

        # case 1 product is in cart 
        # self.items[product] -> quantity of product
        # case 2 product not in cart
        # -> 0 
        
    def delete(self, product):
        del self.items[product] # delete key-value 

    def clear(self): # empty
        self.items.clear()

    def total_quantity(self):
        total = 0
        for product in self.items:
            total += self.items[product]
        return total

    def total_price(self):
        total = 0
        for product in self.items:
            total += self.items[product] * product.price 
        return total

if __name__ == "__main__":
    product1 = Product("001", "MyBook", 20.99, 5)
    product2 = Product("002", "MyDVD", 19.99, 2)
    cart = ShoppingCart()
    cart.add(product1)
    cart.add(product2,quantity=2)
    print(cart)
    print(cart.total_price())
    
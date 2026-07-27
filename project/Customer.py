from Product import Product
from ShoppingCart import ShoppingCart


class Customer:


    def __init__(self, id, name ):
        self.id = id
        self.name = name
        self.cart = ShoppingCart()

    def __repr__(self):
        return f"Customer({self.id}, {self.name})"

    def order(self) -> float: # return total_price 

        if not self.cart.items:
            print("No items in cart")
            return .0 # end of function 


        total = self.cart.total_price()

        for product in self.cart.items:
            quantity = self.cart.items[product]
            product.buy(quantity)

            

        self.cart.clear() # empty the cart 

        return total

if __name__ == "__main__":
    laptop = Product("001", "Laptop", 999.0, 5)
    anna = Customer("u001", "Anna")
    anna.cart.add(laptop,3) 
    print(anna.cart)
    total_price = anna.order()
    print(total_price)
    print(anna.cart)
    print(laptop)



class Product:

    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price 
        self.stock = stock 
    

    #def __str__(self): # for print (humans)
        #pass
    #    return "This my cool product"

    def __repr__(self): # print for containers/other modules 
        return f"Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})"

    def buy(self, quantity):
        if self.stock>= quantity:
            self.stock -= quantity
        else:
            print("Out of stock") # Later: TODO raise an error here 

if __name__ == "__main__": # if we are in entry point 
    product1 = Product("001", "Kiwi", 20.99, 5)
    print([product1])
    print(product1) 
    product1.buy(3)
    print(product1)


# Plan - Online Shop 


- class Product
    - attributes
        - id 
        - name 
        - price
        - description
        - stock  
        - (pictures)
    - methods
        - buy 

- class ShoppingCart
    - attributes 
        - items : dict(Product:quantity)
    - methods
        - add, delete, clear
        - show
        - total_quantity, total_price 

- class Customer 
    - attributes
        - id
        - name
        - address
        - payment method 
        - shopping_cart 
    - methods
        - order
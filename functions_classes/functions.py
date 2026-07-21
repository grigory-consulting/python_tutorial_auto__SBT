


def cube(num): # one parameter
    cube_num = num ** 3
    return cube_num # one return value 


num = 5 
cube_num = cube(num)

print(cube_num)

print([cube(num) for num in range(20)])

def greeting(name = "World"): # one parameter with default value 
    print(f"Hello, {name}!")

greeting() # 
greeting("Markus")


import random 


def random_digit(): # parameterless function 
    """Generate random digit (integer between 0 and 9)"""
    return random.randint(0,9)


help(random_digit)

for i in range(100): print(random_digit(), end=" ")
print()


def add_three_numbers(a,b,c = 1): 
    print("a =", a, "b =", b, "c =", c)
    print(a+b+c)

# What is allowed:

add_three_numbers(1,2)
add_three_numbers(2,1)
add_three_numbers(1,2, 3)
add_three_numbers(c = 4, b = 2, a = 3)
add_three_numbers(1,b=2, c = 5) 


# not allowed 
#def add_three_numbers(a=1,b,c): 
#    print("a =", a, "b =", b, "c =", c)
#    print(a+b+c)

# add_three_numbers(a=1,b, c) 


def my_print(*args): # any number of parameters
    print("(", end="")
    print(*args, sep="|", end = "")
    print(")") 


my_print(1,2,3,34,5,5,6,6,6,7,6)


def dataentrytool(**kwargs): 
    print(kwargs)
    for key in kwargs:
        print(key, kwargs[key])

dataentrytool(Name="Prof. Klug", Age = 50, City = "Wuppertal")
dataentrytool(Name="Prof. Klug", Age = 50, City = "", Country = "Germany")

def everything(a, b=1, *args, **kwargs): 
    print("a", a)
    print("b", b)
    print("args", args)
    print("kwargs", kwargs)

everything(3,70, 4,5,5,6,7,5,4,6, Name = "Anna", Street = "Street" , y = [])



# scope 

count = 0


def increase():
    global count
    count += 1 

increase()
print(count)


def outer():
    x = "outer value"
    
    def inner():
        nonlocal x # same as in global but inside of function 
        x = "x was changed"
    
    inner()
    print(x)

outer()



# decorator 

def changecase(func): 
    var = "X"
    def myinner():
        nonlocal var
        return var + func().upper()
    return myinner 

@changecase
def my_function():
    return "Hello World!"

print(my_function())





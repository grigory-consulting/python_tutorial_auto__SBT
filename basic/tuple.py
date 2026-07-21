

x = (1,2,3)

# x[0] = 10 # TypeError 

# shallow immutability 

l = ["a", "b", "c"] # mutable 

x = (l,) # tuple 

print(x)

l[0] = "D" # Problem -> lists are mutable 

print(x)


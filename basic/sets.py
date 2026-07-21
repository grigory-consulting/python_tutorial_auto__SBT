

setA = set(["a", "b", "c", "d"])
setB = set(["c", "d", "e", "f"])
setC = {"x", "y", "z"}

empty_set = set()

print("e" in setB) # check whether element is in set 

print(setA - setB) # set difference ... elements in setA but not in setB 
print(setA | setB) # set union ... all elements in either setA or setB
print(setA & setB) # set intersection ... all elements in both sets  
print(setA ^ setB) # symmetric difference (union - intersection )

# possible but not that good 
s = set()

for i in range(10): 
    s |= set([i]) # cumulation loop 

l = [1,2,2,23,3,4,4,4,4,4,5,5,6,6,7,7,7,8,8,9,9,0,0,5,4,32,34]

l = list(set(l)) # remove duplicates 

print(l) 


for elem in setC:
    print(elem) 
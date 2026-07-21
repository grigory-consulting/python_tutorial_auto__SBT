


d = {"one": 1, "two": [2], "three": "THREE", 4: "four", (5, 2 ): "FIVE"}  

print(d[(5,2)])

print(d.get((5,), "key is not there"))

#print(d[(5,)])


del d["one"]

value = d.pop("three")
print(value)
print(d)

# iteration 

for key in d:
    print(key, d[key])


# 

print(list(d.keys())) # list of keys
print(list(d.values())) # list of values
print(list(d.items())) # list key value tuples
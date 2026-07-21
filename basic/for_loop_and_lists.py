

for i in range(10):
    print(i, end = " ") 
else:
    #pass
    print("\n") # newline

print("Next")


for i in range(10, 0, -2): # start, end, step ; end is exclusive 
    print(i, end = " ") 


# List 
# - ordered, mutable collection 

l1 = [1,2,3]
print(l1)  

l2 = list(range(0,int(10)))
print(l2)

l3 = [1.0, 2, "3"]  # any type 
print(l3)

l4 = [1.0, 2, "3", l3] 
print(l4)

# PHP-like foreach 

for each in l4:
    print(each) # each is running variable (elements from l4)



numbers = list(range(10))
print(numbers)

# List comprehension 

squares = [num**2 for num in numbers] # num ... running , num**2 is expression 


# same via for loop 

# squares.append(x) -> append an element x to end of list

squares = []
# or
squares = list() 
for num in numbers: squares.append(num**2)

print(num)


food = ["rice", "beans", "bread"]
food.append("broccoli") # append

food += ["pizza", "hotdog"] # list concatenation 



squares = list() 
for num in numbers: squares += [num**2] # try not use list concatenation in for loops 

# Slices 

print(food[0])
print(food[-1])
print(food[2:]) # from third to end
print(food[:2]) # from start to second
print(food[2:5]) # from third to fifth 
print(food[5:2:-1]) # start, end, step  from sixth to third 

# Mutability 
food[0] = "apple juice" # allowed to change 
print(food)




fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"   # Change an element
fruits.append("date")     # Add at the end
fruits.insert(1, "kiwi")  # Insert at index 1
print(fruits)             # ['apple', 'kiwi', 'blueberry', 'cherry', 'date']
fruits.remove("kiwi")     # Remove by value
print(fruits)
item = fruits.pop()       # Remove and return last item
print(item)               # 'date'
print(fruits)             # ['apple', 'blueberry', 'cherry']


nums = [3, 1, 4, 1, 5, 9, 2]
print(len(nums))      # 7
print(nums.count(1))  # 2
nums.sort()
print(nums)  # [1, 1, 2, 3, 4, 5, 9]
nums.reverse()
print(nums)  # [9, 5, 4, 3, 2, 1, 1]


matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6

import copy
a = [[1, 2], [3, 4]]
b = a.copy()         # Shallow copy
c = copy.deepcopy(a) # Deep copy
a[0][0] = 99
print(b)  # [[99, 2], [3, 4]]
b[0][0]  = 1001
print(a)
print(b)
print(c)  # [[1, 2], [3, 4]]





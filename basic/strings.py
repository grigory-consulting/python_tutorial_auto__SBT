


print("Hello World")


my_string1 = "hello"
my_string2 = "WorlD"


print(my_string1 + "_" + my_string2)  # String concatenation 

print(len(my_string2)) # Length of string = number of characters in a string

# Accessing the elements

print(my_string1[0]) # the first element 
print(my_string1[1]) # second element 

# specific to Python 
print(my_string1[-1]) # last element
print(my_string1[-2]) # before last


string1 = "Honey Bee"

print(string1.lower()) # everything lowercase
print(string1.upper()) # everything uppercase

# 

print(string1.startswith("ho")) # False
print(string1.lower().startswith("ho")) # True

# String parsing

my_string_type1 = "6"
my_string_type2 = "7"

print(my_string_type1 + my_string_type2) # 67 

print(int(my_string_type1) + int(my_string_type2)) # Conversion to integer -> 13


my_float1 = 6. # 6.0
my_float2 = 7.2 
my_float3 = .8 # 0.8
my_float4 = 1e-7 # scientific notation 

print(float(my_string_type1) + float(my_string_type2)) # Conversion to float -> 13.0 

print(0.1 + 0.2)

name = "Alice" # empty String evaluates to False in an if-condition 

if name:
    print("string is not empty")
else:
    print("string is empty") 





total = 0
count = 0
print("0 to stop")
num = int(input("Enter a number: "))
while num != 0:
    total += num
    count += 1
    print("0 to stop")
    num = int(input("Enter a number: "))

print("Count:", count)
print("Sum:", total)











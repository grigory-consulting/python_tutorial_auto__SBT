

class Point2D:
    """Two-dimensional point in space"""
    def __init__(self, xx=0, yy=0): # construct our point, default is origin 
        self.x = xx # value is written to the attribute 
        self.y = yy 

    def __str__(self): # we need to return a string (for human)
        return f"Point2D with coordinates ({self.x},{self.y})" 

    def __repr__(self): # string method for non-humans like lists 
        return f"Point2D({self.x},{self.y})"

    def __add__(self,other): # Plus-Operation 
        # new point
        return Point2D(self.x + other.x, self.y + other.y)

    def move(self, dx, dy): # dx ... change in x coord, dy ... in y coord 
        self.x += dx 
        self.y += dy 

    def movex(self,dx): # only x direction
        # either
        self.x += dx 
        # or
        # self.move(dx, 0)

    def movey(self,dy): # only y direction 
        # either 
        self.y += dy
        # or
        # self.move(0, dy)

    def distance_0(self): # distance from coordinate origin
        # Euclidean distance 
        return (self.x**2 + self.y**2)**0.5 

    

    
p = Point2D() 

print(p)

q = Point2D(3,5)
r = Point2D(2,6)

lp = [p,q,r]

print(lp)

print(q+r)

q.move(-2, 3) 
print(q)



# TODO 
# Task 

# 1. create 50 random points (-10 <= x <= 10, -10 <= y <= 10) with 
# integer coordinates. (import random. Use function random.randint)
# 2. Determine all points whose distance from the origin is > 5.0

import random

points = [] 

for i in range(100): # from 0 to 49 
    points.append(Point2D(random.randint(-10,10),random.randint(-10,10)))

print(len(points)) 


points_filtered = [point for point in points if point.distance_0() > 5.0]
print(len(points_filtered))


# Inheritance 

class Point3D(Point2D): # Point3D ... subclass, Point2D ... superclass
    def __init__(self, xx=0, yy=0, zz=0):
        super().__init__(xx, yy) # Constructor from Point2D 
        self.z = zz # extend with third coordinate 

    # add __str__
    # add __repr__ 
    # implement __add_
    # 
    def __str__(self): # we need to return a string (for human)
        return f"Point3D with coordinates ({self.x},{self.y},{self.z})" 

    def __repr__(self): # string method for non-humans like lists 
        return f"Point3D({self.x},{self.y},{self.z})"

    def __add__(self,other): # Plus-Operation 
        # new point
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def move(self, dx, dy, dz):
        super().move(dx,dy) # move like it would be Point2D 
        self.z += dz 

    def movex(self, dx):
        super().movex(dx)
    
    def movey(self, dy):
        super().movey(dy)

    def distance_0(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5  

p3d = Point3D(1,2,3)

print(p3d) # __str__
print([p3d, p3d+p3d]) # __repr__ and __add__
p3d.move(-1,-2,-3)
print(p3d)
p3d.movex(3) # by inheritance
p3d.movey(2) # by inheritance 
print(p3d)


##### Multiple Inheritance

class A: 
    def methodA(self):
        print("I am method from A")

class B:
    def methodB(self):
        print("I am method from B")

class C(A,B):
    pass 

obj = C()
obj.methodA()
obj.methodB()

# What happens here?

class A: 
    def method(self):
        print("I am method from A")

class B:
    def method(self):
        print("I am method from B")

class C(B,A):
    pass 

obj = C()
obj.method()

print(C.__mro__) # Method resolution order 


# Diamond Problem 

class A:
    def show(self):
        print("A.show()")

class B(A):
    def show(self):
        print("B.show()")
        super().show() 

class C(A):
    def show(self):
        print("C.show()")
        super().show()

class D(C,B):
    def show(self):
        print("D.show()")
        super().show()

d = D()
d.show() 
print(D.mro())
from math import (cos, sin, radians)

def calc_pos(l1, l2, l3, a1, a2, a3):
    a1 = radians(a1)
    a2 = radians(a2)
    a3 = radians(a3)

    x = (l1*cos(a1)) + (l2*cos(a1+a2)) + (l3*cos(a1+a2+a3))
    y = (l1*sin(a1)) + (l2*sin(a1+a2)) + (l3*sin(a1+a2+a3))
    
    return f"Cor: {(x, y)}"

def get_data():
    l1 = int(input("L1: "))
    l2 = int(input("L2: "))
    l3 = int(input("L3: "))
    a1 = int(input("Angle 1: "))
    a2 = int(input("Angle 2: "))
    a3 = int(input("Angle 3: "))

    return l1, l2, l3, a1, a2, a3

l1, l2, l3, a1, a2, a3 = get_data()
print(calc_pos(l1, l2, l3, a1, a2, a3))
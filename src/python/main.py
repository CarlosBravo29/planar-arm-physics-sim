import math as m

def calc_pos(l1, a1):
    ar1 = m.radians(a1)
    x1 = l1 * m.cos(ar1)
    y1 = l1 * m.sin(ar1)
    return f"Cor: {(x1, y1)}"

l1 = int(input("L1: "))
a1 = int(input("Angle 1: "))

print(calc_pos(l1, a1))
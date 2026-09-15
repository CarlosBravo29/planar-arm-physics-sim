from math import (cos, sin, radians, pi, atan2, sqrt)

def calc_pos(l1, l2, l3, a1, a2, a3):
    a1 = radians(a1)
    a2 = radians(a2)
    a3 = radians(a3)

    x = (l1*cos(a1)) + (l2*cos(a1+a2)) + (l3*cos(a1+a2+a3))
    y = (l1*sin(a1)) + (l2*sin(a1+a2)) + (l3*sin(a1+a2+a3))
    
    return f"Cor: {(x, y)}"

def inv_kinematics(l1, l2, l3, phi_angle, x, y):
    xw, yw = x-(l3*cos(phi_angle)), y-(l3*sin(phi_angle))
    a = ((xw**2)+(yw**2)-(l1**2)-(l2**2)) / (2*l1*l2)
    th2A = atan2(a, sqrt(1+a**2))
    th2B = atan2(a, sqrt(1-a**2))
    th1 = atan2(yw, xw)-atan2(l2*sin(th2A), l1+l2*cos(th2A))
    th3 = th1 + th2A - phi_angle

    return (th1, th2A, th3)

def get_data():
    l1 = int(input("L1: "))
    l2 = int(input("L2: "))
    l3 = int(input("L3: "))
    a1 = int(input("Angle 1: "))
    a2 = int(input("Angle 2: "))
    a3 = int(input("Angle 3: "))

    return l1, l2, l3, a1, a2, a3

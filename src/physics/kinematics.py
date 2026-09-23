from math import (cos, sin, radians, pi, atan2, sqrt)

def calc_pos(l1, l2, l3, a1, a2, a3):
    a1 = radians(a1)
    a2 = radians(a2)
    a3 = radians(a3)

    x = (l1*cos(a1)) + (l2*cos(a1+a2)) + (l3*cos(a1+a2+a3))
    y = (l1*sin(a1)) + (l2*sin(a1+a2)) + (l3*sin(a1+a2+a3))
    
    return x, y

def inv_kinematics(l1, l2, l3, phi_angle, x, y, elbow="up"):
    phi = radians(phi_angle)
    xw, yw = x - (l3 * cos(phi)), y - (l3 * sin(phi)) # Wrist position
    a = ((xw**2) + (yw**2) - (l1**2) - (l2**2)) / (2 * l1 * l2)
    if a < -1 or a > 1:
        raise ValueError("Target position is outside the robot workspace.")
    s2 = sqrt(1 - a**2)
    if elbow == "down":
        s2 = -s2
    if elbow == "up":
        s2 = -sqrt(1 - a**2)
    elif elbow == "down":
        s2 = sqrt(1 - a**2)
    else:
        raise ValueError("Invalid elbow configuration.")
    theta2 = atan2(s2, a)
    theta1 = atan2(yw, xw) - atan2(l2 * sin(theta2), l1 + l2 * cos(theta2))
    theta3 = phi - theta1 - theta2

    return theta1, theta2, theta3

def calc_joint_positions(l1, l2, l3, theta1, theta2, theta3):
    x0, y0 = 0, 0
    x1, y1 = l1 * cos(theta1), l1 * sin(theta1)
    x2 = x1 + l2 * cos(theta1 + theta2)
    y2 = y1 + l2 * sin(theta1 + theta2)
    x3 = x2 + l3 * cos(theta1 + theta2 + theta3)
    y3 = y2 + l3 * sin(theta1 + theta2 + theta3)

    return ((x0, y0), (x1, y1), (x2, y2), (x3, y3))

def get_data():
    l1 = int(input("L1: "))
    l2 = int(input("L2: "))
    l3 = int(input("L3: "))
    a1 = int(input("Angle 1: "))
    a2 = int(input("Angle 2: "))
    a3 = int(input("Angle 3: "))

    return l1, l2, l3, a1, a2, a3

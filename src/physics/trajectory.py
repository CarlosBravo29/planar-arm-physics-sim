from . import kinematics as kin
from math import (ceil, sqrt, atan2, cos, sin, pi)

def rotate_orientation(start_pose, end_pose, max_angular_step=1.0):
    x0, y0, phi0 = start_pose
    xf, yf, phif = end_pose

    delta_phi = ((phif - phi0 + 180) % 360 - 180)
    steps = max(1, ceil(abs(delta_phi) / max_angular_step))
    trajectory = []

    for i in range(steps + 1):
        s = i / steps
        phi = phi0 + s * delta_phi
        trajectory.append((x0, y0, phi))
    return trajectory

def move_l(start_pose, end_pose, max_step=0.1):
    x0, y0, phi0 = start_pose
    xf, yf, phif = end_pose

    distance = sqrt((xf - x0)**2 + (yf - y0)**2)
    steps = max(1, ceil(distance / max_step))
    trajectory = []

    for i in range(steps + 1):
        s = i / steps
        x = x0 + s * (xf - x0)
        y = y0 + s * (yf - y0)
        phi = phi0 + s * (phif - phi0)

        trajectory.append((x, y, phi))

    return trajectory

def move_c(start_pose, via_pose, end_pose, max_step=0.1):
    x0, y0, phi0 = start_pose
    xm, ym, phim = via_pose
    xf, yf, phif = end_pose

    cx, cy = calculate_circle_center((x0, y0), (xm, ym), (xf, yf))
    radius = sqrt((x0 - cx)**2 + (y0 - cy)**2)
    start_angle = atan2(y0 - cy, x0 - cx)
    via_angle = atan2(ym - cy, xm - cx)
    end_angle = atan2(yf - cy, xf - cx)
    start_to_via_ccw = normalize_angle_positive(via_angle - start_angle)
    start_to_end_ccw = normalize_angle_positive(end_angle - start_angle)

    if start_to_via_ccw <= start_to_end_ccw:
        # Counterclockwise
        total_angle = start_to_end_ccw
        via_delta = start_to_via_ccw
    else:
        # Clockwise
        total_angle = -normalize_angle_positive(start_angle - end_angle)
        via_delta = -normalize_angle_positive(start_angle - via_angle)
        
    arc_length = abs(radius * total_angle)
    steps = max(1, ceil(arc_length / max_step))

    if abs(total_angle) > 1e-9:
        via_progress = abs(via_delta / total_angle)
    else:
        via_progress = 0.5
        
    trajectory = []

    for i in range(steps + 1):
        s = i / steps
        angle = (start_angle + s * total_angle)
        x = cx + radius * cos(angle)
        y = cy + radius * sin(angle)
        if s <= via_progress:
            if via_progress > 1e-9:
                local_s = s / via_progress
            else:
                local_s = 1.0
            delta_phi = shortest_angle_delta(phi0, phim)
            phi = (phi0 + local_s * delta_phi)
        else:
            remaining = 1.0 - via_progress
            if remaining > 1e-9:
                local_s = ((s - via_progress) / remaining)
            else:
                local_s = 1.0
            delta_phi = shortest_angle_delta(phim, phif)
            phi = (phim + local_s * delta_phi)
        trajectory.append((x, y, phi))
    return trajectory

def calculate_joint_trajectory(cartesian_trajectory, l1, l2, l3, elbow):
    joint_trajectory = []

    for x, y, phi in cartesian_trajectory:
        theta1, theta2, theta3 = kin.inv_kinematics(l1, l2, l3, phi, x, y, elbow=elbow)
        points = kin.calc_joint_positions(l1, l2, l3, theta1, theta2, theta3)
        joint_trajectory.append(((theta1, theta2, theta3), points))

    return joint_trajectory

def calculate_circle_center(p1, p2, p3, tolerance=1e-9):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < tolerance:
        raise ValueError("MoveC points are collinear. " "A circular trajectory cannot be calculated.")
    cx = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
    cy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
    return cx, cy

def normalize_angle_positive(angle):
    return angle % (2 * pi)

def shortest_angle_delta(start_angle, end_angle):
    return ((end_angle - start_angle + 180) % 360 - 180)

def rotate_end_effector(start_pose, end_pose, max_angular_step=1.0):
    x0, y0, phi0 = start_pose
    xf, yf, phif = end_pose

    delta_phi = shortest_angle_delta(phi0, phif)
    steps = max(1, ceil(abs(delta_phi) / max_angular_step))

    trajectory = []

    for i in range(steps + 1):
        s = i / steps
        phi = phi0 + s * delta_phi
        trajectory.append((x0, y0, phi))

    return trajectory

def get_motion_type(start_pose, end_pose, position_tolerance=1e-6, angle_tolerance=1e-6):
    x0, y0, phi0 = start_pose
    xf, yf, phif = end_pose
    dx = xf - x0
    dy = yf - y0

    position_changed = (abs(dx) > position_tolerance or abs(dy) > position_tolerance)
    delta_phi = shortest_angle_delta(phi0, phif)
    orientation_changed = (abs(delta_phi) > angle_tolerance)

    if not position_changed and orientation_changed:
        return "rotate"
    if position_changed:
        return "move_l"

    return "none"
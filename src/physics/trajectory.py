from . import kinematics as kin
from math import ceil, sqrt

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

def calculate_joint_trajectory(cartesian_trajectory, l1, l2, l3, elbow):
    joint_trajectory = []

    for x, y, phi in cartesian_trajectory:
        theta1, theta2, theta3 = kin.inv_kinematics(l1, l2, l3, phi, x, y, elbow=elbow)
        points = kin.calc_joint_positions(l1, l2, l3, theta1, theta2, theta3)
        joint_trajectory.append(((theta1, theta2, theta3), points))

    return joint_trajectory


from math import ceil, sqrt


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
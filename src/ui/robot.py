
class joint():
    def __init__(self, cords:tuple[float, float], radius:int = 10):
        self.radius = radius
        self.cords = cords

    def reposition(self, cords):
        self.cords = cords

class robot():
    def __init__(self, canvas):
        self.canvas = canvas
        width, height = int(canvas["width"]), int(canvas["height"])
        self.canvas_dim = (width, height)
        self.home = (width / 2, height - 10 - 15)
        self.scale = 20

        self.l1, self.l2, self.l3 = 9, 6, 3
        self.joint_1 = joint(cords=(0, 0), radius=10)
        joint_2_cords = self.calc_initial_joint(self.joint_1.cords, self.l1)
        self.joint_2 = joint(cords=joint_2_cords, radius=10)
        joint_3_cords = self.calc_initial_joint(self.joint_2.cords, self.l2)
        self.joint_3 = joint(cords=joint_3_cords, radius=10)
        end_effector_cords = self.calc_initial_joint(self.joint_3.cords, self.l3)
        self.end_effector = joint(cords=end_effector_cords, radius=10)

    def world_to_canvas(self, x, y):
        xh, yh = self.home
        canvas_x = xh + x * self.scale
        canvas_y = yh - y * self.scale
        return canvas_x, canvas_y

    def calc_initial_joint(self, start_point, link_length):
        x0, y0 = start_point
        x1 = x0
        y1 = y0 + link_length
        return (x1, y1)

    def draw_grid(self):
        width, height = self.canvas_dim
        xh, yh = self.home
        step = self.scale
        self.canvas.delete("grid")
        ## Lines
        x = xh
        while x <= width:
            self.canvas.create_line(x, 0, x, height, fill="#d9d9d9", tags="grid")
            x += step
        x = xh - step
        while x >= 0:
            self.canvas.create_line(x, 0, x, height, fill="#d9d9d9", tags="grid")
            x -= step
        y = yh
        while y >= 0:
            self.canvas.create_line(0, y, width, y, fill="#d9d9d9", tags="grid")
            y -= step
        y = yh + step
        while y <= height:
            self.canvas.create_line(0, y, width, y, fill="#d9d9d9", tags="grid")
            y += step
        ## END lines

        # Axis X
        self.canvas.create_line(0, yh, width, yh, fill="black", width=2, tags="grid")
        # Axis Y
        self.canvas.create_line(xh, 0, xh, height, fill="black", width=2, tags="grid")

    def draw_joint(self, joint):
        x, y = joint.cords
        cx, cy = self.world_to_canvas(x, y)
        r = joint.radius
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="blue", tags="robot")

    def draw_link(self, joint_a, joint_b):
        x1, y1 = self.world_to_canvas(*joint_a.cords)
        x2, y2 = self.world_to_canvas(*joint_b.cords)

        self.canvas.create_line(x1, y1, x2, y2, width=6, fill="blue", tags="robot")

    def set_link_lengths(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

        self.joint_2.cords = self.calc_initial_joint(self.joint_1.cords, self.l1)
        self.joint_3.cords = self.calc_initial_joint(self.joint_2.cords, self.l2)
        self.end_effector.cords = self.calc_initial_joint(self.joint_3.cords, self.l3)
        self.draw()

    def set_position(self, points):
        p0, p1, p2, p3 = points

        self.joint_1.cords = p0
        self.joint_2.cords = p1
        self.joint_3.cords = p2
        self.end_effector.cords = p3

        self.draw()
    
    def draw(self):
        self.canvas.delete("robot")
        self.draw_grid()
        self.draw_link(self.joint_1, self.joint_2)
        self.draw_link(self.joint_2, self.joint_3)
        self.draw_link(self.joint_3, self.end_effector)
        self.draw_joint(self.joint_1)
        self.draw_joint(self.joint_2)
        self.draw_joint(self.joint_3)
        self.draw_joint(self.end_effector)

    def set_home(self, x, y):
        self.home = (x, y)

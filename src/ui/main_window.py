import tkinter as tk
import ui.widgets as widgets
from math import degrees
from physics import kinematics as kin
#from physics import constraints as cst
from ui.robot import robot as rob
from tkinter import ttk

LIGHT_THEME = {
    "bg_main": "#f0f0f0",
    "bg_entry": "#ffffff",
    "canvas_bg": "#fbfbfb",
    "fg_text": "#202020",

    "grid_color": "#d9d9d9",
    "axis_color": "#202020",
    "robot_color": "#0000ff",
    "preview_color": "#8a8aff"
}

DARK_THEME = {
    "bg_main": "#202020",
    "bg_entry": "#2b2b2b",
    "canvas_bg": "#2b2b2b",
    "fg_text": "#f2f2f2",

    "grid_color": "#bfbfbf",
    "axis_color": "#ffffff",
    "robot_color": "#ff991c",
    "preview_color": "#ffd29a"
}

class MainWin:
    def __init__(self, root):
        self.root = root
        self.root.title("TEST sim")
        self.root.geometry("1100x600")
        self.root.iconbitmap("assets/icon_1.ico")

        self.entries = {}
        self.labels = []

        self.elbow_config = tk.StringVar(value="up")
        self.preview_points = None

        self.style = ttk.Style()

        self.create_layout()
        self.create_controls()

    def create_layout(self):
        self.canvas = tk.Canvas(self.root, width=650, height=550, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.controls = tk.Frame(self.root)
        self.controls.pack(side="right", padx=50, pady=20, anchor="n")
        self.create_rob()

    def create_rob(self):
        self.my_robot = rob(self.canvas)
        self.my_robot.draw()

    def create_controls(self):
        self.notebook = ttk.Notebook(self.controls, width=400, height=550)

        self.simulation_tab = tk.Frame(self.notebook)
        self.robot_tab = tk.Frame(self.notebook)
        self.dynamics_tab = tk.Frame(self.notebook)
        self.settings_tab = tk.Frame(self.notebook)

        self.notebook.add(self.simulation_tab, text="Simulation")
        self.notebook.add(self.robot_tab, text="Robot")
        self.notebook.add(self.dynamics_tab, text="Dynamics")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.pack(fill="both", expand=True)

        self.create_simulation_tab()
        self.create_robot_tab()
        self.create_dynamics_tab()
        self.create_settings_tab()

    def create_simulation_tab(self):
        self.sim_status_frame = tk.Frame(self.simulation_tab)
        self.sim_status_frame.pack(side="top", fill="x", padx=20, pady=(10, 20))

        self.status_labels = {}

        status_title = tk.Label(self.sim_status_frame, text="Simulation State")
        status_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        status_fields = [
            ("Joint 1:", "joint_1"), ("Joint 2:", "joint_2"), ("Joint 3:", "joint_3"), ("End effector:", "end_effector"),
            ("θ1:", "theta1"), ("θ2:", "theta2"), ("θ3:", "theta3"),
        ]

        for row, (text, key) in enumerate(status_fields, start=1):
            label = tk.Label(self.sim_status_frame, text=text)
            label.grid(row=row, column=0, sticky="e", pady=2)

            value_label = tk.Label(self.sim_status_frame, text="-")
            value_label.grid(row=row, column=1, sticky="w", padx=5, pady=2)

            self.labels.extend([label, value_label])
            self.status_labels[key] = value_label

        self.sim_input_frame = tk.Frame(self.simulation_tab)
        self.sim_input_frame.pack(side="bottom", fill="x", padx=20, pady=(20, 10))

        title = tk.Label(self.sim_input_frame, text="Target Position")
        title.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        fields = [("X:", "x"), ("Y:", "y"), ("Orientation:", "phi")]

        for row, (text, key) in enumerate(fields, start=1):
            label = tk.Label(self.sim_input_frame, text=text)
            label.grid(row=row, column=0, pady=5, sticky="e")

            entry = tk.Entry(self.sim_input_frame)
            entry.grid(row=row, column=1, pady=5, padx=5)

            self.labels.append(label)
            self.entries[key] = entry

        elbow_title = tk.Label(self.sim_input_frame, text="Elbow Configuration")
        elbow_title.grid(row=4, column=0, columnspan=2, pady=(15, 5))
        self.elbow_up_radio = tk.Radiobutton(self.sim_input_frame, text="Elbow Up", variable=self.elbow_config, value="up")
        self.elbow_up_radio.grid(row=5, column=0, padx=5, pady=5)
        self.elbow_down_radio = tk.Radiobutton(self.sim_input_frame, text="Elbow Down", variable=self.elbow_config, value="down")
        self.elbow_down_radio.grid(row=5, column=1, padx=5, pady=5)

        self.preview_button = tk.Button(self.sim_input_frame, text="Preview", command=self.preview_position)
        self.preview_button.grid(row=6, column=0, pady=15, padx=5)
        self.move_button = tk.Button(self.sim_input_frame, text="Move", command=self.move_to_position)
        self.move_button.grid(row=6, column=1, pady=15, padx=5)
        self.sim_button = tk.Button(self.sim_input_frame, text="Simulate", command=self.simulate_motion)
        self.sim_button.grid(row=6, column=2, columnspan=2, pady=15)

    def create_robot_tab(self):
        fields = [("L1: ", "l1"), ("L2: ", "l2"), ("L3: ", "l3")]
        title = tk.Label(self.robot_tab, text="Robot Geometry")
        title.grid(row=0, column=0, columnspan=2, pady=15)

        for row, (text, key) in enumerate(fields, start=1):
            label = tk.Label(self.robot_tab, text=text)
            label.grid(row=row, column=0, pady=5)
            entry = tk.Entry(self.robot_tab)
            entry.grid(row=row, column=1, pady=5)

            self.labels.append(label)
            self.entries[key] = entry

        apply_button_row = len(fields) + 1
        self.set_button = tk.Button(self.robot_tab, text="Apply", command=self.get_links_lenght)
        self.set_button.grid(row=apply_button_row, column=0, columnspan=2, pady=15)

    def create_dynamics_tab(self):
        fields = [("Link 1 mass:", "m1"), ("Link 2 mass:", "m2"), ("Link 3 mass:", "m3"), ("Payload mass:", "payload")]
        title = tk.Label(self.dynamics_tab, text="Dynamic Parameters")
        title.grid(row=0, column=0, columnspan=2, pady=15)

        for row, (text, key) in enumerate(fields, start=1):
            label = tk.Label(self.dynamics_tab, text=text)
            label.grid(row=row, column=0, pady=5)
            entry = tk.Entry(self.dynamics_tab)
            entry.grid(row=row, column=1, pady=5)
            self.labels.append(label)
            self.entries[key] = entry

    def create_settings_tab(self):
        title = tk.Label(self.settings_tab, text="Appearance")
        title.grid(row=0, column=0, columnspan=2, pady=15)
        self.dark_mode_label = tk.Label(self.settings_tab, text="Dark mode:")
        self.dark_mode_label.grid(row=1, column=0, pady=10)
        self.dark_mode_switch = widgets.ToggleSwitch(self.settings_tab, width=35, height=20, command=self.on_switch_change)
        self.dark_mode_switch.grid(row=1, column=1, pady=10)

    def on_switch_change(self, state):
        theme = DARK_THEME if state else LIGHT_THEME

        self.apply_theme(self.root, theme)

        self.canvas.config(bg=theme["canvas_bg"])
        self.dark_mode_switch.config(bg=theme["bg_main"])
        self.root.config(bg=theme["bg_main"])
        self.my_robot.set_theme_colors(theme["grid_color"], theme["axis_color"], theme["robot_color"])
        self.my_robot.set_preview_color(theme["preview_color"])

    def apply_theme(self, widget, theme):
        if isinstance(widget, tk.Frame):
            widget.config(bg=theme["bg_main"])
        elif isinstance(widget, tk.Label):
            widget.config(bg=theme["bg_main"], fg=theme["fg_text"])
        elif isinstance(widget, tk.Entry):
            widget.config(bg=theme["bg_entry"], fg=theme["fg_text"], insertbackground=theme["fg_text"], selectbackground=theme["robot_color"], selectforeground=theme["bg_entry"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=theme["bg_entry"], fg=theme["fg_text"])
        elif isinstance(widget, tk.Radiobutton):
            widget.config(bg=theme["bg_main"], fg=theme["fg_text"], activebackground=theme["bg_main"], activeforeground=theme["fg_text"], selectcolor=theme["bg_entry"])

        for child in widget.winfo_children():
            self.apply_theme(child, theme)

    def get_target_configuration(self): #get_target_configuration get_new_position
        x = float(self.entries["x"].get())
        y = float(self.entries["y"].get())
        phi = float(self.entries["phi"].get())

        l1 = self.my_robot.l1
        l2 = self.my_robot.l2
        l3 = self.my_robot.l3
        elbow = self.elbow_config.get()

        theta1, theta2, theta3 = kin.inv_kinematics(l1, l2, l3, phi, x, y, elbow=elbow)
        # if not cst.check_joint_limits(theta1, theta2, theta3):
        #     print("Joint limits exceeded")
        #     return
        points = kin.calc_joint_positions(l1, l2, l3, theta1, theta2, theta3)
        angles = (theta1, theta2, theta3)

        return angles, points

    def update_simulation_state(self, angles, points):
        theta1, theta2, theta3 = angles
        p0, p1, p2, p3 = points

        self.status_labels["joint_1"].config(text=f"({p0[0]:.2f}, {p0[1]:.2f})")
        self.status_labels["joint_2"].config(text=f"({p1[0]:.2f}, {p1[1]:.2f})")
        self.status_labels["joint_3"].config(text=f"({p2[0]:.2f}, {p2[1]:.2f})")
        self.status_labels["end_effector"].config(text=f"({p3[0]:.2f}, {p3[1]:.2f})")
        self.status_labels["theta1"].config(text=f"{degrees(theta1):.2f}°")
        self.status_labels["theta2"].config(text=f"{degrees(theta2):.2f}°")
        self.status_labels["theta3"].config(text=f"{degrees(theta3):.2f}°")

    def get_links_lenght(self):
        l1 = float(self.entries["l1"].get())
        l2 = float(self.entries["l2"].get())
        l3 = float(self.entries["l3"].get())
        self.my_robot.set_link_lengths(l1, l2, l3)
        return (l1, l2, l3)

    def on_elbow_change(self):
        if self.preview_points is not None:
            self.preview_position()

    def preview_position(self):
        try:
            angles, points = self.get_target_configuration()
        except ValueError as error:
            print(error)
            return
        self.preview_angles = angles
        self.preview_points = points
        self.my_robot.draw_preview(points)

    def move_to_position(self):
        try:
            angles, points = self.get_target_configuration()
        except ValueError as error:
            print(error)
            return
        self.my_robot.set_position(points)
        self.update_simulation_state(angles, points)
        self.canvas.delete("preview")

    def simulate_motion(self):
        pass

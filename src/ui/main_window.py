import tkinter as tk
import ui.widgets as widgets
from physics import kinematics as kin
from ui.robot import robot as rob

class MainWin:
    def __init__(self, root):
        self.root = root
        self.root.title("TEST sim")
        self.root.geometry("1000x600")
        self.root.iconbitmap("assets/icon_1.ico")

        self.entries = {}
        self.labels = []

        self.create_layout()
        self.create_controls()

    def create_layout(self):
        self.canvas = tk.Canvas(self.root, width=650, height=550, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.controls = tk.Frame(self.root)
        self.controls.pack(side="right", padx=50, expand=True)
        self.create_rob()

    def create_rob(self):
        self.my_robot = rob(self.canvas)
        self.my_robot.draw()

    def create_controls(self):
        self.config_frame = tk.Frame(self.controls, width=200, height=100)
        self.config_frame.pack(side="top", expand=True, pady=10)
        self.input_frame = tk.Frame(self.controls, width=200, height=100)
        self.input_frame.pack(side="top", expand=True, pady=10)

        ## Config Links ##
        config_fields = [("L1: ", "l1"), ("L2: ", "l2"), ("L3: ", "l3")]

        config_label = tk.Label(self.config_frame, text="Config")
        config_label.grid(row=0, column=0, columnspan=2, pady=15)     

        for row, (text, key) in enumerate(config_fields, start=1):
            label = tk.Label(self.config_frame, text=text)
            label.grid(row=row, column=0, pady=5)
            entry = tk.Entry(self.config_frame)
            entry.grid(row=row, column=1, pady=5)
            self.labels.append(label)
            self.entries[key] = entry

        button_row = len(config_fields) + 1
        self.set_button = tk.Button(self.config_frame, text="Set lenght", command=self.get_links_lenght)
        self.set_button.grid(row=button_row, column=0, columnspan=2, pady=15)

        ## Simulation input ##
        simulation_fields = [("x: ", "x"), ("y: ", "y"), ("Orientation: ", "phi")]

        config_label = tk.Label(self.input_frame, text="New Position")
        config_label.grid(row=0, column=0, columnspan=2, pady=15)     

        for row, (text, key) in enumerate(simulation_fields, start=1):
            label = tk.Label(self.input_frame, text=text)
            label.grid(row=row, column=0, pady=5)
            entry = tk.Entry(self.input_frame)
            entry.grid(row=row, column=1, pady=5)
            self.labels.append(label)
            self.entries[key] = entry

        button_row = len(config_fields) + 1
        self.sim_button = tk.Button(self.input_frame, text="Simulate", command=self.get_new_position)
        self.sim_button.grid(row=4, column=0, columnspan=2, pady=15)

        # Dark Mode Toggle button
        self.dark_mode_leb = tk.Label(self.config_frame, text="Dark mode:")
        self.dark_mode_leb.grid(row=5, column=0, pady=15, sticky="e")
        self.dark_mode_switch = widgets.ToggleSwitch(self.config_frame, width=50, height=25, command=self.on_switch_change)
        self.dark_mode_switch.grid(row=5, column=1, pady=15, sticky="w")

    def on_switch_change(self, state):
        if state:
            bg_main = "#202020"
            bg_entry = "#2b2b2b"
            fg_text = "white"
        else:
            bg_main = "white"
            bg_entry = "white"
            fg_text = "black"

        frames = [
            self.root,
            self.controls,
            self.config_frame,
            self.input_frame
        ]

        for lbl in self.labels:
            lbl.config(bg=bg_main, fg=fg_text)
        for entry in self.entries.values():
            entry.config(bg=bg_entry, fg=fg_text)
        for frame in frames:
            frame.config(bg=bg_main)

        self.canvas.config(bg=bg_entry)
        self.sim_button.config(bg=bg_entry, fg=fg_text)
        self.set_button.config(bg=bg_entry, fg=fg_text)
        self.dark_mode_switch.config(bg=bg_main)

    def get_new_position(self):
        x = float(self.entries["x"].get())
        y = float(self.entries["y"].get())
        phi = float(self.entries["phi"].get())

        l1 = self.my_robot.l1
        l2 = self.my_robot.l2
        l3 = self.my_robot.l3

        theta1, theta2, theta3 = kin.inv_kinematics(l1, l2, l3, phi, x, y)
        points = kin.calc_joint_positions(l1, l2, l3, theta1, theta2, theta3)
        self.my_robot.set_position(points)

    def get_links_lenght(self):
        l1 = float(self.entries["l1"].get())
        l2 = float(self.entries["l2"].get())
        l3 = float(self.entries["l3"].get())
        self.my_robot.set_link_lengths(l1, l2, l3)
        return (l1, l2, l3)

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
        self.config_fields = tk.Frame(self.controls, width=200, height=100)
        self.config_fields.pack(side="top", expand=True, pady=10)
        self.input_fields = tk.Frame(self.controls, width=200, height=100)
        self.input_fields.pack(side="top", expand=True, pady=10)

        ## Config Links ##
        # Link 1
        self.link1_lbe = tk.Label(self.config_fields, text="L1: ")
        self.link1_lbe.grid(row=0, column=0, pady=5)
        self.entry_1 = tk.Entry(self.config_fields)
        self.entry_1.grid(row=0, column=1, pady=5)
        # Link 2
        self.link2_lbe = tk.Label(self.config_fields, text="L2: ")
        self.link2_lbe.grid(row=1, column=0, pady=5)
        self.entry_2 = tk.Entry(self.config_fields)
        self.entry_2.grid(row=1, column=1, pady=5)
        # Link 3
        self.link3_lbe = tk.Label(self.config_fields, text="L3: ")
        self.link3_lbe.grid(row=2, column=0, pady=5)
        self.entry_3 = tk.Entry(self.config_fields)
        self.entry_3.grid(row=2, column=1, pady=5)

        self.set_button = tk.Button(self.config_fields, text="Set lenght", command=self.get_links_lenght)
        self.set_button.grid(row=3, column=0, columnspan=2, pady=15)
        ## END - Config Links ##
        
        ## Input position ##
        # X
        self.x_lbe = tk.Label(self.input_fields, text="X: ")
        self.x_lbe.grid(row=0, column=0, pady=5)
        self.x_entry_1 = tk.Entry(self.input_fields)
        self.x_entry_1.grid(row=0, column=1, pady=5)
        # Y
        self.y_lbe = tk.Label(self.input_fields, text="Y: ")
        self.y_lbe.grid(row=1, column=0, pady=5)
        self.y_entry_2 = tk.Entry(self.input_fields)
        self.y_entry_2.grid(row=1, column=1, pady=5)
        # phi Angle (Orientation)
        self.phi_lbe = tk.Label(self.input_fields, text="Orientation: ")
        self.phi_lbe.grid(row=2, column=0, pady=5)
        self.phi_entry_3 = tk.Entry(self.input_fields)
        self.phi_entry_3.grid(row=2, column=1, pady=5)
        ## END - Input position ##

        # Dark Mode Toggle button
        self.dark_mode_leb = tk.Label(self.config_fields, text="Dark mode:")
        self.dark_mode_leb.grid(row=4, column=0, pady=15, sticky="e")
        self.dark_mode_switch = widgets.ToggleSwitch(self.config_fields, width=50, height=25, command=self.on_switch_change)
        self.dark_mode_switch.grid(row=4, column=1, pady=15, sticky="w")

        # Button Simulate
        self.sim_button = tk.Button(self.input_fields, text="Display", command=self.get_new_position)
        self.sim_button.grid(row=4, column=0, columnspan=2, pady=15)

    def on_switch_change(self, state):
        if state:
            bg_main = "#202020"
            bg_entry = "#2b2b2b"
            fg_text = "white"
        else:
            bg_main = "white"
            bg_entry = "white"
            fg_text = "black"
        
        labels = [
            self.link1_lbe,
            self.link2_lbe,
            self.link3_lbe,
            self.x_lbe,
            self.y_lbe,
            self.phi_lbe,
            self.dark_mode_leb
        ]

        entries = [
            self.entry_1,
            self.entry_2,
            self.entry_3,
            self.x_entry_1,
            self.y_entry_2,
            self.phi_entry_3
        ]

        frames = [
            self.root,
            self.controls,
            self.config_fields,
            self.input_fields
        ]

        for label in labels:
            label.config(bg=bg_main, fg=fg_text)
        for entry in entries:
            entry.config(bg=bg_entry, fg=fg_text)
        for frame in frames:
            frame.config(bg=bg_main)

        self.canvas.config(bg=bg_entry)
        self.sim_button.config(bg=bg_entry, fg=fg_text)
        self.dark_mode_switch.config(bg=bg_main)

    def get_new_position(self):
        x = float(self.x_entry_1.get())
        y = float(self.y_entry_2.get())
        phi = float(self.phi_entry_3.get())

        l1 = self.my_robot.l1
        l2 = self.my_robot.l2
        l3 = self.my_robot.l3

        theta1, theta2, theta3 = kin.inv_kinematics(l1, l2, l3, phi, x, y)
        points = kin.calc_joint_positions(l1, l2, l3, theta1, theta2, theta3)
        self.my_robot.set_position(points)

    def get_links_lenght(self):
        l1 = float(self.entry_1.get())
        l2 = float(self.entry_2.get())
        l3 = float(self.entry_3.get())
        self.my_robot.set_link_lengths(l1, l2, l3)
        return (l1, l2, l3)

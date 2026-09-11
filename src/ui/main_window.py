import tkinter as tk
import ui.widgets as widgets
import kinematics as kin

class MainWin:
    def __init__(self, root):
        self.root = root
        self.root.title("TEST sim")
        self.root.geometry("1000x600")
        self.create_layout()
        self.create_controls()

    def create_layout(self):
        self.canvas = tk.Canvas(self.root, width=650, height=550, bg="white")
        self.canvas.pack(side="left", padx=10, pady=10)
        self.controls = tk.Frame(self.root)
        self.controls.pack(side="right", padx=50, expand=True)

    def create_controls(self):
        # Link 1
        self.link1_lbe = tk.Label(self.controls, text="L1: ")
        self.link1_lbe.grid(row=0, column=0, pady=5)
        self.entry_1 = tk.Entry(self.controls)
        self.entry_1.grid(row=0, column=1, pady=5)

        # Link 2
        self.link2_lbe = tk.Label(self.controls, text="L2: ")
        self.link2_lbe.grid(row=1, column=0, pady=5)
        self.entry_2 = tk.Entry(self.controls)
        self.entry_2.grid(row=1, column=1, pady=5)

        # Link 3
        self.link3_lbe = tk.Label(self.controls, text="L3: ")
        self.link3_lbe.grid(row=2, column=0, pady=5)
        self.entry_3 = tk.Entry(self.controls)
        self.entry_3.grid(row=2, column=1, pady=5)

        # Dark Mode Toggle button
        self.dark_mode_leb = tk.Label(self.controls, text="Dark mode:")
        self.dark_mode_leb.grid(row=3, column=0, pady=15, sticky="e")
        self.dark_mode_switch = widgets.ToggleSwitch(self.controls, width=50, height=25, command=self.on_switch_change)
        self.dark_mode_switch.grid(row=3, column=1, pady=15, sticky="w")

        # Button Simulate
        self.sim_button = tk.Button(self.controls, text="Show ans", command=self.print_ans)
        self.sim_button.grid(row=4, column=0, columnspan=2, pady=15)

    def on_switch_change(self, state):
        if state:
            self.link1_lbe.config(bg="#202020", fg="white")
            self.link2_lbe.config(bg="#202020", fg="white")
            self.link3_lbe.config(bg="#202020", fg="white")
            self.dark_mode_leb.config(bg="#202020", fg="white")
            self.entry_1.config(bg="#2b2b2b", fg="white")
            self.entry_2.config(bg="#2b2b2b", fg="white")
            self.entry_3.config(bg="#2b2b2b", fg="white")
            self.sim_button.config(bg="#2b2b2b", fg="white")

            self.root.config(bg="#202020")
            self.controls.config(bg="#202020")
            self.canvas.config(bg="#2b2b2b")
            self.dark_mode_switch.config(bg="#202020")
        else:
            self.link1_lbe.config(bg="white", fg="black")
            self.link2_lbe.config(bg="white", fg="black")
            self.link3_lbe.config(bg="white", fg="black")
            self.dark_mode_leb.config(bg="white", fg="black")
            self.entry_1.config(bg="white", fg="black")
            self.entry_2.config(bg="white", fg="black")
            self.entry_3.config(bg="white", fg="black")
            self.sim_button.config(bg="white", fg="black")

            self.root.config(bg="white")
            self.controls.config(bg="white")
            self.canvas.config(bg="white")
            self.dark_mode_switch.config(bg="white")

    def print_ans(self):
        l1 = self.entry_1.get()
        l2 = self.entry_2.get()
        l3 = self.entry_3.get()

        print(l1, l2, l3)

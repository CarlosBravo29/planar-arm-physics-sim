import tkinter as tk

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, width=35, height=20, command=None, *args, **kwargs):
        kwargs["width"] = width
        kwargs["height"] = height
        kwargs.setdefault("bg", parent.cget("bg"))
        kwargs.setdefault("highlightthickness", 0)

        super().__init__(parent, *args, **kwargs)
        self.command = command
        self.is_on = False

        self.w = width
        self.h = height

        self.color_on = "#13a399"
        self.color_off = "#e0e0e0"
        self.color_knob = "white"

        self.padding = 4
        self.knob_size = self.h - (self.padding * 2)

        self.x_off = self.padding
        self.x_on = self.w - self.knob_size - self.padding

        self.background = self.create_rectangle(2, 2, self.w - 2, self.h - 2, fill=self.color_off, outline="")
        self.knob = self.create_rectangle(self.x_off, self.padding, self.x_off + self.knob_size, self.padding + self.knob_size, fill=self.color_knob, outline="")

        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        self.is_on = not self.is_on
        if self.is_on:
            self.set_position(self.x_on, self.color_on)
        else:
            self.set_position(self.x_off, self.color_off)
        if self.command:
            self.command(self.is_on)

    def set_position(self, x, bg_color):
        self.itemconfig(self.background, fill=bg_color)
        self.coords(self.knob, x, self.padding, x + self.knob_size, self.padding + self.knob_size)

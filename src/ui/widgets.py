import tkinter as tk

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, width=50, height=25, command=None, *args, **kwargs):
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
        self.color_circle = "white"

        r = self.h - 2

        self.bg_oval1 = self.create_oval(2, 2, r, r, fill=self.color_off, outline="")
        self.bg_oval2 = self.create_oval(self.w - r, 2, self.w - 2, r, fill=self.color_off, outline="")
        self.bg_rect = self.create_rectangle(r / 2, 2, self.w - (r / 2), r, fill=self.color_off, outline="")

        self.padding = 4
        self.circle_size = self.h - self.padding * 2

        self.x_off = self.padding
        self.x_on = self.w - self.circle_size - self.padding

        self.circle = self.create_oval(self.x_off, self.padding, self.x_off + self.circle_size, self.padding + self.circle_size, fill=self.color_circle, outline="")
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
        self.itemconfig(self.bg_oval1, fill=bg_color)
        self.itemconfig(self.bg_oval2, fill=bg_color)
        self.itemconfig(self.bg_rect, fill=bg_color)

        self.coords(self.circle, x, self.padding, x + self.circle_size, self.padding + self.circle_size)

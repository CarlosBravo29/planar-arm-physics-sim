import sys
import tkinter as tk
import kinematics as kin
from ui.main_window import MainWin as mw


def main():
    root = tk.Tk()
    app = mw(root)
    root.mainloop()

if __name__ == "__main__":
    main()

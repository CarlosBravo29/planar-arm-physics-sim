import sys
import tkinter as tk
import kinematics as kin

root = tk.Tk()

root.title("TEST sim")
root.geometry("900x600")


def print_ans():
    l1 = entry_1.get()
    l2 = entry_2.get()
    l3 = entry_3.get()
    print(l1, l2, l3)


canvas = tk.Canvas(root, width=650, height=550, bg="white")
canvas.pack(side="left", padx=10, pady=10)
#canvas.create_oval(95, 95, 105, 105, fill="blue")

controls = tk.Frame(root)
controls.pack(side="right", padx=50)

label_1 = tk.Label(controls, text="L1: ").grid(row=0, column=0)
entry_1 = tk.Entry(controls)
entry_1.grid(row=0, column=1)

label_2 = tk.Label(controls, text="L2: ").grid(row=1, column=0)
entry_2 = tk.Entry(controls)
entry_2.grid(row=1, column=1)

label_3 = tk.Label(controls, text="L2: ").grid(row=2, column=0)
entry_3 = tk.Entry(controls)
entry_3.grid(row=2, column=1)

button = tk.Button(controls, text="Show ans", command=print_ans)
button.grid(row=4, column=0)

root.mainloop()
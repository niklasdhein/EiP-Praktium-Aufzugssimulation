import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Chose your settings")
root.configure(bg='#646464')
root.resizable(False, False)

entry_style = ttk.Style()
entry_style.configure("BW.TLabel", foreground="black", background="#646464")


def start_simulation():
    pass

# elevators amount
ttk.Label(
    root,
    text="Elevators:",
    style = "BW.TLabel"
).grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
elevators = ttk.Entry(root)
elevators.grid(row=0, column=2, padx=5, pady=5, ipadx=9)

# levels amount
ttk.Label(
    root,
    text="Levels:",
    style = "BW.TLabel"
).grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
levels = ttk.Entry(root)
levels.grid(row=1, column=2, padx=5, pady=5, ipadx=9)

# portion big elevators
ttk.Label(
    root,
    text="Portion of big elevators:",
    style = "BW.TLabel"
).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
height = ttk.Entry(root)
height.grid(row=2, column=2, padx=5, pady=5, ipadx=9)

#mode
ttk.Label(
    root,
    text="Mode:",
    style = "BW.TLabel"
).grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)
mode = ttk.Combobox(
    root,
    values = ["Random", "Up and Down", "Algorithm"],
    state="readonly"
)
mode.grid(row=0, column=4, padx=5, pady=5)


#spawn rate
ttk.Label(
    root,
    text="Spawn rate:",
    style = "BW.TLabel"
).grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
spawn = ttk.Entry(root)
spawn.grid(row=1, column=4, padx=5, pady=5, ipadx=9)

# patience
ttk.Label(
    root,
    text="Patience (s):",
    style = "BW.TLabel"
).grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)
patience = ttk.Entry(root)
patience.grid(row=2, column=4, padx=5, pady=5, ipadx=9)

# start
start = ttk.Button(
    root,
    text="Start",
    command=start_simulation
)
start.grid(row=5, column=4, padx=5, pady=5, sticky=tk.E)

root.mainloop()
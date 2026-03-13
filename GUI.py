import simulation

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Chose your settings")
root.configure(bg='#646464')
root.resizable(False, False)

entry_style = ttk.Style()
entry_style.configure("BW.TLabel", foreground="black", background="#646464")


def start_simulation():
    simulation.start_simulation(
        elevator_count=int(elevators.get()), 
        level_count=int(levels.get()),
        big_elevator_spawn_probability=float(big_elevator_spawn_probability.get()),
        speed_multiplier=int(speed_multiplier.get()),
        elevator_mode=mode.get(),
        passenger_spawn_rate=float(spawn.get()),
        passenger_patience=int(patience.get()),
        #simulation_time=int(simulation_time.get())
    )

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
big_elevator_spawn_probability = ttk.Entry(root)
big_elevator_spawn_probability.grid(row=2, column=2, padx=5, pady=5, ipadx=9)

# speed multiplier
ttk.Label(
    root,
    text="Speed multiplier:",
    style = "BW.TLabel"
).grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
speed_multiplier = ttk.Entry(root)
speed_multiplier.grid(row=3, column=2, padx=5, pady=5, ipadx=9)

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

# simulation time
ttk.Label(
    root,
    text="Simulation time:",
    style = "BW.TLabel"
).grid(row=3, column=3, padx=5, pady=5, sticky=tk.E)
simulation_time = ttk.Entry(root)
simulation_time.grid(row=3, column=4, padx=5, pady=5, ipadx=9)

# start
start = ttk.Button(
    root,
    text="Start",
    command=start_simulation
)
start.grid(row=5, column=4, padx=5, pady=5, sticky=tk.E)

root.mainloop()
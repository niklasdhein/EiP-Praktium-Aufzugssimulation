import matplotlib.pyplot as plt

import simulation

fig, ax = plt.subplots()

def pie_split(transported, annoyed, spawned):
    labels = ['transported', 'annoyed', 'still traveling']
    traveling = spawned - (transported + annoyed)
    sizes = [transported, annoyed, traveling]
    ax.pie(sizes, labels=labels)
    plt.show()

if __name__ == "__main__":
    #def elevator_effectiveness
    pie_split(5, 2, 9)

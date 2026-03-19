import matplotlib.pyplot as plt

fig, ax = plt.subplots()

def pie_split(transported=int, annoyed=int, spawned=int) -> None:
    labels = ['transported', 'annoyed', 'still traveling']
    traveling = spawned - (transported + annoyed)
    sizes = [transported, annoyed, traveling]
    ax.pie(sizes, labels=labels)
    plt.show()

def elevator_efficiency(transported=int, elevators=list) -> None:
    values = []
    labels = []
    for i in range(len(elevators)):
        if elevators[i].capacity <= 1000:
            labels.append(f"Elevator {i}:small")
        else:
            labels.append(f"Elevator {i}:big")
        transported_elevator = elevators[i].passengers_transported
        values.append(transported_elevator/transported*100)
    plt.bar(labels, values)
    plt.ylabel('transported/elevator')
    plt.show()



if __name__ == "__main__":
    #def elevator_effectiveness
    pie_split(5, 2, 9)

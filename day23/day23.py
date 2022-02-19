from itertools import cycle, islice, dropwhile

import numpy as np

with open('input_test.txt') as file:
    labels = file.read().strip()

NUMBER_MOVES = 10
NUMBER_CUPS = len(labels)

current_labels = np.array([int(x) for x in labels], dtype=np.ubyte)
current_cup = current_labels[0]
current_cup_index = 0
for _ in range(NUMBER_MOVES):
    print(current_labels)
    labels_cycle = cycle(current_labels)
    pick_up = np.array(list(islice(labels_cycle, current_cup_index + 1, current_cup_index + 4)))
    print(pick_up)
    current_labels = np.delete(current_labels, np.where(np.isin(current_labels, pick_up, assume_unique=True)))
    # if end_pick_up_index < start_pick_up_index:
    # pick_up = current_labels[start:end]

    try:
        destination = current_labels[current_labels < current_cup].max()
    except ValueError:
        destination = current_labels[current_labels != current_cup].max()

    #print(destination)
    destination_index = np.argwhere(current_labels == destination)[0][0]
    current_labels = np.concatenate([current_labels[:destination_index + 1],
                                     pick_up,
                                     current_labels[destination_index + 1:]])
    current_cup_index = (np.argwhere(current_labels == current_cup)[0][0] + 1) % 9
    current_cup = current_labels[current_cup_index]

result = ''.join(str(x) for x in islice(dropwhile(lambda x: x != 1, cycle(current_labels)),1, 9))
print(result)

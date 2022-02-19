from itertools import cycle, islice, dropwhile

import numpy as np

with open('input_test.txt') as file:
    labels = file.read().strip()

NUMBER_MOVES = 1000
NUMBER_CUPS = 1000000

if NUMBER_CUPS == 9:
    current_labels = np.array([int(x) for x in labels])
else:
    current_labels = np.concatenate([np.array([int(x) for x in labels], dtype=np.uint32),
                                     np.arange(10, NUMBER_CUPS + 1, dtype=np.uint32)],
                                    dtype=np.uint32)
current_cup = current_labels[0]
current_cup_index = 0
for _ in range(NUMBER_MOVES):
    # print('')
    # print(current_cup_index)
    # print(current_cup)
    # print(current_labels)
    pick_up_indices = np.remainder(np.array([current_cup_index + 1, current_cup_index + 2, current_cup_index + 3],
                                            dtype=np.uint32), NUMBER_CUPS, dtype=np.uint32)
    # print(pick_up_indices)
    pick_up = current_labels[pick_up_indices]
    #print(pick_up)
    current_labels = np.delete(current_labels, pick_up_indices)

    destination_index = np.argmax(np.where(current_labels < current_cup, current_labels, 0))
    if current_labels[destination_index] >= current_cup:
        destination_index = np.argmax(np.where(current_labels != current_cup, current_labels, 0))

    # print(destination_index)
    # print(current_labels[destination_index])

    current_labels = np.concatenate([current_labels[:destination_index + 1],
                                     pick_up,
                                     current_labels[destination_index + 1:]])

    #print(current_labels)
    cup_remove_add = max(current_cup_index+4-NUMBER_CUPS,0)
    if destination_index < current_cup_index:
        left_add = 4
    elif destination_index + 4 > NUMBER_CUPS:
        left_add = (destination_index + 4) - NUMBER_CUPS
    else:
        left_add = 1
    current_cup_index = (current_cup_index + left_add - cup_remove_add) % NUMBER_CUPS
    current_cup = current_labels[current_cup_index]

#result = ''.join(str(x) for x in islice(dropwhile(lambda x: x != 1, cycle(current_labels)), 1, 9))
print(current_labels[-5:5])

import re
from typing import Tuple

import numpy as np

with open('input.txt') as file:
    fields_raw, my_ticket_raw, other_tickets_raw = file.read().split('\n\n')

FIELDS = {field_name: ((int(range1_1), int(range1_2)), (int(range2_1), int(range2_2)))
          for line in fields_raw.strip().split('\n')
          for field_name, range1_1, range1_2, range2_1, range2_2
          in [re.match(r'^([\S ]+): (\d+)-(\d+) or (\d+)-(\d+)$', line.strip()).groups()]}

MY_TICKET = tuple(int(x) for x in re.findall(r'\d+', my_ticket_raw))

OTHER_TICKETS = tuple(tuple(int(x) for x in re.findall(r'\d+', line))
                      for i, line in enumerate(other_tickets_raw.strip().split('\n')) if i > 0)

errors = 0
correct_tickets = []

for ticket in OTHER_TICKETS:
    for number in ticket:
        if all(not (low1 <= number <= high1 or low2 <= number <= high2)
               for (low1, high1), (low2, high2) in FIELDS.values()):
            errors += number
            break

print(errors)


# part2
def is_valid_ticket(ticket_numbers: Tuple[int]):
    return all(any(low1 <= number_ <= high1 or low2 <= number_ <= high2
                   for (low1, high1), (low2, high2) in FIELDS.values())
               for number_ in ticket_numbers)


valid_tickets = np.array(tuple(ticket for ticket in OTHER_TICKETS if is_valid_ticket(ticket)))

possible_fields_for_names = {name: set(range(len(FIELDS))) for name in FIELDS}

# throw out all solutions simply not possible by comparing the conditions to each column
for i, line in enumerate(valid_tickets.T):
    for name, ((low1, high1), (low2, high2)) in FIELDS.items():
        if not all(low1 <= number_ <= high1 or low2 <= number_ <= high2 for number_ in line):
            possible_fields_for_names[name].remove(i)

found_solutions = set()
# iterate through all fields until only one possibility for each is left
while any(len(x) > 1 for x in possible_fields_for_names.values()):
    for name, p in possible_fields_for_names.items():
        if len(p) == 1 and not p.issubset(found_solutions):
            found_solutions.union(p)
            for name2 in possible_fields_for_names:
                if name2 != name:
                    possible_fields_for_names[name2] -= p

departure_fields_indices = {next(iter(x)) for name, x in possible_fields_for_names.items()
                            if name.startswith('departure')}
result = np.product([value for i, value in enumerate(MY_TICKET) if i in departure_fields_indices])

print(result)

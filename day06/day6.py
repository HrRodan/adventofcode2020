with open('input.txt') as file:
    groups = [line.strip().split('\n') for line in file.read().split('\n\n')]

# part1
result = sum(len(set(''.join(group))) for group in groups)
print(result)

# part2

count_yes = 0
for group in groups:
    yes_answers = set(group[0])
    for person in group[1:]:
        yes_answers = yes_answers.intersection(set(person))
    count_yes += len(yes_answers)

print(count_yes)

import re

with open('input.txt') as file:
    pwlist = [tuple((int(a), int(b), c, d)) for line in file.readlines()
              for a, b, c, d in [re.match(r'^(\d+)-(\d+) ([a-z]): (\S+)$', line).groups()]]

# part1

count_correct_pw = 0
for min_, max_, letter, pw in pwlist:
    letter_count = pw.count(letter)
    if min_ <= letter_count <= max_:
        count_correct_pw += 1

print(count_correct_pw)

# part2

count_correct_pw_2 = 0
for min_, max_, letter, pw in pwlist:
    if (pw[min_ - 1] == letter) ^ (pw[max_ - 1] == letter):
        count_correct_pw_2 += 1

print(count_correct_pw_2)

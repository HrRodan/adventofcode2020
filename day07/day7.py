import functools
import re

with open('input.txt') as file:
    rules = [line.strip()[:-1] for line in file.readlines() if line.strip()]

# noinspection PyTypeChecker
rules = dict(rule.replace('bags', 'bag').split(' contain ') for rule in rules)

rules_clean = {key: {} for key in rules}
for key, value in rules.items():
    for bag in value.split(', '):
        if bag != 'no other bag':
            number, bag_name = re.match(r'^(\d)+ ([\S ]+)$', bag).groups()
            rules_clean[key][bag_name] = int(number)
        else:
            rules_clean[key] = {}


@functools.cache
def get_upper_bags(bag: str):
    return {key for key, value in rules_clean.items() if bag in value}


def find_upmost_bags(intital_bag: str):
    final_bags = set()

    def find_next_bag(current_bag):
        if current_bag not in final_bags:
            final_bags.add(current_bag)
            for b in get_upper_bags(current_bag):
                find_next_bag(b)

    find_next_bag(intital_bag)
    return final_bags - {intital_bag}

#part2

def traverse_bags(current_bag):
    return sum(
        number_bag * (1 + traverse_bags(bag_))
        for bag_, number_bag in rules_clean[current_bag].items()
    )


if __name__ == '__main__':
    bag_start = 'shiny gold bag'
    print(len(find_upmost_bags(bag_start)))
    print(traverse_bags(bag_start))

import functools
import re

with open('input_test2.txt') as file:
    rules = [line.strip()[:-1] for line in file.readlines() if line.strip()]

# noinspection PyTypeChecker
rules = dict(rule.replace('bags', 'bag').split(' contain ') for rule in rules
             for value in [rule.replace('bags', 'bag').split(' contain ')])

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

def count_inner_bags(initial_bag: str):

    def traverse_bags(current_bag):
        if not rules_clean[current_bag]:
            return 1
        count_bag = 0 #sum(rules_clean[current_bag].values())
        for bag_, number_bag in rules_clean[current_bag].items():
            print(f'{bag_} {number_bag}')
            count_bag += number_bag*traverse_bags(bag_)


        return count_bag

    return traverse_bags(initial_bag)


if __name__ == '__main__':
    bag_start = 'shiny gold bag'
    print(len(find_upmost_bags(bag_start)))
    print(count_inner_bags(bag_start))

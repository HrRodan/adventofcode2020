import re
from copy import copy

with open('input.txt') as file:
    rules_raw, messages_raw = file.read().strip().split('\n\n')

rules_split = [re.match(r'(^\d+): ([ \S]+)$', line.strip()).groups() for line in rules_raw.split('\n')]
messages = messages_raw.split('\n')
rules = {' ' + str(x) + ' ': ' ' + y.replace('"', '') + ' ' for x, y in rules_split}
rule0: str = rules[' 0 ']


def replace_rule(start_rule: str, rule_dict: dict):
    while re.search(r'\d', start_rule):
        for old, new in rule_dict.items():
            start_rule = start_rule.replace(old, ' (' + new + ') ')
    return start_rule


# create regular expression from rule0
def clean_rule(rule_in: str):
    return r'^' + re.sub(r'\(([a-z])\)', r'\1', rule_in.replace(' ', '')) + r'$'


if __name__ == '__main__':
    x = replace_rule(rule0, rule_dict=rules)
    r1 = sum(re.search(clean_rule(x), line) is not None for line in messages)
    print(r1)

    rules_part2 = copy(rules)
    # 8: 42 | 42 8
    rules_part2[' 8 '] = ' 42 + '
    # 11: 42 31 | 42 11 31
    rules_part2[' 11 '] = ' 42 ~ 31 ~ '
    y_loop_clean = clean_rule(replace_rule(rule0, rules_part2))

    # create several rules so that the number of 42s and 31s of rule 11 are equal
    rules_final = [y_loop_clean.replace('~', '{' + str(y) + '}') for y in range(1, 11)]
    count = 0
    for line in messages:
        for rule in rules_final:
            if re.search(rule, line) is not None:
                count += 1
                break
    print(count)

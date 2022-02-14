import re
import sys
from itertools import takewhile

sys.setrecursionlimit(10000)

with open('input.txt') as file:
    rules_raw, messages_raw = file.read().strip().split('\n\n')

rules = [re.match(r'(^\d+): ([ \S]+)$', line.strip()).groups() for line in rules_raw.split('\n')]

messages = messages_raw.split('\n')

# add space to make values unique if more than one digit
rules = {str(x): re.sub(r'(\d+)', r'\1_', y).replace(' ', '').replace('"', '') for x, y in rules}

rule0: str = rules['0']


# while re.search(r'\d', rule0):
#     print(rule0)
#     for old, new in rules.items():
#         rule0 = rule0.replace(old, new)

def traverse_rule(start_rule_str: str, rule_dict: dict):
    start_rule = iter(start_rule_str)
    exp = ''
    while True:
        next_part: str = ''.join(takewhile(lambda x: x != '_', start_rule))
        is_wildcard = False
        # print(next_part)
        if not next_part:
            return exp
        # remove regex strings from rule and add to expression exp
        if next_part[0] == '|':
            exp += next_part[0]
            next_part = next_part[1:]
        if next_part[-1] == '+':
            is_wildcard = True
            next_part = next_part[:-1]
        # only char left
        if not next_part.isdigit():
            return next_part

        if is_wildcard:
            # add regex '+' at the end if number is wildcarded
            exp += '(' + traverse_rule(rule_dict[next_part], rule_dict=rule_dict) + ')+'
        else:
            exp += '(' + traverse_rule(rule_dict[next_part], rule_dict=rule_dict) + ')'


# create regular expression from rule0
def clean_rule(rule: str):
    return r'^' + re.sub(r'\(([a-z])\)', r'\1', rule) + r'$'


if __name__ == '__main__':
    x = traverse_rule(rule0, rule_dict=rules)
    r1 = sum(re.search(clean_rule(x), line) is not None for line in messages)
    print(r1)

    rules_part2 = rules.copy()
    # replace repetition by regex '+' to allow for arbitary number of repetitions
    rules_part2['8'] = '42+_'
    rules_part2['11'] = '42+_31+_'

    y = traverse_rule(rule0, rule_dict=rules_part2)
    rules_part2 = dict(sorted(rules_part2.items(), key=lambda x: int(x[0])))
    rule_clean_part2 = clean_rule(y)

    rules_results = {x: None for x in rules_part2}
    for rule_nr, rule in rules_part2.items():
        try:
            rules_results[rule_nr] = clean_rule(traverse_rule(rule, rule_dict=rules_part2))
        except RecursionError:
            continue

    count = 0
    for m in messages:
        if re.search(rule_clean_part2, m) is not None:
            n_42 = len(re.findall(rules_results['42'][1:-1], m))
            print(m)
            print(n_42)
            m = re.sub(r'^('+rules_results['42'][1:-1]+r')+','', m)
            print(m)
            n_31 = len(re.findall(rules_results['31'][1:-1], m))
            print(n_31)
            if n_31 < n_42:
                count += 1

    # r2 = sum(re.search(clean_rule(y), line) is not None for line in messages)
    # print(r2)

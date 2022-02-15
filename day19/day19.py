import re
import sys
from itertools import takewhile

sys.setrecursionlimit(10000)

with open('input.txt') as file:
    rules_raw, messages_raw = file.read().strip().split('\n\n')

rules_split = [re.match(r'(^\d+): ([ \S]+)$', line.strip()).groups() for line in rules_raw.split('\n')]

messages = messages_raw.split('\n')

# add _ to make values unique if more than one digit
rules = {str(x): re.sub(r'(\d+)', r'\1_', y).replace(' ', '').replace('"', '') for x, y in rules_split}

rule0: str = rules['0']

# try with loop
rules_loop = {' ' + str(x) + ' ': ' ' + y.replace('"', '') + ' ' for x, y in rules_split}
rule0_loop: str = rules_loop[' 0 ']


def replace_rule(start_rule: str, rule_dict: dict):
    while re.search(r'\d', start_rule):
        for old, new in rule_dict.items():
            start_rule = start_rule.replace(old, ' (' + new + ') ')
    return start_rule


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
    return r'^' + re.sub(r'\(([a-z])\)', r'\1', rule.replace(' ', '')) + r'$'


if __name__ == '__main__':
    x = traverse_rule(rule0, rule_dict=rules)
    r1 = sum(re.search(clean_rule(x), line) is not None for line in messages)
    print(r1)

    rules_part2 = rules.copy()
    # replace repetition by regex '+' to allow for arbitary number of repetitions
    rules_part2['8'] = '42+_'
    rules_part2['11'] = '42+_31+_'

    y = traverse_rule(rule0, rule_dict=rules_part2)
    rule_clean_part2 = clean_rule(y)
    r2 = sum(re.search(rule_clean_part2, line) is not None for line in messages)
    print(r2)

    # more data exploration
    rules_part2 = dict(sorted(rules_part2.items(), key=lambda x: int(x[0])))

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
            m = re.sub(r'^(' + rules_results['42'][1:-1] + r')+', '', m)
            n_31 = len(re.findall(rules_results['31'][1:-1], m))
            if n_31 < n_42:
                count += 1

    # try with loop
    rules_loop_part2 = {key: value for key, value in rules_loop.items()}
    rules_loop_part2[' 8 '] = ' 42 + '
    rules_loop_part2[' 11 '] = ' 42 ~ 31 ~ '
    y_loop_clean = clean_rule(replace_rule(rule0_loop, rules_loop_part2))

    # create more rules that the number of 42s and 31s of rule 11 are equal
    rules_final = [y_loop_clean.replace('~', '{' + str(y) + '}') for y in range(1, 11)]
    count = 0
    for line in messages:
        for rule in rules_final:
            if re.search(rule, line) is not None:
                count += 1
                break
    print(count)
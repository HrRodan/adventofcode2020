import operator
from itertools import takewhile

with open('input.txt') as file:
    formulas = [line.strip().replace(' ', '') for line in file.readlines()]

OPS = {'+': operator.add, '*': operator.mul}

formulas = [[int(x) if x.isdigit() else x for x in line] for line in formulas]

class FormulaBracket():
    def __init__(self):
        #initialize to 1 because it's only called when there is alread a open bracket found
        self.count_brackets_open = 1

    def __call__(self, letter : str):
        if letter == '(':
            self.count_brackets_open += 1
        elif letter == ')':
            self.count_brackets_open -= 1
        return self.count_brackets_open != 0



def calc(formula_part: iter):
    result = None
    while True:
        try:
            x = next(formula_part)
        except StopIteration:
            return result
        if type(x) == int and not result:
            result = x
        elif x in OPS:
            op = OPS[x]
            next_part = next(formula_part)
            if type(next_part) == int:
                result = op(result, next_part)
            elif next_part == '(':
                condition = FormulaBracket()
                result = op(result, calc(takewhile(condition, formula_part)))

#part 2
def calc_part2(formula_part: iter):
    result = None
    while True:
        try:
            x = next(formula_part)
        except StopIteration:
            return result
        if type(x) == int and not result:
            result = x
        elif x in OPS:
            if x == '*':
                # calculate everything first if operator is mul
                result *= calc_part2(formula_part)
            elif x == '+':
                next_part = next(formula_part)
                if type(next_part) == int:
                    result += next_part
                elif next_part == '(':
                    condition = FormulaBracket()
                    result += calc_part2(takewhile(condition, formula_part))
        # only for open bracket directly at start
        elif x == '(':
            condition = FormulaBracket()
            result = calc_part2(takewhile(condition, formula_part))





if __name__ == '__main__':
    r = sum(calc(iter(f)) for f in formulas)
    print(r)
    r2 = sum(calc_part2(iter(f)) for f in formulas)
    print(r2)

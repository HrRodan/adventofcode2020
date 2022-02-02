import re

with open('input.txt') as file:
    pp_data = [line.strip().replace('\n', ' ') for line in file.read().split('\n\n')]

# cid optional
necessary_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

result = sum(all(field in pp for field in necessary_fields) for pp in pp_data)

print(result)


# part 2
def check_hgt(hgt: str):
    if match := re.match(r'^(\d+)(cm|in)$', hgt):
        height, unit = match.groups()
        return (unit == 'cm' and 150 <= int(height) <= 193) \
               or (unit == 'in' and 59 <= int(height) <= 76)
    else:
        return False


count_correct = 0
valids_own = []
for pp in pp_data:
    if all(field in pp for field in necessary_fields):
        # noinspection PyTypeChecker
        fields = dict(line.split(':') for line in pp.split())
        if fields['byr'].isdigit() \
                and 1920 <= int(fields['byr']) <= 2002 \
                and fields['iyr'].isdigit() \
                and 2010 <= int(fields['iyr']) <= 2020 \
                and fields['eyr'].isdigit() \
                and 2020 <= int(fields['eyr']) <= 2030 \
                and check_hgt(fields['hgt']) \
                and fields['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'] \
                and re.match(r'^\d{9}$', fields['pid']) \
                and re.match(r'^#[0-9a-f]{6}$', fields['hcl']):
            count_correct += 1

print(count_correct)

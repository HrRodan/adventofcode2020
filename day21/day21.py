import re

with open('input.txt') as file:
    foods = [(set(re.findall(r'(?<![\(a-z])[a-z]+(?= )', line.strip())),
              set(re.findall(r'[a-z]+(?=[,\)])', line.strip())))
             for line in file.readlines()]

all_ingredients = set()
all_allergenes = set()
allergen_translation = {}
for ingredients, allergenes in foods:
    all_ingredients.update(ingredients)
    all_allergenes.update(allergenes)
    for allergene in allergenes:
        if allergene not in allergen_translation:
            allergen_translation[allergene] = ingredients
        else:
            allergen_translation[allergene] = allergen_translation[allergene].intersection(ingredients)

# remove possible translations by starting at the allergenes with already known translation (len == 1)
while any(len(t) != 1 for t in allergen_translation.values()):
    for allergene, translations in allergen_translation.items():
        if len(translations) == 1:
            for a, value in allergen_translation.items():
                if a != allergene:
                    value -= translations

all_allergenes_translated = set().union(*allergen_translation.values())
non_allergene_ingredients = all_ingredients - all_allergenes_translated

count_non_allergene_ingredients = sum(ingredient in non_allergene_ingredients
                                      for ingredients, _ in foods
                                      for ingredient in ingredients)

print(count_non_allergene_ingredients)
print(','.join(next(iter(y)) for _, y in sorted(allergen_translation.items())))

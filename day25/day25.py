from numba import njit

with open('input.txt') as file:
    card_pk, door_pk = [int(line.strip()) for line in file.readlines()]


@njit
def decrypt_key(pk: int):
    loop = 0
    value = 1
    while True:
        loop += 1
        value = (value * 7) % 20201227
        if value == pk:
            return loop


@njit
def encrypt_int(loop_size: int, subject_number: int):
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % 20201227
    return value


loop_size_card, loop_size_door = (decrypt_key(card_pk), decrypt_key(door_pk))

print(encrypt_int(loop_size_card, door_pk))

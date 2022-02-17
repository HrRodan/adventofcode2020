from collections import deque
from typing import List, Tuple, Union

with open('input.txt') as file:
    players_raw = file.read().strip().split('\n\n')

players_start: Tuple[Tuple[int]] = tuple(tuple(int(card) for i, card in enumerate(player_raw.split('\n')) if i > 0)
                                         for player_raw in players_raw)


def find_winning_player(players_in: List[deque]) -> Union[Tuple[int, List[deque]], bool]:
    if all(len(player) != 0 for player in players_in):
        return False
    for j, player in enumerate(players_in):
        if len(player) > 0:
            return j, players_in


def get_player_score(player_in: deque):
    return sum(
        i * player_in.pop()
        for i in range(1, len(player_in) + 1)
    )


def play_game_part1(players_in: List[deque]):
    while all(len(player) > 0 for player in players_in):
        cards = [player.popleft() for player in players_in]
        players_in[cards.index(max(cards))].extend(sorted(cards, reverse=True))
    return find_winning_player(players_in)


player_won_part1, players_part1 = play_game_part1([deque(player) for player in players_start])

print(get_player_score(players_part1[player_won_part1]))


# part 2

def play_game_part2(players_in: List[deque]) -> (int, List[deque]):
    previous_decks = [set() for _ in range(len(players_in))]
    while True:
        # player 1 wins if
        for (i, player), previous_deck in zip(enumerate(players_in), previous_decks):
            if tuple(player) in previous_deck:
                return 0, players_in

        for player, previous_deck in zip(players_in, previous_decks):
            previous_deck.add(tuple(tuple(player)))

        cards = [player.popleft() for player in players_in]

        # condition for recursion
        if all(len(player) >= card for card, player in zip(cards, players_in)):
            next_cards = []
            for card, player in zip(cards, players_in):
                player_copy = player.copy()
                next_cards.append(deque(player_copy.popleft() for _ in range(card)))
            player_won, _ = play_game_part2(next_cards)
        else:
            player_won = cards.index(max(cards))
        # reorder cards so that first is from player who won
        cards = [cards.pop(player_won), *cards]
        players_in[player_won].extend(cards)

        if winning_player := find_winning_player(players_in):
            return winning_player


player_won_part2, players_part2 = play_game_part2([deque(player) for player in players_start])

print(get_player_score(players_part2[player_won_part2]))

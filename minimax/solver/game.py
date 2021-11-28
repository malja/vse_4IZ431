from enum import IntEnum, auto
import itertools
from heuristics import dice_roll_valuation
import random
from calculations import reroll, generate_valued_rolls
import copy

class PlayerID(IntEnum):
    PLAYER_A = auto()
    PLAYER_B = auto()

class GameState:
    def __init__(self, init_a = None, init_b = None):
        self.current_player = PlayerID.PLAYER_A
        self.rolls = {
            PlayerID.PLAYER_A: [0, 0, 0, 0, 0] if init_a == None else init_a,
            PlayerID.PLAYER_B: [0, 0, 0, 0, 0] if init_b == None else init_b
        }

    def __str__(self):
        value = f"Player A: {self.rolls[PlayerID.PLAYER_A]}\n"
        value += f"Player B: {self.rolls[PlayerID.PLAYER_B]}\n"
        value += f"Current player: {self.current_player.name}\n"

        return value

    def get_current_player(self):
        return self.current_player

    def switch_current_player(self):
        if self.current_player == PlayerID.PLAYER_A:
            self.current_player = PlayerID.PLAYER_B
        else:
            self.current_player = PlayerID.PLAYER_A

    def get_current_player_roll(self):
        return self.rolls[self.current_player]

    def roll(self, dices: list[bool]):
        """
        vytvoří novou instanci s hodem, který je určený polem dices pro aktuálně hraného hráče.
        """
        new_state = copy.deepcopy(self)
        
        for index, reroll in enumerate(dices):
            if reroll:
                new_state.rolls[self.current_player][index] = random.randint(1, 6)

        new_state.switch_current_player()
        return new_state

    def result(self) -> int:
        evaluation = {
            PlayerID.PLAYER_A: dice_roll_valuation(self.rolls[PlayerID.PLAYER_A]),
            PlayerID.PLAYER_B: dice_roll_valuation(self.rolls[PlayerID.PLAYER_B])
        }

        if evaluation[PlayerID.PLAYER_A] > evaluation[PlayerID.PLAYER_B]:
            return -1
        elif evaluation[PlayerID.PLAYER_A] == evaluation[PlayerID.PLAYER_B]:
            return 1
        else:
            return 0

def minimax(state: GameState, maximazing: bool):
    permutations = list(itertools.product([True, False], repeat=5))

    rolls = []

    for permutation in permutations:
        rolls.append(
            [reroll(state.get_current_player_roll(), permutation), permutation]
        )

    rolls.sort(reverse=maximazing)
    return rolls[0]
    
if __name__ == "__main__":
    generate_valued_rolls()
    
    # Pro debug
    random.seed(0)

    game_state = GameState([6,6,1,5,2], [4,4,4,1,2])
    result = minimax(game_state, True)
    print(f"Po výchozím nastavení by měl hráč A táhnout: {result[1]}. Dosáhne skóre: {result[0]}")

    # Hráč A hází kostkami 3, 4, 5. Na 5. mu padne 3. Zbytek na náhodě
    game_state = game_state.roll([False, False, True, True, True])
    game_state.rolls[PlayerID.PLAYER_A][4] = 3

    print(game_state)

    # Hráč B hází kostkami 4 a 5. Hody nechám na náhodě.
    game_state = game_state.roll([False, False, False, True, True])

    print(game_state)
    
    # Hodnocení pro hráče A - čím házet teď?
    result = minimax(game_state, True)
    print(f"Hráč A by měl házet: {result[1]}, aby dosáhl skóre {result[0]}")

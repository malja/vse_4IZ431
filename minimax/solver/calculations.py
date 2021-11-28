import itertools
from heuristics import dice_roll_valuation
import copy

ALL_ROLLS = None

def generate_valued_rolls():
    global ALL_ROLLS

    if ALL_ROLLS != None:
        return
    
    all_rolls = list(itertools.product([1, 2, 3, 4, 5, 6], repeat=5))
    
    valued_rolls = []
    for roll in all_rolls:
        valued_rolls.append([
            dice_roll_valuation(roll), roll
        ])

    ALL_ROLLS = valued_rolls

def filter_all_rolls(current_roll, changed_dices):
    filtered = copy.deepcopy(ALL_ROLLS)

    # Projde každý možný výsledek hodu
    for index in range(len(filtered)):
        # V něm projde každou kostku
        for dice_index, dice in enumerate(filtered[index][1]):
            # Pokud se tato kostka má měnit, není třeba její výsledek kontrolovat
            if changed_dices[dice_index]:
                continue

            if dice != current_roll[dice_index]:
                filtered[index] = None
   
    # Vrátí výsledky hodů, které by ještě mohly nastat
    return filter(lambda x: x != None, filtered)

def reroll(current_roll, dices: list[bool]):
    # Seznam všech možný výsledků, pokud by se měnily jen vybrané kostky, seřazený podle ohodnocení
    filtered = sorted(filter_all_rolls(current_roll, dices))
    
    score = 0
    weight = 0

    # Ještě do hodnocení musím zamíchat pravděpodobnost
    for roll_index in range(len(filtered)):
        # Ohodnocení hodu pronásobím jeho pravděpodobností
        probability = calculate_probability(current_roll, filtered[roll_index][1])
        score += filtered[roll_index][0] * probability
        weight += probability
    
    return score/weight

def calculate_probability(current_roll, wanted_roll):
    changed_dices = 0
    # Kolik kostek je reálně potřeba měnit?
    for index in range(len(current_roll)):
        if current_roll[index] != wanted_roll[index]:
            changed_dices += 1
    
    probability = 1/6 ** changed_dices
    return probability

if __name__ == "__main__":
    print(
        calculate_probability([1, 2, 1, 1, 2], [1, 1, 1, 1, 1])
    )
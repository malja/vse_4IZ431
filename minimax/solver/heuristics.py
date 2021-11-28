from collections import Counter

def dice_roll_valuation(roll: list[int]) -> int:
    """
    Pro předaný hod - tedy kombinaci 5 hodnot, které padly na kostkách vrátí jejich ohodnocení dle zadání.
    0-6     =   Nejvyšší hodnota. Pokud není nalezen žádný z dále popsaných možností, vrátí nejvyšší hodnotu, která
                padla na kostkách.
    7       =   Pár.
    8       =   Dva páry.
    9       =   Trojice.
    10      =   Full house - trojice a dvojice.
    11      =   Čtveřice.
    12      =   Postupka.
    13      =   Pětice.

    :param list roll:   Seznam 5 hodnot, které padly během hodu. Hodnota 0 popřípadě hodnoty vyšší než 6 jsou
                        považované za neplatné.
    """

    def roll_is_quintuplet(roll: list[int]) -> bool:
        """
        Funkce zkontroluje, zda předaný hod obsahuje pětici.
        """
        counter = Counter(roll)
        # Získá nejčastější hodnotu, která padla v daném hodu společně s počtem výskytů.
        most_common_pair = counter.most_common(1)[0]
        # Pokud je nejčastější hodnota obsažena 5x, jde o pětici
        return most_common_pair[1] == 5

    def roll_is_straight(roll: list[int]) -> bool:
        """
        Kontroluje, zda hod obsahuje postupku.
        """
        sorted_values = sorted(roll)

        # Projde celé pole od nejmenší hodnoty k nejvyšší
        # Poslední hodnota v poli sorted se již neprochází, protože není s čím kontrolovat
        for index in range(4):
            # Aktuální hodnota musí být pouze o 1 menší, než následující hodnota
            if sorted_values[index] + 1 != sorted_values[index + 1]:
                return False
        
        return True

    def roll_is_quaternion(roll: list[int]) -> bool:
        """
        Vrací true, pokud hod obsahuje čtveřici.
        """
        counter = Counter(roll)
        # Získá nejčastější hodnotu, která padla v daném hodu společně s počtem výskytů.
        most_common_pair = counter.most_common(1)[0]
        # Pokud je nejčastější hodnota obsažena 4x, jde o čtveřici
        return most_common_pair[1] == 4
    
    def roll_is_fullhouse(roll: list[int]) -> bool:
        """
        Vrací true, pokud hod je full house -> dvojice a trojice.
        """
        counter = Counter(roll)
        # Získá dvě nejčastější hodnoty, které padly v daném hodu společně s počtem výskytů.
        most_common_pair = counter.most_common(2)
        # Uloží počet výskytů u hodnoty, která se vyskytla nejčastěji
        most_common_count = most_common_pair[0][1]
        # Uloží počet výskytů u hodnoty, která se vyskytla jako druhá nejčastější
        second_most_common_count = most_common_pair[1][1]

        return most_common_count == 3 and second_most_common_count == 2

    def roll_is_trio(roll: list[int]) -> bool:
        """
        Vrací true, pokud hod obsahuje trojici.
        """
        counter = Counter(roll)
        most_common_pair = counter.most_common(1)[0]
        return most_common_pair[1] == 3

    def roll_is_two_pairs(roll: list[int]) -> bool:
        """
        Vrací true, pokud hod obsahuje dvě dvojice.
        """
        counter = Counter(roll)
        # Získá dvě nejčastější hodnoty, které padly v daném hodu společně s počtem výskytů.
        most_common_pair = counter.most_common(2)
        # Uloží počet výskytů u hodnoty, která se vyskytla nejčastěji
        most_common_count = most_common_pair[0][1]
        # Uloží počet výskytů u hodnoty, která se vyskytla jako druhá nejčastější
        second_most_common_count = most_common_pair[1][1]

        return most_common_count == 2 and second_most_common_count == 2

    def roll_is_pair(roll: list[int]) -> bool:
        """
        Vrací true, pokud hod obsahuje pouze jednu dvojici.
        """
        counter = Counter(roll)
        most_common_pair = counter.most_common(1)[0]
        return most_common_pair[1] == 2

    # Seznam párů "hodnotící funkce":"hodnocení". Pokud vyjde hodnotící funkce jako True, bude vráceno "hodnocení".
    ratings = [
        (roll_is_quintuplet, 13), (roll_is_straight, 12), (roll_is_quaternion, 11), 
        (roll_is_fullhouse, 10), (roll_is_trio, 9), (roll_is_two_pairs, 8), 
        (roll_is_pair, 7)
    ]
    # Projde všechny páry
    for rating in ratings:
        # Pokud vyjde hodnotící funkce jako True
        if rating[0](roll):
            # Vrátí dané hodnocení
            return rating[1]

    # Žádná hodnotící funkce není True, vrací nejvyšší hodnotu z hodu.
    return max(roll)

if __name__ == "__main__":
    print(dice_roll_valuation([1,2,3,4,5]))

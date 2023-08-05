elo_ratings = [2800, 2600, 2400, 2200, 2000, 1800, 1600, 800, 400, 100]


def floor_elo(elo_input: int) -> int:
    elo_counter = 0
    for elo_rating in elo_ratings[::-1]:
        if elo_input >= elo_rating:
            elo_counter = elo_rating
    return elo_counter

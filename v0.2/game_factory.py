from kpc import KeypadController
from I2C_LCD import I2cLcd
from game import Game, CthulhuGame, PulpCthulhuGame

supported_games = [
    "Call of Cthulhu",
    "Pulp Cthulhu",
]


def get_game(selected_game: str) -> Game:

    if selected_game == supported_games[0]:
        return CthulhuGame

    elif selected_game == supported_games[1]:
        return PulpCthulhuGame

    else:
        raise ValueError


def get_character_sheet() -> str:
    return "pulp_cthulhu_Ana_Engel.json"


class GameFactory:

    @classmethod
    def create_game(cls, keypad: KeypadController, lcd: I2cLcd, selected_game: str):
        file_path = get_character_sheet()
        game = get_game(selected_game)
        return game(keypad, lcd, file_path)

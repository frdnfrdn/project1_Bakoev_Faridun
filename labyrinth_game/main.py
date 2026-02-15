#!/usr/bin/env python3
"""Точка входа в игру Лабиринт сокровищ."""

from labyrinth_game.constants import COMMANDS, DIRECTIONS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str) -> None:
    """Обрабатывает команду пользователя."""
    parts = command.strip().split(maxsplit=1)

    if not parts:
        print("Введите команду. Введите 'help' для списка команд.")
        return

    action = parts[0]
    argument = parts[1] if len(parts) > 1 else ""

    match action:
        case 'go':
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление: north, south, east, west")
        case _ if action in DIRECTIONS:
            move_player(game_state, action)
        case 'look':
            describe_current_room(game_state)
        case 'take':
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет, который хотите поднять.")
        case 'use':
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет, который хотите использовать.")
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'help':
            show_help(COMMANDS)
        case 'quit' | 'exit':
            print("Спасибо за игру! До встречи!")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main() -> None:
    """Основная функция игры."""
    game_state: dict = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Введите 'help' для списка команд.\n")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)

    print(f"\nИгра окончена. Шагов сделано: {game_state['steps_taken']}")


if __name__ == "__main__":
    main()

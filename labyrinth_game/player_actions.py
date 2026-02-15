#!/usr/bin/env python3
"""Действия игрока: перемещение, инвентарь, использование предметов."""

from labyrinth_game.constants import ROOMS


def get_input(prompt: str = "> ") -> str:
    """Получает ввод от пользователя."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    """Перемещает игрока в указанном направлении."""
    from labyrinth_game.utils import describe_current_room

    room = ROOMS[game_state['current_room']]

    if direction not in room['exits']:
        print("Нельзя пойти в этом направлении.")
        return

    game_state['current_room'] = room['exits'][direction]
    game_state['steps_taken'] += 1
    describe_current_room(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Подбирает предмет из комнаты."""
    room = ROOMS[game_state['current_room']]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name not in room['items']:
        print("Такого предмета здесь нет.")
        return

    room['items'].remove(item_name)
    game_state['player_inventory'].append(item_name)
    print(f"Вы подняли: {item_name}")


def show_inventory(game_state: dict) -> None:
    """Показывает инвентарь игрока."""
    inventory = game_state['player_inventory']

    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("Ваш инвентарь:")
    for item in inventory:
        print(f"  - {item}")


def use_item(game_state: dict, item_name: str) -> None:
    """Использует предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case 'torch':
            print("Вы зажигаете факел. Стало светлее!")
        case 'sword':
            print("Вы держите меч наготове. Чувствуете себя увереннее!")
        case 'bronze_box':
            if 'rusty_key' not in game_state['player_inventory']:
                print(
                    "Вы открываете бронзовую шкатулку... "
                    "Внутри ржавый ключ!"
                )
                game_state['player_inventory'].append('rusty_key')
            else:
                print("Шкатулка пуста.")
        case _:
            print(f"Вы не знаете, как использовать {item_name}.")

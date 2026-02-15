#!/usr/bin/env python3
"""Вспомогательные функции игры."""

from labyrinth_game.constants import PUZZLE_REWARDS, ROOMS


def describe_current_room(game_state: dict) -> None:
    """Описывает текущую комнату."""
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        print(f"Заметные предметы: {', '.join(room['items'])}")

    print(f"Выходы: {', '.join(room['exits'].keys())}")

    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state: dict) -> None:
    """Решение загадки в текущей комнате."""
    from labyrinth_game.player_actions import get_input

    room_name = game_state['current_room']
    room = ROOMS[room_name]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(f"\n{question}")

    user_answer = get_input("Ваш ответ: ")

    if user_answer.strip().lower() == answer.lower():
        print("Верно! Загадка решена!")
        room['puzzle'] = None

        reward = PUZZLE_REWARDS.get(room_name)
        if reward:
            game_state['player_inventory'].append(reward)
            print(f"Вы получили: {reward}")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    """Попытка открыть сундук с сокровищами."""
    from labyrinth_game.player_actions import get_input

    room = ROOMS[game_state['current_room']]

    if 'treasure_chest' not in room['items']:
        print("Здесь нет сундука.")
        return

    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт. У вас нет ключа.")
    choice = get_input("Попробовать ввести код? (да/нет): ")

    if choice.strip().lower() == 'да':
        if room['puzzle'] is not None:
            question, answer = room['puzzle']
            print(question)
            code = get_input("Код: ")

            if code.strip() == answer:
                print("Код верный! Сундук открывается!")
                room['items'].remove('treasure_chest')
                room['puzzle'] = None
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается закрытым.")
        else:
            print("Код уже был введен ранее, но сундук всё ещё здесь...")
    else:
        print("Вы отступаете от сундука.")


def show_help() -> None:
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

#!/usr/bin/env python3
"""Вспомогательные функции игры."""

import math

from labyrinth_game.constants import (
    ALTERNATIVE_ANSWERS,
    EVENT_PROBABILITY,
    EVENT_TYPES_COUNT,
    HELP_CMD_WIDTH,
    PUZZLE_REWARDS,
    ROOMS,
    TRAP_DAMAGE_RANGE,
    TRAP_DEATH_THRESHOLD,
)


def pseudo_random(seed: int, modulo: int) -> int:
    """Псевдослучайное число в диапазоне [0, modulo) на основе синуса."""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return math.floor(fractional * modulo)


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
    alternatives = ALTERNATIVE_ANSWERS.get(answer.lower(), [])
    is_correct = (
        user_answer.strip().lower() == answer.lower()
        or user_answer.strip().lower() in alternatives
    )

    if is_correct:
        print("Верно! Загадка решена!")
        room['puzzle'] = None

        reward = PUZZLE_REWARDS.get(room_name)
        if reward:
            game_state['player_inventory'].append(reward)
            print(f"Вы получили: {reward}")
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == 'trap_room':
            trigger_trap(game_state)


def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки с негативными последствиями."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']
    steps = game_state['steps_taken']

    if inventory:
        index = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(index)
        print(f"В суматохе вы потеряли: {lost_item}")
    else:
        damage = pseudo_random(steps, TRAP_DAMAGE_RANGE)
        if damage < TRAP_DEATH_THRESHOLD:
            print("Ловушка оказалась смертельной! Вы проиграли.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться! Повезло.")


def random_event(game_state: dict) -> None:
    """Случайное событие при перемещении между комнатами."""
    steps = game_state['steps_taken']
    room_name = game_state['current_room']

    if pseudo_random(steps, EVENT_PROBABILITY) != 0:
        return

    event_type = pseudo_random(steps + 1, EVENT_TYPES_COUNT)

    match event_type:
        case 0:
            print("\n* Вы заметили на полу блестящую монетку!")
            ROOMS[room_name]['items'].append('coin')
        case 1:
            print("\n* Вы слышите шорох за стеной...")
            if 'sword' in game_state['player_inventory']:
                print("  Вы выхватили меч и отпугнули существо!")
        case 2:
            if (
                room_name == 'trap_room'
                and 'torch' not in game_state['player_inventory']
            ):
                print("\n* В темноте вы задели растяжку!")
                trigger_trap(game_state)


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

            alternatives = ALTERNATIVE_ANSWERS.get(answer.lower(), [])
            if code.strip() == answer or code.strip().lower() in alternatives:
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


def show_help(commands: dict) -> None:
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<{HELP_CMD_WIDTH}} - {desc}")

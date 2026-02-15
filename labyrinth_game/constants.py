#!/usr/bin/env python3
"""Константы и данные игрового мира."""


ROOMS: dict = {
    'entrance': {
        'description': (
            'Вы в темном входе лабиринта. '
            'Стены покрыты мхом. На полу лежит старый факел.'
        ),
        'exits': {
            'north': 'hall',
            'east': 'trap_room',
            'south': 'dark_corridor',
        },
        'items': ['torch'],
        'puzzle': None,
    },
    'hall': {
        'description': (
            'Большой зал с эхом. '
            'По центру стоит пьедестал с запечатанным сундуком.'
        ),
        'exits': {
            'south': 'entrance',
            'west': 'library',
            'north': 'treasure_room',
        },
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, '
            'которое идет после девяти". Введите ответ цифрой.',
            '10',
        ),
    },
    'trap_room': {
        'description': (
            'Комната с хитрой плиточной поломкой. '
            'На стене видна надпись: "Осторожно — ловушка".'
        ),
        'exits': {'west': 'entrance'},
        'items': ['rusty_key'],
        'puzzle': (
            'Система плит активна. Чтобы пройти, назовите слово '
            '"шаг" три раза подряд (введите "шаг шаг шаг").',
            'шаг шаг шаг',
        ),
    },
    'library': {
        'description': (
            'Пыльная библиотека. На полках старые свитки. '
            'Где-то здесь может быть ключ от сокровищницы.'
        ),
        'exits': {'east': 'hall', 'north': 'armory'},
        'items': ['ancient_book'],
        'puzzle': (
            'В одном свитке загадка: '
            '"Что растет, когда его съедают?" (ответ одно слово)',
            'резонанс',
        ),
    },
    'armory': {
        'description': (
            'Старая оружейная комната. На стене висит меч, '
            'рядом — небольшая бронзовая шкатулка.'
        ),
        'exits': {'south': 'library'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None,
    },
    'treasure_room': {
        'description': (
            'Комната сокровищ. На столе стоит большой сундук. '
            'Дверь заперта — нужен особый ключ.'
        ),
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': (
            'Сундук защищен кодом. Введите код '
            '(подсказка: число пятикратного шага, 2*5= ?)',
            '10',
        ),
    },
    'dark_corridor': {
        'description': (
            'Узкий тёмный коридор. Воздух здесь сырой и затхлый. '
            'Слышен далекий шум воды.'
        ),
        'exits': {'north': 'entrance', 'east': 'secret_room'},
        'items': [],
        'puzzle': None,
    },
    'secret_room': {
        'description': (
            'Секретная комната, скрытая за ложной стеной. '
            'На столе лежит потёртая карта лабиринта.'
        ),
        'exits': {'west': 'dark_corridor'},
        'items': ['old_map'],
        'puzzle': (
            'На стене начертана загадка: '
            '"У меня нет голоса, но я отвечаю. Что я?"',
            'эхо',
        ),
    },
}

PUZZLE_REWARDS: dict = {
    'hall': 'golden_coin',
    'trap_room': 'silver_ring',
    'library': 'treasure_key',
    'secret_room': 'magic_compass',
}

ALTERNATIVE_ANSWERS: dict = {
    '10': ['десять', 'ten'],
    'эхо': ['echo'],
}

COMMANDS: dict = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать список команд",
}

DIRECTIONS: tuple = ('north', 'south', 'east', 'west')

# Параметры случайных событий и ловушек
EVENT_PROBABILITY: int = 10
EVENT_TYPES_COUNT: int = 3
TRAP_DAMAGE_RANGE: int = 10
TRAP_DEATH_THRESHOLD: int = 3
HELP_CMD_WIDTH: int = 16

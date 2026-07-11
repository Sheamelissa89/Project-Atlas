import random

from entities.enemy import Enemy
from entities.player import Player
from map import GameMap


class Game:
    def __init__(self):
        self.player = Player()

        self.entities = [
            Enemy("Slime", 50, 10, 25),
            Enemy("Forest Snake", 80, 20, 75),
            Enemy("Wolf", 100, 25, 100),
            Enemy("Goblin", 60, 15, 50),
            Enemy("Orc", 120, 25, 100),
            Enemy("Troll", 150, 30, 150),
            Enemy("Dragon", 200, 40, 200),
            Enemy("Dark Knight", 250, 50, 300),
            Enemy("Necromancer", 300, 60, 400),
            Enemy("Demon Lord", 400, 80, 500),
            Enemy("Owl of the Night", 350, 70, 450),
        ]

        self.map = GameMap()

    def start(self):
        print("Welcome to Project Atlas!")
        print()

        self.player.show_status()
        print()

        self.map.show_location()
        print()

        self.battle()

    def battle(self):
        entity = random.choice(self.entities[:4])

        print("A wild entity appears!")
        print(f"Entity: {entity.name}")
        print()

        while self.player.is_alive() and entity.is_alive():
            self.player.attack(entity)
            print()

            if entity.is_alive():
                entity.attack(self.player)
                print()

        if self.player.is_alive():
            print(f"{self.player.name} won the battle!")
            entity.give_rewards(self.player)
        else:
            print(f"{self.player.name} was defeated...")
    
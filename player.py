class Player:
    def __init__(self, name="Shea", health=100, damage=30, level=1, exp=0):
        self.name = name
        self.health = health
        self.damage = damage
        self.level = level
        self.exp = exp

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        print(f"{self.name} takes {amount} damage.")
        print(f"{self.name} health: {self.health}")

    def attack(self, enemy):
        print(f"{self.name} attacks the {enemy.name}!")
        enemy.take_damage(self.damage)

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} EXP.")
        print(f"Total EXP: {self.exp}")

    def is_alive(self):
        return self.health > 0

    def show_status(self):
        print("===== PLAYER STATUS =====")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Damage: {self.damage}")
        print(f"Level: {self.level}")
        print(f"EXP: {self.exp}")
        print("=========================")
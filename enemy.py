class Enemy:
    def __init__(self, name="Goblin", health=60, damage=15, exp=50):
        self.name = name
        self.health = health
        self.damage = damage
        self.exp = exp

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

        if self.health == 0:
            print(f"The {self.name} was defeated!")
            print(f"Experience gained: {self.exp}")
        else:
            print(f"The {self.name} takes {amount} damage.")
            print(f"{self.name} health: {self.health}")

    def attack(self, player):
        print(f"The {self.name} attacks {player.name}!")
        player.take_damage(self.damage)

    def is_alive(self):
        return self.health > 0

    def __init__(self, name, health, damage, exp):
        self.name = name
        self.health = health
        self.damage = damage
        self.exp = exp

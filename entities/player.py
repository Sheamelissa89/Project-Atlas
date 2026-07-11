from .entity import Entity


class Player(Entity):
    def __init__(
        self,
        name="Shea",
        health=100,
        damage=30,
        level=1,
        exp=0
    ):
        super().__init__(name, health, damage)

        self.level = level
        self.exp = exp
        self.exp_to_next_level = 100
        self.potions = 0
        self.gold = 0

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} EXP.")
        self._check_level_up()

    def receive_gold(self, amount):
        self.gold += amount
        print(f"{self.name} received {amount} gold.")

    def receive_potions(self, amount):
        self.potions += amount
        print(f"{self.name} received {amount} potions.")

    def _check_level_up(self):
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1

            self.max_health += 20
            self.health = self.max_health
            self.damage += 5

            self.exp_to_next_level = int(
                self.exp_to_next_level * 1.25
            )

            print(f"{self.name} reached level {self.level}!")
            print(f"Maximum health increased to {self.max_health}.")
            print(f"Damage increased to {self.damage}.")

    def show_status(self):
        print("\n--- PLAYER STATUS ---")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"Potions: {self.potions}")

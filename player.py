class Player:
    def __init__(self, name="Shea", health=100, damage=30, level=1, exp=0):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.level = level
        self.exp = exp
        self.exp_to_next_level = 100
        self.potions = 0

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
        self._check_level_up()

    def _check_level_up(self):
        leveled = False

        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
            self.max_health += 20
            self.damage += 5
            self.health = self.max_health

            print(f"{self.name} leveled up! Now at level {self.level}.")
            leveled = True

        if leveled:
            self.show_status()

    def after_battle_reward(self):
        self.potions += 2
        print(f"{self.name} received 2 health potions.")
        print(f"Total potions: {self.potions}")

    def use_potion(self):
        if self.potions <= 0:
            print("No potions to use.")
            return

        self.potions -= 1
        heal_amount = 100
        self.health = min(self.max_health, self.health + heal_amount)

        print(f"{self.name} used a health potion.")
        print(f"{self.name} restored {heal_amount} health.")
        print(f"{self.name} health: {self.health}/{self.max_health}")

    def is_alive(self):
        return self.health > 0

    def show_status(self):
        print("===== PLAYER STATUS =====")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"Level: {self.level}")
        print(f"EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"Potions: {self.potions}")
        print("=========================")

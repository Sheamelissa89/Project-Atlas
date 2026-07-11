class Entity:
    """Base class for all living entities in Project Atlas."""

    def __init__(self, name, health, damage):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        amount = max(0, amount)
        self.health = max(0, self.health - amount)

        print(f"{self.name} takes {amount} damage.")
        print(f"{self.name} health: {self.health}/{self.max_health}")

    def attack(self, target):
        if not self.is_alive():
            print(f"{self.name} cannot attack because they have been defeated.")
            return

        print(f"{self.name} attacks {target.name}!")
        target.take_damage(self.damage)

    def heal(self, amount):
        if not self.is_alive():
            print(f"{self.name} cannot heal because they have been defeated.")
            return

        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        healed_amount = self.health - old_health

        print(f"{self.name} heals for {healed_amount} health.")
        print(f"{self.name} health: {self.health}/{self.max_health}")

    def __str__(self):
        return (
            f"{self.name} | "
            f"Health: {self.health}/{self.max_health} | "
            f"Damage: {self.damage}"
        )
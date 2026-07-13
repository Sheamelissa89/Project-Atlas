from .entity import Entity


class Player(Entity):
    def __init__(
        self,
        name="Shea",
        health=100,
        damage=30,
        level=1,
        exp=0,
        species="Human",
        role="Player",
        alignment="Neutral",
        background=(
            "A developing adventurer whose choices shape both "
            "the world and the entities within it."
        ),
        motivation="Growth, discovery, and meaningful choice",
        traits=None,
        abilities=None,
        emotions=None,
    ):
        default_traits = [
            "curious",
            "persistent",
            "adaptable",
            "compassionate",
            "independent",
        ]

        default_abilities = {
            "strength": 55,
            "knowledge": 55,
            "comprehension": 70,
            "ingenuity": 70,
            "perception": 60,
            "wisdom": 55,
            "adaptability": 75,
            "willpower": 75,
            "dexterity": 55,
            "endurance": 70,
            "charisma": 55,
            "empathy": 70,
            "intuition": 70,
            "discipline": 65,
            "courage": 70,
            "resilience": 75,
        }

        default_emotions = {
            "joy": 50,
            "fear": 20,
            "anger": 10,
            "sadness": 10,
            "curiosity": 75,
            "hope": 70,
            "confidence": 65,
            "affection": 20,
            "resentment": 0,
        }

        super().__init__(
            name=name,
            health=health,
            damage=damage,
            species=species,
            role=role,
            alignment=alignment,
            background=background,
            motivation=motivation,
            traits=traits if traits is not None else default_traits,
            abilities=(
                abilities
                if abilities is not None
                else default_abilities
            ),
            emotions=(
                emotions
                if emotions is not None
                else default_emotions
            ),
        )

        self.level = level
        self.exp = exp
        self.exp_to_next_level = 100
        self.potions = 0
        self.gold = 0

    def gain_exp(self, amount):
        amount = max(0, amount)

        self.exp += amount
        print(f"{self.name} gained {amount} EXP.")

        self._check_level_up()

    def receive_gold(self, amount):
        amount = max(0, amount)

        self.gold += amount
        print(f"{self.name} received {amount} gold.")

    def receive_potions(self, amount):
        amount = max(0, amount)

        self.potions += amount
        print(f"{self.name} received {amount} potions.")

    def use_potion(self, healing_amount=30):
        if self.potions <= 0:
            print(f"{self.name} does not have any potions.")
            return

        if self.health >= self.max_health:
            print(f"{self.name} is already at full health.")
            return

        self.potions -= 1
        self.heal(healing_amount)

        print(f"Potions remaining: {self.potions}")

    def _check_level_up(self):
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1

            self.max_health += 20
            self.health = self.max_health
            self.damage += 5

            self._increase_growth_abilities()

            self.exp_to_next_level = int(
                self.exp_to_next_level * 1.25
            )

            print(f"{self.name} reached level {self.level}!")
            print(
                f"Maximum health increased to "
                f"{self.max_health}."
            )
            print(f"Damage increased to {self.damage}.")

    def _increase_growth_abilities(self):
        """
        Improve selected abilities whenever the player levels up.

        The player grows mentally and emotionally as well as physically.
        """
        ability_growth = {
            "strength": 2,
            "comprehension": 2,
            "ingenuity": 2,
            "adaptability": 2,
            "willpower": 2,
            "endurance": 2,
            "discipline": 1,
            "courage": 1,
            "resilience": 2,
        }

        for ability, amount in ability_growth.items():
            current_value = self.abilities.get(ability, 50)

            self.abilities[ability] = self._clamp(
                current_value + amount
            )

    def show_status(self):
        dominant = self.dominant_emotion()

        print("\n--- PLAYER STATUS ---")
        print(f"Name: {self.name}")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"Potions: {self.potions}")
        print(f"Gold: {self.gold}")

        if dominant:
            intensity = self.get_emotional_intensity(dominant)

            print(
                f"Dominant emotion: "
                f"{dominant.title()} "
                f"({self.emotions[dominant]}, {intensity})"
            )

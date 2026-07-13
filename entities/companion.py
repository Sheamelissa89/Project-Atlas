from .entity import Entity


class Companion(Entity):
    def __init__(
        self,
        name,
        health=80,
        damage=15,
        species="Human",
        role="Companion",
        alignment="Neutral",
        background="A potential ally with their own history and motives.",
        motivation="Support, belonging, and shared purpose",
        traits=None,
        abilities=None,
        emotions=None,
        loyalty=25,
    ):
        default_traits = [
            "loyal",
            "observant",
            "supportive",
            "adaptable",
        ]

        default_abilities = {
            "strength": 45,
            "knowledge": 50,
            "comprehension": 60,
            "ingenuity": 55,
            "perception": 60,
            "wisdom": 55,
            "adaptability": 65,
            "willpower": 60,
            "dexterity": 55,
            "endurance": 55,
            "charisma": 55,
            "empathy": 70,
            "intuition": 60,
            "discipline": 60,
            "courage": 60,
            "resilience": 60,
        }

        default_emotions = {
            "joy": 55,
            "fear": 20,
            "anger": 10,
            "sadness": 10,
            "curiosity": 60,
            "hope": 65,
            "confidence": 55,
            "affection": 40,
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
            abilities=abilities if abilities is not None else default_abilities,
            emotions=emotions if emotions is not None else default_emotions,
        )

        self.loyalty = self._clamp(loyalty)
        self.is_following = False

    def follow(self):
        if not self.is_alive():
            print(
                f"{self.name} cannot follow because they have been defeated."
            )
            return

        if self.loyalty < 25:
            print(
                f"{self.name} does not trust the player enough to follow."
            )
            return

        self.is_following = True
        print(f"{self.name} is now following the player.")

    def stop_following(self):
        self.is_following = False
        print(f"{self.name} has stopped following the player.")

    def change_loyalty(self, amount):
        old_loyalty = self.loyalty
        self.loyalty = self._clamp(self.loyalty + amount)

        print(
            f"{self.name}'s loyalty changed: "
            f"{old_loyalty} -> {self.loyalty}"
        )

    def assist(self, target):
        if not self.is_following:
            print(
                f"{self.name} is not currently following the player."
            )
            return

        if not self.is_alive():
            print(
                f"{self.name} cannot assist because they have been defeated."
            )
            return

        self.attack(target)

    def show_status(self):
        dominant = self.dominant_emotion()

        print("===== COMPANION STATUS =====")
        print(f"Name: {self.name}")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"Loyalty: {self.loyalty}")
        print(f"Following: {self.is_following}")
        print(f"Traits: {', '.join(self.traits) or 'None assigned'}")

        if dominant:
            intensity = self.get_emotional_intensity(dominant)

            print(
                f"Dominant emotion: "
                f"{dominant.title()} "
                f"({self.emotions[dominant]}, {intensity})"
            )

        print("============================")
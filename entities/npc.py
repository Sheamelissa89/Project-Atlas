from .entity import Entity


class NPC(Entity):
    def __init__(
        self,
        name,
        role="Villager",
        dialogue=None,
        health=50,
        damage=5,
        species="Human",
        alignment="Neutral",
        background="A resident of the world with a story of their own.",
        motivation="Safety, belonging, and purpose",
        traits=None,
        abilities=None,
        emotions=None,
    ):
        default_traits = [
            "social",
            "observant",
            "cautious",
            "adaptable",
        ]

        default_abilities = {
            "strength": 35,
            "knowledge": 50,
            "comprehension": 55,
            "ingenuity": 50,
            "perception": 55,
            "wisdom": 50,
            "adaptability": 55,
            "willpower": 45,
            "dexterity": 40,
            "endurance": 40,
            "charisma": 55,
            "empathy": 60,
            "intuition": 50,
            "discipline": 50,
            "courage": 40,
            "resilience": 45,
        }

        default_emotions = {
            "joy": 50,
            "fear": 25,
            "anger": 10,
            "sadness": 10,
            "curiosity": 55,
            "hope": 50,
            "confidence": 45,
            "affection": 15,
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

        # Kept for compatibility with existing code.
        self.role = role

        self.dialogue = (
            list(dialogue)
            if dialogue
            else ["Greetings, traveler."]
        )

        self.current_dialogue_index = 0

    def talk(self):
        """Speak the current dialogue line and cycle to the next one."""
        if not self.dialogue:
            print(f"{self.name} has nothing to say.")
            return

        message = self.dialogue[self.current_dialogue_index]
        print(f"{self.name}: {message}")

        self.current_dialogue_index += 1

        if self.current_dialogue_index >= len(self.dialogue):
            self.current_dialogue_index = 0

    def add_dialogue(self, message):
        """Add a new dialogue line if the message is valid."""
        if isinstance(message, str) and message.strip():
            self.dialogue.append(message.strip())

    def respond_to_player(self):
        """
        Choose a simple response based on the NPC's current emotions.

        This is an early foundation for emotionally influenced dialogue.
        """
        fear = self.get_emotion("fear")
        anger = self.get_emotion("anger")
        curiosity = self.get_emotion("curiosity")
        affection = self.get_emotion("affection")

        if fear >= 80:
            print(
                f"{self.name}: Please, stay away from me!"
            )

        elif anger >= 80:
            print(
                f"{self.name}: I have nothing to say to you."
            )

        elif affection >= 70:
            print(
                f"{self.name}: It is truly good to see you again."
            )

        elif curiosity >= 70:
            print(
                f"{self.name}: You seem interesting. "
                "What brings you here?"
            )

        else:
            self.talk()

    def show_status(self):
        dominant = self.dominant_emotion()

        print("======= NPC STATUS =======")
        print(f"Name: {self.name}")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Alignment: {self.identity['alignment']}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"Dialogue lines: {len(self.dialogue)}")
        print(
            f"Traits: "
            f"{', '.join(self.traits) or 'None assigned'}"
        )

        if dominant:
            intensity = self.get_emotional_intensity(dominant)

            print(
                f"Dominant emotion: "
                f"{dominant.title()} "
                f"({self.emotions[dominant]}, {intensity})"
            )

        print("==========================")
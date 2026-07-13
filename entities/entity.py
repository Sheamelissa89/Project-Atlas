class Entity:
    """Base class for all living entities in Project Atlas."""

    DEFAULT_ABILITIES = {
        "strength": 50,
        "knowledge": 50,
        "comprehension": 50,
        "ingenuity": 50,
        "perception": 50,
        "wisdom": 50,
        "adaptability": 50,
        "willpower": 50,
        "dexterity": 50,
        "endurance": 50,
        "charisma": 50,
        "empathy": 50,
        "intuition": 50,
        "discipline": 50,
        "courage": 50,
        "resilience": 50,
    }

    DEFAULT_EMOTIONS = {
        "joy": 50,
        "fear": 20,
        "anger": 10,
        "sadness": 10,
        "curiosity": 50,
        "hope": 50,
        "confidence": 50,
        "affection": 0,
        "resentment": 0,
    }

    def __init__(
        self,
        name,
        health,
        damage,
        species="Unknown",
        role="Entity",
        alignment="Neutral",
        background="",
        motivation="Survival",
        traits=None,
        abilities=None,
        emotions=None,
    ):
        # Basic combat information
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage

        # Core identity
        self.identity = {
            "name": name,
            "species": species,
            "role": role,
            "alignment": alignment,
            "background": background,
            "motivation": motivation,
        }

        # Stable personality traits
        self.traits = list(traits) if traits else []

        # Mental, physical, and social abilities
        self.abilities = self.DEFAULT_ABILITIES.copy()

        if abilities:
            for ability, value in abilities.items():
                self.abilities[ability] = self._clamp(value)

        # Baseline emotions represent the entity's natural emotional state
        self.emotional_baselines = self.DEFAULT_EMOTIONS.copy()

        if emotions:
            for emotion, value in emotions.items():
                self.emotional_baselines[emotion] = self._clamp(value)

        # Current emotions can change through interactions
        self.emotions = self.emotional_baselines.copy()

        # Information that will grow as the entity experiences the world
        self.relationships = {}
        self.memories = []
        self.observations = []

    @staticmethod
    def _clamp(value, minimum=0, maximum=100):
        """Keep a numerical value inside an allowed range."""
        return max(minimum, min(maximum, value))

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        amount = max(0, amount)
        self.health = max(0, self.health - amount)

        print(f"{self.name} takes {amount} damage.")
        print(f"{self.name} health: {self.health}/{self.max_health}")

    def attack(self, target):
        if not self.is_alive():
            print(
                f"{self.name} cannot attack because they have been defeated."
            )
            return

        if not target.is_alive():
            print(
                f"{self.name} cannot attack {target.name} "
                "because the target has already been defeated."
            )
            return

        print(f"{self.name} attacks {target.name}!")
        target.take_damage(self.damage)

    def heal(self, amount):
        if not self.is_alive():
            print(
                f"{self.name} cannot heal because they have been defeated."
            )
            return

        amount = max(0, amount)

        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        healed_amount = self.health - old_health

        print(f"{self.name} heals for {healed_amount} health.")
        print(f"{self.name} health: {self.health}/{self.max_health}")

    def get_ability(self, ability):
        """Return the value of one ability."""
        return self.abilities.get(ability, 0)

    def set_ability(self, ability, value):
        """Create or update an ability using the 0-100 scale."""
        self.abilities[ability] = self._clamp(value)

    def change_ability(self, ability, amount):
        """Increase or decrease an ability."""
        current_value = self.abilities.get(ability, 50)
        self.abilities[ability] = self._clamp(current_value + amount)

        print(
            f"{self.name}'s {ability} is now "
            f"{self.abilities[ability]}."
        )

    def get_emotion(self, emotion):
        """Return the current value of one emotion."""
        return self.emotions.get(emotion, 0)

    def set_emotion(self, emotion, value):
        """Create or update an emotion using the 0-100 scale."""
        value = self._clamp(value)

        self.emotions[emotion] = value

        if emotion not in self.emotional_baselines:
            self.emotional_baselines[emotion] = value

    def change_emotion(self, emotion, amount, show_message=True):
        """Increase or decrease an emotional value."""
        current_value = self.emotions.get(emotion, 0)
        new_value = self._clamp(current_value + amount)

        self.emotions[emotion] = new_value

        if emotion not in self.emotional_baselines:
            self.emotional_baselines[emotion] = current_value

        if show_message:
            direction = "increases" if amount > 0 else "decreases"

            if amount == 0:
                direction = "remains unchanged"

            print(
                f"{self.name}'s {emotion} {direction}: "
                f"{current_value} -> {new_value}"
            )

        return new_value

    def return_emotions_toward_baseline(self, amount=1):
        """
        Move current emotions gradually toward their normal baselines.

        This can later be called after a turn, scene, rest period,
        or unit of game time.
        """
        amount = max(0, amount)

        for emotion, baseline in self.emotional_baselines.items():
            current_value = self.emotions.get(emotion, baseline)

            if current_value < baseline:
                self.emotions[emotion] = min(
                    baseline,
                    current_value + amount,
                )

            elif current_value > baseline:
                self.emotions[emotion] = max(
                    baseline,
                    current_value - amount,
                )

    def get_emotional_intensity(self, emotion):
        """Describe how strongly an emotion is affecting the entity."""
        value = self.get_emotion(emotion)

        if value <= 19:
            return "minimal"

        if value <= 39:
            return "present"

        if value <= 59:
            return "noticeable"

        if value <= 79:
            return "strong"

        return "dominant"

    def dominant_emotion(self):
        """Return the entity's strongest current emotion."""
        if not self.emotions:
            return None

        return max(self.emotions, key=self.emotions.get)

    def show_identity(self):
        """Display the entity's basic identity."""
        print(f"\n--- {self.name}: Identity ---")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Alignment: {self.identity['alignment']}")
        print(f"Motivation: {self.identity['motivation']}")
        print(f"Traits: {', '.join(self.traits) or 'None assigned'}")

        if self.identity["background"]:
            print(f"Background: {self.identity['background']}")

    def show_abilities(self):
        """Display all current ability values."""
        print(f"\n--- {self.name}: Abilities ---")

        for ability, value in self.abilities.items():
            print(f"{ability.title()}: {value}")

    def show_emotions(self):
        """Display current emotions and their intensity levels."""
        print(f"\n--- {self.name}: Emotional State ---")

        for emotion, value in self.emotions.items():
            intensity = self.get_emotional_intensity(emotion)

            print(
                f"{emotion.title()}: {value} "
                f"({intensity})"
            )

        dominant = self.dominant_emotion()

        if dominant:
            print(
                f"Dominant emotion: {dominant.title()} "
                f"({self.emotions[dominant]})"
            )

    def __str__(self):
        dominant = self.dominant_emotion()

        emotional_state = "Unknown"

        if dominant:
            emotional_state = (
                f"{dominant.title()} "
                f"({self.emotions[dominant]})"
            )

        return (
            f"{self.name} | "
            f"Species: {self.identity['species']} | "
            f"Role: {self.identity['role']} | "
            f"Health: {self.health}/{self.max_health} | "
            f"Damage: {self.damage} | "
            f"Dominant Emotion: {emotional_state}"
        )
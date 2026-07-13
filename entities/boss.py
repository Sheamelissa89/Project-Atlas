from .enemy import Enemy


class Boss(Enemy):
    def __init__(
        self,
        name,
        health=200,
        damage=40,
        exp_reward=250,
        gold_reward=100,
        potion_reward=2,
        species="Unknown",
        role="Boss",
        alignment="Hostile",
        background="A powerful entity with influence over the surrounding world.",
        motivation="Power, control, survival, or a personal objective",
        traits=None,
        abilities=None,
        emotions=None,
        phase=1,
    ):
        default_traits = [
            "powerful",
            "strategic",
            "dominant",
            "resilient",
        ]

        default_abilities = {
            "strength": 85,
            "knowledge": 65,
            "comprehension": 70,
            "ingenuity": 65,
            "perception": 70,
            "wisdom": 60,
            "adaptability": 75,
            "willpower": 85,
            "dexterity": 60,
            "endurance": 90,
            "charisma": 60,
            "empathy": 25,
            "intuition": 70,
            "discipline": 75,
            "courage": 90,
            "resilience": 90,
        }

        default_emotions = {
            "joy": 20,
            "fear": 10,
            "anger": 50,
            "sadness": 10,
            "curiosity": 35,
            "hope": 45,
            "confidence": 85,
            "affection": 0,
            "resentment": 25,
        }

        super().__init__(
            name=name,
            health=health,
            damage=damage,
            exp_reward=exp_reward,
            gold_reward=gold_reward,
            potion_reward=potion_reward,
            species=species,
            role=role,
            alignment=alignment,
            background=background,
            motivation=motivation,
            traits=traits if traits is not None else default_traits,
            abilities=abilities if abilities is not None else default_abilities,
            emotions=emotions if emotions is not None else default_emotions,
        )

        self.phase = max(1, phase)
        self.enraged = False

    def check_phase(self):
        health_percent = (
            self.health / self.max_health
            if self.max_health > 0
            else 0
        )

        if health_percent <= 0.25:
            new_phase = 3
        elif health_percent <= 0.50:
            new_phase = 2
        else:
            new_phase = 1

        if new_phase != self.phase:
            self.phase = new_phase
            print(f"{self.name} entered phase {self.phase}!")

        if self.phase == 3 and not self.enraged:
            self.enrage()

        return self.phase

    def enrage(self):
        if self.enraged:
            return

        self.enraged = True
        self.damage += 10
        self.change_emotion("anger", 30)
        self.change_emotion("confidence", 10)

        print(f"{self.name} has become enraged!")
        print(f"{self.name}'s damage increased to {self.damage}.")

    def take_damage(self, amount):
        super().take_damage(amount)
        self.check_phase()

    def evaluate_behavior(self):
        self.check_phase()

        fear = self.get_emotion("fear")
        anger = self.get_emotion("anger")
        confidence = self.get_emotion("confidence")

        if self.phase == 3 and self.enraged:
            return "attack"

        if fear >= 90 and confidence < 40:
            return "retreat"

        if anger >= 60 or confidence >= 70:
            return "attack"

        return "observe"

    def show_status(self):
        dominant = self.dominant_emotion()

        print("======= BOSS STATUS =======")
        print(f"Name: {self.name}")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"Phase: {self.phase}")
        print(f"Enraged: {self.enraged}")
        print(f"Behavior: {self.evaluate_behavior().title()}")
        print(f"EXP Reward: {self.exp_reward}")
        print(f"Gold Reward: {self.gold_reward}")
        print(f"Potion Reward: {self.potion_reward}")
        print(f"Traits: {', '.join(self.traits) or 'None assigned'}")

        if dominant:
            intensity = self.get_emotional_intensity(dominant)

            print(
                f"Dominant emotion: "
                f"{dominant.title()} "
                f"({self.emotions[dominant]}, {intensity})"
            )

        print("===========================")
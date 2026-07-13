from .entity import Entity


class Enemy(Entity):
    def __init__(
        self,
        name,
        health=60,
        damage=15,
        exp_reward=50,
        gold_reward=10,
        potion_reward=0,
        species="Unknown",
        role="Enemy",
        alignment="Neutral",
        background="",
        motivation="Survival",
        traits=None,
        abilities=None,
        emotions=None,
    ):
        default_traits = [
            "cautious",
            "territorial",
            "survival-driven",
        ]

        default_abilities = {
            "strength": 55,
            "knowledge": 30,
            "comprehension": 40,
            "ingenuity": 35,
            "perception": 55,
            "wisdom": 35,
            "adaptability": 50,
            "willpower": 50,
            "dexterity": 50,
            "endurance": 55,
            "charisma": 20,
            "empathy": 20,
            "intuition": 50,
            "discipline": 40,
            "courage": 55,
            "resilience": 55,
        }

        default_emotions = {
            "joy": 25,
            "fear": 30,
            "anger": 35,
            "sadness": 10,
            "curiosity": 40,
            "hope": 25,
            "confidence": 50,
            "affection": 0,
            "resentment": 10,
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
            traits=(
                traits
                if traits is not None
                else default_traits
            ),
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

        self.exp_reward = max(0, exp_reward)
        self.gold_reward = max(0, gold_reward)
        self.potion_reward = max(0, potion_reward)

        self.rewards_given = False

    def give_rewards(self, player):
        """Give rewards once after the enemy has been defeated."""
        if self.is_alive():
            print(
                f"{self.name} must be defeated before "
                "rewards can be collected."
            )
            return

        if self.rewards_given:
            print(
                f"The rewards from {self.name} "
                "have already been collected."
            )
            return

        print(f"{self.name} dropped rewards!")

        player.gain_exp(self.exp_reward)
        player.receive_gold(self.gold_reward)
        player.receive_potions(self.potion_reward)

        self.rewards_given = True

    def evaluate_behavior(self):
        """
        Return a basic behavior based on the enemy's emotions.

        This is the first foundation for enemies that do not
        automatically attack during every encounter.
        """
        fear = self.get_emotion("fear")
        anger = self.get_emotion("anger")
        curiosity = self.get_emotion("curiosity")
        confidence = self.get_emotion("confidence")

        courage = self.get_ability("courage")
        perception = self.get_ability("perception")

        if fear >= 80 and courage < 60:
            return "flee"

        if anger >= 75 and confidence >= 50:
            return "attack"

        if curiosity >= 70 and perception >= 50:
            return "observe"

        if fear >= 55:
            return "defend"

        return "wait"

    def choose_action(self, target=None):
        """
        Perform or announce an action selected from the enemy's
        current emotional state.
        """
        behavior = self.evaluate_behavior()

        if behavior == "attack":
            if target is None:
                print(
                    f"{self.name} is prepared to attack, "
                    "but no target is available."
                )
                return behavior

            self.attack(target)

        elif behavior == "flee":
            print(
                f"{self.name} is overwhelmed by fear "
                "and attempts to flee."
            )

        elif behavior == "observe":
            print(
                f"{self.name} watches carefully before deciding "
                "what to do."
            )

        elif behavior == "defend":
            print(
                f"{self.name} becomes defensive and prepares "
                "for danger."
            )

        else:
            print(
                f"{self.name} waits and evaluates the situation."
            )

        return behavior

    def show_status(self):
        dominant = self.dominant_emotion()
        behavior = self.evaluate_behavior()

        print("===== ENEMY STATUS =====")
        print(f"Name: {self.name}")
        print(f"Species: {self.identity['species']}")
        print(f"Role: {self.identity['role']}")
        print(f"Alignment: {self.identity['alignment']}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Damage: {self.damage}")
        print(f"Traits: {', '.join(self.traits) or 'None assigned'}")
        print(f"Current behavior: {behavior.title()}")
        print(f"EXP Reward: {self.exp_reward}")
        print(f"Gold Reward: {self.gold_reward}")
        print(f"Potion Reward: {self.potion_reward}")

        if dominant:
            intensity = self.get_emotional_intensity(dominant)

            print(
                f"Dominant emotion: "
                f"{dominant.title()} "
                f"({self.emotions[dominant]}, {intensity})"
            )

        print("========================")

   

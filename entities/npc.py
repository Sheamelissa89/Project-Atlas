from .entity import Entity


class NPC(Entity):
    def __init__(
        self,
        name,
        role="Villager",
        dialogue=None,
        health=50,
        damage=5
    ):
        super().__init__(name, health, damage)

        self.role = role
        self.dialogue = dialogue or ["Greetings, traveler."]
        self.current_dialogue_index = 0

    def talk(self):
        message = self.dialogue[self.current_dialogue_index]
        print(f"{self.name}: {message}")

        self.current_dialogue_index += 1

        if self.current_dialogue_index >= len(self.dialogue):
            self.current_dialogue_index = 0

    def add_dialogue(self, message):
        if message:
            self.dialogue.append(message)

    def show_status(self):
        print("======= NPC STATUS =======")
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Dialogue lines: {len(self.dialogue)}")
        print("==========================")
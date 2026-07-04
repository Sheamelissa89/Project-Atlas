class Player:
    def __init__(self):
        self.name = "Shea"
        self.health = 100
        self.level = 1
        self.gold = 50
        self.experience = 0

    def take_damage(self, amount):
        self.health = self.health - amount
        print(f"{self.name} takes {amount} damage!")

    def show_status(self):
        print("----- PLAYER STATUS -----")
        print("Name:", self.name)
        print("Health:", self.health)
        print("Level:", self.level)
        print("Gold:", self.gold)
        print("Experience:", self.experience)
        print("-------------------------")
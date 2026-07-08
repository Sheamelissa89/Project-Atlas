class GameMap:
    def __init__(self):
        self.current_location = "Forest Entrance"

    def show_location(self):
        print(f"You are currently at: {self.current_location}")

    def move_to(self, new_location):
        self.current_location = new_location
        print(f"You travel to: {self.current_location}")
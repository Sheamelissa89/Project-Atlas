class GameMap:
    """
    Controls navigation through the Project Atlas world.

    GameMap tracks the player's current location and can optionally
    connect to a World object for location validation and history.
    """

    def __init__(
        self,
        starting_location="Forest Entrance",
        world=None,
    ):
        self.current_location = starting_location
        self.previous_location = None
        self.world = world
        self.travel_history = [starting_location]

    def connect_world(self, world):
        """Connect the map to an existing World object."""
        self.world = world

        if self.current_location not in self.world.locations:
            self.world.add_location(
                name=self.current_location,
                description="The starting point of the player's journey.",
                danger_level=10,
                traits=["starting-area"],
            )

    def location_exists(self, location_name):
        """
        Check whether a location exists.

        If no World object is connected, movement remains unrestricted
        so older game code continues working.
        """
        if self.world is None:
            return True

        return location_name in self.world.locations

    def show_location(self):
        """Display the player's current location."""
        print(f"You are currently at: {self.current_location}")

        if self.world is not None:
            location = self.world.get_location(self.current_location)

            if location:
                description = location.get("description", "")

                if description:
                    print(description)

                danger_level = location.get("danger_level", 0)
                print(f"Danger level: {danger_level}")

                entities = self.world.get_entities_in_location(
                    self.current_location
                )

                if entities:
                    print("Nearby entities:")

                    for entity in entities:
                        print(f"- {entity.name}")

                else:
                    print("Nearby entities: None")

    def move_to(self, new_location):
        """Move the player to another location."""
        if not new_location:
            print("You must choose a valid location.")
            return False

        if new_location == self.current_location:
            print(f"You are already at: {self.current_location}")
            return False

        if not self.location_exists(new_location):
            print(
                f"You cannot travel to {new_location} "
                "because it does not exist."
            )
            return False

        self.previous_location = self.current_location
        self.current_location = new_location
        self.travel_history.append(new_location)

        print(f"You travel to: {self.current_location}")

        if self.world is not None:
            self.world.mark_location_visited(new_location)

            self.world.record_event(
                event_type="player_traveled",
                description=(
                    f"The player traveled from "
                    f"{self.previous_location} to "
                    f"{self.current_location}."
                ),
                location=self.current_location,
                importance=20,
            )

        return True

    def return_to_previous_location(self):
        """Return to the location visited immediately before this one."""
        if self.previous_location is None:
            print("There is no previous location to return to.")
            return False

        destination = self.previous_location

        return self.move_to(destination)

    def get_available_locations(self):
        """Return all locations currently available for travel."""
        if self.world is None:
            return []

        return list(self.world.locations.keys())

    def show_available_locations(self):
        """Display all known travel destinations."""
        locations = self.get_available_locations()

        if not locations:
            print("No connected world locations are available.")
            return

        print("\n===== AVAILABLE LOCATIONS =====")

        for location_name in locations:
            marker = ""

            if location_name == self.current_location:
                marker = " (current location)"

            print(f"- {location_name}{marker}")

        print("===============================")

    def show_travel_history(self):
        """Display every location visited in order."""
        print("\n===== TRAVEL HISTORY =====")

        for number, location_name in enumerate(
            self.travel_history,
            start=1,
        ):
            print(f"{number}. {location_name}")

        print("==========================")
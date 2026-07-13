class World:
    """
    Represents the living world of Project Atlas.

    The World stores locations, tracks entities, and remembers
    where each entity currently exists.
    """

    def __init__(self, name="Atlas"):
        self.name = name

        # Stores location information by location name.
        self.locations = {}

        # Stores every registered entity by entity name.
        self.entities = {}

        # Stores the current location of each entity.
        self.entity_locations = {}

        # Records important world events.
        self.world_history = []

    def add_location(
        self,
        name,
        description="",
        danger_level=0,
        traits=None,
    ):
        """Add a location to the world."""
        if not name:
            print("A location must have a name.")
            return

        if name in self.locations:
            print(f"{name} already exists in the world.")
            return

        self.locations[name] = {
            "name": name,
            "description": description,
            "danger_level": self._clamp(danger_level),
            "traits": list(traits) if traits else [],
            "entities": [],
            "visited": False,
        }

        print(f"Location added: {name}")

    def register_entity(self, entity, location_name=None):
        """Register an entity as part of the world."""
        if entity.name in self.entities:
            print(f"{entity.name} is already registered.")
            return

        self.entities[entity.name] = entity
        self.entity_locations[entity.name] = None

        print(f"Entity registered: {entity.name}")

        if location_name:
            self.place_entity(entity.name, location_name)

    def place_entity(self, entity_name, location_name):
        """Place or move an entity into a location."""
        if entity_name not in self.entities:
            print(f"{entity_name} is not registered in the world.")
            return

        if location_name not in self.locations:
            print(f"{location_name} does not exist in the world.")
            return

        old_location = self.entity_locations.get(entity_name)

        if old_location == location_name:
            print(f"{entity_name} is already in {location_name}.")
            return

        if old_location:
            old_entities = self.locations[old_location]["entities"]

            if entity_name in old_entities:
                old_entities.remove(entity_name)

        self.locations[location_name]["entities"].append(entity_name)
        self.entity_locations[entity_name] = location_name

        self.record_event(
            event_type="entity_moved",
            description=(
                f"{entity_name} moved to {location_name}."
            ),
            entities=[entity_name],
            location=location_name,
        )

        print(f"{entity_name} is now in {location_name}.")

    def remove_entity(self, entity_name):
        """Remove an entity from the active world."""
        if entity_name not in self.entities:
            print(f"{entity_name} is not registered.")
            return

        location_name = self.entity_locations.get(entity_name)

        if location_name:
            location_entities = self.locations[location_name]["entities"]

            if entity_name in location_entities:
                location_entities.remove(entity_name)

        del self.entities[entity_name]
        del self.entity_locations[entity_name]

        print(f"{entity_name} was removed from the world.")

    def get_entity(self, entity_name):
        """Return a registered entity by name."""
        return self.entities.get(entity_name)

    def get_location(self, location_name):
        """Return location information by name."""
        return self.locations.get(location_name)

    def get_entity_location(self, entity_name):
        """Return the name of an entity's current location."""
        return self.entity_locations.get(entity_name)

    def get_entities_in_location(self, location_name):
        """Return all entity objects currently in a location."""
        location = self.locations.get(location_name)

        if not location:
            return []

        return [
            self.entities[entity_name]
            for entity_name in location["entities"]
            if entity_name in self.entities
        ]

    def mark_location_visited(self, location_name):
        """Mark a location as visited by the player."""
        if location_name not in self.locations:
            print(f"{location_name} does not exist.")
            return

        self.locations[location_name]["visited"] = True

        self.record_event(
            event_type="location_visited",
            description=f"{location_name} was visited.",
            location=location_name,
        )

    def record_event(
        self,
        event_type,
        description,
        entities=None,
        location=None,
        importance=50,
    ):
        """Store an important event in the world's history."""
        event = {
            "event_type": event_type,
            "description": description,
            "entities": list(entities) if entities else [],
            "location": location,
            "importance": self._clamp(importance),
        }

        self.world_history.append(event)

        return event

    def show_location(self, location_name):
        """Display information about one location."""
        location = self.locations.get(location_name)

        if not location:
            print(f"{location_name} does not exist.")
            return

        print(f"\n===== {location_name.upper()} =====")
        print(f"Description: {location['description']}")
        print(f"Danger level: {location['danger_level']}")
        print(f"Visited: {location['visited']}")

        traits = ", ".join(location["traits"]) or "None"
        print(f"Traits: {traits}")

        if location["entities"]:
            print("Entities:")

            for entity_name in location["entities"]:
                print(f"- {entity_name}")
        else:
            print("Entities: None")

        print("=" * (12 + len(location_name)))

    def show_world_status(self):
        """Display a summary of the current world."""
        print(f"\n======= WORLD: {self.name.upper()} =======")
        print(f"Locations: {len(self.locations)}")
        print(f"Registered entities: {len(self.entities)}")
        print(f"Recorded events: {len(self.world_history)}")

        if self.locations:
            print("\nKnown locations:")

            for location_name, location in self.locations.items():
                entity_count = len(location["entities"])

                print(
                    f"- {location_name}: "
                    f"{entity_count} entities, "
                    f"danger {location['danger_level']}"
                )

        print("==============================")

    @staticmethod
    def _clamp(value, minimum=0, maximum=100):
        """Keep a numerical value inside an allowed range."""
        return max(minimum, min(maximum, value))
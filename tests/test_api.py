import importlib
import tempfile
import unittest
from pathlib import Path

import backend.database as database


app_module = importlib.import_module("backend.app")


class AtlasApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.original_database_path = database.DATABASE_PATH
        cls.original_get_connection = app_module.get_connection

        database.DATABASE_PATH = (
            Path(cls.temporary_directory.name)
            / "atlas_test.db"
        )

        database.init_database()

        app_module.get_connection = database.get_connection
        app_module.app.config.update(TESTING=True)

        cls.client = app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        app_module.get_connection = cls.original_get_connection
        database.DATABASE_PATH = cls.original_database_path
        cls.temporary_directory.cleanup()

    def setUp(self):
        connection = database.get_connection()

        try:
            connection.execute("DELETE FROM battle_sessions")
            connection.execute("DELETE FROM world_locations")
            connection.execute("DELETE FROM journal_entries")
            connection.execute("DELETE FROM companions")
            connection.execute("DELETE FROM quests")
            connection.execute("DELETE FROM inventory_items")
            connection.execute("DELETE FROM characters")
            connection.commit()
        finally:
            connection.close()

    def create_character(self):
        response = self.client.post(
            "/api/characters",
            json={
                "name": "Shea",
                "character_class": "Explorer",
            },
        )

        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def assert_resource_crud(
        self,
        resource_name,
        list_name,
        create_data,
        created_field,
        created_value,
        update_data,
        updated_field,
        updated_value,
    ):
        character = self.create_character()
        create_data["character_id"] = character["id"]

        create_response = self.client.post(
            f"/api/{resource_name}",
            json=create_data,
        )
        created_resource = create_response.get_json()

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(
            created_resource[created_field],
            created_value,
        )

        list_response = self.client.get(
            f"/api/characters/{character['id']}/{list_name}"
        )
        listed_resources = list_response.get_json()

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(listed_resources), 1)

        resource_id = created_resource["id"]

        update_response = self.client.patch(
            f"/api/{resource_name}/{resource_id}",
            json=update_data,
        )
        updated_resource = update_response.get_json()

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(
            updated_resource[updated_field],
            updated_value,
        )

        delete_response = self.client.delete(
            f"/api/{resource_name}/{resource_id}"
        )

        self.assertEqual(delete_response.status_code, 204)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["status"], "ok")

    def test_create_character(self):
        character = self.create_character()

        self.assertEqual(character["name"], "Shea")
        self.assertEqual(
            character["character_class"],
            "Explorer",
        )
        self.assertEqual(character["level"], 1)
        self.assertEqual(character["health"], 100)
        self.assertEqual(character["gold"], 0)

    def test_list_characters(self):
        created_character = self.create_character()

        response = self.client.get("/api/characters")
        characters = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(characters), 1)
        self.assertEqual(
            characters[0]["id"],
            created_character["id"],
        )

    def test_get_one_character(self):
        created_character = self.create_character()

        response = self.client.get(
            f"/api/characters/{created_character['id']}"
        )
        character = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(character["name"], "Shea")

    def test_update_character(self):
        created_character = self.create_character()

        response = self.client.patch(
            f"/api/characters/{created_character['id']}",
            json={
                "health": 75,
                "gold": 25,
                "experience": 40,
            },
        )
        character = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(character["health"], 75)
        self.assertEqual(character["gold"], 25)
        self.assertEqual(character["experience"], 40)

    def test_reject_invalid_character(self):
        response = self.client.post(
            "/api/characters",
            json={
                "name": "",
                "character_class": "",
            },
        )
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_data)

    def test_character_not_found(self):
        response = self.client.get("/api/characters/9999")
        response_data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_data)

    def test_delete_character(self):
        created_character = self.create_character()
        character_id = created_character["id"]

        delete_response = self.client.delete(
            f"/api/characters/{character_id}"
        )

        self.assertEqual(delete_response.status_code, 204)

        get_response = self.client.get(
            f"/api/characters/{character_id}"
        )

        self.assertEqual(get_response.status_code, 404)

    def test_inventory_crud(self):
        self.assert_resource_crud(
            resource_name="inventory",
            list_name="inventory",
            create_data={
                "name": "Healing Potion",
                "item_type": "Potion",
                "description": "Restores health.",
                "quantity": 3,
                "value": 10,
                "equipped": False,
            },
            created_field="name",
            created_value="Healing Potion",
            update_data={"quantity": 5},
            updated_field="quantity",
            updated_value=5,
        )

    def test_quest_crud(self):
        self.assert_resource_crud(
            resource_name="quests",
            list_name="quests",
            create_data={
                "title": "Into the Forest",
                "description": "Travel beyond the Forest Entrance.",
                "status": "active",
                "reward_gold": 30,
                "reward_experience": 50,
            },
            created_field="title",
            created_value="Into the Forest",
            update_data={"status": "completed"},
            updated_field="status",
            updated_value="completed",
        )

    def test_companion_crud(self):
        self.assert_resource_crud(
            resource_name="companions",
            list_name="companions",
            create_data={
                "name": "Elara",
                "species": "Human",
                "role": "Village Scout",
                "relationship": "Acquaintance",
                "level": 1,
                "health": 100,
                "ability": "Pathfinder",
            },
            created_field="name",
            created_value="Elara",
            update_data={"relationship": "Trusted"},
            updated_field="relationship",
            updated_value="Trusted",
        )

    def test_journal_crud(self):
        self.assert_resource_crud(
            resource_name="journal",
            list_name="journal",
            create_data={
                "title": "The Journey Begins",
                "content": "I arrived at the Forest Entrance.",
                "category": "Story",
            },
            created_field="title",
            created_value="The Journey Begins",
            update_data={"category": "Discovery"},
            updated_field="category",
            updated_value="Discovery",
        )

    def test_world_location_crud(self):
        self.assert_resource_crud(
            resource_name="locations",
            list_name="locations",
            create_data={
                "name": "Forest Entrance",
                "description": "A quiet path into the ancient woods.",
                "status": "current",
            },
            created_field="name",
            created_value="Forest Entrance",
            update_data={"status": "discovered"},
            updated_field="status",
            updated_value="discovered",
        )

    def test_battle_crud(self):
        self.assert_resource_crud(
            resource_name="battles",
            list_name="battles",
            create_data={
                "enemy_name": "Forest Wolf",
                "player_health": 100,
                "player_max_health": 100,
                "enemy_health": 100,
                "enemy_max_health": 100,
                "status": "active",
                "turn_count": 0,
                "battle_log": [
                    "The Forest Wolf watches carefully."
                ],
            },
            created_field="enemy_name",
            created_value="Forest Wolf",
            update_data={
                "enemy_health": 82,
                "turn_count": 1,
                "battle_log": [
                    "The Forest Wolf watches carefully.",
                    "Shea attacks for 18 damage.",
                ],
            },
            updated_field="enemy_health",
            updated_value=82,
        )


if __name__ == "__main__":
    unittest.main()
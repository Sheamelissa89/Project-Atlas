import json
from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.database import get_connection, init_database
from backend.validators import (
    validate_battle_session,
    validate_character,
    validate_companion,
    validate_inventory_item,
    validate_journal_entry,
    validate_quest,
    validate_world_location,
)


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "http://localhost:5173",
        }
    },
)

init_database()


def fetch_character(character_id):
    """Return one character or None."""
    connection = get_connection()

    try:
        character = connection.execute(
            """
            SELECT *
            FROM characters
            WHERE id = ?
            """,
            (character_id,),
        ).fetchone()

        return dict(character) if character else None
    finally:
        connection.close()


@app.get("/api/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "message": "Project Atlas API is running.",
        }
    ), 200


@app.get("/api/characters")
def get_characters():
    connection = get_connection()

    try:
        characters = connection.execute(
            """
            SELECT *
            FROM characters
            ORDER BY id
            """
        ).fetchall()

        return jsonify(
            [dict(character) for character in characters]
        ), 200
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>")
def get_character(character_id):
    character = fetch_character(character_id)

    if character is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    return jsonify(character), 200


@app.post("/api/characters")
def create_character():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_character(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character = {
        "name": data["name"].strip(),
        "character_class": data["character_class"].strip(),
        "level": data.get("level", 1),
        "experience": data.get("experience", 0),
        "health": data.get("health", 100),
        "max_health": data.get("max_health", 100),
        "gold": data.get("gold", 0),
    }

    if character["health"] > character["max_health"]:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    "health cannot exceed max_health."
                ],
            }
        ), 400

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO characters (
                name,
                character_class,
                level,
                experience,
                health,
                max_health,
                gold
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                character["name"],
                character["character_class"],
                character["level"],
                character["experience"],
                character["health"],
                character["max_health"],
                character["gold"],
            ),
        )

        connection.commit()
        character_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(fetch_character(character_id)), 201


@app.patch("/api/characters/<int:character_id>")
def update_character(character_id):
    existing_character = fetch_character(character_id)

    if existing_character is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_character(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    updated_character = {
        "name": data.get(
            "name",
            existing_character["name"],
        ),
        "character_class": data.get(
            "character_class",
            existing_character["character_class"],
        ),
        "level": data.get(
            "level",
            existing_character["level"],
        ),
        "experience": data.get(
            "experience",
            existing_character["experience"],
        ),
        "health": data.get(
            "health",
            existing_character["health"],
        ),
        "max_health": data.get(
            "max_health",
            existing_character["max_health"],
        ),
        "gold": data.get(
            "gold",
            existing_character["gold"],
        ),
    }

    if updated_character["health"] > updated_character["max_health"]:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    "health cannot exceed max_health."
                ],
            }
        ), 400

    updated_character["name"] = updated_character["name"].strip()
    updated_character["character_class"] = (
        updated_character["character_class"].strip()
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE characters
            SET
                name = ?,
                character_class = ?,
                level = ?,
                experience = ?,
                health = ?,
                max_health = ?,
                gold = ?
            WHERE id = ?
            """,
            (
                updated_character["name"],
                updated_character["character_class"],
                updated_character["level"],
                updated_character["experience"],
                updated_character["health"],
                updated_character["max_health"],
                updated_character["gold"],
                character_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(fetch_character(character_id)), 200


@app.delete("/api/characters/<int:character_id>")
def delete_character(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM characters
            WHERE id = ?
            """,
            (character_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def fetch_inventory_item(item_id):
    """Return one inventory item or None."""
    connection = get_connection()

    try:
        item = connection.execute(
            """
            SELECT *
            FROM inventory_items
            WHERE id = ?
            """,
            (item_id,),
        ).fetchone()

        return dict(item) if item else None
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/inventory")
def get_inventory(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        items = connection.execute(
            """
            SELECT *
            FROM inventory_items
            WHERE character_id = ?
            ORDER BY id
            """,
            (character_id,),
        ).fetchall()

        inventory = []

        for item in items:
            item_data = dict(item)
            item_data["equipped"] = bool(item_data["equipped"])
            inventory.append(item_data)

        return jsonify(inventory), 200
    finally:
        connection.close()


@app.get("/api/inventory/<int:item_id>")
def get_inventory_item(item_id):
    item = fetch_inventory_item(item_id)

    if item is None:
        return jsonify(
            {"error": "Inventory item not found."}
        ), 404

    item["equipped"] = bool(item["equipped"])

    return jsonify(item), 200


@app.post("/api/inventory")
def create_inventory_item():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_inventory_item(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    if fetch_character(data["character_id"]) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    item = {
        "character_id": data["character_id"],
        "name": data["name"].strip(),
        "item_type": data["item_type"].strip(),
        "description": data.get("description", "").strip(),
        "quantity": data.get("quantity", 1),
        "value": data.get("value", 0),
        "equipped": data.get("equipped", False),
    }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO inventory_items (
                character_id,
                name,
                item_type,
                description,
                quantity,
                value,
                equipped
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["character_id"],
                item["name"],
                item["item_type"],
                item["description"],
                item["quantity"],
                item["value"],
                int(item["equipped"]),
            ),
        )

        connection.commit()
        item_id = cursor.lastrowid
    finally:
        connection.close()

    created_item = fetch_inventory_item(item_id)
    created_item["equipped"] = bool(created_item["equipped"])

    return jsonify(created_item), 201


@app.patch("/api/inventory/<int:item_id>")
def update_inventory_item(item_id):
    existing_item = fetch_inventory_item(item_id)

    if existing_item is None:
        return jsonify(
            {"error": "Inventory item not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_inventory_item(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_item["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_item = {
        "character_id": character_id,
        "name": data.get(
            "name",
            existing_item["name"],
        ),
        "item_type": data.get(
            "item_type",
            existing_item["item_type"],
        ),
        "description": data.get(
            "description",
            existing_item["description"],
        ),
        "quantity": data.get(
            "quantity",
            existing_item["quantity"],
        ),
        "value": data.get(
            "value",
            existing_item["value"],
        ),
        "equipped": data.get(
            "equipped",
            bool(existing_item["equipped"]),
        ),
    }

    updated_item["name"] = updated_item["name"].strip()
    updated_item["item_type"] = (
        updated_item["item_type"].strip()
    )
    updated_item["description"] = (
        updated_item["description"].strip()
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE inventory_items
            SET
                character_id = ?,
                name = ?,
                item_type = ?,
                description = ?,
                quantity = ?,
                value = ?,
                equipped = ?
            WHERE id = ?
            """,
            (
                updated_item["character_id"],
                updated_item["name"],
                updated_item["item_type"],
                updated_item["description"],
                updated_item["quantity"],
                updated_item["value"],
                int(updated_item["equipped"]),
                item_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    saved_item = fetch_inventory_item(item_id)
    saved_item["equipped"] = bool(saved_item["equipped"])

    return jsonify(saved_item), 200


@app.delete("/api/inventory/<int:item_id>")
def delete_inventory_item(item_id):
    if fetch_inventory_item(item_id) is None:
        return jsonify(
            {"error": "Inventory item not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM inventory_items
            WHERE id = ?
            """,
            (item_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def fetch_quest(quest_id):
    """Return one quest or None."""
    connection = get_connection()

    try:
        quest = connection.execute(
            """
            SELECT *
            FROM quests
            WHERE id = ?
            """,
            (quest_id,),
        ).fetchone()

        return dict(quest) if quest else None
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/quests")
def get_quests(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        quests = connection.execute(
            """
            SELECT *
            FROM quests
            WHERE character_id = ?
            ORDER BY id
            """,
            (character_id,),
        ).fetchall()

        return jsonify(
            [dict(quest) for quest in quests]
        ), 200
    finally:
        connection.close()


@app.get("/api/quests/<int:quest_id>")
def get_quest(quest_id):
    quest = fetch_quest(quest_id)

    if quest is None:
        return jsonify(
            {"error": "Quest not found."}
        ), 404

    return jsonify(quest), 200


@app.post("/api/quests")
def create_quest():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_quest(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    if fetch_character(data["character_id"]) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    quest = {
        "character_id": data["character_id"],
        "title": data["title"].strip(),
        "description": data.get(
            "description",
            "",
        ).strip(),
        "status": data.get(
            "status",
            "available",
        ).strip().lower(),
        "reward_gold": data.get(
            "reward_gold",
            0,
        ),
        "reward_experience": data.get(
            "reward_experience",
            0,
        ),
    }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO quests (
                character_id,
                title,
                description,
                status,
                reward_gold,
                reward_experience
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                quest["character_id"],
                quest["title"],
                quest["description"],
                quest["status"],
                quest["reward_gold"],
                quest["reward_experience"],
            ),
        )

        connection.commit()
        quest_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(fetch_quest(quest_id)), 201


@app.patch("/api/quests/<int:quest_id>")
def update_quest(quest_id):
    existing_quest = fetch_quest(quest_id)

    if existing_quest is None:
        return jsonify(
            {"error": "Quest not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_quest(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_quest["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_quest = {
        "character_id": character_id,
        "title": data.get(
            "title",
            existing_quest["title"],
        ),
        "description": data.get(
            "description",
            existing_quest["description"],
        ),
        "status": data.get(
            "status",
            existing_quest["status"],
        ),
        "reward_gold": data.get(
            "reward_gold",
            existing_quest["reward_gold"],
        ),
        "reward_experience": data.get(
            "reward_experience",
            existing_quest["reward_experience"],
        ),
    }

    updated_quest["title"] = (
        updated_quest["title"].strip()
    )
    updated_quest["description"] = (
        updated_quest["description"].strip()
    )
    updated_quest["status"] = (
        updated_quest["status"].strip().lower()
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE quests
            SET
                character_id = ?,
                title = ?,
                description = ?,
                status = ?,
                reward_gold = ?,
                reward_experience = ?
            WHERE id = ?
            """,
            (
                updated_quest["character_id"],
                updated_quest["title"],
                updated_quest["description"],
                updated_quest["status"],
                updated_quest["reward_gold"],
                updated_quest["reward_experience"],
                quest_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(fetch_quest(quest_id)), 200


@app.delete("/api/quests/<int:quest_id>")
def delete_quest(quest_id):
    if fetch_quest(quest_id) is None:
        return jsonify(
            {"error": "Quest not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM quests
            WHERE id = ?
            """,
            (quest_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def fetch_companion(companion_id):
    """Return one companion or None."""
    connection = get_connection()

    try:
        companion = connection.execute(
            """
            SELECT *
            FROM companions
            WHERE id = ?
            """,
            (companion_id,),
        ).fetchone()

        return dict(companion) if companion else None
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/companions")
def get_companions(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        companions = connection.execute(
            """
            SELECT *
            FROM companions
            WHERE character_id = ?
            ORDER BY id
            """,
            (character_id,),
        ).fetchall()

        return jsonify(
            [dict(companion) for companion in companions]
        ), 200
    finally:
        connection.close()


@app.get("/api/companions/<int:companion_id>")
def get_companion(companion_id):
    companion = fetch_companion(companion_id)

    if companion is None:
        return jsonify(
            {"error": "Companion not found."}
        ), 404

    return jsonify(companion), 200


@app.post("/api/companions")
def create_companion():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_companion(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    if fetch_character(data["character_id"]) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    companion = {
        "character_id": data["character_id"],
        "name": data["name"].strip(),
        "species": data.get(
            "species",
            "Human",
        ).strip(),
        "role": data.get(
            "role",
            "",
        ).strip(),
        "relationship": data.get(
            "relationship",
            "Unknown",
        ).strip(),
        "level": data.get("level", 1),
        "health": data.get("health", 100),
        "ability": data.get(
            "ability",
            "",
        ).strip(),
    }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO companions (
                character_id,
                name,
                species,
                role,
                relationship,
                level,
                health,
                ability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                companion["character_id"],
                companion["name"],
                companion["species"],
                companion["role"],
                companion["relationship"],
                companion["level"],
                companion["health"],
                companion["ability"],
            ),
        )

        connection.commit()
        companion_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(
        fetch_companion(companion_id)
    ), 201


@app.patch("/api/companions/<int:companion_id>")
def update_companion(companion_id):
    existing_companion = fetch_companion(companion_id)

    if existing_companion is None:
        return jsonify(
            {"error": "Companion not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_companion(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_companion["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_companion = {
        "character_id": character_id,
        "name": data.get(
            "name",
            existing_companion["name"],
        ),
        "species": data.get(
            "species",
            existing_companion["species"],
        ),
        "role": data.get(
            "role",
            existing_companion["role"],
        ),
        "relationship": data.get(
            "relationship",
            existing_companion["relationship"],
        ),
        "level": data.get(
            "level",
            existing_companion["level"],
        ),
        "health": data.get(
            "health",
            existing_companion["health"],
        ),
        "ability": data.get(
            "ability",
            existing_companion["ability"],
        ),
    }

    for field in (
        "name",
        "species",
        "role",
        "relationship",
        "ability",
    ):
        updated_companion[field] = (
            updated_companion[field].strip()
        )

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE companions
            SET
                character_id = ?,
                name = ?,
                species = ?,
                role = ?,
                relationship = ?,
                level = ?,
                health = ?,
                ability = ?
            WHERE id = ?
            """,
            (
                updated_companion["character_id"],
                updated_companion["name"],
                updated_companion["species"],
                updated_companion["role"],
                updated_companion["relationship"],
                updated_companion["level"],
                updated_companion["health"],
                updated_companion["ability"],
                companion_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(
        fetch_companion(companion_id)
    ), 200


@app.delete("/api/companions/<int:companion_id>")
def delete_companion(companion_id):
    if fetch_companion(companion_id) is None:
        return jsonify(
            {"error": "Companion not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM companions
            WHERE id = ?
            """,
            (companion_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def fetch_journal_entry(entry_id):
    """Return one journal entry or None."""
    connection = get_connection()

    try:
        entry = connection.execute(
            """
            SELECT *
            FROM journal_entries
            WHERE id = ?
            """,
            (entry_id,),
        ).fetchone()

        return dict(entry) if entry else None
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/journal")
def get_journal_entries(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        entries = connection.execute(
            """
            SELECT *
            FROM journal_entries
            WHERE character_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (character_id,),
        ).fetchall()

        return jsonify(
            [dict(entry) for entry in entries]
        ), 200
    finally:
        connection.close()


@app.get("/api/journal/<int:entry_id>")
def get_journal_entry(entry_id):
    entry = fetch_journal_entry(entry_id)

    if entry is None:
        return jsonify(
            {"error": "Journal entry not found."}
        ), 404

    return jsonify(entry), 200


@app.post("/api/journal")
def create_journal_entry():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_journal_entry(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    if fetch_character(data["character_id"]) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    entry = {
        "character_id": data["character_id"],
        "title": data["title"].strip(),
        "category": data.get(
            "category",
            "Story",
        ).strip(),
        "content": data["content"].strip(),
    }

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO journal_entries (
                character_id,
                title,
                category,
                content
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                entry["character_id"],
                entry["title"],
                entry["category"],
                entry["content"],
            ),
        )

        connection.commit()
        entry_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(
        fetch_journal_entry(entry_id)
    ), 201


@app.patch("/api/journal/<int:entry_id>")
def update_journal_entry(entry_id):
    existing_entry = fetch_journal_entry(entry_id)

    if existing_entry is None:
        return jsonify(
            {"error": "Journal entry not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_journal_entry(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_entry["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_entry = {
        "character_id": character_id,
        "title": data.get(
            "title",
            existing_entry["title"],
        ),
        "category": data.get(
            "category",
            existing_entry["category"],
        ),
        "content": data.get(
            "content",
            existing_entry["content"],
        ),
    }

    for field in ("title", "category", "content"):
        updated_entry[field] = (
            updated_entry[field].strip()
        )

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE journal_entries
            SET
                character_id = ?,
                title = ?,
                category = ?,
                content = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                updated_entry["character_id"],
                updated_entry["title"],
                updated_entry["category"],
                updated_entry["content"],
                entry_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(
        fetch_journal_entry(entry_id)
    ), 200


@app.delete("/api/journal/<int:entry_id>")
def delete_journal_entry(entry_id):
    if fetch_journal_entry(entry_id) is None:
        return jsonify(
            {"error": "Journal entry not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM journal_entries
            WHERE id = ?
            """,
            (entry_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def fetch_world_location(location_id):
    """Return one world location or None."""
    connection = get_connection()

    try:
        location = connection.execute(
            """
            SELECT *
            FROM world_locations
            WHERE id = ?
            """,
            (location_id,),
        ).fetchone()

        return dict(location) if location else None
    finally:
        connection.close()


def fetch_location_by_name(character_id, name):
    """Return a character location with the given name or None."""
    connection = get_connection()

    try:
        location = connection.execute(
            """
            SELECT *
            FROM world_locations
            WHERE character_id = ?
              AND LOWER(name) = LOWER(?)
            """,
            (character_id, name),
        ).fetchone()

        return dict(location) if location else None
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/locations")
def get_world_locations(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        locations = connection.execute(
            """
            SELECT *
            FROM world_locations
            WHERE character_id = ?
            ORDER BY id
            """,
            (character_id,),
        ).fetchall()

        return jsonify(
            [dict(location) for location in locations]
        ), 200
    finally:
        connection.close()


@app.get("/api/locations/<int:location_id>")
def get_world_location(location_id):
    location = fetch_world_location(location_id)

    if location is None:
        return jsonify(
            {"error": "World location not found."}
        ), 404

    return jsonify(location), 200


@app.post("/api/locations")
def create_world_location():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_world_location(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data["character_id"]

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    name = data["name"].strip()

    if fetch_location_by_name(character_id, name):
        return jsonify(
            {
                "error": (
                    "A location with this name already exists "
                    "for the character."
                )
            }
        ), 409

    location = {
        "character_id": character_id,
        "name": name,
        "description": data.get(
            "description",
            "",
        ).strip(),
        "status": data.get(
            "status",
            "locked",
        ).strip().lower(),
    }

    connection = get_connection()

    try:
        if location["status"] == "current":
            connection.execute(
                """
                UPDATE world_locations
                SET status = 'discovered'
                WHERE character_id = ?
                  AND status = 'current'
                """,
                (character_id,),
            )

        cursor = connection.execute(
            """
            INSERT INTO world_locations (
                character_id,
                name,
                description,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                location["character_id"],
                location["name"],
                location["description"],
                location["status"],
            ),
        )

        connection.commit()
        location_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(
        fetch_world_location(location_id)
    ), 201


@app.patch("/api/locations/<int:location_id>")
def update_world_location(location_id):
    existing_location = fetch_world_location(location_id)

    if existing_location is None:
        return jsonify(
            {"error": "World location not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_world_location(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_location["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_location = {
        "character_id": character_id,
        "name": data.get(
            "name",
            existing_location["name"],
        ).strip(),
        "description": data.get(
            "description",
            existing_location["description"],
        ).strip(),
        "status": data.get(
            "status",
            existing_location["status"],
        ).strip().lower(),
    }

    duplicate = fetch_location_by_name(
        updated_location["character_id"],
        updated_location["name"],
    )

    if duplicate and duplicate["id"] != location_id:
        return jsonify(
            {
                "error": (
                    "A location with this name already exists "
                    "for the character."
                )
            }
        ), 409

    connection = get_connection()

    try:
        if updated_location["status"] == "current":
            connection.execute(
                """
                UPDATE world_locations
                SET status = 'discovered'
                WHERE character_id = ?
                  AND status = 'current'
                  AND id != ?
                """,
                (
                    updated_location["character_id"],
                    location_id,
                ),
            )

        connection.execute(
            """
            UPDATE world_locations
            SET
                character_id = ?,
                name = ?,
                description = ?,
                status = ?
            WHERE id = ?
            """,
            (
                updated_location["character_id"],
                updated_location["name"],
                updated_location["description"],
                updated_location["status"],
                location_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(
        fetch_world_location(location_id)
    ), 200


@app.delete("/api/locations/<int:location_id>")
def delete_world_location(location_id):
    if fetch_world_location(location_id) is None:
        return jsonify(
            {"error": "World location not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM world_locations
            WHERE id = ?
            """,
            (location_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

def serialize_battle(battle):
    """Convert a SQLite battle row into API-safe data."""
    if battle is None:
        return None

    battle_data = dict(battle)

    try:
        battle_data["battle_log"] = json.loads(
            battle_data["battle_log"]
        )
    except (TypeError, json.JSONDecodeError):
        battle_data["battle_log"] = []

    return battle_data


def fetch_battle(battle_id):
    """Return one serialized battle session or None."""
    connection = get_connection()

    try:
        battle = connection.execute(
            """
            SELECT *
            FROM battle_sessions
            WHERE id = ?
            """,
            (battle_id,),
        ).fetchone()

        return serialize_battle(battle)
    finally:
        connection.close()


@app.get("/api/characters/<int:character_id>/battles")
def get_battles(character_id):
    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    connection = get_connection()

    try:
        battles = connection.execute(
            """
            SELECT *
            FROM battle_sessions
            WHERE character_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (character_id,),
        ).fetchall()

        return jsonify(
            [serialize_battle(battle) for battle in battles]
        ), 200
    finally:
        connection.close()


@app.get("/api/battles/<int:battle_id>")
def get_battle(battle_id):
    battle = fetch_battle(battle_id)

    if battle is None:
        return jsonify(
            {"error": "Battle session not found."}
        ), 404

    return jsonify(battle), 200


@app.post("/api/battles")
def create_battle():
    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    errors = validate_battle_session(data)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character = fetch_character(data["character_id"])

    if character is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    battle = {
        "character_id": data["character_id"],
        "enemy_name": data["enemy_name"].strip(),
        "player_health": data.get(
            "player_health",
            character["health"],
        ),
        "player_max_health": data.get(
            "player_max_health",
            character["max_health"],
        ),
        "enemy_health": data.get("enemy_health", 100),
        "enemy_max_health": data.get(
            "enemy_max_health",
            100,
        ),
        "status": data.get(
            "status",
            "active",
        ).strip().lower(),
        "turn_count": data.get("turn_count", 0),
        "battle_log": data.get(
            "battle_log",
            [
                (
                    f'{data["enemy_name"].strip()} '
                    "watches your movements carefully."
                )
            ],
        ),
    }

    if battle["player_health"] > battle["player_max_health"]:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    (
                        "player_health cannot exceed "
                        "player_max_health."
                    )
                ],
            }
        ), 400

    if battle["enemy_health"] > battle["enemy_max_health"]:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    (
                        "enemy_health cannot exceed "
                        "enemy_max_health."
                    )
                ],
            }
        ), 400

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO battle_sessions (
                character_id,
                enemy_name,
                player_health,
                player_max_health,
                enemy_health,
                enemy_max_health,
                status,
                turn_count,
                battle_log
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                battle["character_id"],
                battle["enemy_name"],
                battle["player_health"],
                battle["player_max_health"],
                battle["enemy_health"],
                battle["enemy_max_health"],
                battle["status"],
                battle["turn_count"],
                json.dumps(battle["battle_log"]),
            ),
        )

        connection.commit()
        battle_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(fetch_battle(battle_id)), 201


@app.patch("/api/battles/<int:battle_id>")
def update_battle(battle_id):
    existing_battle = fetch_battle(battle_id)

    if existing_battle is None:
        return jsonify(
            {"error": "Battle session not found."}
        ), 404

    if not request.is_json:
        return jsonify(
            {"error": "Content-Type must be application/json."}
        ), 415

    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {"error": "Request body must contain valid JSON."}
        ), 400

    if not data:
        return jsonify(
            {"error": "At least one field must be provided."}
        ), 400

    errors = validate_battle_session(data, partial=True)

    if errors:
        return jsonify(
            {
                "error": "Validation failed.",
                "details": errors,
            }
        ), 400

    character_id = data.get(
        "character_id",
        existing_battle["character_id"],
    )

    if fetch_character(character_id) is None:
        return jsonify(
            {"error": "Character not found."}
        ), 404

    updated_battle = {
        "character_id": character_id,
        "enemy_name": data.get(
            "enemy_name",
            existing_battle["enemy_name"],
        ).strip(),
        "player_health": data.get(
            "player_health",
            existing_battle["player_health"],
        ),
        "player_max_health": data.get(
            "player_max_health",
            existing_battle["player_max_health"],
        ),
        "enemy_health": data.get(
            "enemy_health",
            existing_battle["enemy_health"],
        ),
        "enemy_max_health": data.get(
            "enemy_max_health",
            existing_battle["enemy_max_health"],
        ),
        "status": data.get(
            "status",
            existing_battle["status"],
        ).strip().lower(),
        "turn_count": data.get(
            "turn_count",
            existing_battle["turn_count"],
        ),
        "battle_log": data.get(
            "battle_log",
            existing_battle["battle_log"],
        ),
    }

    if (
        updated_battle["player_health"]
        > updated_battle["player_max_health"]
    ):
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    (
                        "player_health cannot exceed "
                        "player_max_health."
                    )
                ],
            }
        ), 400

    if (
        updated_battle["enemy_health"]
        > updated_battle["enemy_max_health"]
    ):
        return jsonify(
            {
                "error": "Validation failed.",
                "details": [
                    (
                        "enemy_health cannot exceed "
                        "enemy_max_health."
                    )
                ],
            }
        ), 400

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE battle_sessions
            SET
                character_id = ?,
                enemy_name = ?,
                player_health = ?,
                player_max_health = ?,
                enemy_health = ?,
                enemy_max_health = ?,
                status = ?,
                turn_count = ?,
                battle_log = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                updated_battle["character_id"],
                updated_battle["enemy_name"],
                updated_battle["player_health"],
                updated_battle["player_max_health"],
                updated_battle["enemy_health"],
                updated_battle["enemy_max_health"],
                updated_battle["status"],
                updated_battle["turn_count"],
                json.dumps(updated_battle["battle_log"]),
                battle_id,
            ),
        )

        connection.commit()
    finally:
        connection.close()

    return jsonify(fetch_battle(battle_id)), 200


@app.delete("/api/battles/<int:battle_id>")
def delete_battle(battle_id):
    if fetch_battle(battle_id) is None:
        return jsonify(
            {"error": "Battle session not found."}
        ), 404

    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM battle_sessions
            WHERE id = ?
            """,
            (battle_id,),
        )

        connection.commit()
    finally:
        connection.close()

    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
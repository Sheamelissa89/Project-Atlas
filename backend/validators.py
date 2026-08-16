def is_valid_integer(value, minimum=0):
    """Return True when value is an integer at or above the minimum."""
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= minimum
    )


def validate_character(data, partial=False):
    """Validate character data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = ("name", "character_class")

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    for field in required_fields:
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{field} must be a non-empty string."
                )
            elif len(value.strip()) > 100:
                errors.append(
                    f"{field} cannot exceed 100 characters."
                )

    integer_fields = {
        "level": 1,
        "experience": 0,
        "health": 0,
        "max_health": 1,
        "gold": 0,
    }

    for field, minimum in integer_fields.items():
        if field in data and not is_valid_integer(
            data[field],
            minimum,
        ):
            errors.append(
                f"{field} must be an integer of at least {minimum}."
            )

    if (
        "health" in data
        and "max_health" in data
        and is_valid_integer(data["health"])
        and is_valid_integer(data["max_health"], 1)
        and data["health"] > data["max_health"]
    ):
        errors.append("health cannot exceed max_health.")

    allowed_fields = {
        "name",
        "character_class",
        "level",
        "experience",
        "health",
        "max_health",
        "gold",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_inventory_item(data, partial=False):
    """Validate inventory data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "name",
        "item_type",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    for field in ("name", "item_type"):
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{field} must be a non-empty string."
                )
            elif len(value.strip()) > 100:
                errors.append(
                    f"{field} cannot exceed 100 characters."
                )

    if "description" in data:
        description = data["description"]

        if not isinstance(description, str):
            errors.append("description must be a string.")
        elif len(description) > 500:
            errors.append(
                "description cannot exceed 500 characters."
            )

    if "quantity" in data and not is_valid_integer(
        data["quantity"],
        1,
    ):
        errors.append(
            "quantity must be an integer of at least 1."
        )

    if "value" in data and not is_valid_integer(
        data["value"],
        0,
    ):
        errors.append(
            "value must be a non-negative integer."
        )

    if (
        "equipped" in data
        and not isinstance(data["equipped"], bool)
    ):
        errors.append("equipped must be true or false.")

    allowed_fields = {
        "character_id",
        "name",
        "item_type",
        "description",
        "quantity",
        "value",
        "equipped",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_quest(data, partial=False):
    """Validate quest data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "title",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    if "title" in data:
        title = data["title"]

        if not isinstance(title, str) or not title.strip():
            errors.append(
                "title must be a non-empty string."
            )
        elif len(title.strip()) > 150:
            errors.append(
                "title cannot exceed 150 characters."
            )

    if "description" in data:
        description = data["description"]

        if not isinstance(description, str):
            errors.append("description must be a string.")
        elif len(description) > 1000:
            errors.append(
                "description cannot exceed 1000 characters."
            )

    allowed_statuses = {
        "available",
        "active",
        "completed",
        "locked",
        "failed",
    }

    if "status" in data:
        status = data["status"]

        if not isinstance(status, str):
            errors.append("status must be a string.")
        elif status.strip().lower() not in allowed_statuses:
            errors.append(
                "status must be available, active, completed, "
                "locked, or failed."
            )

    for field in (
        "reward_gold",
        "reward_experience",
    ):
        if field in data and not is_valid_integer(
            data[field],
            0,
        ):
            errors.append(
                f"{field} must be a non-negative integer."
            )

    allowed_fields = {
        "character_id",
        "title",
        "description",
        "status",
        "reward_gold",
        "reward_experience",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_companion(data, partial=False):
    """Validate companion data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "name",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    string_fields = {
        "name": 100,
        "species": 100,
        "role": 150,
        "relationship": 100,
        "ability": 200,
    }

    for field, maximum_length in string_fields.items():
        if field in data:
            value = data[field]

            if not isinstance(value, str):
                errors.append(f"{field} must be a string.")
            elif field == "name" and not value.strip():
                errors.append(
                    "name must be a non-empty string."
                )
            elif len(value.strip()) > maximum_length:
                errors.append(
                    f"{field} cannot exceed "
                    f"{maximum_length} characters."
                )

    if "level" in data and not is_valid_integer(
        data["level"],
        1,
    ):
        errors.append(
            "level must be an integer of at least 1."
        )

    if "health" in data and not is_valid_integer(
        data["health"],
        0,
    ):
        errors.append(
            "health must be a non-negative integer."
        )

    allowed_fields = {
        "character_id",
        "name",
        "species",
        "role",
        "relationship",
        "level",
        "health",
        "ability",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_journal_entry(data, partial=False):
    """Validate journal entry data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "title",
        "content",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    string_fields = {
        "title": 150,
        "category": 50,
        "content": 5000,
    }

    for field, maximum_length in string_fields.items():
        if field in data:
            value = data[field]

            if not isinstance(value, str):
                errors.append(f"{field} must be a string.")
            elif field in {"title", "content"} and not value.strip():
                errors.append(
                    f"{field} must be a non-empty string."
                )
            elif len(value.strip()) > maximum_length:
                errors.append(
                    f"{field} cannot exceed "
                    f"{maximum_length} characters."
                )

    allowed_fields = {
        "character_id",
        "title",
        "category",
        "content",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_world_location(data, partial=False):
    """Validate world location data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "name",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    if "name" in data:
        name = data["name"]

        if not isinstance(name, str) or not name.strip():
            errors.append(
                "name must be a non-empty string."
            )
        elif len(name.strip()) > 150:
            errors.append(
                "name cannot exceed 150 characters."
            )

    if "description" in data:
        description = data["description"]

        if not isinstance(description, str):
            errors.append("description must be a string.")
        elif len(description) > 1000:
            errors.append(
                "description cannot exceed 1000 characters."
            )

    allowed_statuses = {
        "current",
        "discovered",
        "locked",
    }

    if "status" in data:
        status = data["status"]

        if not isinstance(status, str):
            errors.append("status must be a string.")
        elif status.strip().lower() not in allowed_statuses:
            errors.append(
                "status must be current, discovered, or locked."
            )

    allowed_fields = {
        "character_id",
        "name",
        "description",
        "status",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors

def validate_battle_session(data, partial=False):
    """Validate battle session data for POST and PATCH requests."""
    errors = []

    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]

    required_fields = (
        "character_id",
        "enemy_name",
    )

    if not partial:
        for field in required_fields:
            if field not in data:
                errors.append(f"{field} is required.")

    if "character_id" in data and not is_valid_integer(
        data["character_id"],
        1,
    ):
        errors.append(
            "character_id must be an integer of at least 1."
        )

    if "enemy_name" in data:
        enemy_name = data["enemy_name"]

        if (
            not isinstance(enemy_name, str)
            or not enemy_name.strip()
        ):
            errors.append(
                "enemy_name must be a non-empty string."
            )
        elif len(enemy_name.strip()) > 150:
            errors.append(
                "enemy_name cannot exceed 150 characters."
            )

    integer_fields = {
        "player_health": 0,
        "player_max_health": 1,
        "enemy_health": 0,
        "enemy_max_health": 1,
        "turn_count": 0,
    }

    for field, minimum in integer_fields.items():
        if field in data and not is_valid_integer(
            data[field],
            minimum,
        ):
            errors.append(
                f"{field} must be an integer "
                f"of at least {minimum}."
            )

    allowed_statuses = {
        "active",
        "victory",
        "defeat",
        "peace",
    }

    if "status" in data:
        status = data["status"]

        if not isinstance(status, str):
            errors.append("status must be a string.")
        elif status.strip().lower() not in allowed_statuses:
            errors.append(
                "status must be active, victory, defeat, or peace."
            )

    if "battle_log" in data:
        battle_log = data["battle_log"]

        if not isinstance(battle_log, list):
            errors.append("battle_log must be a list.")
        elif not all(
            isinstance(message, str)
            and message.strip()
            and len(message) <= 500
            for message in battle_log
        ):
            errors.append(
                "Every battle_log message must be a non-empty "
                "string of no more than 500 characters."
            )

    if (
        "player_health" in data
        and "player_max_health" in data
        and is_valid_integer(data["player_health"])
        and is_valid_integer(data["player_max_health"], 1)
        and data["player_health"] > data["player_max_health"]
    ):
        errors.append(
            "player_health cannot exceed player_max_health."
        )

    if (
        "enemy_health" in data
        and "enemy_max_health" in data
        and is_valid_integer(data["enemy_health"])
        and is_valid_integer(data["enemy_max_health"], 1)
        and data["enemy_health"] > data["enemy_max_health"]
    ):
        errors.append(
            "enemy_health cannot exceed enemy_max_health."
        )

    allowed_fields = {
        "character_id",
        "enemy_name",
        "player_health",
        "player_max_health",
        "enemy_health",
        "enemy_max_health",
        "status",
        "turn_count",
        "battle_log",
    }

    unexpected_fields = set(data) - allowed_fields

    for field in sorted(unexpected_fields):
        errors.append(f"{field} is not an allowed field.")

    return errors
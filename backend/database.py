import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "instance"
    / "atlas.db"
)


def get_connection():
    """Create and return a configured SQLite connection."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_database():
    """Create and safely upgrade the Project Atlas database."""
    connection = get_connection()

    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                character_class TEXT NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                experience INTEGER NOT NULL DEFAULT 0,
                health INTEGER NOT NULL DEFAULT 100,
                max_health INTEGER NOT NULL DEFAULT 100,
                gold INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                item_type TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                quantity INTEGER NOT NULL DEFAULT 1,
                value INTEGER NOT NULL DEFAULT 0,
                equipped INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'available',
                reward_gold INTEGER NOT NULL DEFAULT 0,
                reward_experience INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS world_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'locked',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (character_id, name),
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );

                        CREATE TABLE IF NOT EXISTS battle_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                enemy_name TEXT NOT NULL,
                player_health INTEGER NOT NULL DEFAULT 100,
                player_max_health INTEGER NOT NULL DEFAULT 100,
                enemy_health INTEGER NOT NULL DEFAULT 100,
                enemy_max_health INTEGER NOT NULL DEFAULT 100,
                status TEXT NOT NULL DEFAULT 'active',
                turn_count INTEGER NOT NULL DEFAULT 0,
                battle_log TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS companions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                species TEXT NOT NULL DEFAULT 'Human',
                role TEXT NOT NULL DEFAULT '',
                relationship TEXT NOT NULL DEFAULT 'Unknown',
                level INTEGER NOT NULL DEFAULT 1,
                health INTEGER NOT NULL DEFAULT 100,
                ability TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Story',
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id)
                    REFERENCES characters(id)
                    ON DELETE CASCADE
            );
            """
        )

        companion_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(companions)"
            ).fetchall()
        }

        if "role" not in companion_columns:
            connection.execute(
                """
                ALTER TABLE companions
                ADD COLUMN role TEXT NOT NULL DEFAULT ''
                """
            )

        if "relationship" not in companion_columns:
            connection.execute(
                """
                ALTER TABLE companions
                ADD COLUMN relationship
                TEXT NOT NULL DEFAULT 'Unknown'
                """
            )

        journal_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(journal_entries)"
            ).fetchall()
        }

        if "category" not in journal_columns:
            connection.execute(
                """
                ALTER TABLE journal_entries
                ADD COLUMN category
                TEXT NOT NULL DEFAULT 'Story'
                """
            )

        connection.commit()
    finally:
        connection.close()
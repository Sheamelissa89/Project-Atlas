# 🏔️ Project Atlas

## ⚔️ A Persistent Modular RPG Engine

Project Atlas is a full-stack RPG engine built with React, Flask, and SQLite. It combines modular gameplay systems with persistent data, RESTful API design, input validation, and an interactive frontend.

Rather than representing one fixed game, Atlas is designed as an expandable engine where independent systems work together to create a living world shaped by player choices.

---

## 📖 Project Vision

Project Atlas explores the idea that every choice has consequences.

Encounters do not always need to end in combat. Players may overcome situations through observation, dialogue, relationships, exploration, wisdom, or battle.

The long-term goal is to simulate both the external game world and the internal development of the player.

---

## ✨ Current Features

- React single-page application
- Responsive dark-fantasy interface
- React Router navigation
- Flask REST API
- SQLite data persistence
- Input validation and structured error responses
- Appropriate HTTP status codes
- Character CRUD and progression
- Persistent inventory management
- Quest tracking
- Companion relationships
- Journal entries
- World location discovery
- Interactive turn-based battles
- Battle state and battle-log persistence
- Frontend service and custom-hook layers
- Automated backend API tests
- Frontend linting and production builds

---

## 🛠️ Technology Stack

### Frontend

- React
- React Router
- JavaScript ES6+
- HTML5
- CSS3
- Vite
- ESLint

### Backend

- Python
- Flask
- Flask-CORS
- SQLite
- Python `unittest`

### Development Tools

- Git and GitHub
- Visual Studio Code
- PowerShell
- Python virtual environments
- npm

---

## 🧩 Project Architecture

```text
Project Atlas/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   └── validators.py
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── eslint.config.js
│   ├── package.json
│   └── vite.config.js
│
├── entities/
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── instance/
│   └── atlas.db
│
├── requirements.txt
└── README.md
```

The `instance` directory and SQLite database are generated locally and excluded from Git tracking.

---

## 🎮 Implemented Game Systems

### Character System

Characters include persistent information such as:

- Name
- Character class
- Level
- Experience
- Health and maximum health
- Gold

### Inventory System

Inventory items support:

- Item names and types
- Descriptions
- Quantities
- Values
- Equipped status
- Character ownership

### Quest System

Quests include:

- Titles and descriptions
- Availability and completion status
- Gold rewards
- Experience rewards
- Character ownership

### Companion System

Companions include:

- Name and species
- Role
- Relationship status
- Level and health
- Special ability
- Character ownership

### Journal System

Journal entries support:

- Titles
- Categories
- Written content
- Creation timestamps
- Update timestamps
- Character ownership

### World System

World locations include:

- Location name
- Description
- Discovery status
- Current-location status
- Character ownership

### Battle System

Battle sessions include:

- Player and enemy health
- Maximum health values
- Enemy name
- Battle status
- Turn count
- Persistent battle log
- Character ownership

Players can currently:

- Attack
- Defend
- Use a potion
- Attempt peace

Battle changes remain saved after the page is refreshed.

---

## 🌐 REST API

The Flask backend exposes RESTful endpoints under:

```text
http://127.0.0.1:5000/api
```

### Main Resources

| Resource | Collection endpoint | Character-specific endpoint |
|---|---|---|
| Characters | `/api/characters` | `/api/characters/<id>` |
| Inventory | `/api/inventory` | `/api/characters/<id>/inventory` |
| Quests | `/api/quests` | `/api/characters/<id>/quests` |
| Companions | `/api/companions` | `/api/characters/<id>/companions` |
| Journal | `/api/journal` | `/api/characters/<id>/journal` |
| Locations | `/api/locations` | `/api/characters/<id>/locations` |
| Battles | `/api/battles` | `/api/characters/<id>/battles` |

### Supported HTTP Methods

- `GET` retrieves resources.
- `POST` creates resources.
- `PATCH` updates existing resources.
- `DELETE` removes resources.

### Status Codes

The API uses meaningful HTTP status codes, including:

- `200 OK`
- `201 Created`
- `204 No Content`
- `400 Bad Request`
- `404 Not Found`

Validation failures and missing resources return structured JSON error responses.

---

## 💾 SQLite Persistence

Project Atlas stores game data in:

```text
instance/atlas.db
```

The database is initialized automatically when the Flask application starts.

Foreign-key relationships associate gameplay records with characters. Related records use cascading deletion, ensuring that character-owned resources are removed when their character is deleted.

---

## 🚀 Local Setup

### 1. Clone the repository

```powershell
git clone <repository-url>
cd "Project Atlas"
```

### 2. Create a Python virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Install frontend dependencies

```powershell
cd frontend
npm install
```

---

## ▶️ Running Project Atlas

The backend and frontend run in separate terminals.

### Terminal 1 — Flask backend

From the Project Atlas root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m backend.app
```

The API will run at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

### Terminal 2 — React frontend

From the `frontend` directory:

```powershell
npm run dev
```

The application will run at:

```text
http://localhost:5173
```

---

## 🧪 Testing and Verification

### Run backend tests

From the Project Atlas root:

```powershell
python -m unittest tests.test_api -v
```

The automated suite currently contains 14 passing tests covering:

- API health
- Character CRUD
- Character validation
- Missing-character handling
- Inventory CRUD
- Quest CRUD
- Companion CRUD
- Journal CRUD
- World-location CRUD
- Battle CRUD and persistence

### Run frontend linting

From the `frontend` directory:

```powershell
npm run lint
```

### Create a production build

From the `frontend` directory:

```powershell
npm run build
```

The generated production files are written to `frontend/dist` and excluded from Git tracking.

---

## 🎓 Applied Course Concepts

Project Atlas incorporates concepts developed throughout Courses 110–112:

- RESTful API architecture
- HTTP methods and status codes
- Request validation
- Structured JSON responses
- CRUD operations
- Relational database design
- SQLite persistence
- Foreign-key relationships
- Cascading deletion
- Separation of concerns
- Reusable frontend components
- React services and custom hooks
- Automated API testing
- Modular package organization

The project applies organizational concepts also encountered in Django—such as modular packages, clear responsibility boundaries, validation, database relationships, and URL-driven resources—without unnecessarily mixing Django into the Flask backend.

---

## 🧭 Development Roadmap

Future development may include:

- User authentication and authorization
- Multiple save profiles
- Expanded character statistics
- Equipment bonuses
- Enemy artificial intelligence
- Dynamic quest consequences
- Dialogue trees
- Reputation systems
- Deeper companion relationships
- Emotional-development mechanics
- Trading and crafting
- Procedural encounters
- Soundtracks and sound effects
- Original character artwork
- 3D character models
- Production deployment
- PostgreSQL support

---

## 💡 Design Philosophy

Each gameplay mechanic is developed as an independent system with its own database representation, API routes, validation, frontend service, custom hook, and interface.

This separation makes Project Atlas easier to test, maintain, and expand while allowing new systems to interact with existing ones through consistent interfaces.

---

## 🌟 Long-Term Goal

Project Atlas is intended to become an expandable RPG framework capable of supporting evolving characters, interconnected stories, meaningful choices, persistent consequences, original artwork, and immersive sound design.

---

## 📜 License

This project is under active personal development.

© Shea Mullin — All Rights Reserved.
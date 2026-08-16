import { useCompanions } from "../hooks/useCompanions";
import "../styles/GamePages.css";


const starterCompanions = [
  {
    name: "Elara",
    species: "Human",
    role: "Village Scout",
    relationship: "Acquaintance",
    ability: "Pathfinder",
    level: 1,
    health: 100,
  },
  {
    name: "Orin",
    species: "Human",
    role: "Traveling Scholar",
    relationship: "Unknown",
    ability: "Ancient Knowledge",
    level: 1,
    health: 100,
  },
  {
    name: "Nyx",
    species: "Forest Guardian",
    role: "Guardian of the Grove",
    relationship: "Undiscovered",
    ability: "Nature Bond",
    level: 1,
    health: 100,
  },
];


function Companions() {
  const {
    companions,
    isLoading,
    isSaving,
    error,
    saveStarterCompanions,
  } = useCompanions();

  const displayedCompanions =
    companions.length > 0
      ? companions
      : starterCompanions;

  function handleSaveStarterCompanions() {
    saveStarterCompanions(starterCompanions);
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Companions</h1>

        <p>
          Build relationships, unlock companion abilities, and discover
          how each person responds to the player’s choices.
        </p>
      </header>

      {isLoading && (
        <p>Loading companions...</p>
      )}

      {error && (
        <p role="alert">
          Unable to load companions: {error}
        </p>
      )}

      {!isLoading
        && companions.length === 0
        && !error && (
          <section className="page-section">
            <p>
              These companions have not been saved to the Atlas
              database yet.
            </p>

            <button
              className="game-button"
              type="button"
              disabled={isSaving}
              onClick={handleSaveStarterCompanions}
            >
              {isSaving
                ? "Saving Companions..."
                : "Save Starter Companions"}
            </button>
          </section>
        )}

      <section className="game-grid">
        {displayedCompanions.map((companion) => (
          <article
            className="game-card"
            key={companion.id || companion.name}
          >
            <h2>{companion.name}</h2>

            <p>{companion.role}</p>

            <p>
              <strong>Species:</strong>{" "}
              {companion.species}
            </p>

            <p>
              <strong>Relationship:</strong>{" "}
              {companion.relationship}
            </p>

            <p>
              <strong>Ability:</strong>{" "}
              {companion.ability}
            </p>

            <p>
              <strong>Level:</strong>{" "}
              {companion.level}
            </p>

            <p>
              <strong>Health:</strong>{" "}
              {companion.health}
            </p>

            <button className="game-button" type="button">
              View Companion
            </button>
          </article>
        ))}
      </section>
    </main>
  );
}

export default Companions;
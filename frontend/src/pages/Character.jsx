import { useCharacter } from "../hooks/useCharacter";
import "../styles/GamePages.css";


function Character() {
  const {
    character,
    isLoading,
    error,
    saveCharacter,
  } = useCharacter();

  const displayedCharacter = character || {
    name: "Shea",
    character_class: "Explorer",
    level: 1,
    experience: 15,
    health: 100,
    max_health: 100,
    gold: 0,
  };

  const stats = [
    { label: "Health", value: displayedCharacter.health },
    { label: "Strength", value: 8 },
    { label: "Knowledge", value: 7 },
    { label: "Observation", value: 9 },
    { label: "Ingenuity", value: 6 },
    { label: "Character", value: 8 },
  ];

  const experiencePercentage = Math.min(
    displayedCharacter.experience,
    100,
  );

  async function handleCreateCharacter() {
    await saveCharacter({
      name: "Shea",
      character_class: "Explorer",
      level: 1,
      experience: 15,
      health: 100,
      max_health: 100,
      gold: 0,
    });
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Character</h1>
        <p>
          View the player’s current condition, abilities, traits, emotions,
          and progression throughout the world of Atlas.
        </p>
      </header>

      {isLoading && <p>Loading character data...</p>}

      {error && (
        <p role="alert">
          Unable to load character: {error}
        </p>
      )}

      {!isLoading && !character && !error && (
        <section className="page-section">
          <p>
            This character has not been saved to the Atlas database yet.
          </p>

          <button
            type="button"
            onClick={handleCreateCharacter}
          >
            Create Character Save
          </button>
        </section>
      )}

      <section className="game-grid">
        <article className="game-card">
          <h2>{displayedCharacter.name}</h2>

          <p>
            Level {displayedCharacter.level}{" "}
            {displayedCharacter.character_class}
          </p>

          <p>Current location: Forest Entrance</p>
          <p>Gold: {displayedCharacter.gold}</p>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${experiencePercentage}%` }}
            />
          </div>

          <p>{displayedCharacter.experience} / 100 XP</p>
        </article>

        <article className="game-card">
          <h2>Core Traits</h2>

          <div className="tag-row">
            <span className="game-tag">Observant</span>
            <span className="game-tag">Persistent</span>
            <span className="game-tag">Protective</span>
            <span className="game-tag">Curious</span>
          </div>
        </article>
      </section>

      <section className="page-section">
        <h2>Character Stats</h2>

        <div className="game-grid">
          {stats.map((stat) => (
            <article className="game-card" key={stat.label}>
              <h3>{stat.label}</h3>
              <p>{stat.value}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default Character;
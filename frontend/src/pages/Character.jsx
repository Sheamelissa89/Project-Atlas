import "../styles/GamePages.css";

function Character() {
  const stats = [
    { label: "Health", value: 100 },
    { label: "Strength", value: 8 },
    { label: "Knowledge", value: 7 },
    { label: "Observation", value: 9 },
    { label: "Ingenuity", value: 6 },
    { label: "Character", value: 8 },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Character</h1>
        <p>
          View the player’s current condition, abilities, traits, emotions,
          and progression throughout the world of Atlas.
        </p>
      </header>

      <section className="game-grid">
        <article className="game-card">
          <h2>Shea</h2>
          <p>Level 1 Explorer</p>
          <p>Current location: Forest Entrance</p>

          <div className="progress-track">
            <div className="progress-fill" style={{ width: "15%" }} />
          </div>

          <p>15 / 100 XP</p>
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
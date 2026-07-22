import "../styles/GamePages.css";

function Companions() {
  const companions = [
    {
      name: "Elara",
      role: "Village Scout",
      relationship: "Acquaintance",
      ability: "Pathfinder",
    },
    {
      name: "Orin",
      role: "Traveling Scholar",
      relationship: "Unknown",
      ability: "Ancient Knowledge",
    },
    {
      name: "Nyx",
      role: "Forest Guardian",
      relationship: "Undiscovered",
      ability: "Nature Bond",
    },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Companions</h1>
        <p>
          Build relationships, unlock companion abilities, and discover how
          each person responds to the player’s choices.
        </p>
      </header>

      <section className="game-grid">
        {companions.map((companion) => (
          <article className="game-card" key={companion.name}>
            <h2>{companion.name}</h2>
            <p>{companion.role}</p>
            <p>
              <strong>Relationship:</strong> {companion.relationship}
            </p>
            <p>
              <strong>Ability:</strong> {companion.ability}
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
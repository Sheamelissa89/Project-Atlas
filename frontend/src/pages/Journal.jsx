import "../styles/GamePages.css";

function Journal() {
  const entries = [
    {
      title: "The Journey Begins",
      category: "Story",
      text: "I arrived at the Forest Entrance with only a map and a few supplies.",
    },
    {
      title: "A Choice Without Violence",
      category: "Reflection",
      text: "Not every enemy must remain an enemy. Observation may reveal another path.",
    },
    {
      title: "Whispers in the Grove",
      category: "Discovery",
      text: "The trees react differently when approached with patience.",
    },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Atlas Journal</h1>
        <p>
          Record discoveries, choices, consequences, emotional development,
          and important moments from the journey.
        </p>
      </header>

      <section className="game-grid">
        {entries.map((entry) => (
          <article className="game-card" key={entry.title}>
            <span className="game-tag">{entry.category}</span>
            <h2>{entry.title}</h2>
            <p>{entry.text}</p>
          </article>
        ))}
      </section>
    </main>
  );
}

export default Journal;
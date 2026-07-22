import "../styles/GamePages.css";

function World() {
  const locations = [
    {
      name: "Forest Entrance",
      status: "Current Location",
      description: "A quiet path leading into the ancient woods.",
    },
    {
      name: "Whispering Grove",
      status: "Discovered",
      description: "The trees appear to remember every traveler.",
    },
    {
      name: "Village of Emberfall",
      status: "Discovered",
      description: "A protected settlement built around an old watchtower.",
    },
    {
      name: "Moonlit Ruins",
      status: "Locked",
      description: "A forgotten structure that becomes visible after sunset.",
    },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>World Map</h1>
        <p>
          Explore discovered locations, unlock hidden regions, and track the
          player’s current position.
        </p>
      </header>

      <section className="game-grid">
        {locations.map((location) => (
          <article className="game-card" key={location.name}>
            <h2>{location.name}</h2>
            <p>{location.description}</p>
            <span className="game-tag">{location.status}</span>
          </article>
        ))}
      </section>
    </main>
  );
}

export default World;
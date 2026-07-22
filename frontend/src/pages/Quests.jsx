import "../styles/GamePages.css";

function Quests() {
  const quests = [
    {
      title: "Into the Forest",
      status: "Active",
      goal: "Travel beyond the Forest Entrance.",
    },
    {
      title: "The Missing Herbalist",
      status: "Active",
      goal: "Find clues near the Whispering Grove.",
    },
    {
      title: "A Light in the Darkness",
      status: "Locked",
      goal: "Discover the entrance to the Moonlit Ruins.",
    },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Quests</h1>
        <p>
          Track current objectives, completed missions, important discoveries,
          and future rewards.
        </p>
      </header>

      <section className="game-grid">
        {quests.map((quest) => (
          <article className="game-card" key={quest.title}>
            <h2>{quest.title}</h2>
            <p>{quest.goal}</p>
            <span className="game-tag">{quest.status}</span>
          </article>
        ))}
      </section>
    </main>
  );
}

export default Quests;
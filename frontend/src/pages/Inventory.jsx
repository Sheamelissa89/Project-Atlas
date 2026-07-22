import "../styles/GamePages.css";

function Inventory() {
  const items = [
    {
      name: "Healing Potion",
      type: "Potion",
      quantity: 3,
      description: "Restores health during or after battle.",
    },
    {
      name: "Ancient Map",
      type: "Quest Item",
      quantity: 1,
      description: "Shows fragments of a forgotten region.",
    },
    {
      name: "Explorer Backpack",
      type: "Equipment",
      quantity: 1,
      description: "Increases the number of items the player can carry.",
    },
    {
      name: "Crystal Lantern",
      type: "Tool",
      quantity: 1,
      description: "Reveals hidden pathways and magical markings.",
    },
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Inventory</h1>
        <p>
          Manage equipment, potions, quest items, tools, and everything
          collected during the journey.
        </p>
      </header>

      <section className="game-grid">
        {items.map((item) => (
          <article className="game-card" key={item.name}>
            <h2>{item.name}</h2>
            <p>{item.description}</p>
            <p>
              <strong>Type:</strong> {item.type}
            </p>
            <p>
              <strong>Quantity:</strong> {item.quantity}
            </p>

            <button className="game-button" type="button">
              View Item
            </button>
          </article>
        ))}
      </section>
    </main>
  );
}

export default Inventory;
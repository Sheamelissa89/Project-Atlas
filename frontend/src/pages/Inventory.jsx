import { useInventory } from "../hooks/useInventory";
import "../styles/GamePages.css";


const starterItems = [
  {
    name: "Healing Potion",
    type: "Potion",
    quantity: 3,
    value: 25,
    description: "Restores health during or after battle.",
  },
  {
    name: "Ancient Map",
    type: "Quest Item",
    quantity: 1,
    value: 0,
    description: "Shows fragments of a forgotten region.",
  },
  {
    name: "Explorer Backpack",
    type: "Equipment",
    quantity: 1,
    value: 50,
    description:
      "Increases the number of items the player can carry.",
  },
  {
    name: "Crystal Lantern",
    type: "Tool",
    quantity: 1,
    value: 40,
    description:
      "Reveals hidden pathways and magical markings.",
  },
];


function Inventory() {
  const {
    items,
    isLoading,
    isSaving,
    error,
    saveStarterItems,
  } = useInventory();

  const displayedItems =
    items.length > 0 ? items : starterItems;

  function handleSaveStarterItems() {
    saveStarterItems(starterItems);
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Inventory</h1>

        <p>
          Manage equipment, potions, quest items, tools, and everything
          collected during the journey.
        </p>
      </header>

      {isLoading && (
        <p>Loading inventory...</p>
      )}

      {error && (
        <p role="alert">
          Unable to load inventory: {error}
        </p>
      )}

      {!isLoading && items.length === 0 && !error && (
        <section className="page-section">
          <p>
            These starter items have not been saved to the Atlas
            database yet.
          </p>

          <button
            className="game-button"
            type="button"
            disabled={isSaving}
            onClick={handleSaveStarterItems}
          >
            {isSaving
              ? "Saving Inventory..."
              : "Save Starter Inventory"}
          </button>
        </section>
      )}

      <section className="game-grid">
        {displayedItems.map((item) => {
          const itemType = item.item_type || item.type;

          return (
            <article
              className="game-card"
              key={item.id || item.name}
            >
              <h2>{item.name}</h2>

              <p>{item.description}</p>

              <p>
                <strong>Type:</strong> {itemType}
              </p>

              <p>
                <strong>Quantity:</strong> {item.quantity}
              </p>

              {"value" in item && (
                <p>
                  <strong>Value:</strong> {item.value} gold
                </p>
              )}

              {"equipped" in item && (
                <p>
                  <strong>Status:</strong>{" "}
                  {item.equipped ? "Equipped" : "Stored"}
                </p>
              )}

              <button className="game-button" type="button">
                View Item
              </button>
            </article>
          );
        })}
      </section>
    </main>
  );
}

export default Inventory;
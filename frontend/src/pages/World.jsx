import { useWorld } from "../hooks/useWorld";
import "../styles/GamePages.css";


const starterLocations = [
  {
    name: "Forest Entrance",
    status: "Current Location",
    description:
      "A quiet path leading into the ancient woods.",
  },
  {
    name: "Whispering Grove",
    status: "Discovered",
    description:
      "The trees appear to remember every traveler.",
  },
  {
    name: "Village of Emberfall",
    status: "Discovered",
    description:
      "A protected settlement built around an old watchtower.",
  },
  {
    name: "Moonlit Ruins",
    status: "Locked",
    description:
      "A forgotten structure that becomes visible after sunset.",
  },
];


function formatStatus(status) {
  if (status === "current") {
    return "Current Location";
  }

  if (!status) {
    return "Locked";
  }

  return (
    status.charAt(0).toUpperCase()
    + status.slice(1).toLowerCase()
  );
}


function World() {
  const {
    locations,
    isLoading,
    isSaving,
    error,
    saveStarterLocations,
  } = useWorld();

  const displayedLocations =
    locations.length > 0
      ? locations
      : starterLocations;

  function handleSaveStarterLocations() {
    saveStarterLocations(starterLocations);
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>World Map</h1>

        <p>
          Explore discovered locations, unlock hidden regions, and track
          the player’s current position.
        </p>
      </header>

      {isLoading && (
        <p>Loading world locations...</p>
      )}

      {error && (
        <p role="alert">
          Unable to load world: {error}
        </p>
      )}

      {!isLoading
        && locations.length === 0
        && !error && (
          <section className="page-section">
            <p>
              These locations have not been saved to the Atlas
              database yet.
            </p>

            <button
              className="game-button"
              type="button"
              disabled={isSaving}
              onClick={handleSaveStarterLocations}
            >
              {isSaving
                ? "Saving World..."
                : "Save Starter World"}
            </button>
          </section>
        )}

      <section className="game-grid">
        {displayedLocations.map((location) => (
          <article
            className="game-card"
            key={location.id || location.name}
          >
            <h2>{location.name}</h2>

            <p>{location.description}</p>

            <span className="game-tag">
              {formatStatus(location.status)}
            </span>
          </article>
        ))}
      </section>
    </main>
  );
}

export default World;
import { useJournal } from "../hooks/useJournal";
import "../styles/GamePages.css";


const starterEntries = [
  {
    title: "The Journey Begins",
    category: "Story",
    text:
      "I arrived at the Forest Entrance with only a map and a few supplies.",
  },
  {
    title: "A Choice Without Violence",
    category: "Reflection",
    text:
      "Not every enemy must remain an enemy. Observation may reveal another path.",
  },
  {
    title: "Whispers in the Grove",
    category: "Discovery",
    text:
      "The trees react differently when approached with patience.",
  },
];


function Journal() {
  const {
    entries,
    isLoading,
    isSaving,
    error,
    saveStarterEntries,
  } = useJournal();

  const displayedEntries =
    entries.length > 0 ? entries : starterEntries;

  function handleSaveStarterEntries() {
    saveStarterEntries(starterEntries);
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Atlas Journal</h1>

        <p>
          Record discoveries, choices, consequences, emotional
          development, and important moments from the journey.
        </p>
      </header>

      {isLoading && (
        <p>Loading journal...</p>
      )}

      {error && (
        <p role="alert">
          Unable to load journal: {error}
        </p>
      )}

      {!isLoading && entries.length === 0 && !error && (
        <section className="page-section">
          <p>
            These journal entries have not been saved to the Atlas
            database yet.
          </p>

          <button
            className="game-button"
            type="button"
            disabled={isSaving}
            onClick={handleSaveStarterEntries}
          >
            {isSaving
              ? "Saving Journal..."
              : "Save Starter Journal"}
          </button>
        </section>
      )}

      <section className="game-grid">
        {displayedEntries.map((entry) => {
          const entryText = entry.content || entry.text;

          return (
            <article
              className="game-card"
              key={entry.id || entry.title}
            >
              <span className="game-tag">
                {entry.category}
              </span>

              <h2>{entry.title}</h2>

              <p>{entryText}</p>

              {entry.created_at && (
                <p>
                  <small>
                    Recorded: {entry.created_at}
                  </small>
                </p>
              )}
            </article>
          );
        })}
      </section>
    </main>
  );
}

export default Journal;
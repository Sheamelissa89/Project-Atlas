import { useQuests } from "../hooks/useQuests";
import "../styles/GamePages.css";


const starterQuests = [
  {
    title: "Into the Forest",
    status: "Active",
    goal: "Travel beyond the Forest Entrance.",
    rewardGold: 30,
    rewardExperience: 50,
  },
  {
    title: "The Missing Herbalist",
    status: "Active",
    goal: "Find clues near the Whispering Grove.",
    rewardGold: 50,
    rewardExperience: 75,
  },
  {
    title: "A Light in the Darkness",
    status: "Locked",
    goal: "Discover the entrance to the Moonlit Ruins.",
    rewardGold: 100,
    rewardExperience: 150,
  },
];


function formatStatus(status) {
  if (!status) {
    return "Available";
  }

  return (
    status.charAt(0).toUpperCase()
    + status.slice(1).toLowerCase()
  );
}


function Quests() {
  const {
    quests,
    isLoading,
    isSaving,
    error,
    saveStarterQuests,
  } = useQuests();

  const displayedQuests =
    quests.length > 0 ? quests : starterQuests;

  function handleSaveStarterQuests() {
    saveStarterQuests(starterQuests);
  }

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Quests</h1>

        <p>
          Track current objectives, completed missions, important
          discoveries, and future rewards.
        </p>
      </header>

      {isLoading && (
        <p>Loading quests...</p>
      )}

      {error && (
        <p role="alert">
          Unable to load quests: {error}
        </p>
      )}

      {!isLoading && quests.length === 0 && !error && (
        <section className="page-section">
          <p>
            These starter quests have not been saved to the Atlas
            database yet.
          </p>

          <button
            className="game-button"
            type="button"
            disabled={isSaving}
            onClick={handleSaveStarterQuests}
          >
            {isSaving
              ? "Saving Quests..."
              : "Save Starter Quests"}
          </button>
        </section>
      )}

      <section className="game-grid">
        {displayedQuests.map((quest) => {
          const goal =
            quest.description || quest.goal;

          const rewardGold =
            quest.reward_gold ?? quest.rewardGold;

          const rewardExperience =
            quest.reward_experience
            ?? quest.rewardExperience;

          return (
            <article
              className="game-card"
              key={quest.id || quest.title}
            >
              <h2>{quest.title}</h2>

              <p>{goal}</p>

              <span className="game-tag">
                {formatStatus(quest.status)}
              </span>

              {rewardGold !== undefined && (
                <p>
                  <strong>Gold Reward:</strong>{" "}
                  {rewardGold}
                </p>
              )}

              {rewardExperience !== undefined && (
                <p>
                  <strong>XP Reward:</strong>{" "}
                  {rewardExperience}
                </p>
              )}
            </article>
          );
        })}
      </section>
    </main>
  );
}

export default Quests;
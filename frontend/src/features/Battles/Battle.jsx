import "../../styles/GamePages.css";

import ActionButtons from "../../components/ActionButtons.jsx";
import BattleLog from "../../components/BattleLog.jsx";
import EnemyCard from "../../components/EnemyCard.jsx";
import PlayerCard from "../../components/PlayerCard.jsx";
import { useBattle } from "../../hooks/useBattle.js";

function Battle() {
  const {
    battle,
    character,
    isLoading,
    isActing,
    error,
    startBattle,
    performAction,
  } = useBattle();

  if (isLoading) {
    return (
      <main className="game-page">
        <p>Loading battle arena...</p>
      </main>
    );
  }

  const player = {
    name: character?.name || "Shea",
    level: character?.level || 1,
    health: battle?.player_health ?? character?.health ?? 100,
    maxHealth:
      battle?.player_max_health ?? character?.max_health ?? 100,
  };

  const enemy = {
    name: battle?.enemy_name || "Forest Wolf",
    health: battle?.enemy_health ?? 100,
    maxHealth: battle?.enemy_max_health ?? 100,
  };

  const battleMessages = battle?.battle_log || [
    "Begin a battle to enter the arena.",
  ];

  const battleIsFinished =
    battle &&
    ["victory", "defeat", "peace"].includes(battle.status);

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Battle Arena</h1>

        <p>
          Face enemies, choose an action, and follow each turn through the
          battle log.
        </p>
      </header>

      {error && (
        <p>
          <strong>Unable to update battle:</strong> {error}
        </p>
      )}

      {!character && (
        <section className="game-card">
          <h2>Character Required</h2>
          <p>Create a character before entering the battle arena.</p>
        </section>
      )}

      {character && !battle && (
        <section className="game-card">
          <h2>The Forest Wolf Awaits</h2>
          <p>Begin a new battle when you are ready.</p>

          <button
            className="game-button"
            type="button"
            disabled={isActing}
            onClick={startBattle}
          >
            {isActing ? "Starting Battle..." : "Begin Battle"}
          </button>
        </section>
      )}

      {character && battle && (
        <>
          <section className="game-grid">
            <PlayerCard player={player} />
            <EnemyCard enemy={enemy} />
          </section>

          <section className="page-section">
            <p>
              <strong>Status:</strong> {battle.status}
            </p>

            <p>
              <strong>Turn:</strong> {battle.turn_count}
            </p>
          </section>

          {!battleIsFinished && (
            <ActionButtons
              onAction={performAction}
              disabled={isActing}
            />
          )}

          {battleIsFinished && (
            <section className="page-section game-card">
              <h2>Battle Complete</h2>

              <p>
                Final result: <strong>{battle.status}</strong>
              </p>

              <button
                className="game-button"
                type="button"
                disabled={isActing}
                onClick={startBattle}
              >
                {isActing ? "Preparing Battle..." : "Start New Battle"}
              </button>
            </section>
          )}

          <BattleLog messages={battleMessages} />
        </>
      )}
    </main>
  );
}

export default Battle;
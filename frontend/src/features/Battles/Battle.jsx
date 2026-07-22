import "../../styles/GamePages.css";

import ActionButtons from "../../components/ActionButtons.jsx";
import BattleLog from "../../components/BattleLog.jsx";
import EnemyCard from "../../components/EnemyCard.jsx";
import PlayerCard from "../../components/PlayerCard.jsx";

function Battle() {
  const player = {
    name: "Shea",
    level: 1,
    health: 100,
    maxHealth: 100,
  };

  const enemy = {
    name: "Forest Wolf",
    health: 100,
    maxHealth: 100,
  };

  const battleMessages = [
    "The Forest Wolf watches your movements carefully.",
  ];

  return (
    <main className="game-page">
      <header className="game-page-header">
        <h1>Battle Arena</h1>

        <p>
          Face enemies, choose an action, and follow each turn through the
          battle log.
        </p>
      </header>

      <section className="game-grid">
        <PlayerCard player={player} />
        <EnemyCard enemy={enemy} />
      </section>

      <ActionButtons />

      <BattleLog messages={battleMessages} />
    </main>
  );
}

export default Battle;
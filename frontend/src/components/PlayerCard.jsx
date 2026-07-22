import HealthBar from "./HealthBar.jsx";

function PlayerCard({ player }) {
  return (
    <article className="game-card">
      <h2>Player</h2>
      <p>
        {player.name} — Level {player.level}
      </p>

      <HealthBar
        currentHealth={player.health}
        maxHealth={player.maxHealth}
      />
    </article>
  );
}

export default PlayerCard;
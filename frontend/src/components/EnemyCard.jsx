import HealthBar from "./HealthBar.jsx";

function EnemyCard({ enemy }) {
  return (
    <article className="game-card">
      <h2>Enemy</h2>
      <p>{enemy.name}</p>

      <HealthBar
        currentHealth={enemy.health}
        maxHealth={enemy.maxHealth}
      />
    </article>
  );
}

export default EnemyCard;
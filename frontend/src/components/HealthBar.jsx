function HealthBar({ currentHealth, maxHealth }) {
  const percentage = Math.max(
    0,
    Math.min(100, (currentHealth / maxHealth) * 100),
  );

  return (
    <div>
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <p>
        Health: {currentHealth} / {maxHealth}
      </p>
    </div>
  );
}

export default HealthBar;
function ActionButtons({ onAction, disabled = false }) {
  return (
    <section className="page-section game-card">
      <h2>Choose an Action</h2>

      <div className="tag-row">
        <button
          className="game-button"
          type="button"
          disabled={disabled}
          onClick={() => onAction("attack")}
        >
          Attack
        </button>

        <button
          className="game-button"
          type="button"
          disabled={disabled}
          onClick={() => onAction("defend")}
        >
          Defend
        </button>

        <button
          className="game-button"
          type="button"
          disabled={disabled}
          onClick={() => onAction("potion")}
        >
          Use Potion
        </button>

        <button
          className="game-button"
          type="button"
          disabled={disabled}
          onClick={() => onAction("peace")}
        >
          Attempt Peace
        </button>
      </div>
    </section>
  );
}

export default ActionButtons;
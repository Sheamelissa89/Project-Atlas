function ActionButtons() {
  return (
    <section className="page-section game-card">
      <h2>Choose an Action</h2>

      <div className="tag-row">
        <button className="game-button" type="button">
          Attack
        </button>

        <button className="game-button" type="button">
          Defend
        </button>

        <button className="game-button" type="button">
          Use Potion
        </button>

        <button className="game-button" type="button">
          Attempt Peace
        </button>
      </div>
    </section>
  );
}

export default ActionButtons;
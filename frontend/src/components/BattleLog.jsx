function BattleLog({ messages }) {
  return (
    <section className="page-section game-card">
      <h2>Battle Log</h2>

      {messages.map((message, index) => (
        <p key={`${message}-${index}`}>{message}</p>
      ))}
    </section>
  );
}

export default BattleLog;
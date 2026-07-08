function saveGame() {
    const gameData = {
        player: player,
        enemy: enemy
    };

    localStorage.setItem("projectAtlasSave", JSON.stringify(gameData));

    addLog("Game saved successfully.");
}

function loadGame() {
    const savedData = localStorage.getItem("projectAtlasSave");

    if (savedData === null) {
        addLog("No saved game found.");
        return;
    }

    const gameData = JSON.parse(savedData);

    Object.assign(player, gameData.player);
    Object.assign(enemy, gameData.enemy);

    displayPlayer();
    displayEnemy();

    addLog("Game loaded successfully.");
}
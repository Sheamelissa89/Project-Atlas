const player = new Player("Shea");

let enemy = createRandomEnemy();

function startGame() {
    displayPlayer();
    displayEnemy();

    addLog("Welcome to Project Atlas.");
    addLog(`A wild ${enemy.name} appeared!`);
}

document.getElementById("attackButton").addEventListener("click", function () {
    attackEnemy();
});

document.getElementById("healButton").addEventListener("click", function () {
    player.heal(15);
});

document.getElementById("xpButton").addEventListener("click", function () {
    player.gainXP(25);
});

document.getElementById("saveButton").addEventListener("click", function () {
    saveGame();
});

document.getElementById("loadButton").addEventListener("click", function () {
    loadGame();
});

document.getElementById("newEnemyButton").addEventListener("click", function () {
    summonNewEnemy();
});

startGame();
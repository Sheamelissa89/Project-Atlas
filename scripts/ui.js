function displayPlayer() {
    const stats = document.getElementById("playerStats");

    const healthPercent = (player.health / player.maxHealth) * 100;
    const xpPercent = (player.xp / player.xpNeeded) * 100;

    stats.innerHTML = `
        <h3>${player.name}</h3>
        <p>Level: ${player.level}</p>
        <p>Attack Power: ${player.attackPower}</p>
        <p>Gold: ${player.gold}</p>

        <p>Health: ${player.health} / ${player.maxHealth}</p>
        <div class="stat-bar">
            <div class="health-fill" style="width: ${healthPercent}%"></div>
        </div>

        <p>XP: ${player.xp} / ${player.xpNeeded}</p>
        <div class="stat-bar">
            <div class="xp-fill" style="width: ${xpPercent}%"></div>
        </div>
    `;

    displayInventory();
}

function displayEnemy() {
    const enemyStats = document.getElementById("enemyStats");

    const enemyHealthPercent = (enemy.health / enemy.maxHealth) * 100;

    enemyStats.innerHTML = `
        <h3>${enemy.name}</h3>
        <p>Attack Power: ${enemy.attackPower}</p>
        <p>XP Reward: ${enemy.xpReward}</p>
        <p>Gold Reward: ${enemy.goldReward}</p>

        <p>Health: ${enemy.health} / ${enemy.maxHealth}</p>
        <div class="stat-bar">
            <div class="enemy-fill" style="width: ${enemyHealthPercent}%"></div>
        </div>
    `;
}

function displayInventory() {
    const inventoryList = document.getElementById("inventoryList");

    inventoryList.innerHTML = "";

    for (let item of player.inventory) {
        inventoryList.innerHTML += `<li>${item}</li>`;
    }
}

function addLog(message) {
    const battleLog = document.getElementById("battleLog");

    battleLog.innerHTML = `
        <div class="log-message">${message}</div>
        ${battleLog.innerHTML}
    `;
}
function attackEnemy() {
    if (player.health === 0) {
        addLog("You cannot attack. You have been defeated.");
        return;
    }

    if (enemy.health === 0) {
        addLog("This enemy is already defeated. Summon a new enemy.");
        return;
    }

    enemy.health -= player.attackPower;

    if (enemy.health < 0) {
        enemy.health = 0;
    }

    addLog(`${player.name} attacked ${enemy.name} for ${player.attackPower} damage.`);

    if (enemy.health === 0) {
        defeatEnemy();
    } else {
        enemy.attack(player);
    }

    displayPlayer();
    displayEnemy();
}

function defeatEnemy() {
    addLog(`${enemy.name} was defeated!`);

    player.gainXP(enemy.xpReward);
    player.gold += enemy.goldReward;

    addLog(`${player.name} earned ${enemy.goldReward} gold.`);

    const lootChance = Math.random();

    if (lootChance > 0.5) {
        const loot = getRandomLoot();
        addItem(loot);
        addLog(`${enemy.name} dropped ${loot}.`);
    } else {
        addLog(`${enemy.name} dropped no loot.`);
    }

    displayPlayer();
}

function summonNewEnemy() {
    enemy = createRandomEnemy();

    addLog(`A wild ${enemy.name} appeared!`);

    displayEnemy();
}
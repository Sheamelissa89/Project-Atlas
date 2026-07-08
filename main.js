class Player {
    constructor(name) {
        this.name = name;
        this.level = 1;
        this.health = 100;
        this.maxHealth = 100;
        this.xp = 0;
        this.xpNeeded = 100;
        this.attackPower = 20;
        this.inventory = ["Iron Sword", "Wooden Shield", "Health Potion x3", "Mana Potion x2", "Leather Armor", "Boots of Speed", "Ring of Strength", "Amulet of Wisdom", "Cloak of Invisibility", "Fire Staff", "Ice Wand", "Thunder Hammer", "Poison Dagger", "Bow of Accuracy", "Crossbow of Precision", "Helmet of Insight", "Gauntlets of Power", "Greaves of Agility", "Belt of Fortitude", "Bracers of Defense", "Cape of Shadows", "Orb of Magic", "Tome of Knowledge", "Crystal Ball", "Elixir of Life", "Scroll of Teleportation", "Gem of Luck", "Pendant of Protection", "Charm of Courage", "Sigil of the Ancients"];
    }

    attack(enemy) {
        enemy.health -= this.attackPower;

        if (enemy.health < 0) {
            enemy.health = 0;
        }

        addLog(`${this.name} attacked ${enemy.name} for ${this.attackPower} damage.`);

        if (enemy.health === 0) {
            addLog(`${enemy.name} was defeated!`);
            this.gainXP(50);
        } else {
            enemy.attack(this);
        }

        displayPlayer();
        displayEnemy();
    }

    heal(amount) {
        this.health += amount;

        if (this.health > this.maxHealth) {
            this.health = this.maxHealth;
        }

        addLog(`${this.name} healed ${amount} health.`);
        displayPlayer();
    }

    gainXP(amount) {
        this.xp += amount;
        addLog(`${this.name} gained ${amount} XP.`);

        if (this.xp >= this.xpNeeded) {
            this.levelUp();
        }

        displayPlayer();
    }

    levelUp() {
        this.level++;
        this.xp = 0;
        this.xpNeeded += 50;
        this.maxHealth += 20;
        this.health = this.maxHealth;
        this.attackPower += 5;

        addLog(`${this.name} leveled up to Level ${this.level}!`);
    }
}

class Enemy {
    constructor(name, health, attackPower) {
        this.name = name;
        this.health = health;
        this.maxHealth = health;
        this.attackPower = attackPower;
    }

    attack(player) {
        player.health -= this.attackPower;

        if (player.health < 0) {
            player.health = 0;
        }

        addLog(`${this.name} attacked ${player.name} for ${this.attackPower} damage.`);

        if (player.health === 0) {
            addLog(`${player.name} has been defeated.`);
        }
    }
}

const player = new Player("Shea");

let enemy = new Enemy("Goblin", 60, 10);

function displayPlayer() {
    const stats = document.getElementById("playerStats");

    const healthPercent = (player.health / player.maxHealth) * 100;
    const xpPercent = (player.xp / player.xpNeeded) * 100;

    stats.innerHTML = `
        <h3>${player.name}</h3>
        <p>Level: ${player.level}</p>
        <p>Attack Power: ${player.attackPower}</p>

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

function summonNewEnemy() {
    const enemies = [
        new Enemy("Goblin", 60, 10),
        new Enemy("Wolf", 80, 12),
        new Enemy("Skeleton", 100, 15),
        new Enemy("Dark Knight", 140, 20),
        new Enemy("Necromancer", 160, 25),
        new Enemy("Dragon", 200, 30),
        new Enemy("Demon Lord", 400, 80),
        new Enemy("Owl of the Night", 350, 70),
        new Enemy("Slime", 50, 8),
        new Enemy("Orc", 120, 18),
        new Enemy("Troll", 180, 22),
        new Enemy("Forest Snake", 90, 14),
        new Enemy("Vampire", 150, 28),
        new Enemy("Giant Spider", 130, 16),
        
    ];

    const randomIndex = Math.floor(Math.random() * enemies.length);

    enemy = enemies[randomIndex];

    addLog(`A wild ${enemy.name} appeared!`);

    displayEnemy();
}

document.getElementById("attackButton").addEventListener("click", function () {
    if (player.health === 0) {
        addLog("You cannot attack. You have been defeated.");
        return;
    }

    if (enemy.health === 0) {
        addLog("This enemy is already defeated. Summon a new enemy.");
        return;
    }

    player.attack(enemy);
});

document.getElementById("healButton").addEventListener("click", function () {
    if (player.health === 0) {
        addLog("You cannot heal after defeat.");
        return;
    }

    player.heal(15);
});

document.getElementById("xpButton").addEventListener("click", function () {
    player.gainXP(25);
});

document.getElementById("newEnemyButton").addEventListener("click", function () {
    summonNewEnemy();
});

displayPlayer();
displayEnemy();
addLog("Welcome to Project Atlas.");

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

document.getElementById("saveButton").addEventListener("click", saveGame);
document.getElementById("loadButton").addEventListener("click", loadGame);
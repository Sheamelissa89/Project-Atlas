class Enemy {
    constructor(name, health, attackPower, xpReward, goldReward) {
        this.name = name;
        this.health = health;
        this.maxHealth = health;
        this.attackPower = attackPower;
        this.xpReward = xpReward;
        this.goldReward = goldReward;
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

        displayPlayer();
    }
}

const enemyTypes = [
    new Enemy("Goblin", 60, 10, 40, 15),
    new Enemy("Wolf", 80, 12, 45, 20),
    new Enemy("Skeleton", 100, 15, 60, 30),
    new Enemy("Dark Knight", 140, 20, 90, 50),
    new Enemy("Slime", 40, 6, 25, 10),
    new Enemy("Bandit", 90, 14, 55, 25),
    new Enemy("Orc", 120, 18, 75, 40),
    new Enemy("Spider", 70, 11, 35, 18),
    new Enemy("Zombie", 110, 13, 50, 22),
    new Enemy("Fire Imp", 85, 17, 65, 35),
    new Enemy("Ice Wraith", 130, 19, 85, 45),
    new Enemy("Forest Troll", 160, 22, 110, 65),
    new Enemy("Shadow Beast", 180, 25, 130, 80),
    new Enemy("Dragon Whelp", 220, 30, 180, 120)
];

function createRandomEnemy() {
    const randomIndex = Math.floor(Math.random() * enemyTypes.length);
    const selectedEnemy = enemyTypes[randomIndex];

    return new Enemy(
        selectedEnemy.name,
        selectedEnemy.maxHealth,
        selectedEnemy.attackPower,
        selectedEnemy.xpReward,
        selectedEnemy.goldReward
    );
}
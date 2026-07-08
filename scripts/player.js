class Player {
    constructor(name) {
        this.name = name;
        this.level = 1;
        this.health = 100;
        this.maxHealth = 100;
        this.xp = 0;
        this.xpNeeded = 100;
        this.attackPower = 20;
        this.gold = 100;
        this.inventory = startingInventory;
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

        addLog(`LEVEL UP! ${this.name} is now Level ${this.level}.`);
    }

    heal(amount) {
        this.health += amount;

        if (this.health > this.maxHealth) {
            this.health = this.maxHealth;
        }

        addLog(`${this.name} healed ${amount} health.`);
        displayPlayer();
    }
}
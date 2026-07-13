"use strict";

/*
    PROJECT ATLAS
    Main JavaScript File

    This file currently controls:

    1. Player information
    2. Enemy information
    3. Battle actions
    4. Inventory actions
    5. Equipment bonuses
    6. Experience and leveling
    7. Battle log messages
    8. Saving and loading
*/


// ==================================================
// 1. PLAYER CLASS
// ==================================================

class Player {
    constructor(name) {
        this.name = name;

        // Player progression
        this.level = 1;
        this.xp = 0;
        this.xpNeeded = 100;

        // Player health
        this.health = 100;
        this.maxHealth = 100;

        // Base statistics
        this.baseAttackPower = 20;
        this.attackPower = 20;
        this.defense = 0;

        // Player inventory
        this.inventory = createStartingInventory();
    }

    attack(enemyTarget) {
        if (this.health === 0) {
            addLog(
                `${this.name} cannot attack after being defeated.`,
                "warning"
            );

            return;
        }

        if (enemyTarget.health === 0) {
            addLog(
                `${enemyTarget.name} has already been defeated. Summon a new enemy.`,
                "warning"
            );

            return;
        }

        enemyTarget.health -= this.attackPower;

        if (enemyTarget.health < 0) {
            enemyTarget.health = 0;
        }

        addLog(
            `${this.name} attacked ${enemyTarget.name} for ` +
            `${this.attackPower} damage.`,
            "player"
        );

        if (enemyTarget.health === 0) {
            addLog(
                `${enemyTarget.name} was defeated!`,
                "victory"
            );

            this.gainXP(enemyTarget.xpReward);
        } else {
            enemyTarget.attack(this);
        }

        displayPlayer();
        displayEnemy();
    }

    heal(amount) {
        if (this.health === 0) {
            addLog(
                `${this.name} cannot recover after being defeated.`,
                "warning"
            );

            return;
        }

        if (this.health === this.maxHealth) {
            addLog(
                `${this.name} already has full health.`,
                "warning"
            );

            return;
        }

        const healthBeforeHealing = this.health;

        this.health = Math.min(
            this.maxHealth,
            this.health + amount
        );

        const actualHealing = this.health - healthBeforeHealing;

        addLog(
            `${this.name} recovered ${actualHealing} health.`,
            "healing"
        );

        displayPlayer();
    }

    gainXP(amount) {
        this.xp += amount;

        addLog(
            `${this.name} gained ${amount} XP.`,
            "xp"
        );

        while (this.xp >= this.xpNeeded) {
            this.levelUp();
        }

        displayPlayer();
    }

    levelUp() {
        this.xp -= this.xpNeeded;
        this.level++;
        this.xpNeeded += 50;

        this.maxHealth += 20;
        this.health = this.maxHealth;

        this.baseAttackPower += 5;

        this.updateEquipmentStats();

        addLog(
            `${this.name} advanced to Level ${this.level}!`,
            "level-up"
        );

        addLog(
            `${this.name}'s health and attack power increased.`,
            "level-up"
        );
    }

    useItem(itemId) {
        const item = this.inventory.find(
            inventoryItem => inventoryItem.id === itemId
        );

        if (!item) {
            addLog(
                "That item could not be found.",
                "warning"
            );

            return;
        }

        if (item.type !== "consumable") {
            addLog(
                `${item.name} cannot be consumed.`,
                "warning"
            );

            return;
        }

        if (this.health === 0) {
            addLog(
                `${this.name} cannot use an item after being defeated.`,
                "warning"
            );

            return;
        }

        if (item.healAmount) {
            if (this.health === this.maxHealth) {
                addLog(
                    `${this.name} already has full health.`,
                    "warning"
                );

                return;
            }

            const healthBeforeHealing = this.health;

            this.health = Math.min(
                this.maxHealth,
                this.health + item.healAmount
            );

            const actualHealing =
                this.health - healthBeforeHealing;

            addLog(
                `${this.name} used ${item.name} and recovered ` +
                `${actualHealing} health.`,
                "healing"
            );
        } else {
            addLog(
                `${item.name} does not have an active effect yet.`,
                "warning"
            );

            return;
        }

        item.quantity--;

        if (item.quantity <= 0) {
            this.inventory = this.inventory.filter(
                inventoryItem => inventoryItem.id !== itemId
            );

            addLog(
                `${item.name} has been removed from the inventory.`,
                "inventory"
            );
        }

        displayPlayer();
    }

    equipItem(itemId) {
        const item = this.inventory.find(
            inventoryItem => inventoryItem.id === itemId
        );

        if (!item) {
            addLog(
                "That item could not be found.",
                "warning"
            );

            return;
        }

        const equippableTypes = [
            "weapon",
            "armor",
            "shield",
            "helmet",
            "boots",
            "gloves",
            "accessory",
            "cloak"
        ];

        if (!equippableTypes.includes(item.type)) {
            addLog(
                `${item.name} cannot be equipped.`,
                "warning"
            );

            return;
        }

        if (item.equipped) {
            addLog(
                `${item.name} is already equipped.`,
                "warning"
            );

            return;
        }

        /*
            Only one item from each equipment type may be
            equipped at a time.

            Example:
            Equipping a new weapon automatically removes the
            currently equipped weapon.
        */

        for (const inventoryItem of this.inventory) {
            if (
                inventoryItem.type === item.type &&
                inventoryItem.equipped
            ) {
                inventoryItem.equipped = false;

                addLog(
                    `${inventoryItem.name} was unequipped.`,
                    "inventory"
                );
            }
        }

        item.equipped = true;

        this.updateEquipmentStats();

        addLog(
            `${this.name} equipped ${item.name}.`,
            "equipment"
        );

        displayPlayer();
    }

    unequipItem(itemId) {
        const item = this.inventory.find(
            inventoryItem => inventoryItem.id === itemId
        );

        if (!item) {
            addLog(
                "That item could not be found.",
                "warning"
            );

            return;
        }

        if (!item.equipped) {
            addLog(
                `${item.name} is not currently equipped.`,
                "warning"
            );

            return;
        }

        item.equipped = false;

        this.updateEquipmentStats();

        addLog(
            `${this.name} unequipped ${item.name}.`,
            "inventory"
        );

        displayPlayer();
    }

    dropItem(itemId) {
        const item = this.inventory.find(
            inventoryItem => inventoryItem.id === itemId
        );

        if (!item) {
            addLog(
                "That item could not be found.",
                "warning"
            );

            return;
        }

        if (item.type === "quest") {
            addLog(
                `${item.name} is an important quest item and ` +
                "cannot be dropped.",
                "warning"
            );

            return;
        }

        if (item.equipped) {
            item.equipped = false;
        }

        this.inventory = this.inventory.filter(
            inventoryItem => inventoryItem.id !== itemId
        );

        this.updateEquipmentStats();

        addLog(
            `${this.name} dropped ${item.name}.`,
            "inventory"
        );

        displayPlayer();
    }

    updateEquipmentStats() {
        let attackBonus = 0;
        let defenseBonus = 0;

        for (const item of this.inventory) {
            if (!item.equipped) {
                continue;
            }

            attackBonus += item.attackBonus || 0;
            defenseBonus += item.defenseBonus || 0;
        }

        this.attackPower =
            this.baseAttackPower + attackBonus;

        this.defense = defenseBonus;
    }
}


// ==================================================
// 2. ENEMY CLASS
// ==================================================

class Enemy {
    constructor(
        name,
        health,
        attackPower,
        xpReward = 50
    ) {
        this.name = name;
        this.health = health;
        this.maxHealth = health;
        this.attackPower = attackPower;
        this.xpReward = xpReward;
    }

    attack(playerTarget) {
        const damageTaken = Math.max(
            1,
            this.attackPower - playerTarget.defense
        );

        const blockedDamage =
            this.attackPower - damageTaken;

        playerTarget.health -= damageTaken;

        if (playerTarget.health < 0) {
            playerTarget.health = 0;
        }

        addLog(
            `${this.name} attacked ${playerTarget.name} for ` +
            `${damageTaken} damage.`,
            "enemy"
        );

        if (blockedDamage > 0) {
            addLog(
                `${playerTarget.name}'s equipment blocked ` +
                `${blockedDamage} damage.`,
                "defense"
            );
        }

        if (playerTarget.health === 0) {
            addLog(
                `${playerTarget.name} has been defeated.`,
                "defeat"
            );
        }
    }
}


// ==================================================
// 3. STARTING INVENTORY
// ==================================================

function createStartingInventory() {
    return [
        {
            id: 1,
            name: "Iron Sword",
            type: "weapon",
            quantity: 1,
            attackBonus: 10,
            defenseBonus: 0,
            equipped: false,
            description:
                "A dependable iron blade that adds 10 attack."
        },
        {
            id: 2,
            name: "Wooden Shield",
            type: "shield",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 5,
            equipped: false,
            description:
                "A simple shield that adds 5 defense."
        },
        {
            id: 3,
            name: "Health Potion",
            type: "consumable",
            quantity: 3,
            healAmount: 30,
            equipped: false,
            description:
                "Restores up to 30 health."
        },
        {
            id: 4,
            name: "Mana Potion",
            type: "consumable",
            quantity: 2,
            equipped: false,
            description:
                "A magical potion awaiting the future mana system."
        },
        {
            id: 5,
            name: "Leather Armor",
            type: "armor",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 8,
            equipped: false,
            description:
                "Light armor that adds 8 defense."
        },
        {
            id: 6,
            name: "Boots of Speed",
            type: "boots",
            quantity: 1,
            attackBonus: 2,
            defenseBonus: 2,
            equipped: false,
            description:
                "Agile boots that add 2 attack and 2 defense."
        },
        {
            id: 7,
            name: "Ring of Strength",
            type: "accessory",
            quantity: 1,
            attackBonus: 5,
            defenseBonus: 0,
            equipped: false,
            description:
                "A powerful ring that adds 5 attack."
        },
        {
            id: 8,
            name: "Amulet of Wisdom",
            type: "accessory",
            quantity: 1,
            attackBonus: 2,
            defenseBonus: 3,
            equipped: false,
            description:
                "An enchanted amulet that adds 2 attack and 3 defense."
        },
        {
            id: 9,
            name: "Cloak of Invisibility",
            type: "cloak",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 7,
            equipped: false,
            description:
                "A mysterious cloak that adds 7 defense."
        },
        {
            id: 10,
            name: "Fire Staff",
            type: "weapon",
            quantity: 1,
            attackBonus: 18,
            defenseBonus: 0,
            equipped: false,
            description:
                "A magical staff that adds 18 attack."
        },
        {
            id: 11,
            name: "Ice Wand",
            type: "weapon",
            quantity: 1,
            attackBonus: 15,
            defenseBonus: 2,
            equipped: false,
            description:
                "A frozen wand that adds 15 attack and 2 defense."
        },
        {
            id: 12,
            name: "Thunder Hammer",
            type: "weapon",
            quantity: 1,
            attackBonus: 22,
            defenseBonus: 0,
            equipped: false,
            description:
                "A heavy hammer that adds 22 attack."
        },
        {
            id: 13,
            name: "Poison Dagger",
            type: "weapon",
            quantity: 1,
            attackBonus: 12,
            defenseBonus: 0,
            equipped: false,
            description:
                "A swift dagger that adds 12 attack."
        },
        {
            id: 14,
            name: "Bow of Accuracy",
            type: "weapon",
            quantity: 1,
            attackBonus: 14,
            defenseBonus: 0,
            equipped: false,
            description:
                "A precise bow that adds 14 attack."
        },
        {
            id: 15,
            name: "Crossbow of Precision",
            type: "weapon",
            quantity: 1,
            attackBonus: 16,
            defenseBonus: 0,
            equipped: false,
            description:
                "A mechanical crossbow that adds 16 attack."
        },
        {
            id: 16,
            name: "Helmet of Insight",
            type: "helmet",
            quantity: 1,
            attackBonus: 1,
            defenseBonus: 4,
            equipped: false,
            description:
                "A thoughtful helmet that adds 1 attack and 4 defense."
        },
        {
            id: 17,
            name: "Gauntlets of Power",
            type: "gloves",
            quantity: 1,
            attackBonus: 6,
            defenseBonus: 2,
            equipped: false,
            description:
                "Reinforced gauntlets that add 6 attack and 2 defense."
        },
        {
            id: 18,
            name: "Greaves of Agility",
            type: "boots",
            quantity: 1,
            attackBonus: 3,
            defenseBonus: 4,
            equipped: false,
            description:
                "Flexible greaves that add 3 attack and 4 defense."
        },
        {
            id: 19,
            name: "Belt of Fortitude",
            type: "accessory",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 6,
            equipped: false,
            description:
                "A fortified belt that adds 6 defense."
        },
        {
            id: 20,
            name: "Bracers of Defense",
            type: "gloves",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 7,
            equipped: false,
            description:
                "Protective bracers that add 7 defense."
        },
        {
            id: 21,
            name: "Cape of Shadows",
            type: "cloak",
            quantity: 1,
            attackBonus: 4,
            defenseBonus: 5,
            equipped: false,
            description:
                "A shadowed cape that adds 4 attack and 5 defense."
        },
        {
            id: 22,
            name: "Orb of Magic",
            type: "artifact",
            quantity: 1,
            equipped: false,
            description:
                "A magical artifact reserved for a future spell system."
        },
        {
            id: 23,
            name: "Tome of Knowledge",
            type: "artifact",
            quantity: 1,
            equipped: false,
            description:
                "A mysterious book reserved for future skill upgrades."
        },
        {
            id: 24,
            name: "Crystal Ball",
            type: "artifact",
            quantity: 1,
            equipped: false,
            description:
                "A crystal that may reveal future paths."
        },
        {
            id: 25,
            name: "Elixir of Life",
            type: "consumable",
            quantity: 1,
            healAmount: 100,
            equipped: false,
            description:
                "Restores up to 100 health."
        },
        {
            id: 26,
            name: "Scroll of Teleportation",
            type: "consumable",
            quantity: 1,
            equipped: false,
            description:
                "A scroll reserved for the future world map."
        },
        {
            id: 27,
            name: "Gem of Luck",
            type: "artifact",
            quantity: 1,
            equipped: false,
            description:
                "A rare gem reserved for the future luck system."
        },
        {
            id: 28,
            name: "Pendant of Protection",
            type: "accessory",
            quantity: 1,
            attackBonus: 0,
            defenseBonus: 8,
            equipped: false,
            description:
                "A protective pendant that adds 8 defense."
        },
        {
            id: 29,
            name: "Charm of Courage",
            type: "accessory",
            quantity: 1,
            attackBonus: 4,
            defenseBonus: 4,
            equipped: false,
            description:
                "A courageous charm that adds 4 attack and 4 defense."
        },
        {
            id: 30,
            name: "Sigil of the Ancients",
            type: "quest",
            quantity: 1,
            equipped: false,
            description:
                "An ancient quest item that cannot be dropped."
        }
    ];
}


// ==================================================
// 4. PLAYER AND ENEMY CREATION
// ==================================================

const player = new Player("Shea");

let enemy = new Enemy(
    "Goblin",
    60,
    10,
    50
);


// ==================================================
// 5. PLAYER DISPLAY
// ==================================================

function displayPlayer() {
    const stats =
        document.getElementById("playerStats");

    if (!stats) {
        return;
    }

    const healthPercent = calculatePercent(
        player.health,
        player.maxHealth
    );

    const xpPercent = calculatePercent(
        player.xp,
        player.xpNeeded
    );

    const equippedItems = player.inventory.filter(
        item => item.equipped
    );

    const equippedNames = equippedItems.length > 0
        ? equippedItems
            .map(item => item.name)
            .join(", ")
        : "None";

    stats.innerHTML = `
        <div class="character-name-row">
            <h3>${escapeHTML(player.name)}</h3>

            <span class="level-badge">
                Level ${player.level}
            </span>
        </div>

        <div class="stat-number-grid">
            <div class="stat-number-card">
                <span class="stat-number-label">
                    Attack
                </span>

                <strong>
                    ${player.attackPower}
                </strong>
            </div>

            <div class="stat-number-card">
                <span class="stat-number-label">
                    Defense
                </span>

                <strong>
                    ${player.defense}
                </strong>
            </div>
        </div>

        <div class="bar-group">
            <div class="bar-label-row">
                <span>Health</span>

                <span>
                    ${player.health} / ${player.maxHealth}
                </span>
            </div>

            <div
                class="stat-bar"
                role="progressbar"
                aria-valuemin="0"
                aria-valuemax="${player.maxHealth}"
                aria-valuenow="${player.health}"
            >
                <div
                    class="stat-fill health-fill"
                    style="width: ${healthPercent}%"
                ></div>
            </div>
        </div>

        <div class="bar-group">
            <div class="bar-label-row">
                <span>Experience</span>

                <span>
                    ${player.xp} / ${player.xpNeeded}
                </span>
            </div>

            <div
                class="stat-bar"
                role="progressbar"
                aria-valuemin="0"
                aria-valuemax="${player.xpNeeded}"
                aria-valuenow="${player.xp}"
            >
                <div
                    class="stat-fill xp-fill"
                    style="width: ${xpPercent}%"
                ></div>
            </div>
        </div>

        <div class="equipped-summary">
            <span>Equipped:</span>

            <p>${escapeHTML(equippedNames)}</p>
        </div>
    `;

    displayInventory();
}


// ==================================================
// 6. ENEMY DISPLAY
// ==================================================

function displayEnemy() {
    const enemyStats =
        document.getElementById("enemyStats");

    const statusBadge =
        document.getElementById("enemyStatusBadge");

    if (!enemyStats) {
        return;
    }

    const enemyHealthPercent = calculatePercent(
        enemy.health,
        enemy.maxHealth
    );

    const isDefeated = enemy.health === 0;

    enemyStats.innerHTML = `
        <div class="character-name-row">
            <h3>${escapeHTML(enemy.name)}</h3>

            <span class="enemy-reward">
                ${enemy.xpReward} XP
            </span>
        </div>

        <div class="stat-number-grid">
            <div class="stat-number-card">
                <span class="stat-number-label">
                    Attack
                </span>

                <strong>
                    ${enemy.attackPower}
                </strong>
            </div>

            <div class="stat-number-card">
                <span class="stat-number-label">
                    Status
                </span>

                <strong>
                    ${isDefeated ? "Defeated" : "Hostile"}
                </strong>
            </div>
        </div>

        <div class="bar-group">
            <div class="bar-label-row">
                <span>Health</span>

                <span>
                    ${enemy.health} / ${enemy.maxHealth}
                </span>
            </div>

            <div
                class="stat-bar"
                role="progressbar"
                aria-valuemin="0"
                aria-valuemax="${enemy.maxHealth}"
                aria-valuenow="${enemy.health}"
            >
                <div
                    class="stat-fill enemy-fill"
                    style="width: ${enemyHealthPercent}%"
                ></div>
            </div>
        </div>

        <div class="enemy-message">
            ${
                isDefeated
                    ? `${escapeHTML(enemy.name)} has fallen.`
                    : `${escapeHTML(enemy.name)} stands in your path.`
            }
        </div>
    `;

    if (statusBadge) {
        statusBadge.textContent =
            isDefeated ? "Defeated" : "Hostile";

        statusBadge.classList.toggle(
            "defeated-badge",
            isDefeated
        );
    }
}


// ==================================================
// 7. INVENTORY DISPLAY
// ==================================================

function displayInventory() {
    const inventoryList =
        document.getElementById("inventoryList");

    const inventoryCount =
        document.getElementById("inventoryCount");

    if (!inventoryList) {
        return;
    }

    inventoryList.innerHTML = "";

    if (inventoryCount) {
        const totalQuantity = player.inventory.reduce(
            (total, item) => total + item.quantity,
            0
        );

        inventoryCount.textContent =
            `${totalQuantity} total items`;
    }

    if (player.inventory.length === 0) {
        inventoryList.innerHTML = `
            <li class="empty-inventory">
                <strong>Your inventory is empty.</strong>

                <p>
                    Future victories may provide new equipment
                    and supplies.
                </p>
            </li>
        `;

        return;
    }

    for (const item of player.inventory) {
        const itemElement =
            document.createElement("li");

        itemElement.className = "inventory-item";

        itemElement.dataset.itemType = item.type;

        if (item.equipped) {
            itemElement.classList.add("equipped-item");
        }

        const statDescription =
            createItemStatDescription(item);

        itemElement.innerHTML = `
            <div class="item-information">
                <div class="item-heading">
                    <div>
                        <span class="item-type">
                            ${capitalizeWord(item.type)}
                        </span>

                        <h3>${escapeHTML(item.name)}</h3>
                    </div>

                    <span class="item-quantity">
                        x${item.quantity}
                    </span>
                </div>

                <p class="item-description">
                    ${escapeHTML(item.description)}
                </p>

                ${
                    statDescription
                        ? `
                            <p class="item-stat-description">
                                ${statDescription}
                            </p>
                        `
                        : ""
                }

                ${
                    item.equipped
                        ? `
                            <span class="equipped-label">
                                Equipped
                            </span>
                        `
                        : ""
                }
            </div>

            <div class="inventory-actions">
                ${createInventoryButtons(item)}
            </div>
        `;

        inventoryList.appendChild(itemElement);
    }
}


// ==================================================
// 8. INVENTORY BUTTON CREATION
// ==================================================

function createInventoryButtons(item) {
    if (item.type === "consumable") {
        return `
            <button
                class="inventory-button use-item-button"
                data-item-id="${item.id}"
                type="button"
            >
                Use
            </button>

            <button
                class="inventory-button drop-item-button"
                data-item-id="${item.id}"
                type="button"
            >
                Drop
            </button>
        `;
    }

    if (item.type === "quest") {
        return `
            <button
                class="inventory-button protected-item-button"
                type="button"
                disabled
            >
                Protected
            </button>
        `;
    }

    const equippableTypes = [
        "weapon",
        "armor",
        "shield",
        "helmet",
        "boots",
        "gloves",
        "accessory",
        "cloak"
    ];

    if (equippableTypes.includes(item.type)) {
        if (item.equipped) {
            return `
                <button
                    class="inventory-button unequip-item-button"
                    data-item-id="${item.id}"
                    type="button"
                >
                    Unequip
                </button>

                <button
                    class="inventory-button drop-item-button"
                    data-item-id="${item.id}"
                    type="button"
                >
                    Drop
                </button>
            `;
        }

        return `
            <button
                class="inventory-button equip-item-button"
                data-item-id="${item.id}"
                type="button"
            >
                Equip
            </button>

            <button
                class="inventory-button drop-item-button"
                data-item-id="${item.id}"
                type="button"
            >
                Drop
            </button>
        `;
    }

    return `
        <button
            class="inventory-button future-item-button"
            type="button"
            disabled
        >
            Future Item
        </button>

        <button
            class="inventory-button drop-item-button"
            data-item-id="${item.id}"
            type="button"
        >
            Drop
        </button>
    `;
}


// ==================================================
// 9. ITEM INFORMATION
// ==================================================

function createItemStatDescription(item) {
    const statParts = [];

    if (item.attackBonus) {
        statParts.push(
            `+${item.attackBonus} Attack`
        );
    }

    if (item.defenseBonus) {
        statParts.push(
            `+${item.defenseBonus} Defense`
        );
    }

    if (item.healAmount) {
        statParts.push(
            `Restores ${item.healAmount} Health`
        );
    }

    return statParts.join(" • ");
}


// ==================================================
// 10. BATTLE LOG
// ==================================================

function addLog(message, messageType = "normal") {
    const battleLog =
        document.getElementById("battleLog");

    if (!battleLog) {
        return;
    }

    const logMessage =
        document.createElement("div");

    logMessage.className =
        `log-message log-${messageType}`;

    logMessage.textContent = message;

    battleLog.prepend(logMessage);

    /*
        Keep the battle log from growing forever.
        Only the newest 50 messages remain visible.
    */

    while (battleLog.children.length > 50) {
        battleLog.removeChild(
            battleLog.lastElementChild
        );
    }
}

function clearBattleLog() {
    const battleLog =
        document.getElementById("battleLog");

    if (!battleLog) {
        return;
    }

    battleLog.innerHTML = "";

    addLog(
        "The battle log was cleared.",
        "normal"
    );
}


// ==================================================
// 11. ENEMY CREATION
// ==================================================

function summonNewEnemy() {
    const enemyTemplates = [
        {
            name: "Goblin",
            health: 60,
            attackPower: 10,
            xpReward: 50
        },
        {
            name: "Wolf",
            health: 80,
            attackPower: 12,
            xpReward: 65
        },
        {
            name: "Skeleton",
            health: 100,
            attackPower: 15,
            xpReward: 80
        },
        {
            name: "Dark Knight",
            health: 140,
            attackPower: 20,
            xpReward: 120
        },
        {
            name: "Necromancer",
            health: 160,
            attackPower: 25,
            xpReward: 150
        },
        {
            name: "Dragon",
            health: 200,
            attackPower: 30,
            xpReward: 200
        },
        {
            name: "Demon Lord",
            health: 400,
            attackPower: 80,
            xpReward: 500
        },
        {
            name: "Owl of the Night",
            health: 350,
            attackPower: 70,
            xpReward: 450
        },
        {
            name: "Slime",
            health: 50,
            attackPower: 8,
            xpReward: 35
        },
        {
            name: "Orc",
            health: 120,
            attackPower: 18,
            xpReward: 100
        },
        {
            name: "Troll",
            health: 180,
            attackPower: 22,
            xpReward: 160
        },
        {
            name: "Forest Snake",
            health: 90,
            attackPower: 14,
            xpReward: 75
        },
        {
            name: "Vampire",
            health: 150,
            attackPower: 28,
            xpReward: 175
        },
        {
            name: "Giant Spider",
            health: 130,
            attackPower: 16,
            xpReward: 110
        }
    ];

    const randomIndex = Math.floor(
        Math.random() * enemyTemplates.length
    );

    const selectedEnemy =
        enemyTemplates[randomIndex];

    enemy = new Enemy(
        selectedEnemy.name,
        selectedEnemy.health,
        selectedEnemy.attackPower,
        selectedEnemy.xpReward
    );

    addLog(
        `A wild ${enemy.name} appeared!`,
        "enemy"
    );

    displayEnemy();
}


// ==================================================
// 12. SAVE AND LOAD
// ==================================================

function saveGame() {
    const gameData = {
        player: {
            name: player.name,
            level: player.level,
            xp: player.xp,
            xpNeeded: player.xpNeeded,
            health: player.health,
            maxHealth: player.maxHealth,
            baseAttackPower: player.baseAttackPower,
            attackPower: player.attackPower,
            defense: player.defense,
            inventory: player.inventory
        },

        enemy: {
            name: enemy.name,
            health: enemy.health,
            maxHealth: enemy.maxHealth,
            attackPower: enemy.attackPower,
            xpReward: enemy.xpReward
        }
    };

    localStorage.setItem(
        "projectAtlasSave",
        JSON.stringify(gameData)
    );

    addLog(
        "Game saved successfully.",
        "save"
    );
}

function loadGame() {
    const savedData =
        localStorage.getItem("projectAtlasSave");

    if (savedData === null) {
        addLog(
            "No saved game was found.",
            "warning"
        );

        return;
    }

    try {
        const gameData =
            JSON.parse(savedData);

        Object.assign(
            player,
            gameData.player
        );

        /*
            Older saved games may not contain these properties.
            These checks prevent errors when loading an older save.
        */

        if (!player.baseAttackPower) {
            player.baseAttackPower = 20;
        }

        if (!Array.isArray(player.inventory)) {
            player.inventory =
                createStartingInventory();
        }

        enemy = new Enemy(
            gameData.enemy.name,
            gameData.enemy.maxHealth,
            gameData.enemy.attackPower,
            gameData.enemy.xpReward
        );

        enemy.health =
            gameData.enemy.health;

        player.updateEquipmentStats();

        displayPlayer();
        displayEnemy();

        addLog(
            "Game loaded successfully.",
            "save"
        );
    } catch (error) {
        console.error(
            "Unable to load Project Atlas:",
            error
        );

        addLog(
            "The saved game could not be loaded.",
            "warning"
        );
    }
}


// ==================================================
// 13. HELPER FUNCTIONS
// ==================================================

function calculatePercent(current, maximum) {
    if (maximum <= 0) {
        return 0;
    }

    const percent =
        (current / maximum) * 100;

    return Math.max(
        0,
        Math.min(100, percent)
    );
}

function capitalizeWord(word) {
    if (!word) {
        return "";
    }

    return (
        word.charAt(0).toUpperCase() +
        word.slice(1)
    );
}

function escapeHTML(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ==================================================
// 14. BUTTON EVENT LISTENERS
// ==================================================

document
    .getElementById("attackButton")
    .addEventListener("click", function () {
        player.attack(enemy);
    });

document
    .getElementById("healButton")
    .addEventListener("click", function () {
        player.heal(15);
    });

document
    .getElementById("xpButton")
    .addEventListener("click", function () {
        player.gainXP(25);
    });

document
    .getElementById("newEnemyButton")
    .addEventListener("click", function () {
        summonNewEnemy();
    });

document
    .getElementById("saveButton")
    .addEventListener("click", function () {
        saveGame();
    });

document
    .getElementById("loadButton")
    .addEventListener("click", function () {
        loadGame();
    });

document
    .getElementById("clearLogButton")
    .addEventListener("click", function () {
        clearBattleLog();
    });


// ==================================================
// 15. INVENTORY EVENT LISTENER
// ==================================================

document
    .getElementById("inventoryList")
    .addEventListener("click", function (event) {
        const button =
            event.target.closest("button");

        if (!button) {
            return;
        }

        const itemId =
            Number(button.dataset.itemId);

        if (
            button.classList.contains(
                "use-item-button"
            )
        ) {
            player.useItem(itemId);
        }

        if (
            button.classList.contains(
                "equip-item-button"
            )
        ) {
            player.equipItem(itemId);
        }

        if (
            button.classList.contains(
                "unequip-item-button"
            )
        ) {
            player.unequipItem(itemId);
        }

        if (
            button.classList.contains(
                "drop-item-button"
            )
        ) {
            player.dropItem(itemId);
        }
    });


// ==================================================
// 16. START THE GAME
// ==================================================

displayPlayer();
displayEnemy();

addLog(
    "Welcome to Project Atlas.",
    "welcome"
);

addLog(
    "Equip an item or begin the battle.",
    "normal"
);
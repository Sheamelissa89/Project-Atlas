const startingInventory = [
    "Iron Sword",
    "Wooden Shield",
    "Health Potion x3",
    "Leather Boots",
    "Silver Ring",
    "Torch",
    "Map Fragment",
    "Small Dagger",
    "Mana Crystal",
    "Hunter Bow",
    "Steel Helmet",
    "Chainmail Vest",
    "Magic Scroll",
    "Ancient Coin",
    "Ruby Gem",
    "Emerald Gem",
    "Dragon Scale",
    "Healing Herb",
    "Mystery Key",
    "Traveler Cloak"
];

const lootTable = [
    "Gold Coin",
    "Rusty Blade",
    "Wolf Fang",
    "Bone Shard",
    "Shadow Essence",
    "Potion",
    "Rare Gem",
    "Ancient Relic"
];

function addItem(item) {
    player.inventory.push(item);
    addLog(`${item} was added to inventory.`);
    displayInventory();
}

function getRandomLoot() {
    const randomIndex = Math.floor(Math.random() * lootTable.length);
    return lootTable[randomIndex];
}
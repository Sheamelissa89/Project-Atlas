import { useCallback, useEffect, useState } from "react";

import {
  createBattle,
  getBattles,
  updateBattle,
} from "../services/battleService";
import { getCharacters } from "../services/characterService";

export function useBattle() {
  const [battle, setBattle] = useState(null);
  const [character, setCharacter] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isActing, setIsActing] = useState(false);
  const [error, setError] = useState("");

  const loadBattle = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const currentCharacter = characters[0];

      if (!currentCharacter) {
        setCharacter(null);
        setBattle(null);
        return;
      }

      setCharacter(currentCharacter);

      const battles = await getBattles(currentCharacter.id);
      const activeBattle = battles.find(
        (savedBattle) => savedBattle.status === "active",
      );

      setBattle(activeBattle || battles[0] || null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBattle();
  }, [loadBattle]);

  async function startBattle() {
    if (!character) {
      setError("Create a character before beginning a battle.");
      return;
    }

    setIsActing(true);
    setError("");

    try {
      const newBattle = await createBattle({
        character_id: character.id,
        enemy_name: "Forest Wolf",
        player_health: character.health,
        player_max_health: character.max_health,
        enemy_health: 100,
        enemy_max_health: 100,
        status: "active",
        turn_count: 0,
        battle_log: [
          "The Forest Wolf watches your movements carefully.",
        ],
      });

      setBattle(newBattle);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsActing(false);
    }
  }

  async function performAction(action) {
    if (!battle || battle.status !== "active") {
      return;
    }

    setIsActing(true);
    setError("");

    let playerHealth = battle.player_health;
    let enemyHealth = battle.enemy_health;
    let status = battle.status;
    const messages = [...(battle.battle_log || [])];

    if (action === "attack") {
      enemyHealth = Math.max(0, enemyHealth - 18);
      messages.push("Shea attacks the Forest Wolf for 18 damage.");

      if (enemyHealth > 0) {
        playerHealth = Math.max(0, playerHealth - 10);
        messages.push("The Forest Wolf retaliates for 10 damage.");
      }
    }

    if (action === "defend") {
      playerHealth = Math.max(0, playerHealth - 4);
      messages.push(
        "Shea takes a defensive stance and receives only 4 damage.",
      );
    }

    if (action === "potion") {
      const previousHealth = playerHealth;
      playerHealth = Math.min(
        battle.player_max_health,
        playerHealth + 25,
      );
      const restoredHealth = playerHealth - previousHealth;

      messages.push(
        `Shea uses a potion and restores ${restoredHealth} health.`,
      );

      playerHealth = Math.max(0, playerHealth - 8);
      messages.push("The Forest Wolf attacks for 8 damage.");
    }

    if (action === "peace") {
      const peaceSucceeded = Math.random() < 0.45;

      if (peaceSucceeded) {
        status = "peace";
        messages.push(
          "Shea lowers their weapon. The Forest Wolf accepts the peaceful gesture.",
        );
      } else {
        playerHealth = Math.max(0, playerHealth - 6);
        messages.push(
          "The Forest Wolf rejects the peaceful gesture and attacks for 6 damage.",
        );
      }
    }

    if (enemyHealth === 0) {
      status = "victory";
      messages.push("The Forest Wolf is defeated. Shea is victorious.");
    } else if (playerHealth === 0) {
      status = "defeat";
      messages.push("Shea can no longer fight. The battle is lost.");
    }

    try {
      const updatedBattle = await updateBattle(battle.id, {
        player_health: playerHealth,
        enemy_health: enemyHealth,
        status,
        turn_count: battle.turn_count + 1,
        battle_log: messages,
      });

      setBattle(updatedBattle);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsActing(false);
    }
  }

  return {
    battle,
    character,
    isLoading,
    isActing,
    error,
    startBattle,
    performAction,
    reloadBattle: loadBattle,
  };
}
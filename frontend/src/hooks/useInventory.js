import { useCallback, useEffect, useState } from "react";

import { getCharacters } from "../services/characterService";
import {
  createInventoryItem,
  deleteInventoryItem,
  getInventory,
  updateInventoryItem,
} from "../services/inventoryService";


export function useInventory() {
  const [items, setItems] = useState([]);
  const [characterId, setCharacterId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const loadInventory = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const activeCharacter = characters[0];

      if (!activeCharacter) {
        setCharacterId(null);
        setItems([]);
        setError(
          "Create a character before loading inventory.",
        );
        return;
      }

      setCharacterId(activeCharacter.id);

      const savedItems = await getInventory(
        activeCharacter.id,
      );

      setItems(savedItems);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInventory();
  }, [loadInventory]);

  async function saveStarterItems(starterItems) {
    if (!characterId) {
      setError(
        "A saved character is required before adding inventory.",
      );
      return;
    }

    if (items.length > 0) {
      setError(
        "Starter inventory can only be added when inventory is empty.",
      );
      return;
    }

    setIsSaving(true);
    setError("");

    try {
      const savedItems = await Promise.all(
        starterItems.map((item) =>
          createInventoryItem({
            character_id: characterId,
            name: item.name,
            item_type: item.type,
            description: item.description,
            quantity: item.quantity,
            value: item.value || 0,
            equipped: false,
          }),
        ),
      );

      setItems(savedItems);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function updateItem(itemId, itemData) {
    setError("");

    try {
      const updatedItem = await updateInventoryItem(
        itemId,
        itemData,
      );

      setItems((currentItems) =>
        currentItems.map((item) =>
          item.id === itemId ? updatedItem : item,
        ),
      );

      return updatedItem;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  async function removeItem(itemId) {
    setError("");

    try {
      await deleteInventoryItem(itemId);

      setItems((currentItems) =>
        currentItems.filter((item) => item.id !== itemId),
      );
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    items,
    isLoading,
    isSaving,
    error,
    saveStarterItems,
    updateItem,
    removeItem,
    reloadInventory: loadInventory,
  };
}
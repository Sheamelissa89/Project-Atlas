import { useCallback, useEffect, useState } from "react";

import { getCharacters } from "../services/characterService";
import {
  createCompanion,
  deleteCompanion,
  getCompanions,
  updateCompanion,
} from "../services/companionService";


export function useCompanions() {
  const [companions, setCompanions] = useState([]);
  const [characterId, setCharacterId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const loadCompanions = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const activeCharacter = characters[0];

      if (!activeCharacter) {
        setCharacterId(null);
        setCompanions([]);
        setError(
          "Create a character before loading companions.",
        );
        return;
      }

      setCharacterId(activeCharacter.id);

      const savedCompanions = await getCompanions(
        activeCharacter.id,
      );

      setCompanions(savedCompanions);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCompanions();
  }, [loadCompanions]);

  async function saveStarterCompanions(starterCompanions) {
    if (!characterId) {
      setError(
        "A saved character is required before adding companions.",
      );
      return;
    }

    if (companions.length > 0) {
      setError(
        "Starter companions can only be added when the list is empty.",
      );
      return;
    }

    setIsSaving(true);
    setError("");

    try {
      const savedCompanions = await Promise.all(
        starterCompanions.map((companion) =>
          createCompanion({
            character_id: characterId,
            name: companion.name,
            species: companion.species || "Human",
            role: companion.role,
            relationship: companion.relationship,
            level: companion.level || 1,
            health: companion.health || 100,
            ability: companion.ability,
          }),
        ),
      );

      setCompanions(savedCompanions);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function updateSavedCompanion(
    companionId,
    companionData,
  ) {
    setError("");

    try {
      const updatedCompanion = await updateCompanion(
        companionId,
        companionData,
      );

      setCompanions((currentCompanions) =>
        currentCompanions.map((companion) =>
          companion.id === companionId
            ? updatedCompanion
            : companion,
        ),
      );

      return updatedCompanion;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  async function removeCompanion(companionId) {
    setError("");

    try {
      await deleteCompanion(companionId);

      setCompanions((currentCompanions) =>
        currentCompanions.filter(
          (companion) => companion.id !== companionId,
        ),
      );
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    companions,
    isLoading,
    isSaving,
    error,
    saveStarterCompanions,
    updateCompanion: updateSavedCompanion,
    removeCompanion,
    reloadCompanions: loadCompanions,
  };
}
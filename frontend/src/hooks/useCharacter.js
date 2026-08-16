import { useCallback, useEffect, useState } from "react";

import {
  createCharacter,
  getCharacters,
  updateCharacter,
} from "../services/characterService";


export function useCharacter() {
  const [character, setCharacter] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const loadCharacter = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      setCharacter(characters[0] || null);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCharacter();
  }, [loadCharacter]);

  async function saveCharacter(characterData) {
    setError("");

    try {
      const savedCharacter = character
        ? await updateCharacter(character.id, characterData)
        : await createCharacter(characterData);

      setCharacter(savedCharacter);
      return savedCharacter;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    character,
    isLoading,
    error,
    saveCharacter,
    reloadCharacter: loadCharacter,
  };
}
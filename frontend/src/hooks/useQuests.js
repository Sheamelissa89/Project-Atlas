import { useCallback, useEffect, useState } from "react";

import { getCharacters } from "../services/characterService";
import {
  createQuest,
  deleteQuest,
  getQuests,
  updateQuest,
} from "../services/questService";


export function useQuests() {
  const [quests, setQuests] = useState([]);
  const [characterId, setCharacterId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const loadQuests = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const activeCharacter = characters[0];

      if (!activeCharacter) {
        setCharacterId(null);
        setQuests([]);
        setError(
          "Create a character before loading quests.",
        );
        return;
      }

      setCharacterId(activeCharacter.id);

      const savedQuests = await getQuests(
        activeCharacter.id,
      );

      setQuests(savedQuests);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadQuests();
  }, [loadQuests]);

  async function saveStarterQuests(starterQuests) {
    if (!characterId) {
      setError(
        "A saved character is required before adding quests.",
      );
      return;
    }

    if (quests.length > 0) {
      setError(
        "Starter quests can only be added when quests are empty.",
      );
      return;
    }

    setIsSaving(true);
    setError("");

    try {
      const savedQuests = await Promise.all(
        starterQuests.map((quest) =>
          createQuest({
            character_id: characterId,
            title: quest.title,
            description: quest.goal,
            status: quest.status.toLowerCase(),
            reward_gold: quest.rewardGold || 0,
            reward_experience: quest.rewardExperience || 0,
          }),
        ),
      );

      setQuests(savedQuests);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function updateSavedQuest(questId, questData) {
    setError("");

    try {
      const updatedQuest = await updateQuest(
        questId,
        questData,
      );

      setQuests((currentQuests) =>
        currentQuests.map((quest) =>
          quest.id === questId ? updatedQuest : quest,
        ),
      );

      return updatedQuest;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  async function removeQuest(questId) {
    setError("");

    try {
      await deleteQuest(questId);

      setQuests((currentQuests) =>
        currentQuests.filter(
          (quest) => quest.id !== questId,
        ),
      );
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    quests,
    isLoading,
    isSaving,
    error,
    saveStarterQuests,
    updateQuest: updateSavedQuest,
    removeQuest,
    reloadQuests: loadQuests,
  };
}
import { useCallback, useEffect, useState } from "react";

import { getCharacters } from "../services/characterService";
import {
  createJournalEntry,
  deleteJournalEntry,
  getJournalEntries,
  updateJournalEntry,
} from "../services/journalService";


export function useJournal() {
  const [entries, setEntries] = useState([]);
  const [characterId, setCharacterId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const loadJournal = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const activeCharacter = characters[0];

      if (!activeCharacter) {
        setCharacterId(null);
        setEntries([]);
        setError(
          "Create a character before loading the journal.",
        );
        return;
      }

      setCharacterId(activeCharacter.id);

      const savedEntries = await getJournalEntries(
        activeCharacter.id,
      );

      setEntries(savedEntries);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadJournal();
  }, [loadJournal]);

  async function saveStarterEntries(starterEntries) {
    if (!characterId) {
      setError(
        "A saved character is required before adding journal entries.",
      );
      return;
    }

    if (entries.length > 0) {
      setError(
        "Starter entries can only be added when the journal is empty.",
      );
      return;
    }

    setIsSaving(true);
    setError("");

    try {
      const savedEntries = await Promise.all(
        starterEntries.map((entry) =>
          createJournalEntry({
            character_id: characterId,
            title: entry.title,
            category: entry.category,
            content: entry.text,
          }),
        ),
      );

      setEntries(savedEntries);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function updateEntry(entryId, entryData) {
    setError("");

    try {
      const updatedEntry = await updateJournalEntry(
        entryId,
        entryData,
      );

      setEntries((currentEntries) =>
        currentEntries.map((entry) =>
          entry.id === entryId ? updatedEntry : entry,
        ),
      );

      return updatedEntry;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  async function removeEntry(entryId) {
    setError("");

    try {
      await deleteJournalEntry(entryId);

      setEntries((currentEntries) =>
        currentEntries.filter(
          (entry) => entry.id !== entryId,
        ),
      );
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    entries,
    isLoading,
    isSaving,
    error,
    saveStarterEntries,
    updateEntry,
    removeEntry,
    reloadJournal: loadJournal,
  };
}
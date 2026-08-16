import { apiRequest } from "./api";


export function getJournalEntries(characterId) {
  return apiRequest(`/characters/${characterId}/journal`);
}


export function getJournalEntry(entryId) {
  return apiRequest(`/journal/${entryId}`);
}


export function createJournalEntry(entryData) {
  return apiRequest("/journal", {
    method: "POST",
    body: JSON.stringify(entryData),
  });
}


export function updateJournalEntry(entryId, entryData) {
  return apiRequest(`/journal/${entryId}`, {
    method: "PATCH",
    body: JSON.stringify(entryData),
  });
}


export function deleteJournalEntry(entryId) {
  return apiRequest(`/journal/${entryId}`, {
    method: "DELETE",
  });
}
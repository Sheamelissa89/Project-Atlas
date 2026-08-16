import { apiRequest } from "./api";


export function getQuests(characterId) {
  return apiRequest(`/characters/${characterId}/quests`);
}


export function getQuest(questId) {
  return apiRequest(`/quests/${questId}`);
}


export function createQuest(questData) {
  return apiRequest("/quests", {
    method: "POST",
    body: JSON.stringify(questData),
  });
}


export function updateQuest(questId, questData) {
  return apiRequest(`/quests/${questId}`, {
    method: "PATCH",
    body: JSON.stringify(questData),
  });
}


export function deleteQuest(questId) {
  return apiRequest(`/quests/${questId}`, {
    method: "DELETE",
  });
}
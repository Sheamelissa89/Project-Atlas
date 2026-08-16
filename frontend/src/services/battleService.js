import { apiRequest } from "./api";


export function getBattles(characterId) {
  return apiRequest(`/characters/${characterId}/battles`);
}


export function getBattle(battleId) {
  return apiRequest(`/battles/${battleId}`);
}


export function createBattle(battleData) {
  return apiRequest("/battles", {
    method: "POST",
    body: JSON.stringify(battleData),
  });
}


export function updateBattle(battleId, battleData) {
  return apiRequest(`/battles/${battleId}`, {
    method: "PATCH",
    body: JSON.stringify(battleData),
  });
}


export function deleteBattle(battleId) {
  return apiRequest(`/battles/${battleId}`, {
    method: "DELETE",
  });
}
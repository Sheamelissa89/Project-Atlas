import { apiRequest } from "./api";


export function getCharacters() {
  return apiRequest("/characters");
}


export function getCharacter(characterId) {
  return apiRequest(`/characters/${characterId}`);
}


export function createCharacter(characterData) {
  return apiRequest("/characters", {
    method: "POST",
    body: JSON.stringify(characterData),
  });
}


export function updateCharacter(characterId, characterData) {
  return apiRequest(`/characters/${characterId}`, {
    method: "PATCH",
    body: JSON.stringify(characterData),
  });
}


export function deleteCharacter(characterId) {
  return apiRequest(`/characters/${characterId}`, {
    method: "DELETE",
  });
}
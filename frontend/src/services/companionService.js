import { apiRequest } from "./api";


export function getCompanions(characterId) {
  return apiRequest(`/characters/${characterId}/companions`);
}


export function getCompanion(companionId) {
  return apiRequest(`/companions/${companionId}`);
}


export function createCompanion(companionData) {
  return apiRequest("/companions", {
    method: "POST",
    body: JSON.stringify(companionData),
  });
}


export function updateCompanion(companionId, companionData) {
  return apiRequest(`/companions/${companionId}`, {
    method: "PATCH",
    body: JSON.stringify(companionData),
  });
}


export function deleteCompanion(companionId) {
  return apiRequest(`/companions/${companionId}`, {
    method: "DELETE",
  });
}
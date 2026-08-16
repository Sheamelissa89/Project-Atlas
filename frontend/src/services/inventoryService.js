import { apiRequest } from "./api";


export function getInventory(characterId) {
  return apiRequest(`/characters/${characterId}/inventory`);
}


export function getInventoryItem(itemId) {
  return apiRequest(`/inventory/${itemId}`);
}


export function createInventoryItem(itemData) {
  return apiRequest("/inventory", {
    method: "POST",
    body: JSON.stringify(itemData),
  });
}


export function updateInventoryItem(itemId, itemData) {
  return apiRequest(`/inventory/${itemId}`, {
    method: "PATCH",
    body: JSON.stringify(itemData),
  });
}


export function deleteInventoryItem(itemId) {
  return apiRequest(`/inventory/${itemId}`, {
    method: "DELETE",
  });
}
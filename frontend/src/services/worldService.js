import { apiRequest } from "./api";


export function getLocations(characterId) {
  return apiRequest(`/characters/${characterId}/locations`);
}


export function getLocation(locationId) {
  return apiRequest(`/locations/${locationId}`);
}


export function createLocation(locationData) {
  return apiRequest("/locations", {
    method: "POST",
    body: JSON.stringify(locationData),
  });
}


export function updateLocation(locationId, locationData) {
  return apiRequest(`/locations/${locationId}`, {
    method: "PATCH",
    body: JSON.stringify(locationData),
  });
}


export function deleteLocation(locationId) {
  return apiRequest(`/locations/${locationId}`, {
    method: "DELETE",
  });
}
import { useCallback, useEffect, useState } from "react";

import { getCharacters } from "../services/characterService";
import {
  createLocation,
  deleteLocation,
  getLocations,
  updateLocation,
} from "../services/worldService";


function normalizeStatus(status) {
  if (status === "Current Location") {
    return "current";
  }

  return status.toLowerCase();
}


export function useWorld() {
  const [locations, setLocations] = useState([]);
  const [characterId, setCharacterId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");

  const loadLocations = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const characters = await getCharacters();
      const activeCharacter = characters[0];

      if (!activeCharacter) {
        setCharacterId(null);
        setLocations([]);
        setError(
          "Create a character before loading the world.",
        );
        return;
      }

      setCharacterId(activeCharacter.id);

      const savedLocations = await getLocations(
        activeCharacter.id,
      );

      setLocations(savedLocations);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadLocations();
  }, [loadLocations]);

  async function saveStarterLocations(starterLocations) {
    if (!characterId) {
      setError(
        "A saved character is required before adding locations.",
      );
      return;
    }

    if (locations.length > 0) {
      setError(
        "Starter locations can only be added when the world is empty.",
      );
      return;
    }

    setIsSaving(true);
    setError("");

    try {
      const savedLocations = await Promise.all(
        starterLocations.map((location) =>
          createLocation({
            character_id: characterId,
            name: location.name,
            description: location.description,
            status: normalizeStatus(location.status),
          }),
        ),
      );

      setLocations(savedLocations);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function updateSavedLocation(
    locationId,
    locationData,
  ) {
    setError("");

    try {
      const updatedLocation = await updateLocation(
        locationId,
        locationData,
      );

      if (updatedLocation.status === "current") {
        setLocations((currentLocations) =>
          currentLocations.map((location) => {
            if (location.id === locationId) {
              return updatedLocation;
            }

            if (location.status === "current") {
              return {
                ...location,
                status: "discovered",
              };
            }

            return location;
          }),
        );
      } else {
        setLocations((currentLocations) =>
          currentLocations.map((location) =>
            location.id === locationId
              ? updatedLocation
              : location,
          ),
        );
      }

      return updatedLocation;
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  async function removeLocation(locationId) {
    setError("");

    try {
      await deleteLocation(locationId);

      setLocations((currentLocations) =>
        currentLocations.filter(
          (location) => location.id !== locationId,
        ),
      );
    } catch (requestError) {
      setError(requestError.message);
      throw requestError;
    }
  }

  return {
    locations,
    isLoading,
    isSaving,
    error,
    saveStarterLocations,
    updateLocation: updateSavedLocation,
    removeLocation,
    reloadWorld: loadLocations,
  };
}
/**
 * useScenario - Custom React Hook for Scenario State Management
 * 
 * Manages scenario CRUD operations, local storage persistence,
 * and scenario comparison functionality.
 */

import { useState, useCallback, useEffect } from 'react';
import {
  Scenario,
  MCDAWeights,
  SolarParams,
  DEFAULT_WEIGHTS,
  DEFAULT_SOLAR_PARAMS,
  STORAGE_KEYS,
} from '../core';
import { authenticatedFetch, getAuthHeader } from '../auth';

export function useScenario(apiUrl: string = '') {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load scenarios from localStorage on mount
   */
  useEffect(() => {
    loadLocalScenarios();
  }, []);

  /**
   * Load scenarios from localStorage
   */
  const loadLocalScenarios = useCallback(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.scenarios);
      if (stored) {
        const parsed = JSON.parse(stored);
        setScenarios(Array.isArray(parsed) ? parsed : []);
      }
    } catch (err) {
      console.error('Failed to load scenarios from storage:', err);
    }
  }, []);

  /**
   * Save scenarios to localStorage
   */
  const saveLocalScenarios = useCallback((scenariosToSave: Scenario[]) => {
    try {
      localStorage.setItem(STORAGE_KEYS.scenarios, JSON.stringify(scenariosToSave));
    } catch (err) {
      console.error('Failed to save scenarios to storage:', err);
    }
  }, []);

  /**
   * Create a new scenario
   */
  const createScenario = useCallback(
    async (
      name: string,
      weights: MCDAWeights = DEFAULT_WEIGHTS,
      params: SolarParams = DEFAULT_SOLAR_PARAMS
    ): Promise<Scenario | null> => {
      try {
        setLoading(true);
        setError(null);

        const newScenario: Scenario = {
          id: `scenario_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          name,
          weights,
          params,
          timestamp: Date.now(),
        };

        // Try to save to backend if authenticated
        if (Object.keys(getAuthHeader()).length > 0) {
          try {
            const response = await authenticatedFetch(`${apiUrl}/api/scenarios`, {
              method: 'POST',
              body: JSON.stringify(newScenario),
            });

            if (!response.ok) {
              console.warn('Failed to save scenario to backend');
            }
          } catch (err) {
            console.warn('Backend save failed, using local storage only:', err);
          }
        }

        // Always save to local storage
        const updated = [...scenarios, newScenario];
        setScenarios(updated);
        saveLocalScenarios(updated);

        return newScenario;
      } catch (err: any) {
        const errorMsg = err.message || 'Failed to create scenario';
        setError(errorMsg);
        console.error('Create scenario error:', err);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [scenarios, apiUrl, saveLocalScenarios]
  );

  /**
   * Update an existing scenario
   */
  const updateScenario = useCallback(
    async (
      scenarioId: string,
      updates: Partial<Omit<Scenario, 'id' | 'timestamp'>>
    ): Promise<Scenario | null> => {
      try {
        setLoading(true);
        setError(null);

        const scenario = scenarios.find((s) => s.id === scenarioId);
        if (!scenario) {
          throw new Error('Scenario not found');
        }

        const updated: Scenario = {
          ...scenario,
          ...updates,
          id: scenario.id,
          timestamp: scenario.timestamp,
        };

        // Try to update on backend
        if (Object.keys(getAuthHeader()).length > 0) {
          try {
            const response = await authenticatedFetch(`${apiUrl}/api/scenarios/${scenarioId}`, {
              method: 'PUT',
              body: JSON.stringify(updated),
            });

            if (!response.ok) {
              console.warn('Failed to update scenario on backend');
            }
          } catch (err) {
            console.warn('Backend update failed, using local storage only:', err);
          }
        }

        // Update local storage
        const updatedScenarios = scenarios.map((s) =>
          s.id === scenarioId ? updated : s
        );
        setScenarios(updatedScenarios);
        saveLocalScenarios(updatedScenarios);

        return updated;
      } catch (err: any) {
        const errorMsg = err.message || 'Failed to update scenario';
        setError(errorMsg);
        console.error('Update scenario error:', err);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [scenarios, apiUrl, saveLocalScenarios]
  );

  /**
   * Delete a scenario
   */
  const deleteScenario = useCallback(
    async (scenarioId: string): Promise<boolean> => {
      try {
        setLoading(true);
        setError(null);

        // Try to delete from backend
        if (Object.keys(getAuthHeader()).length > 0) {
          try {
            const response = await authenticatedFetch(`${apiUrl}/api/scenarios/${scenarioId}`, {
              method: 'DELETE',
            });

            if (!response.ok) {
              console.warn('Failed to delete scenario from backend');
            }
          } catch (err) {
            console.warn('Backend delete failed, using local storage only:', err);
          }
        }

        // Delete from local storage
        const updated = scenarios.filter((s) => s.id !== scenarioId);
        setScenarios(updated);
        saveLocalScenarios(updated);

        return true;
      } catch (err: any) {
        const errorMsg = err.message || 'Failed to delete scenario';
        setError(errorMsg);
        console.error('Delete scenario error:', err);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [scenarios, apiUrl, saveLocalScenarios]
  );

  /**
   * Get a specific scenario by ID
   */
  const getScenario = useCallback(
    (scenarioId: string): Scenario | undefined => {
      return scenarios.find((s) => s.id === scenarioId);
    },
    [scenarios]
  );

  /**
   * Get all scenarios
   */
  const getAllScenarios = useCallback((): Scenario[] => {
    return [...scenarios];
  }, [scenarios]);

  /**
   * Load scenarios from backend
   */
  const loadFromBackend = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      if (Object.keys(getAuthHeader()).length === 0) {
        throw new Error('Not authenticated');
      }

      const response = await authenticatedFetch(`${apiUrl}/api/scenarios`);

      if (!response.ok) {
        throw new Error(`Failed to load scenarios: ${response.statusText}`);
      }

      const loaded: Scenario[] = await response.json();
      setScenarios(loaded);
      saveLocalScenarios(loaded);

      return loaded;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to load scenarios';
      setError(errorMsg);
      console.error('Load scenarios error:', err);
      return [];
    } finally {
      setLoading(false);
    }
  }, [apiUrl, saveLocalScenarios]);

  /**
   * Duplicate a scenario
   */
  const duplicateScenario = useCallback(
    (scenarioId: string): Scenario | null => {
      const scenario = getScenario(scenarioId);
      if (!scenario) return null;

      const duplicated: Scenario = {
        ...scenario,
        id: `scenario_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        name: `${scenario.name} (Copy)`,
        timestamp: Date.now(),
      };

      const updated = [...scenarios, duplicated];
      setScenarios(updated);
      saveLocalScenarios(updated);

      return duplicated;
    },
    [scenarios, getScenario, saveLocalScenarios]
  );

  /**
   * Compare two scenarios
   */
  const compareScenarios = useCallback(
    (scenarioId1: string, scenarioId2: string) => {
      const s1 = getScenario(scenarioId1);
      const s2 = getScenario(scenarioId2);

      if (!s1 || !s2) return null;

      return {
        scenario1: s1,
        scenario2: s2,
        weightDifferences: {
          climate: Math.abs(s1.weights.climate - s2.weights.climate),
          soil: Math.abs(s1.weights.soil - s2.weights.soil),
          terrain: Math.abs(s1.weights.terrain - s2.weights.terrain),
          infrastructure: Math.abs(
            s1.weights.infrastructure - s2.weights.infrastructure
          ),
        },
        paramDifferences: {
          wattage: Math.abs(s1.params.wattage - s2.params.wattage),
          efficiency: Math.abs(s1.params.efficiency - s2.params.efficiency),
          lifetime: Math.abs(s1.params.lifetime - s2.params.lifetime),
          omCost: Math.abs(s1.params.omCost - s2.params.omCost),
          capitalCost: Math.abs(s1.params.capitalCost - s2.params.capitalCost),
        },
      };
    },
    [getScenario]
  );

  /**
   * Export scenarios to JSON
   */
  const exportToJSON = useCallback((): string => {
    return JSON.stringify(scenarios, null, 2);
  }, [scenarios]);

  /**
   * Import scenarios from JSON
   */
  const importFromJSON = useCallback(
    (jsonString: string): boolean => {
      try {
        const imported = JSON.parse(jsonString);
        if (!Array.isArray(imported)) return false;

        // Validate structure
        const valid = imported.every(
          (s) =>
            s.id &&
            s.name &&
            s.weights &&
            s.params &&
            typeof s.timestamp === 'number'
        );

        if (valid) {
          const merged = [...scenarios, ...imported];
          // Remove duplicates by ID
          const unique = Array.from(
            new Map(merged.map((s) => [s.id, s])).values()
          );
          setScenarios(unique);
          saveLocalScenarios(unique);
          return true;
        }

        return false;
      } catch (err) {
        console.error('Failed to import scenarios:', err);
        return false;
      }
    },
    [scenarios, saveLocalScenarios]
  );

  return {
    scenarios,
    loading,
    error,
    createScenario,
    updateScenario,
    deleteScenario,
    getScenario,
    getAllScenarios,
    loadFromBackend,
    duplicateScenario,
    compareScenarios,
    exportToJSON,
    importFromJSON,
  };
}

export default useScenario;

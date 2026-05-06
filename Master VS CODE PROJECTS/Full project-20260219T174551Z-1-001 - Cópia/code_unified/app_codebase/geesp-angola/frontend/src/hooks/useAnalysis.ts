/**
 * useAnalysis - Custom React Hook for Analysis State Management
 * 
 * Manages the analysis results, loading state, and analysis operations
 * including fetching results, caching, and error handling.
 */

import { useState, useCallback, useRef } from 'react';
import {
  SuitabilityResult,
  MCDAWeights,
  SolarParams,
  Community,
  ANGOLA_COMMUNITIES,
  DEFAULT_WEIGHTS,
  DEFAULT_SOLAR_PARAMS,
} from '../core';
import { authenticatedFetch } from '../auth';

/**
 * Analysis cache to prevent redundant API calls
 */
interface CacheEntry {
  results: SuitabilityResult[];
  timestamp: number;
}

const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

export function useAnalysis() {
  const [results, setResults] = useState<SuitabilityResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const cacheRef = useRef<Map<string, CacheEntry>>(new Map());

  /**
   * Generate cache key from analysis parameters
   */
  const getCacheKey = useCallback((weights: MCDAWeights, params: SolarParams): string => {
    return JSON.stringify({ weights, params });
  }, []);

  /**
   * Check if cache entry is still valid
   */
  const isCacheValid = useCallback((entry: CacheEntry): boolean => {
    return Date.now() - entry.timestamp < CACHE_DURATION;
  }, []);

  /**
   * Run solar suitability analysis
   */
  const runAnalysis = useCallback(
    async (
      weights: MCDAWeights = DEFAULT_WEIGHTS,
      params: SolarParams = DEFAULT_SOLAR_PARAMS,
      communities: Community[] = ANGOLA_COMMUNITIES,
      apiUrl: string = ''
    ) => {
      try {
        setLoading(true);
        setError(null);

        const cacheKey = getCacheKey(weights, params);

        // Check cache first
        const cached = cacheRef.current.get(cacheKey);
        if (cached && isCacheValid(cached)) {
          setResults(cached.results);
          setLoading(false);
          return cached.results;
        }

        // Fetch from API
        const response = await authenticatedFetch(`${apiUrl}/api/analyze`, {
          method: 'POST',
          body: JSON.stringify({
            weights,
            params,
            communities: communities.map((c) => ({
              id: c.id,
              ghi: c.ghi,
              soilType: c.soilType,
              slope: c.slope,
              distToGrid: c.distToGrid,
            })),
          }),
        });

        if (!response.ok) {
          throw new Error(`Analysis failed: ${response.statusText}`);
        }

        const data = await response.json();
        const analysisResults: SuitabilityResult[] = data.results ?? data;

        // Cache results
        cacheRef.current.set(cacheKey, {
          results: analysisResults,
          timestamp: Date.now(),
        });

        setResults(analysisResults);
        return analysisResults;
      } catch (err: any) {
        const errorMsg = err.message || 'Analysis failed';
        setError(errorMsg);
        console.error('Analysis error:', err);
        return [];
      } finally {
        setLoading(false);
      }
    },
    [getCacheKey, isCacheValid]
  );

  /**
   * Clear results
   */
  const clearResults = useCallback(() => {
    setResults([]);
    setError(null);
  }, []);

  /**
   * Clear cache
   */
  const clearCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  /**
   * Get statistics about current results
   */
  const getStatistics = useCallback(() => {
    if (results.length === 0) {
      return null;
    }

    const scores = results.map((r) => r.score);
    const lcoes = results.map((r) => r.lcoe);

    return {
      count: results.length,
      avgScore: scores.reduce((a, b) => a + b, 0) / scores.length,
      maxScore: Math.max(...scores),
      minScore: Math.min(...scores),
      avgLcoe: lcoes.reduce((a, b) => a + b, 0) / lcoes.length,
      maxLcoe: Math.max(...lcoes),
      minLcoe: Math.min(...lcoes),
      excellent: results.filter((r) => r.aptitude === 'Excellent').length,
      good: results.filter((r) => r.aptitude === 'Good').length,
      moderate: results.filter((r) => r.aptitude === 'Moderate').length,
      poor: results.filter((r) => r.aptitude === 'Poor').length,
      unsuitable: results.filter((r) => r.aptitude === 'Unsuitable').length,
    };
  }, [results]);

  /**
   * Get results sorted by score
   */
  const getSortedResults = useCallback(
    (order: 'asc' | 'desc' = 'desc'): SuitabilityResult[] => {
      return [...results].sort((a, b) =>
        order === 'desc' ? b.score - a.score : a.score - b.score
      );
    },
    [results]
  );

  /**
   * Get results filtered by aptitude
   */
  const filterByAptitude = useCallback(
    (aptitudes: SuitabilityResult['aptitude'][]): SuitabilityResult[] => {
      return results.filter((r) => aptitudes.includes(r.aptitude));
    },
    [results]
  );

  /**
   * Get result by community ID
   */
  const getResultById = useCallback(
    (communityId: string): SuitabilityResult | undefined => {
      return results.find((r) => r.communityId === communityId);
    },
    [results]
  );

  return {
    results,
    loading,
    error,
    runAnalysis,
    clearResults,
    clearCache,
    getStatistics,
    getSortedResults,
    filterByAptitude,
    getResultById,
  };
}

export default useAnalysis;

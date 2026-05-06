import React, { useState } from 'react';
import { Filter, X, Search } from 'lucide-react';
import { SuitabilityResult, Community } from '../core';

interface AdvancedFilterProps {
  communities: Community[];
  results: SuitabilityResult[];
  onFilter: (filtered: Community[]) => void;
}

interface FilterCriteria {
  min_aptitude_score: number;
  max_lcoe: number;
  province: string;
  min_ghi: number;
  max_population: number;
  search_text: string;
}

const DEFAULT_CRITERIA: FilterCriteria = {
  min_aptitude_score: 40,
  max_lcoe: 0.20,
  province: '',
  min_ghi: 0,
  max_population: 999999,
  search_text: '',
};

export const AdvancedFilter: React.FC<AdvancedFilterProps> = ({ communities, results, onFilter }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [criteria, setCriteria] = useState<FilterCriteria>(DEFAULT_CRITERIA);
  const [activeFilters, setActiveFilters] = useState(0);

  // Extract unique provinces
  const provinces = Array.from(new Set(communities.map(c => c.province))).sort();

  // Apply filters
  const applyFilters = () => {
    let filtered = [...communities];

    // Filter by search text
    if (criteria.search_text.trim()) {
      const searchLower = criteria.search_text.toLowerCase();
      filtered = filtered.filter(
        c =>
          c.name.toLowerCase().includes(searchLower) ||
          c.province.toLowerCase().includes(searchLower)
      );
    }

    // Filter by suitability score
    if (criteria.min_aptitude_score > 0) {
      filtered = filtered.filter(c => {
        const result = results.find(r => r.communityId === c.id);
        return result && result.score >= criteria.min_aptitude_score;
      });
    }

    // Filter by LCOE
    if (criteria.max_lcoe > 0) {
      filtered = filtered.filter(c => {
        const result = results.find(r => r.communityId === c.id);
        return result && result.lcoe <= criteria.max_lcoe;
      });
    }

    // Filter by province
    if (criteria.province) {
      filtered = filtered.filter(c => c.province === criteria.province);
    }

    // Filter by GHI
    if (criteria.min_ghi > 0) {
      filtered = filtered.filter(c => c.ghi >= criteria.min_ghi);
    }

    // Filter by population
    if (criteria.max_population < 999999) {
      filtered = filtered.filter(c => c.population <= criteria.max_population);
    }

    onFilter(filtered);

    // Count active filters
    let count = 0;
    if (criteria.search_text.trim()) count++;
    if (criteria.min_aptitude_score > 40) count++;
    if (criteria.max_lcoe < 0.20) count++;
    if (criteria.province) count++;
    if (criteria.min_ghi > 0) count++;
    if (criteria.max_population < 999999) count++;

    setActiveFilters(count);
  };

  // Reset filters
  const resetFilters = () => {
    setCriteria(DEFAULT_CRITERIA);
    setActiveFilters(0);
    onFilter(communities);
  };

  // Trigger filter on criteria change
  React.useEffect(() => {
    applyFilters();
  }, [criteria]);

  const aptitudeScores = [
    { value: 0, label: 'All (Any)' },
    { value: 20, label: 'Poor+' },
    { value: 40, label: 'Moderate+' },
    { value: 60, label: 'Good+' },
    { value: 80, label: 'Excellent' },
  ];

  const ghiRanges = [
    { value: 0, label: 'All' },
    { value: 5.0, label: '5.0 kWh/m²/day+' },
    { value: 5.5, label: '5.5 kWh/m²/day+' },
    { value: 6.0, label: '6.0 kWh/m²/day+ (High)' },
  ];

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-zinc-800/50 transition border-b border-zinc-800"
      >
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-emerald-400" />
          <span className="text-sm font-bold text-white">Advanced Filters</span>
          {activeFilters > 0 && (
            <span className="px-2 py-0.5 bg-emerald-600 text-white text-xs font-bold rounded">
              {activeFilters} active
            </span>
          )}
        </div>
        <span className="text-zinc-500">{isOpen ? '✕' : '✓'}</span>
      </button>

      {/* Filter Panel */}
      {isOpen && (
        <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
          {/* Search */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">Search Community</label>
            <div className="relative">
              <Search size={14} className="absolute left-2 top-2 text-zinc-500" />
              <input
                type="text"
                placeholder="Name or province..."
                value={criteria.search_text}
                onChange={e => setCriteria({ ...criteria, search_text: e.target.value })}
                className="w-full pl-7 pr-3 py-1.5 bg-zinc-800 border border-zinc-700 rounded text-xs text-white placeholder-zinc-500"
              />
            </div>
          </div>

          {/* Aptitude Score */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">
              Min Suitability Score
            </label>
            <div className="space-y-2">
              {aptitudeScores.map(option => (
                <label key={option.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="aptitude"
                    value={option.value}
                    checked={criteria.min_aptitude_score === option.value}
                    onChange={e => setCriteria({ ...criteria, min_aptitude_score: Number(e.target.value) })}
                    className="w-3 h-3"
                  />
                  <span className="text-xs text-zinc-300">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* LCOE */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">
              Max LCOE ($/kWh)
            </label>
            <input
              type="number"
              min="0"
              max="1"
              step="0.01"
              value={criteria.max_lcoe}
              onChange={e => setCriteria({ ...criteria, max_lcoe: Number(e.target.value) })}
              className="w-full px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-xs text-white"
            />
            <p className="text-xs text-zinc-500 mt-1">Current: ${criteria.max_lcoe.toFixed(3)}</p>
          </div>

          {/* GHI */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">
              Min Solar Irradiance (GHI)
            </label>
            <div className="space-y-2">
              {ghiRanges.map(option => (
                <label key={option.value} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="ghi"
                    value={option.value}
                    checked={criteria.min_ghi === option.value}
                    onChange={e => setCriteria({ ...criteria, min_ghi: Number(e.target.value) })}
                    className="w-3 h-3"
                  />
                  <span className="text-xs text-zinc-300">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Province */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">Province</label>
            <select
              value={criteria.province}
              onChange={e => setCriteria({ ...criteria, province: e.target.value })}
              className="w-full px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-xs text-white"
            >
              <option value="">All Provinces</option>
              {provinces.map(province => (
                <option key={province} value={province}>
                  {province}
                </option>
              ))}
            </select>
          </div>

          {/* Population */}
          <div>
            <label className="block text-xs font-bold text-zinc-400 mb-2">
              Max Population
            </label>
            <input
              type="number"
              min="0"
              value={criteria.max_population}
              onChange={e => setCriteria({ ...criteria, max_population: Number(e.target.value) })}
              className="w-full px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-xs text-white"
            />
          </div>

          {/* Actions */}
          <div className="flex gap-2 pt-2 border-t border-zinc-700">
            <button
              onClick={resetFilters}
              className="flex-1 px-2 py-1 bg-zinc-700 hover:bg-zinc-600 text-white text-xs font-bold rounded transition flex items-center justify-center gap-1"
            >
              <X size={12} /> Reset
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="flex-1 px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded transition"
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

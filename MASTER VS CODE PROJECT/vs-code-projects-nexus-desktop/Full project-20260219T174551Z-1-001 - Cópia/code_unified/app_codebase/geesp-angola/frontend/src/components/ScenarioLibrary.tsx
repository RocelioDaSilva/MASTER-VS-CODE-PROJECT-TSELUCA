import React, { useState, useEffect } from 'react';
import { Save, Trash2, Plus, ChevronDown, TrendingUp, DollarSign, Clock } from 'lucide-react';
import { MCDAWeights, SolarParams, SuitabilityResult, Scenario } from '../core';

interface ScenarioLibraryProps {
  currentWeights: MCDAWeights;
  currentParams: SolarParams;
  onLoadScenario: (weights: MCDAWeights, params: SolarParams) => void;
}

interface SavedScenario {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
  tags?: string[];
}

const API_BASE = '/api';

export const ScenarioLibrary: React.FC<ScenarioLibraryProps> = ({
  currentWeights,
  currentParams,
  onLoadScenario,
}) => {
  const [scenarios, setScenarios] = useState<SavedScenario[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [showSaveForm, setShowSaveForm] = useState(false);
  const [scenarioName, setScenarioName] = useState('');
  const [scenarioDescription, setScenarioDescription] = useState('');
  const [scenarioTags, setScenarioTags] = useState('');
  const [loading, setLoading] = useState(false);

  // Load scenarios on mount
  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      const response = await fetch(`${API_BASE}/scenarios`);
      if (response.ok) {
        const data = await response.json();
        setScenarios(data);
      }
    } catch (error) {
      console.error('Error loading scenarios:', error);
    }
  };

  const handleSaveScenario = async () => {
    if (!scenarioName.trim()) {
      alert('Scenario name is required');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/scenarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: scenarioName,
          description: scenarioDescription,
          weights: currentWeights,
          solar_params: currentParams,
          tags: scenarioTags.split(',').map(t => t.trim()).filter(Boolean),
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`✅ Scenario "${scenarioName}" saved!`);
        setScenarioName('');
        setScenarioDescription('');
        setScenarioTags('');
        setShowSaveForm(false);
        loadScenarios();
      }
    } catch (error) {
      console.error('Error saving scenario:', error);
      alert('Failed to save scenario');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadScenario = async (scenarioId: string) => {
    try {
      const response = await fetch(`${API_BASE}/scenarios/${scenarioId}`);
      if (response.ok) {
        const scenario = await response.json();
        onLoadScenario(scenario.weights, scenario.solar_params);
        alert(`✅ Loaded scenario: "${scenario.name}"`);
      }
    } catch (error) {
      console.error('Error loading scenario:', error);
      alert('Failed to load scenario');
    }
  };

  const handleDeleteScenario = async (scenarioId: string) => {
    if (!confirm('Are you sure? This action cannot be undone.')) return;

    try {
      const response = await fetch(`${API_BASE}/scenarios/${scenarioId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        alert('Scenario deleted');
        loadScenarios();
      }
    } catch (error) {
      console.error('Error deleting scenario:', error);
      alert('Failed to delete scenario');
    }
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold uppercase tracking-widest text-emerald-400">
          📚 Scenario Library
        </h3>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-zinc-500 hover:text-zinc-300"
        >
          <ChevronDown size={16} className={`transition ${isOpen ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {isOpen && (
        <>
          {/* Save New Scenario */}
          {!showSaveForm ? (
            <button
              onClick={() => setShowSaveForm(true)}
              className="w-full mb-4 px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold uppercase rounded flex items-center justify-center gap-2 transition"
            >
              <Plus size={14} /> Save Current Config
            </button>
          ) : (
            <div className="mb-4 p-3 bg-zinc-800 rounded border border-zinc-700">
              <input
                type="text"
                placeholder="Scenario name..."
                value={scenarioName}
                onChange={e => setScenarioName(e.target.value)}
                className="w-full px-2 py-1 mb-2 bg-zinc-700 border border-zinc-600 rounded text-xs text-white placeholder-zinc-500"
              />
              <textarea
                placeholder="Description (optional)..."
                value={scenarioDescription}
                onChange={e => setScenarioDescription(e.target.value)}
                className="w-full px-2 py-1 mb-2 bg-zinc-700 border border-zinc-600 rounded text-xs text-white placeholder-zinc-500 h-12 resize-none"
              />
              <input
                type="text"
                placeholder="Tags (comma-separated)..."
                value={scenarioTags}
                onChange={e => setScenarioTags(e.target.value)}
                className="w-full px-2 py-1 mb-2 bg-zinc-700 border border-zinc-600 rounded text-xs text-white placeholder-zinc-500"
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSaveScenario}
                  disabled={loading}
                  className="flex-1 px-2 py-1 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white text-xs font-bold rounded transition"
                >
                  {loading ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={() => setShowSaveForm(false)}
                  className="flex-1 px-2 py-1 bg-zinc-700 hover:bg-zinc-600 text-white text-xs font-bold rounded"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* Scenario List */}
          <div className="flex-1 overflow-y-auto space-y-2">
            {scenarios.length === 0 ? (
              <p className="text-xs text-zinc-500 text-center py-4">No scenarios saved yet</p>
            ) : (
              scenarios.map(scenario => (
                <div
                  key={scenario.id}
                  className="p-2 bg-zinc-800 border border-zinc-700 rounded hover:border-emerald-500/50 transition"
                >
                  <h4 className="text-xs font-bold text-white mb-1">{scenario.name}</h4>
                  {scenario.description && (
                    <p className="text-xs text-zinc-400 mb-2">{scenario.description}</p>
                  )}
                  {scenario.tags && scenario.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {scenario.tags.map(tag => (
                        <span
                          key={tag}
                          className="px-1.5 py-0.5 bg-emerald-500/20 text-emerald-300 text-xs rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  <div className="flex gap-1">
                    <button
                      onClick={() => handleLoadScenario(scenario.id)}
                      className="flex-1 px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded transition"
                    >
                      Load
                    </button>
                    <button
                      onClick={() => handleDeleteScenario(scenario.id)}
                      className="px-2 py-1 bg-red-600 hover:bg-red-700 text-white rounded transition"
                    >
                      <Trash2 size={12} />
                    </button>
                  </div>
                  <p className="text-xs text-zinc-500 mt-1">
                    {new Date(scenario.updated_at).toLocaleDateString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

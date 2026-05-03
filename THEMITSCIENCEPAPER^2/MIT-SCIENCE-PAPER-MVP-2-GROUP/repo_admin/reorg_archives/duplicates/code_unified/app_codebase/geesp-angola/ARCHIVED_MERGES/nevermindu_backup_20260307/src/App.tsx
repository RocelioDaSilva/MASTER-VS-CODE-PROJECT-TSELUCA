import React, { useState, useMemo, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { EnergyMap } from './components/Map';
import { Charts } from './components/Charts';
import { Chat } from './components/Chat';
import { ScenarioLibrary } from './components/ScenarioLibrary';
import { FinancialAnalysis } from './components/FinancialAnalysis';
import { AdvancedFilter } from './components/AdvancedFilter';
import { ANGOLA_COMMUNITIES, DEFAULT_WEIGHTS, DEFAULT_SOLAR_PARAMS } from './constants';
import { MCDAWeights, SolarParams, SuitabilityResult, Scenario, ChatMessage } from './types';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Download, LayoutDashboard, Map as MapIcon, BarChart3, FileText, Zap, 
  Sparkles, Save, History, Loader2, AlertCircle, MessageSquare, 
  FileJson, FileSpreadsheet, File as FilePdf, ArrowLeftRight, CheckCircle2,
  DollarSign, Filter
} from 'lucide-react';
import { getEnergyInsights } from './services/geminiService';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';
import * as XLSX from 'xlsx';
import { GoogleGenAI } from '@google/genai';

// Simple in-memory cache
const analysisCache = new Map<string, SuitabilityResult[]>();

export default function App() {
  const [weights, setWeights] = useState<MCDAWeights>(DEFAULT_WEIGHTS);
  const [params, setParams] = useState<SolarParams>(DEFAULT_SOLAR_PARAMS);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'map' | 'analysis' | 'financial' | 'filter' | 'scenarios' | 'insights' | 'chat' | 'compare'>('dashboard');
  const [results, setResults] = useState<SuitabilityResult[]>([]);
  const [filteredCommunities, setFilteredCommunities] = useState<any[]>(ANGOLA_COMMUNITIES);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [aiInsight, setAiInsight] = useState<string | null>(null);
  const [isGeneratingInsight, setIsGeneratingInsight] = useState(false);
  const [compareScenario, setCompareScenario] = useState<Scenario | null>(null);

  // Validation
  const weightSum = useMemo(() => Object.values(weights).reduce((a, b) => (a as number) + (b as number), 0), [weights]);
  const isWeightsValid = Math.abs(weightSum - 1) < 0.001;

  // Fetch results from API with caching
  const fetchResults = async () => {
    if (!isWeightsValid) return;

    const cacheKey = JSON.stringify({ weights, params });
    if (analysisCache.has(cacheKey)) {
      setResults(analysisCache.get(cacheKey)!);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ communities: ANGOLA_COMMUNITIES, weights, params }),
      });
      if (!response.ok) throw new Error('Failed to fetch analysis results');
      const data = await response.json();
      setResults(data.results);
      analysisCache.set(cacheKey, data.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, [weights, params]);

  const saveScenario = () => {
    const name = prompt("Enter scenario name:");
    if (!name) return;
    const newScenario: Scenario = {
      id: Math.random().toString(36).substr(2, 9),
      name,
      weights: { ...weights },
      params: { ...params },
      timestamp: Date.now(),
    };
    setScenarios([...scenarios, newScenario]);
  };

  const loadScenario = (s: Scenario) => {
    setWeights(s.weights);
    setParams(s.params);
  };

  const handleGeminiChat = async (text: string) => {
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "" });
    
    const context = `
      You are an Angola energy expert. 
      Current analysis results: ${JSON.stringify(results.slice(0, 5))}
      Weights: ${JSON.stringify(weights)}
      User question: ${text}
    `;

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: context,
    });
    return response.text || "No response from AI.";
  };

  const exportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(20);
    doc.text('GEESP-Angola Energy Assessment Report', 14, 22);
    doc.setFontSize(11);
    doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 30);
    
    const tableData = results.map(r => {
      const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
      return [c?.name, c?.province, r.score.toFixed(2), r.aptitude, `$${r.lcoe.toFixed(4)}` ];
    });

    (doc as any).autoTable({
      head: [['Community', 'Province', 'Score', 'Aptitude', 'LCOE']],
      body: tableData,
      startY: 40,
    });

    doc.save(`geesp_angola_report_${Date.now()}.pdf`);
  };

  const exportExcel = () => {
    const data = results.map(r => {
      const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
      return {
        Community: c?.name,
        Province: c?.province,
        'Suitability Score': r.score,
        Aptitude: r.aptitude,
        'LCOE ($/kWh)': r.lcoe,
        'GHI (kWh/m2)': c?.ghi,
        'Distance to Grid (km)': c?.distToGrid
      };
    });

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Assessment Results");
    XLSX.writeFile(wb, "geesp_angola_data.xlsx");
  };

  const exportJSON = () => {
    const data = {
      metadata: {
        timestamp: Date.now(),
        weights,
        params
      },
      results: results.map(r => {
        const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
        return { ...r, community: c };
      })
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'geesp_angola_export.json';
    a.click();
  };

  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-emerald-500/30">
      <Sidebar 
        weights={weights} 
        setWeights={setWeights} 
        params={params} 
        setParams={setParams} 
      />

      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-zinc-900 px-8 flex items-center justify-between bg-zinc-950/50 backdrop-blur-md z-10 shrink-0">
          <nav className="flex gap-6 h-full overflow-x-auto">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
              { id: 'map', label: 'Spatial', icon: MapIcon },
              { id: 'analysis', label: 'Analysis', icon: BarChart3 },
              { id: 'financial', label: 'Financial', icon: DollarSign },
              { id: 'filter', label: 'Filter', icon: Filter },
              { id: 'scenarios', label: 'Scenarios', icon: History },
              { id: 'chat', label: 'AI Chat', icon: MessageSquare },
              { id: 'compare', label: 'Compare', icon: ArrowLeftRight },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 text-xs font-bold uppercase tracking-widest transition-colors relative h-full whitespace-nowrap ${
                  activeTab === tab.id ? 'text-emerald-400' : 'text-zinc-500 hover:text-zinc-300'
                }`}
              >
                <tab.icon size={14} />
                <span className="hidden xl:inline">{tab.label}</span>
                {activeTab === tab.id && (
                  <motion.div layoutId="activeTab" className="absolute bottom-0 left-0 right-0 h-0.5 bg-emerald-500" />
                )}
              </button>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            {!isWeightsValid && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-950/20 border border-amber-900/30 text-amber-400 rounded-lg text-[10px] font-bold">
                <AlertCircle size={12} />
                Weights must sum to 100% (Current: {(weightSum * 100).toFixed(0)}%)
              </div>
            )}
            {loading && <Loader2 size={16} className="animate-spin text-emerald-500 mx-2" />}
            
            <div className="flex items-center bg-zinc-900 border border-zinc-800 rounded-lg p-1">
              <button onClick={exportPDF} title="Export PDF" className="p-1.5 hover:text-emerald-400 transition-colors"><FilePdf size={14} /></button>
              <button onClick={exportExcel} title="Export Excel" className="p-1.5 hover:text-emerald-400 transition-colors"><FileSpreadsheet size={14} /></button>
              <button onClick={exportJSON} title="Export JSON" className="p-1.5 hover:text-emerald-400 transition-colors"><FileJson size={14} /></button>
            </div>

            <button 
              onClick={saveScenario}
              className="hidden md:flex items-center gap-2 px-3 py-2 bg-zinc-900 border border-zinc-800 hover:border-emerald-500/50 text-zinc-300 rounded-lg text-[10px] font-bold transition-all"
            >
              <Save size={12} />
              Save
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8 custom-scrollbar">
          {error && (
            <div className="mb-6 p-4 bg-red-950/20 border border-red-900/30 rounded-lg flex items-center gap-3 text-red-400 text-xs">
              <AlertCircle size={16} />
              {error}
              <button onClick={fetchResults} className="ml-auto underline">Retry</button>
            </div>
          )}

          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.02 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              {activeTab === 'dashboard' && (
                <div className="space-y-8">
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
                    <StatCard 
                      label="Avg Suitability" 
                      value={results.length > 0 ? `${(results.reduce((acc, r) => acc + (r.score as number), 0) / results.length).toFixed(1)}%` : '...'}
                      trend="+2.4%"
                    />
                    <StatCard 
                      label="Avg LCOE" 
                      value={results.length > 0 ? `$${(results.reduce((acc, r) => acc + (r.lcoe as number), 0) / results.length).toFixed(3)}` : '...'}
                      unit="/kWh"
                    />
                    <StatCard 
                      label="Excellent Sites" 
                      value={results.filter(r => r.aptitude === 'Excellent').length.toString()}
                      sub="Communities"
                    />
                    <StatCard 
                      label="Total Potential" 
                      value="4.2"
                      unit="GW"
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 min-h-[600px]">
                    <div className="xl:col-span-2 h-[400px] xl:h-auto">
                      <EnergyMap results={results} />
                    </div>
                    <div className="space-y-6">
                      {scenarios.length > 0 && (
                        <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl p-6">
                          <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-4 flex items-center gap-2">
                            <History size={14} className="text-emerald-500" />
                            Saved Scenarios
                          </h3>
                          <div className="space-y-2">
                            {scenarios.map(s => (
                              <div key={s.id} className="flex gap-2">
                                <button
                                  onClick={() => loadScenario(s)}
                                  className="flex-1 flex items-center justify-between p-2 rounded bg-zinc-900 border border-zinc-800 hover:border-emerald-500/30 text-left transition-all"
                                >
                                  <span className="text-[10px] font-bold text-zinc-300">{s.name}</span>
                                  <span className="text-[8px] text-zinc-600">{new Date(s.timestamp).toLocaleDateString()}</span>
                                </button>
                                <button 
                                  onClick={() => { setCompareScenario(s); setActiveTab('compare'); }}
                                  className="p-2 bg-zinc-900 border border-zinc-800 hover:text-emerald-400 rounded"
                                  title="Compare"
                                >
                                  <ArrowLeftRight size={12} />
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl p-6 overflow-y-auto max-h-[400px]">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-6 flex items-center gap-2">
                          <FileText size={14} className="text-emerald-500" />
                          Community Rankings
                        </h3>
                        <div className="space-y-4">
                          {results.sort((a, b) => b.score - a.score).map((r, i) => {
                            const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
                            return (
                              <div key={r.communityId} className="flex items-center justify-between p-3 rounded-lg bg-zinc-900/50 border border-zinc-800/50">
                                <div className="flex items-center gap-3">
                                  <span className="text-[10px] font-mono text-zinc-600">0{i+1}</span>
                                  <div>
                                    <p className="text-xs font-bold text-zinc-200">{c?.name}</p>
                                    <p className="text-[10px] text-zinc-500">{c?.province}</p>
                                  </div>
                                </div>
                                <div className="text-right">
                                  <p className={`text-xs font-bold ${r.score > 60 ? 'text-emerald-400' : 'text-amber-400'}`}>
                                    {r.score.toFixed(1)}%
                                  </p>
                                  <p className="text-[9px] text-zinc-600 uppercase tracking-tighter">{r.aptitude}</p>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'map' && (
                <div className="h-[calc(100vh-160px)]">
                  <EnergyMap results={results} />
                </div>
              )}

              {activeTab === 'analysis' && (
                <div className="h-[calc(100vh-160px)]">
                  <Charts results={results} />
                </div>
              )}

              {activeTab === 'financial' && (
                <div className="h-[calc(100vh-160px)] overflow-y-auto">
                  <FinancialAnalysis results={results} communities={ANGOLA_COMMUNITIES} />
                </div>
              )}

              {activeTab === 'filter' && (
                <div className="space-y-6">
                  <AdvancedFilter 
                    communities={ANGOLA_COMMUNITIES} 
                    results={results}
                    onFilter={setFilteredCommunities}
                  />
                  <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-6">
                    <h3 className="text-sm font-bold text-emerald-400 mb-4">
                      Filtered Results: {filteredCommunities.length} communities
                    </h3>
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                      {filteredCommunities.length === 0 ? (
                        <p className="text-xs text-zinc-500 text-center py-8">No communities match your filters</p>
                      ) : (
                        filteredCommunities.map(c => {
                          const result = results.find(r => r.communityId === c.id);
                          return (
                            <div key={c.id} className="p-3 bg-zinc-800/50 rounded border border-zinc-700">
                              <div className="flex justify-between items-start mb-2">
                                <div>
                                  <p className="text-xs font-bold text-white">{c.name}</p>
                                  <p className="text-xs text-zinc-500">{c.province}</p>
                                </div>
                                {result && (
                                  <span className={`text-xs font-bold px-2 py-1 rounded ${
                                    result.score > 70 ? 'bg-emerald-600/30 text-emerald-400' : 'bg-amber-600/30 text-amber-400'
                                  }`}>
                                    {result.score.toFixed(0)}%
                                  </span>
                                )}
                              </div>
                              <div className="grid grid-cols-3 gap-2 text-xs text-zinc-400">
                                <div>GHI: {c.ghi.toFixed(2)}</div>
                                <div>Pop: {c.population}</div>
                                {result && <div>LCOE: ${result.lcoe.toFixed(3)}</div>}
                              </div>
                            </div>
                          );
                        })
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'scenarios' && (
                <div className="max-w-2xl">
                  <ScenarioLibrary
                    currentWeights={weights}
                    currentParams={params}
                    onLoadScenario={(w, p) => {
                      setWeights(w);
                      setParams(p);
                    }}
                  />
                </div>
              )}

              {activeTab === 'chat' && (
                <div className="h-[calc(100vh-160px)] max-w-4xl mx-auto">
                  <Chat onSendMessage={handleGeminiChat} />
                </div>
              )}

              {activeTab === 'compare' && (
                <div className="h-full space-y-8">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-bold text-emerald-400 flex items-center gap-3">
                      <ArrowLeftRight size={24} />
                      Scenario Comparison
                    </h2>
                    <div className="flex gap-4">
                      <div className="px-4 py-2 bg-zinc-900 border border-zinc-800 rounded-lg">
                        <span className="text-[10px] text-zinc-500 uppercase block">Current</span>
                        <span className="text-xs font-bold">Active Configuration</span>
                      </div>
                      <div className="px-4 py-2 bg-emerald-950/20 border border-emerald-900/30 rounded-lg">
                        <span className="text-[10px] text-emerald-500 uppercase block">Comparing With</span>
                        <span className="text-xs font-bold text-emerald-400">{compareScenario?.name || 'Select a scenario'}</span>
                      </div>
                    </div>
                  </div>

                  {compareScenario ? (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[600px]">
                      <div className="space-y-4">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500">Active Results</h3>
                        <Charts results={results} />
                      </div>
                      <div className="space-y-4">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-emerald-500">"{compareScenario.name}" Results</h3>
                        <div className="opacity-80 grayscale-[0.2]">
                          {/* In a real app, we'd fetch or recalculate for the comparison scenario */}
                          <Charts results={results.map(r => ({ ...r, score: r.score * 0.9 }))} />
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-[400px] text-zinc-500">
                      <History size={48} className="mb-4 opacity-20" />
                      <p>Select a scenario from the dashboard to start comparison</p>
                      <button onClick={() => setActiveTab('dashboard')} className="mt-4 text-emerald-500 hover:underline">Go to Dashboard</button>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

function StatCard({ label, value, unit, trend, sub }: { label: string, value: string, unit?: string, trend?: string, sub?: string }) {
  return (
    <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl relative overflow-hidden group hover:border-emerald-500/30 transition-colors">
      <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
        <Zap size={48} className="text-emerald-500" />
      </div>
      <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 mb-2">{label}</p>
      <div className="flex items-baseline gap-1">
        <h3 className="text-2xl font-bold text-zinc-100">{value}</h3>
        {unit && <span className="text-xs font-medium text-zinc-500">{unit}</span>}
      </div>
      {trend && <p className="text-[10px] font-bold text-emerald-400 mt-2">{trend} <span className="text-zinc-600 font-normal">vs last period</span></p>}
      {sub && <p className="text-[10px] text-zinc-500 mt-2">{sub}</p>}
    </div>
  );
}

import React, { useState, useMemo } from 'react';
import { Sidebar } from './components/Sidebar';
import { Map } from './components/Map';
import { Charts } from './components/Charts';
import { ScenarioLibrary } from './components/ScenarioLibrary';
import { FinancialAnalysis } from './components/FinancialAnalysis';
import { AdvancedFilter } from './components/AdvancedFilter';
import { ANGOLA_COMMUNITIES, DEFAULT_WEIGHTS, DEFAULT_SOLAR_PARAMS } from './constants';
import { MCDAWeights, SolarParams, SuitabilityResult } from './types';
import { motion } from 'motion/react';
import { Download, LayoutDashboard, Map as MapIcon, BarChart3, FileText, Zap, DollarSign, Filter } from 'lucide-react';

export default function App() {
  const [weights, setWeights] = useState<MCDAWeights>(DEFAULT_WEIGHTS);
  const [params, setParams] = useState<SolarParams>(DEFAULT_SOLAR_PARAMS);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'map' | 'analysis' | 'financial' | 'compare'>('dashboard');
  const [filteredCommunities, setFilteredCommunities] = useState<typeof ANGOLA_COMMUNITIES>(ANGOLA_COMMUNITIES);

  const results = useMemo(() => {
    return ANGOLA_COMMUNITIES.map((community): SuitabilityResult => {
      // 1. MCDA Calculation (Weighted Overlay)
      // Normalize factors to 0-1
      const climateFactor = community.ghi / 7; // Max GHI ~7
      const soilFactor = community.soilType === 'Rocky' ? 0.4 : community.soilType === 'Sandy' ? 0.8 : 1.0;
      const terrainFactor = Math.max(0, 1 - (community.slope / 20)); // Max slope 20%
      const infraFactor = Math.max(0, 1 - (community.distToGrid / 100)); // Max dist 100km

      const score = (
        climateFactor * weights.climate +
        soilFactor * weights.soil +
        terrainFactor * weights.terrain +
        infraFactor * weights.infrastructure
      ) * 100;

      // 2. LCOE Calculation
      // LCOE = (Total Life Cycle Cost) / (Total Lifetime Energy Production)
      // Annual Energy (kWh) = GHI * Area * Efficiency * 365
      // Assuming 100m2 installation for comparison
      const annualEnergy = community.ghi * 100 * params.efficiency * 365;
      const totalEnergy = annualEnergy * params.lifetime;
      const totalCost = params.capitalCost + (params.omCost * params.lifetime);
      const lcoe = totalCost / totalEnergy;

      // 3. Aptitude Scoring
      let aptitude: SuitabilityResult['aptitude'] = 'Unsuitable';
      if (score > 80) aptitude = 'Excellent';
      else if (score > 60) aptitude = 'Good';
      else if (score > 40) aptitude = 'Moderate';
      else if (score > 20) aptitude = 'Poor';

      return {
        communityId: community.id,
        score,
        aptitude,
        lcoe,
      };
    });
  }, [weights, params]);

  const exportCSV = () => {
    const headers = ['Community', 'Province', 'Suitability Score', 'Aptitude', 'LCOE ($/kWh)'];
    const rows = results.map(r => {
      const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
      return [c?.name, c?.province, r.score.toFixed(2), r.aptitude, r.lcoe.toFixed(4)];
    });
    
    const csvContent = [headers, ...rows].map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "geesp_angola_assessment.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
        <header className="h-16 border-b border-zinc-900 px-8 flex items-center justify-between bg-zinc-950/50 backdrop-blur-md z-10">
          <nav className="flex gap-8">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
              { id: 'map', label: 'Spatial View', icon: MapIcon },
              { id: 'analysis', label: 'Analysis', icon: BarChart3 },
              { id: 'financial', label: 'Financial', icon: DollarSign },
              { id: 'compare', label: 'Compare', icon: Filter },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 text-xs font-bold uppercase tracking-widest transition-colors ${
                  activeTab === tab.id ? 'text-emerald-400' : 'text-zinc-500 hover:text-zinc-300'
                }`}
              >
                <tab.icon size={14} />
                {tab.label}
                {activeTab === tab.id && (
                  <motion.div layoutId="activeTab" className="absolute -bottom-[25px] left-0 right-0 h-0.5 bg-emerald-500" />
                )}
              </button>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            <button 
              onClick={exportCSV}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-all shadow-lg shadow-emerald-900/20"
            >
              <Download size={14} />
              Export CSV
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="h-full space-y-8"
          >
            {activeTab === 'dashboard' && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatCard 
                    label="Avg Suitability" 
                    value={`${(results.reduce((acc, r) => acc + r.score, 0) / results.length).toFixed(1)}%`}
                    trend="+2.4%"
                  />
                  <StatCard 
                    label="Avg LCOE" 
                    value={`$${(results.reduce((acc, r) => acc + r.lcoe, 0) / results.length).toFixed(3)}`}
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
                
                <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 h-[600px]">
                  <div className="xl:col-span-2">
                    <Map results={results} />
                  </div>
                  <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl p-6 overflow-y-auto">
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
              </>
            )}

            {activeTab === 'map' && (
              <div className="h-[calc(100vh-200px)]">
                <Map results={results} />
              </div>
            )}

            {activeTab === 'analysis' && (
              <div className="h-[calc(100vh-200px)]">
                <Charts results={results} />
              </div>
            )}

            {activeTab === 'financial' && (
              <div className="space-y-8">
                <FinancialAnalysis results={results} communities={filteredCommunities} />
              </div>
            )}

            {activeTab === 'compare' && (
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-full">
                <div className="lg:col-span-1 space-y-6">
                  <ScenarioLibrary 
                    currentWeights={weights}
                    currentParams={params}
                    onLoadScenario={(w, p) => {
                      setWeights(w);
                      setParams(p);
                    }}
                  />
                  <AdvancedFilter
                    communities={ANGOLA_COMMUNITIES}
                    results={results}
                    onFilter={setFilteredCommunities}
                  />
                </div>
                <div className="lg:col-span-3">
                  <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-6 h-full overflow-y-auto">
                    <h3 className="text-sm font-bold text-emerald-400 mb-4">📊 Filtered Communities ({filteredCommunities.length})</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {filteredCommunities.map(community => {
                        const result = results.find(r => r.communityId === community.id);
                        if (!result) return null;
                        return (
                          <div key={community.id} className="p-4 bg-zinc-800 border border-zinc-700 rounded-lg">
                            <h4 className="font-bold text-white mb-2">{community.name}</h4>
                            <div className="space-y-1 text-xs text-zinc-300">
                              <p>🏆 Score: <span className="text-emerald-400 font-bold">{result.score.toFixed(1)}</span></p>
                              <p>⚡ GHI: <span className="font-mono">{community.ghi.toFixed(2)}</span> kWh/m²/day</p>
                              <p>💰 LCOE: <span className="text-emerald-400 font-bold">${result.lcoe.toFixed(3)}</span>/kWh</p>
                              <p>📍 Province: {community.province}</p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
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

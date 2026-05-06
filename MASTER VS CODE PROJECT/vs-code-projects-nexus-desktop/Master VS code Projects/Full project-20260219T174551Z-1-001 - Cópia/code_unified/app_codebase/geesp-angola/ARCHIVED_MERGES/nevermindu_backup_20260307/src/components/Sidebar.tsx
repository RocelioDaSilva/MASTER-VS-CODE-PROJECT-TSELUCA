import React, { useState } from 'react';
import { MCDAWeights, SolarParams } from '../types';
import { Settings, Zap, Map as MapIcon, DollarSign, Info, Menu, X } from 'lucide-react';

interface SidebarProps {
  weights: MCDAWeights;
  setWeights: (w: MCDAWeights) => void;
  params: SolarParams;
  setParams: (p: SolarParams) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ weights, setWeights, params, setParams }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Mobile Toggle */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed bottom-6 left-6 z-[2000] p-4 bg-emerald-600 text-white rounded-full shadow-2xl"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      <div className={`
        fixed inset-y-0 left-0 z-[1500] w-80 bg-zinc-950 border-r border-emerald-900/30 text-zinc-100 flex flex-col overflow-y-auto transition-transform duration-300 ease-in-out
        lg:relative lg:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
      <div className="p-6 border-b border-emerald-900/30">
        <div className="flex items-center gap-2 mb-2">
          <Zap className="text-emerald-400" size={24} />
          <h1 className="text-lg font-bold tracking-tight text-emerald-50">GEESP-Angola</h1>
        </div>
        <p className="text-xs text-zinc-500 uppercase tracking-widest font-semibold">Energy Suitability Assessment</p>
      </div>

      <div className="p-6 space-y-8">
        {/* MCDA Weights */}
        <section>
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <Settings size={18} />
            <h2 className="text-sm font-bold uppercase tracking-wider">MCDA Weights</h2>
          </div>
          <div className="space-y-4">
            {Object.entries(weights).map(([key, value]) => (
              <div key={key} className="space-y-1">
                <div className="flex justify-between text-xs font-mono">
                  <span className="capitalize">{key}</span>
                  <span>{((value as number) * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={value}
                  onChange={(e) => setWeights({ ...weights, [key as keyof MCDAWeights]: parseFloat(e.target.value) })}
                  className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
              </div>
            ))}
          </div>
        </section>

        {/* Solar Parameters */}
        <section>
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <Zap size={18} />
            <h2 className="text-sm font-bold uppercase tracking-wider">Solar Config</h2>
          </div>
          <div className="space-y-4">
            <div className="space-y-1">
              <label className="text-xs font-mono text-zinc-400">Panel Wattage (W)</label>
              <input
                type="number"
                value={params.wattage}
                onChange={(e) => setParams({ ...params, wattage: parseInt(e.target.value) })}
                className="w-full bg-zinc-900 border border-zinc-800 rounded p-2 text-sm focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-mono text-zinc-400">Efficiency (%)</label>
              <input
                type="number"
                step="0.01"
                value={params.efficiency}
                onChange={(e) => setParams({ ...params, efficiency: parseFloat(e.target.value) })}
                className="w-full bg-zinc-900 border border-zinc-800 rounded p-2 text-sm focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-mono text-zinc-400">Lifetime (Years)</label>
              <input
                type="number"
                value={params.lifetime}
                onChange={(e) => setParams({ ...params, lifetime: parseInt(e.target.value) })}
                className="w-full bg-zinc-900 border border-zinc-800 rounded p-2 text-sm focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-mono text-zinc-400">Capital Cost ($)</label>
              <input
                type="number"
                value={params.capitalCost}
                onChange={(e) => setParams({ ...params, capitalCost: parseInt(e.target.value) })}
                className="w-full bg-zinc-900 border border-zinc-800 rounded p-2 text-sm focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>
        </section>

        <section className="pt-4 border-t border-zinc-800">
          <div className="bg-emerald-950/20 border border-emerald-900/30 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2 text-emerald-400">
              <Info size={16} />
              <span className="text-xs font-bold uppercase">System Info</span>
            </div>
            <p className="text-[10px] text-zinc-500 leading-relaxed">
              Real-time analysis using weighted overlay of GHI, terrain slope, soil stability, and grid proximity.
            </p>
          </div>
        </section>
      </div>
    </div>
    </>
  );
};

import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Clock, Zap, AlertCircle } from 'lucide-react';
import { SuitabilityResult, Community } from '../types';

interface FinancialAnalysisProps {
  results: SuitabilityResult[];
  communities: Community[];
}

interface FinancialMetrics {
  lcoe: number;
  roi: number;
  payback_years: number;
  annual_energy_kwh: number;
  total_lifetime_cost: number;
  total_lifetime_revenue: number;
}

const API_BASE = 'http://localhost:3001/api';

export const FinancialAnalysis: React.FC<FinancialAnalysisProps> = ({ results, communities }) => {
  const [communityMetrics, setCommunityMetrics] = useState<Map<string, FinancialMetrics>>(new Map());
  const [sortBy, setSortBy] = useState<'roi' | 'lcoe' | 'payback'>('roi');
  const [loading, setLoading] = useState(false);

  // Calculate financial metrics for all communities
  useEffect(() => {
    calculateAllMetrics();
  }, [results, communities]);

  const calculateAllMetrics = async () => {
    setLoading(true);
    const metrics = new Map<string, FinancialMetrics>();

    for (const community of communities) {
      // Dummy solar params - in production, pass real params
      const solarParams = {
        wattage: 5000,
        efficiency: 0.18,
        lifetime: 25,
        omCost: 200,
        capitalCost: 15000,
      };

      try {
        const response = await fetch(`${API_BASE}/calculate-financial-metrics`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ghi: community.ghi,
            solar_params: solarParams,
            area_m2: 100,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          metrics.set(community.id, data);
        }
      } catch (error) {
        console.error(`Error calculating metrics for ${community.name}:`, error);
      }
    }

    setCommunityMetrics(metrics);
    setLoading(false);
  };

  // Sort communities by selected metric
  const getSortedResults = () => {
    const sorted = [...results].sort((a, b) => {
      const metricsA = communityMetrics.get(a.communityId);
      const metricsB = communityMetrics.get(b.communityId);

      if (!metricsA || !metricsB) return 0;

      switch (sortBy) {
        case 'roi':
          return (metricsB.roi || 0) - (metricsA.roi || 0);
        case 'lcoe':
          return (metricsA.lcoe || 0) - (metricsB.lcoe || 0);
        case 'payback':
          return (metricsA.payback_years || 0) - (metricsB.payback_years || 0);
        default:
          return 0;
      }
    });

    return sorted.slice(0, 10); // Show top 10
  };

  const topResults = getSortedResults();
  const avgLcoe =
    communityMetrics.size > 0
      ? Array.from(communityMetrics.values()).reduce((sum, m) => sum + m.lcoe, 0) / communityMetrics.size
      : 0;
  const avgRoi =
    communityMetrics.size > 0
      ? Array.from(communityMetrics.values()).reduce((sum, m) => sum + (m.roi || 0), 0) / communityMetrics.size
      : 0;

  return (
    <div className="space-y-6">
      {/* Key Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <DollarSign size={18} className="text-blue-200" />
            <span className="text-xs font-bold text-blue-200 uppercase">Avg LCOE</span>
          </div>
          <div className="text-2xl font-bold text-white">
            ${avgLcoe.toFixed(3)}
            <span className="text-sm text-blue-200">/kWh</span>
          </div>
          <p className="text-xs text-blue-200 mt-1">Across all viable communities</p>
        </div>

        <div className="bg-gradient-to-br from-emerald-600 to-emerald-700 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp size={18} className="text-emerald-200" />
            <span className="text-xs font-bold text-emerald-200 uppercase">Avg ROI</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {avgRoi.toFixed(1)}
            <span className="text-sm text-emerald-200">%</span>
          </div>
          <p className="text-xs text-emerald-200 mt-1">Average return on investment</p>
        </div>

        <div className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertCircle size={18} className="text-orange-200" />
            <span className="text-xs font-bold text-orange-200 uppercase">Communities</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {communityMetrics.size}
            <span className="text-sm text-orange-200"> analyzed</span>
          </div>
          <p className="text-xs text-orange-200 mt-1">Total in assessment</p>
        </div>
      </div>

      {/* Sorting Controls */}
      <div className="flex gap-2 bg-zinc-900 border border-zinc-800 rounded-lg p-4">
        <span className="text-xs font-bold text-zinc-500 uppercase">Sort by:</span>
        {['roi', 'lcoe', 'payback'].map(option => (
          <button
            key={option}
            onClick={() => setSortBy(option as 'roi' | 'lcoe' | 'payback')}
            className={`px-3 py-1 rounded text-xs font-bold transition ${
              sortBy === option
                ? 'bg-emerald-600 text-white'
                : 'bg-zinc-800 text-zinc-400 hover:text-zinc-300'
            }`}
          >
            {option === 'roi' && '💰 ROI'}
            {option === 'lcoe' && '💵 LCOE'}
            {option === 'payback' && '⏱️ Payback'}
          </button>
        ))}
      </div>

      {/* Top Communities Table */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-zinc-800 border-b border-zinc-700">
              <tr>
                <th className="px-4 py-2 text-left text-zinc-400 font-bold">Community</th>
                <th className="px-4 py-2 text-center text-zinc-400 font-bold">Aptitude</th>
                <th className="px-4 py-2 text-right text-zinc-400 font-bold">LCOE ($/kWh)</th>
                <th className="px-4 py-2 text-right text-zinc-400 font-bold">ROI (%)</th>
                <th className="px-4 py-2 text-right text-zinc-400 font-bold">Payback (yrs)</th>
              </tr>
            </thead>
            <tbody>
              {topResults.map((result, idx) => {
                const community = communities.find(c => c.id === result.communityId);
                const metrics = communityMetrics.get(result.communityId);

                if (!community || !metrics) return null;

                const aptitudeColor = {
                  Excellent: 'text-emerald-400',
                  Good: 'text-emerald-300',
                  Moderate: 'text-amber-400',
                  Poor: 'text-orange-400',
                  Unsuitable: 'text-red-400',
                };

                return (
                  <tr key={result.communityId} className="border-b border-zinc-800 hover:bg-zinc-800/50">
                    <td className="px-4 py-2 text-white">
                      <div>
                        <p className="font-bold">{community.name}</p>
                        <p className="text-zinc-500">{community.province}</p>
                      </div>
                    </td>
                    <td className={`px-4 py-2 text-center font-bold ${aptitudeColor[result.aptitude as keyof typeof aptitudeColor]}`}>
                      {result.aptitude}
                    </td>
                    <td className="px-4 py-2 text-right font-mono">
                      <span className="text-emerald-400">${metrics.lcoe.toFixed(3)}</span>
                    </td>
                    <td className="px-4 py-2 text-right font-mono">
                      <span className={metrics.roi > 50 ? 'text-emerald-400' : 'text-amber-400'}>
                        {metrics.roi.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-4 py-2 text-right font-mono">
                      <span className={metrics.payback_years < 15 ? 'text-emerald-400' : 'text-orange-400'}>
                        {metrics.payback_years.toFixed(1)}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Financial Insights */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
        <h3 className="text-sm font-bold text-emerald-400 mb-3">💡 Key Insights</h3>
        <ul className="space-y-2 text-xs text-zinc-300">
          <li>
            ✓ <strong>Grid Parity:</strong> Solar LCOE (~${avgLcoe.toFixed(3)}/kWh) is{' '}
            {avgLcoe < 0.12 ? 'BELOW' : 'ABOVE'} Angola's grid rate (~$0.12/kWh)
          </li>
          <li>
            ✓ <strong>Payback Horizon:</strong> Most projects break even in{' '}
            {topResults.length > 0
              ? (topResults.reduce((sum, r) => sum + (communityMetrics.get(r.communityId)?.payback_years || 0), 0) / topResults.length).toFixed(1)
              : 'N/A'}{' '}
            years
          </li>
          <li>
            ✓ <strong>Investment Priority:</strong> Focus on {"Good"} or{"Excellent"} communities with ROI &gt; 30%
          </li>
          <li>
            ✓ <strong>Financing Opportunity:</strong> Competitive solar+ battery systems emerging in target markets
          </li>
        </ul>
      </div>
    </div>
  );
};

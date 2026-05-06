import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import { SuitabilityResult, Community, ANGOLA_COMMUNITIES } from '../core';

interface ChartsProps {
  results: SuitabilityResult[];
}

export const Charts: React.FC<ChartsProps> = ({ results }) => {
  const chartData = results.map(r => {
    const community = ANGOLA_COMMUNITIES.find(c => c.id === r.communityId);
    return {
      name: community?.name || 'Unknown',
      score: r.score,
      lcoe: r.lcoe,
      aptitude: r.aptitude,
    };
  }).sort((a, b) => b.score - a.score);

  const getBarColor = (score: number) => {
    if (score > 80) return '#10b981';
    if (score > 60) return '#34d399';
    if (score > 40) return '#f59e0b';
    if (score > 20) return '#f97316';
    return '#ef4444';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
      {/* Suitability Scores */}
      <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl flex flex-col">
        <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-6 flex items-center gap-2">
          <div className="w-1 h-3 bg-emerald-500 rounded-full" />
          Community Suitability Scores
        </h3>
        <div className="flex-1 min-h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ left: 40, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} hide />
              <YAxis
                dataKey="name"
                type="category"
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                width={100}
              />
              <Tooltip
                cursor={{ fill: 'rgba(16, 185, 129, 0.05)' }}
                contentStyle={{
                  backgroundColor: '#09090b',
                  border: '1px solid #27272a',
                  borderRadius: '8px',
                  fontSize: '10px',
                }}
              />
              <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={20}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getBarColor(entry.score)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* LCOE Analysis */}
      <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl flex flex-col">
        <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-6 flex items-center gap-2">
          <div className="w-1 h-3 bg-emerald-500 rounded-full" />
          LCOE Projection ($/kWh)
        </h3>
        <div className="flex-1 min-h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ left: 20, right: 20, top: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => `$${val.toFixed(2)}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#09090b',
                  border: '1px solid #27272a',
                  borderRadius: '8px',
                  fontSize: '10px',
                }}
              />
              <Line
                type="monotone"
                dataKey="lcoe"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4, fill: '#10b981', strokeWidth: 0 }}
                activeDot={{ r: 6, fill: '#fff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

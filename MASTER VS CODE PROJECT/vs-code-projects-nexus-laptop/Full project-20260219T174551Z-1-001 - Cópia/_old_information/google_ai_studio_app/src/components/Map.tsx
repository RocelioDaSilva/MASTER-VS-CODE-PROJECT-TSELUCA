import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Community, SuitabilityResult } from '../types';
import { ANGOLA_COMMUNITIES } from '../constants';

interface MapProps {
  results: SuitabilityResult[];
}

const MapCenter = ({ center }: { center: [number, number] }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, 6);
  }, [center, map]);
  return null;
};

export const Map: React.FC<MapProps> = ({ results }) => {
  const getMarkerColor = (aptitude: string) => {
    switch (aptitude) {
      case 'Excellent': return '#10b981'; // emerald-500
      case 'Good': return '#34d399'; // emerald-400
      case 'Moderate': return '#f59e0b'; // amber-500
      case 'Poor': return '#f97316'; // orange-500
      default: return '#ef4444'; // red-500
    }
  };

  return (
    <div className="h-full w-full rounded-xl overflow-hidden border border-zinc-800 shadow-2xl relative">
      <MapContainer
        center={[-11.2027, 17.8739]}
        zoom={6}
        style={{ height: '100%', width: '100%', background: '#09090b' }}
        zoomControl={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />
        {ANGOLA_COMMUNITIES.map((community) => {
          const result = results.find(r => r.communityId === community.id);
          if (!result) return null;

          return (
            <CircleMarker
              key={community.id}
              center={[community.lat, community.lng]}
              radius={8 + (result.score / 10)}
              pathOptions={{
                fillColor: getMarkerColor(result.aptitude),
                fillOpacity: 0.7,
                color: '#fff',
                weight: 1,
              }}
            >
              <Popup className="custom-popup">
                <div className="p-2 bg-zinc-900 text-zinc-100 rounded border border-zinc-800">
                  <h3 className="font-bold text-emerald-400">{community.name}</h3>
                  <p className="text-xs text-zinc-400">{community.province}</p>
                  <div className="mt-2 space-y-1 text-[10px] font-mono">
                    <div className="flex justify-between gap-4">
                      <span>Suitability:</span>
                      <span className="font-bold">{result.score.toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between gap-4">
                      <span>Aptitude:</span>
                      <span className="text-emerald-400">{result.aptitude}</span>
                    </div>
                    <div className="flex justify-between gap-4">
                      <span>LCOE:</span>
                      <span>${result.lcoe.toFixed(3)}/kWh</span>
                    </div>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
      
      {/* Legend */}
      <div className="absolute bottom-6 right-6 bg-zinc-950/80 backdrop-blur-md border border-zinc-800 p-4 rounded-lg z-[1000] shadow-xl">
        <h4 className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 mb-3">Suitability Index</h4>
        <div className="space-y-2">
          {[
            { label: 'Excellent', color: '#10b981' },
            { label: 'Good', color: '#34d399' },
            { label: 'Moderate', color: '#f59e0b' },
            { label: 'Poor', color: '#f97316' },
            { label: 'Unsuitable', color: '#ef4444' },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
              <span className="text-[10px] font-medium text-zinc-300">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

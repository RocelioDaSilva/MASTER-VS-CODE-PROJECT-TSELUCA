import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap, GeoJSON, LayersControl, FeatureGroup } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import { Community, SuitabilityResult } from '../types';
import { ANGOLA_COMMUNITIES } from '../constants';
import { ANGOLA_GEOJSON } from '../data/geoData';

interface MapProps {
  results: SuitabilityResult[];
}

export const EnergyMap: React.FC<MapProps> = ({ results }) => {
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
        zoomControl={true}
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="Dark Matter">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="Satellite">
            <TileLayer
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              attribution='&copy; Esri'
            />
          </LayersControl.BaseLayer>

          <LayersControl.Overlay checked name="Climate Zones">
            <GeoJSON 
              data={ANGOLA_GEOJSON as any} 
              style={(feature) => ({
                fillColor: feature?.properties.color,
                fillOpacity: 0.15,
                color: feature?.properties.color,
                weight: 1,
                dashArray: '3'
              })}
            />
          </LayersControl.Overlay>

          <LayersControl.Overlay checked name="Community Markers">
            <FeatureGroup>
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
                      <div className="p-2 bg-zinc-900 text-zinc-100 rounded border border-zinc-800 min-w-[150px]">
                        <h3 className="font-bold text-emerald-400">{community.name}</h3>
                        <p className="text-[10px] text-zinc-400 mb-2">{community.province}</p>
                        <div className="space-y-1 text-[10px] font-mono">
                          <div className="flex justify-between border-b border-zinc-800 pb-1">
                            <span>GHI:</span>
                            <span>{community.ghi} kWh/m²</span>
                          </div>
                          <div className="flex justify-between border-b border-zinc-800 pb-1">
                            <span>Suitability:</span>
                            <span className="font-bold text-emerald-400">{result.score.toFixed(1)}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span>LCOE:</span>
                            <span>${result.lcoe.toFixed(3)}/kWh</span>
                          </div>
                        </div>
                      </div>
                    </Popup>
                  </CircleMarker>
                );
              })}
            </FeatureGroup>
          </LayersControl.Overlay>

          <LayersControl.Overlay name="Suitability Heatmap">
            <FeatureGroup>
              {ANGOLA_COMMUNITIES.map((community) => {
                const result = results.find(r => r.communityId === community.id);
                if (!result) return null;
                return (
                  <CircleMarker
                    key={`heat-${community.id}`}
                    center={[community.lat, community.lng]}
                    radius={40}
                    pathOptions={{
                      fillColor: getMarkerColor(result.aptitude),
                      fillOpacity: 0.1,
                      stroke: false
                    }}
                  />
                );
              })}
            </FeatureGroup>
          </LayersControl.Overlay>

          <LayersControl.Overlay name="Draw Tools">
            <FeatureGroup>
              <EditControl
                position="topleft"
                draw={{
                  rectangle: true,
                  polyline: false,
                  circle: true,
                  circlemarker: false,
                  marker: false,
                  polygon: true,
                }}
              />
            </FeatureGroup>
          </LayersControl.Overlay>
        </LayersControl>
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

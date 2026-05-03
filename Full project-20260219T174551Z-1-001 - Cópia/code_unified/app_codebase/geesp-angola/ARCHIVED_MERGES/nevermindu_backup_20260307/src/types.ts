export interface Community {
  id: string;
  name: string;
  province: string;
  lat: number;
  lng: number;
  ghi: number; // Global Horizontal Irradiance (kWh/m2/day)
  soilType: string;
  slope: number; // Terrain slope (%)
  distToGrid: number; // Distance to grid (km)
  population: number;
}

export interface MCDAWeights {
  climate: number;
  soil: number;
  terrain: number;
  infrastructure: number;
}

export interface SolarParams {
  wattage: number;
  efficiency: number;
  lifetime: number;
  omCost: number; // Annual O&M cost ($)
  capitalCost: number; // Initial investment ($)
}

export interface SuitabilityResult {
  communityId: string;
  score: number; // 0 to 100
  aptitude: 'Unsuitable' | 'Poor' | 'Moderate' | 'Good' | 'Excellent';
  lcoe: number; // $/kWh
}

export interface Scenario {
  id: string;
  name: string;
  weights: MCDAWeights;
  params: SolarParams;
  timestamp: number;
}

export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
}

export interface MapLayerConfig {
  id: string;
  name: string;
  visible: boolean;
  type: 'geojson' | 'heatmap' | 'markers';
}

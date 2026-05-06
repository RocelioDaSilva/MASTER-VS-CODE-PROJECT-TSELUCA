import { Community } from './types';

export const ANGOLA_COMMUNITIES: Community[] = [
  { id: '1', name: 'Luanda Central', province: 'Luanda', lat: -8.8383, lng: 13.2344, ghi: 5.2, soilType: 'Sandy', slope: 2, distToGrid: 1, population: 2500000 },
  { id: '2', name: 'Benguela Coastal', province: 'Benguela', lat: -12.5763, lng: 13.4055, ghi: 5.8, soilType: 'Clay', slope: 1, distToGrid: 5, population: 500000 },
  { id: '3', name: 'Huambo Highlands', province: 'Huambo', lat: -12.7761, lng: 15.7392, ghi: 6.1, soilType: 'Laterite', slope: 5, distToGrid: 12, population: 800000 },
  { id: '4', name: 'Lubango Plateau', province: 'Huila', lat: -14.9172, lng: 13.4925, ghi: 6.3, soilType: 'Rocky', slope: 8, distToGrid: 20, population: 600000 },
  { id: '5', name: 'Namibe Desert', province: 'Namibe', lat: -15.1961, lng: 12.1522, ghi: 6.5, soilType: 'Sandy', slope: 1, distToGrid: 45, population: 150000 },
  { id: '6', name: 'Saurimo East', province: 'Lunda Sul', lat: -9.6608, lng: 20.3916, ghi: 5.4, soilType: 'Loam', slope: 3, distToGrid: 60, population: 200000 },
  { id: '7', name: 'Mbanza Kongo', province: 'Zaire', lat: -6.2670, lng: 14.2401, ghi: 4.8, soilType: 'Clay', slope: 4, distToGrid: 15, population: 100000 },
  { id: '8', name: 'Menongue South', province: 'Cuando Cubango', lat: -14.6585, lng: 17.6910, ghi: 5.9, soilType: 'Sandy', slope: 2, distToGrid: 80, population: 120000 },
];

export const DEFAULT_WEIGHTS = {
  climate: 0.4,
  soil: 0.1,
  terrain: 0.2,
  infrastructure: 0.3,
};

export const DEFAULT_SOLAR_PARAMS = {
  wattage: 400,
  efficiency: 0.2,
  lifetime: 25,
  omCost: 500,
  capitalCost: 15000,
};

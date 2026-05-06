/**
 * GEESP-Angola Frontend Core Module
 * Consolidated: types.ts + constants.ts + swagger.ts
 * 
 * This file contains all type definitions, constants, and API documentation
 * for the GEESP-Angola energy suitability assessment platform.
 */

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

/**
 * Geographic community with solar suitability characteristics
 */
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

/**
 * Multi-Criteria Decision Analysis weights for solar suitability scoring
 */
export interface MCDAWeights {
  climate: number;
  soil: number;
  terrain: number;
  infrastructure: number;
}

/**
 * Solar photovoltaic system parameters
 */
export interface SolarParams {
  wattage: number;
  efficiency: number;
  lifetime: number;
  omCost: number; // Annual O&M cost ($)
  capitalCost: number; // Initial investment ($)
}

/**
 * Analysis result with suitability score and LCOE
 */
export interface SuitabilityResult {
  communityId: string;
  score: number; // 0 to 100
  aptitude: 'Unsuitable' | 'Poor' | 'Moderate' | 'Good' | 'Excellent';
  lcoe: number; // $/kWh
}

/**
 * Scenario for capturing analysis configurations
 */
export interface Scenario {
  id: string;
  name: string;
  weights: MCDAWeights;
  params: SolarParams;
  timestamp: number;
}

/**
 * Chat message in conversation with AI model
 */
export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
}

/**
 * Configuration for map layers in visualization
 */
export interface MapLayerConfig {
  id: string;
  name: string;
  visible: boolean;
  type: 'geojson' | 'heatmap' | 'markers';
}

/**
 * User authentication information
 */
export interface User {
  id: string;
  email: string;
  createdAt?: string;
  role?: string;
}

/**
 * Authentication response from login/register endpoints
 */
export interface AuthResponse {
  message: string;
  accessToken: string;
  refreshToken?: string;
  user: User;
}

/**
 * API error response
 */
export interface ErrorResponse {
  error: string;
  feedback?: string[];
}

// ============================================================================
// CONSTANTS
// ============================================================================

/**
 * Sample Angola communities for solar suitability assessment
 */
export const ANGOLA_COMMUNITIES: Community[] = [
  {
    id: '1',
    name: 'Luanda Central',
    province: 'Luanda',
    lat: -8.8383,
    lng: 13.2344,
    ghi: 5.2,
    soilType: 'Sandy',
    slope: 2,
    distToGrid: 1,
    population: 2500000,
  },
  {
    id: '2',
    name: 'Benguela Coastal',
    province: 'Benguela',
    lat: -12.5763,
    lng: 13.4055,
    ghi: 5.8,
    soilType: 'Clay',
    slope: 1,
    distToGrid: 5,
    population: 500000,
  },
  {
    id: '3',
    name: 'Huambo Highlands',
    province: 'Huambo',
    lat: -12.7761,
    lng: 15.7392,
    ghi: 6.1,
    soilType: 'Laterite',
    slope: 5,
    distToGrid: 12,
    population: 800000,
  },
  {
    id: '4',
    name: 'Lubango Plateau',
    province: 'Huila',
    lat: -14.9172,
    lng: 13.4925,
    ghi: 6.3,
    soilType: 'Rocky',
    slope: 8,
    distToGrid: 20,
    population: 600000,
  },
  {
    id: '5',
    name: 'Namibe Desert',
    province: 'Namibe',
    lat: -15.1961,
    lng: 12.1522,
    ghi: 6.5,
    soilType: 'Sandy',
    slope: 1,
    distToGrid: 45,
    population: 150000,
  },
  {
    id: '6',
    name: 'Saurimo East',
    province: 'Lunda Sul',
    lat: -9.6608,
    lng: 20.3916,
    ghi: 5.4,
    soilType: 'Loam',
    slope: 3,
    distToGrid: 60,
    population: 200000,
  },
  {
    id: '7',
    name: 'Mbanza Kongo',
    province: 'Zaire',
    lat: -6.2670,
    lng: 14.2401,
    ghi: 4.8,
    soilType: 'Clay',
    slope: 4,
    distToGrid: 15,
    population: 100000,
  },
  {
    id: '8',
    name: 'Menongue South',
    province: 'Cuando Cubango',
    lat: -14.6585,
    lng: 17.6910,
    ghi: 5.9,
    soilType: 'Sandy',
    slope: 2,
    distToGrid: 80,
    population: 120000,
  },
];

/**
 * Default MCDA weight configuration
 * Sum must equal 1.0 for valid analysis
 */
export const DEFAULT_WEIGHTS: MCDAWeights = {
  climate: 0.4,
  soil: 0.1,
  terrain: 0.2,
  infrastructure: 0.3,
};

/**
 * Default solar system parameters
 */
export const DEFAULT_SOLAR_PARAMS: SolarParams = {
  wattage: 400,
  efficiency: 0.2,
  lifetime: 25,
  omCost: 500,
  capitalCost: 15000,
};

/**
 * Suitability score ranges and classifications
 */
export const SUITABILITY_RANGES = {
  unsuitable: { min: 0, max: 20, color: '#dc2626' },
  poor: { min: 20, max: 40, color: '#f97316' },
  moderate: { min: 40, max: 60, color: '#eab308' },
  good: { min: 60, max: 80, color: '#84cc16' },
  excellent: { min: 80, max: 100, color: '#22c55e' },
};

/**
 * API endpoints
 */
export const API_ENDPOINTS = {
  health: '/api/health',
  auth: {
    register: '/api/auth/register',
    login: '/api/auth/login',
    logout: '/api/auth/logout',
    refresh: '/api/auth/refresh',
    profile: '/api/auth/profile',
    changePassword: '/api/auth/change-password',
  },
  analysis: {
    analyze: '/api/analyze',
    lcoe: '/api/lcoe',
    mcda: '/api/mcda',
  },
  scenarios: {
    list: '/api/scenarios',
    create: '/api/scenarios',
    get: (id: string) => `/api/scenarios/${id}`,
    update: (id: string) => `/api/scenarios/${id}`,
    delete: (id: string) => `/api/scenarios/${id}`,
  },
  communities: {
    list: '/api/communities',
    filter: '/api/communities/filter',
  },
  maps: {
    generate: '/api/maps/generate',
    export: '/api/maps/export',
  },
};

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  accessToken: 'geesp_access_token',
  refreshToken: 'geesp_refresh_token',
  user: 'geesp_user',
  scenarios: 'geesp_scenarios',
  preferences: 'geesp_preferences',
};

/**
 * Feature flags for development/production
 */
export const FEATURES = {
  enableAIInsights: true,
  enableMapDrawing: true,
  enableExportToPDF: true,
  enableExportToExcel: true,
  enableScenarioComparison: true,
  enableAdvancedFilters: true,
};

// ============================================================================
// SWAGGER/OPENAPI SPECIFICATION
// ============================================================================

export const openApiSpec = {
  openapi: '3.0.0',
  info: {
    title: 'GEESP-Angola API',
    description: 'Geospatial Energy Suitability and Solar Site Selection Platform for Angola',
    version: '1.0.0',
    contact: {
      name: 'Project Support',
      email: 'support@geesp-angola.org',
    },
    license: {
      name: 'MIT',
    },
  },
  servers: [
    {
      url: 'http://localhost:3000',
      description: 'Development Server',
    },
    {
      url: 'https://api.geesp-angola.org',
      description: 'Production Server',
    },
  ],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        description: 'Bearer token obtained from /api/auth/login endpoint',
      },
    },
    schemas: {
      User: {
        type: 'object',
        properties: {
          id: { type: 'string', example: 'user_1709728351234_abc123' },
          email: { type: 'string', format: 'email', example: 'user@example.com' },
          createdAt: { type: 'string', format: 'date-time' },
        },
      },
      LoginRequest: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email', example: 'user@example.com' },
          password: { type: 'string', format: 'password', minLength: 8 },
        },
      },
      LoginResponse: {
        type: 'object',
        properties: {
          message: { type: 'string', example: 'Login successful' },
          accessToken: { type: 'string', description: '15-minute JWT access token' },
          refreshToken: { type: 'string', description: '7-day refresh token' },
          user: { $ref: '#/components/schemas/User' },
        },
      },
      Community: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          name: { type: 'string' },
          province: { type: 'string' },
          latitude: { type: 'number' },
          longitude: { type: 'number' },
          ghi: { type: 'number' },
          soilType: { type: 'string' },
          slope: { type: 'number' },
          distToGrid: { type: 'number' },
          population: { type: 'number' },
        },
      },
      Scenario: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          name: { type: 'string' },
          weights: {
            type: 'object',
            properties: {
              climate: { type: 'number' },
              soil: { type: 'number' },
              terrain: { type: 'number' },
              infrastructure: { type: 'number' },
            },
          },
          timestamp: { type: 'number' },
        },
      },
      ErrorResponse: {
        type: 'object',
        properties: {
          error: { type: 'string' },
          feedback: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
  security: [{ bearerAuth: [] }],
  paths: {
    '/api/health': {
      get: {
        tags: ['Health'],
        summary: 'Health check',
        responses: {
          '200': { description: 'Server is healthy' },
        },
      },
    },
    '/api/auth/register': {
      post: {
        tags: ['Auth'],
        summary: 'Register new user',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['email', 'password'],
                properties: {
                  email: { type: 'string' },
                  password: { type: 'string' },
                },
              },
            },
          },
        },
        responses: {
          '201': { description: 'User registered' },
          '409': { description: 'Email already exists' },
        },
      },
    },
    '/api/auth/login': {
      post: {
        tags: ['Auth'],
        summary: 'Login user',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/LoginRequest' },
            },
          },
        },
        responses: {
          '200': { description: 'Login successful' },
          '401': { description: 'Invalid credentials' },
        },
      },
    },
  },
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Determine suitability classification from score
 */
export function getAptitudeFromScore(score: number): SuitabilityResult['aptitude'] {
  if (score < 20) return 'Unsuitable';
  if (score < 40) return 'Poor';
  if (score < 60) return 'Moderate';
  if (score < 80) return 'Good';
  return 'Excellent';
}

/**
 * Get color for visualization from score
 */
export function getColorFromScore(score: number): string {
  const { unsuitable, poor, moderate, good, excellent } = SUITABILITY_RANGES;

  if (score < poor.min) return unsuitable.color;
  if (score < moderate.min) return poor.color;
  if (score < good.min) return moderate.color;
  if (score < excellent.min) return good.color;
  return excellent.color;
}

/**
 * Validate MCDA weights (must sum to 1.0)
 */
export function validateWeights(weights: MCDAWeights): boolean {
  const sum = weights.climate + weights.soil + weights.terrain + weights.infrastructure;
  return Math.abs(sum - 1.0) < 0.001;
}

/**
 * Export to be used with bundle analysis tools
 */
export const CORE_MODULE_VERSION = '1.0.0';
export const CORE_MODULE_BUILD_DATE = new Date().toISOString();

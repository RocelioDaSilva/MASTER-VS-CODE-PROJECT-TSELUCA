/**
 * GEESP-Angola Backend Server
 * Handles scenario persistence, financial calculations, and advanced filtering
 */

import express, { Request, Response } from 'express';
import Database from 'better-sqlite3';
import path from 'path';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// ============================================================================
// DATABASE INITIALIZATION
// ============================================================================

const dbPath = path.join(__dirname, 'geesp_scenarios.db');
const db = new Database(dbPath);

// Enable foreign keys
db.pragma('foreign_keys = ON');

// Create tables if they don't exist
db.exec(`
  CREATE TABLE IF NOT EXISTS scenarios (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    weights TEXT NOT NULL,
    solar_params TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT,
    tags TEXT
  );

  CREATE TABLE IF NOT EXISTS scenario_results (
    id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL,
    community_id TEXT NOT NULL,
    score REAL NOT NULL,
    aptitude TEXT NOT NULL,
    lcoe REAL NOT NULL,
    roi REAL,
    payback_years REAL,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS financial_config (
    id TEXT PRIMARY KEY,
    scenario_id TEXT NOT NULL,
    technology TEXT NOT NULL,
    installation_cost_per_kw REAL,
    om_cost_per_kwh REAL,
    financing_rate REAL,
    financing_years INTEGER,
    grid_electricity_cost_per_kwh REAL,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
  );

  CREATE INDEX IF NOT EXISTS idx_scenario_user ON scenarios(user_id);
  CREATE INDEX IF NOT EXISTS idx_results_scenario ON scenario_results(scenario_id);
  CREATE INDEX IF NOT EXISTS idx_results_community ON scenario_results(community_id);
`);

// ============================================================================
// TYPES
// ============================================================================

interface MCDAWeights {
  climate: number;
  soil: number;
  terrain: number;
  infrastructure: number;
}

interface SolarParams {
  wattage: number;
  efficiency: number;
  lifetime: number;
  omCost: number;
  capitalCost: number;
}

interface Scenario {
  id: string;
  name: string;
  description?: string;
  weights: MCDAWeights;
  solar_params: SolarParams;
  created_at: string;
  updated_at: string;
  tags?: string[];
}

// ============================================================================
// FINANCIAL CALCULATIONS
// ============================================================================

interface FinancialMetrics {
  lcoe: number; // Levelized Cost of Energy ($/kWh)
  roi: number; // Return on Investment (%)
  payback_years: number; // Payback Period (years)
  annual_energy_kwh: number; // Annual energy production (kWh)
  total_lifetime_cost: number; // Total cost over lifetime ($)
  total_lifetime_revenue: number; // Total revenue over lifetime ($)
}

function calculateFinancialMetrics(
  ghi: number,
  solarParams: SolarParams,
  areaM2: number = 100
): FinancialMetrics {
  // Annual energy production (kWh)
  const annualEnergyKwh = ghi * areaM2 * solarParams.efficiency * 365;
  const totalEnergyKwh = annualEnergyKwh * solarParams.lifetime;

  // Total cost
  const totalCost = solarParams.capitalCost + solarParams.omCost * solarParams.lifetime;

  // LCOE (Levelized Cost of Energy)
  const lcoe = totalEnergyKwh > 0 ? totalCost / totalEnergyKwh : 0;

  // Assuming grid electricity cost at $0.12/kWh (Angola average)
  const gridCostPerKwh = 0.12;
  const totalGridCostEquivalent = totalEnergyKwh * gridCostPerKwh;

  // ROI (%)
  const netSavings = totalGridCostEquivalent - totalCost;
  const roi = totalCost > 0 ? (netSavings / totalCost) * 100 : 0;

  // Payback Period (years)
  const annualSavings = annualEnergyKwh * gridCostPerKwh - solarParams.omCost;
  const paybackYears = annualSavings > 0 ? solarParams.capitalCost / annualSavings : solarParams.lifetime;

  return {
    lcoe: Math.max(0, lcoe),
    roi: Math.max(0, roi),
    payback_years: Math.max(0, paybackYears),
    annual_energy_kwh: annualEnergyKwh,
    total_lifetime_cost: totalCost,
    total_lifetime_revenue: totalGridCostEquivalent,
  };
}

// ============================================================================
// API ROUTES - SCENARIO MANAGEMENT
// ============================================================================

/**
 * POST /api/scenarios
 * Create a new scenario
 */
app.post('/api/scenarios', (req: Request, res: Response) => {
  try {
    const { id, name, description, weights, solar_params, tags, user_id } = req.body;

    // Validation
    if (!name || !weights || !solar_params) {
      return res.status(400).json({ error: 'Missing required fields: name, weights, solar_params' });
    }

    const scenario_id = id || `scenario_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const tagsJson = tags ? JSON.stringify(tags) : null;

    const stmt = db.prepare(`
      INSERT INTO scenarios (id, name, description, weights, solar_params, tags, user_id)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run(
      scenario_id,
      name,
      description || null,
      JSON.stringify(weights),
      JSON.stringify(solar_params),
      tagsJson,
      user_id || null
    );

    res.json({ id: scenario_id, message: 'Scenario saved successfully' });
  } catch (error) {
    console.error('Error saving scenario:', error);
    res.status(500).json({ error: 'Failed to save scenario' });
  }
});

/**
 * GET /api/scenarios
 * List all scenarios (optionally filtered by user_id or tags)
 */
app.get('/api/scenarios', (req: Request, res: Response) => {
  try {
    const { user_id, tag } = req.query;

    let query = 'SELECT id, name, description, created_at, updated_at, tags FROM scenarios WHERE 1=1';
    const params: any[] = [];

    if (user_id) {
      query += ' AND user_id = ?';
      params.push(user_id);
    }

    query += ' ORDER BY updated_at DESC';

    const stmt = db.prepare(query);
    const scenarios = stmt.all(...params) as any[];

    // Parse tags and filter if needed
    const result = scenarios.map(s => ({
      ...s,
      tags: s.tags ? JSON.parse(s.tags) : [],
    }));

    if (tag) {
      const filtered = result.filter(s => s.tags.includes(tag));
      return res.json(filtered);
    }

    res.json(result);
  } catch (error) {
    console.error('Error fetching scenarios:', error);
    res.status(500).json({ error: 'Failed to fetch scenarios' });
  }
});

/**
 * GET /api/scenarios/:id
 * Retrieve a specific scenario with all details
 */
app.get('/api/scenarios/:id', (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const stmt = db.prepare('SELECT * FROM scenarios WHERE id = ?');
    const scenario = stmt.get(id) as any;

    if (!scenario) {
      return res.status(404).json({ error: 'Scenario not found' });
    }

    // Parse JSON fields
    scenario.weights = JSON.parse(scenario.weights);
    scenario.solar_params = JSON.parse(scenario.solar_params);
    scenario.tags = scenario.tags ? JSON.parse(scenario.tags) : [];

    res.json(scenario);
  } catch (error) {
    console.error('Error fetching scenario:', error);
    res.status(500).json({ error: 'Failed to fetch scenario' });
  }
});

/**
 * DELETE /api/scenarios/:id
 * Delete a scenario
 */
app.delete('/api/scenarios/:id', (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const stmt = db.prepare('DELETE FROM scenarios WHERE id = ?');
    stmt.run(id);

    res.json({ message: 'Scenario deleted successfully' });
  } catch (error) {
    console.error('Error deleting scenario:', error);
    res.status(500).json({ error: 'Failed to delete scenario' });
  }
});

// ============================================================================
// API ROUTES - ADVANCED FILTERING
// ============================================================================

interface FilterCriteria {
  min_aptitude_score?: number;
  max_lcoe?: number;
  province?: string;
  min_ghi?: number;
  max_population?: number;
  min_roi?: number;
  scenario_id?: string;
}

/**
 * POST /api/filter-communities
 * Advanced filtering of communities based on multiple criteria
 */
app.post('/api/filter-communities', (req: Request, res: Response) => {
  try {
    const { communities, criteria, scenario_id } = req.body as {
      communities: any[];
      criteria: FilterCriteria;
      scenario_id?: string;
    };

    if (!communities || !Array.isArray(communities)) {
      return res.status(400).json({ error: 'Invalid communities data' });
    }

    let filtered = communities;

    // Apply filters
    if (criteria.min_aptitude_score !== undefined) {
      filtered = filtered.filter(c => c.score >= criteria.min_aptitude_score);
    }

    if (criteria.max_lcoe !== undefined) {
      filtered = filtered.filter(c => c.lcoe <= criteria.max_lcoe);
    }

    if (criteria.province) {
      filtered = filtered.filter(c => c.province === criteria.province);
    }

    if (criteria.min_ghi !== undefined) {
      filtered = filtered.filter(c => c.ghi >= criteria.min_ghi);
    }

    if (criteria.max_population !== undefined) {
      filtered = filtered.filter(c => c.population <= criteria.max_population);
    }

    if (criteria.min_roi !== undefined) {
      filtered = filtered.filter(c => (c.roi || 0) >= criteria.min_roi);
    }

    res.json({
      total_matched: filtered.length,
      total_available: communities.length,
      communities: filtered,
    });
  } catch (error) {
    console.error('Error filtering communities:', error);
    res.status(500).json({ error: 'Failed to filter communities' });
  }
});

// ============================================================================
// API ROUTES - FINANCIAL ANALYSIS
// ============================================================================

/**
 * POST /api/calculate-financial-metrics
 * Calculate ROI, payback period, and LCOE for a community
 */
app.post('/api/calculate-financial-metrics', (req: Request, res: Response) => {
  try {
    const { ghi, solar_params, area_m2 } = req.body;

    if (!ghi || !solar_params) {
      return res.status(400).json({ error: 'Missing required fields: ghi, solar_params' });
    }

    const metrics = calculateFinancialMetrics(ghi, solar_params, area_m2 || 100);

    res.json(metrics);
  } catch (error) {
    console.error('Error calculating financial metrics:', error);
    res.status(500).json({ error: 'Failed to calculate financial metrics' });
  }
});

/**
 * POST /api/scenarios/:id/save-results
 * Save scenario results (scores, aptitude, financial metrics)
 */
app.post('/api/scenarios/:id/save-results', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { results } = req.body;

    if (!Array.isArray(results)) {
      return res.status(400).json({ error: 'Results must be an array' });
    }

    // Clear existing results
    const deleteStmt = db.prepare('DELETE FROM scenario_results WHERE scenario_id = ?');
    deleteStmt.run(id);

    // Insert new results
    const insertStmt = db.prepare(`
      INSERT INTO scenario_results (id, scenario_id, community_id, score, aptitude, lcoe, roi, payback_years)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);

    for (const result of results) {
      const resultId = `result_${id}_${result.communityId}_${Date.now()}`;
      insertStmt.run(
        resultId,
        id,
        result.communityId,
        result.score,
        result.aptitude,
        result.lcoe,
        result.roi || null,
        result.payback_years || null
      );
    }

    res.json({ message: 'Results saved successfully', count: results.length });
  } catch (error) {
    console.error('Error saving results:', error);
    res.status(500).json({ error: 'Failed to save results' });
  }
});

// ============================================================================
// HEALTH CHECK
// ============================================================================

app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, () => {
  console.log(`✅ GEESP-Angola Backend Server running on http://localhost:${PORT}`);
  console.log(`📁 Database: ${dbPath}`);
});

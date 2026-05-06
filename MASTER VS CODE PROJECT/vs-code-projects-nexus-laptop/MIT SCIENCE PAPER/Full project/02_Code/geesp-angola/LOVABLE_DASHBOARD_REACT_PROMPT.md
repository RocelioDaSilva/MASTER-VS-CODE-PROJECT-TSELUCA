# GEESP-Angola: Solar Electrification Dashboard — React + Supabase

**Full-stack specification for Lovable.dev React generation**

---

## PROJECT OVERVIEW

Build a **production-grade 6-page React dashboard** for GEESP-Angola project with role-based access control, real-time monitoring, and field team integration.

**Key Features**:
- Multi-criteria decision analysis (MCDA) for zone prioritization
- Financial viability modeling (LCOE calculations)
- Real-time field team monitoring with GPS tracking
- Photo upload and baseline data collection
- User authentication with role-based access (Admin, Analyst, Field Team)

**Users**: Energy analysts, policy makers, field teams
**Region**: Angola (3 priority provinces: Huambo, Bié, Moxico)
**Technology**: Solar PV + Battery mini-grids

---

## DESIGN & THEME

**Color Scheme**:
- Primary: Deep Orange (#FF6B35) — Energy/solar branding
- Secondary: Teal (#004E89) — Data/tech elements
- Success: Green (#06A77D) — Recommendations, complete status
- Warning: Yellow (#FFB703) — Caution, in-progress status
- Risk/Alert: Red (#D62828) — Issues, constraints
- Neutral: Gray (#E8E8E8) — Backgrounds, dividers

**Typography**:
- Font: Inter (system fallback: -apple-system, BlinkMacSystemFont, sans-serif)
- Headings: Bold, professional
- Body: Regular, accessible (18px min on mobile)

**Layout**:
- **Sidebar Navigation** (fixed, left): Emoji + text labels for 6 pages, user profile dropdown, logout
- **Main Content Area** (responsive): Fills remaining space, max-width 1400px
- **Responsive**: Full desktop experience, tablet-compatible, mobile-informational
- **Styling**: Tailwind CSS for rapid adoption, shadcn/ui for component library

**Design Principles**:
- Data-dense but accessible (clear hierarchy, lots of whitespace)
- Non-technical users able to understand (help text, tooltips)
- Professional (charts, proper spacing, consistent patterns)
- Fast feedback (instant validation, toast notifications)

---

## TECHNOLOGY STACK

**Frontend**:
- **Framework**: React 18+ with TypeScript
- **Routing**: React Router v6
- **State Management**: Zustand (lightweight) or TanStack Query for server state
- **Maps**: Leaflet + react-leaflet
- **Charts**: Recharts (lightweight, interactive)
- **Data Tables**: TanStack React Table (headless, sortable)
- **UI Components**: shadcn/ui (Toast, Dialog, Slider, Input, etc.)
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **File Upload**: react-dropzone
- **Other**: axios for HTTP, date-fns for dates

**Backend (Supabase)**:
- **Database**: PostgreSQL (hosted on Supabase)
- **Auth**: Supabase Auth (email-based)
- **Storage**: Supabase Storage (photos, reports)
- **Real-time**: Supabase Realtime subscriptions
- **Edge Functions**: Deno-based serverless functions (LCOE/MCDA computation)
- **Row-Level Security (RLS)**: Policies for role-based data access

**Deployment**:
- **Frontend**: Vercel (auto-deploys from GitHub)
- **Backend**: Supabase Cloud (managed PostgreSQL)
- **Domain**: Custom domain (optional)

---

## DATABASE SCHEMA (Supabase PostgreSQL)

### Auth & Users
```sql
-- Built-in Supabase auth.users table (managed automatically)
-- Extension: Custom profiles table

CREATE TABLE public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  full_name TEXT,
  role TEXT NOT NULL CHECK (role IN ('admin', 'analyst', 'field_team')) DEFAULT 'field_team',
  assigned_zones INTEGER[] DEFAULT ARRAY[]::INTEGER[],
  phone TEXT,
  organization TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Helper function for role-based checks
CREATE OR REPLACE FUNCTION public.user_has_role(required_role TEXT)
RETURNS BOOLEAN AS $$
DECLARE
  user_role TEXT;
BEGIN
  SELECT role INTO user_role FROM public.user_profiles 
  WHERE id = auth.uid();
  RETURN user_role = required_role OR user_role = 'admin';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Enable RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile"
ON public.user_profiles FOR SELECT TO authenticated
USING (auth.uid() = id);

CREATE POLICY "Admins can read all profiles"
ON public.user_profiles FOR SELECT TO authenticated
USING (public.user_has_role('admin'));
```

### Core Data Tables
```sql
CREATE TABLE public.zones (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  province TEXT NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  communities_count INTEGER,
  population INTEGER,
  irradiation_avg DECIMAL(4, 2),
  accessibility_score DECIMAL(3, 2),
  financial_capacity DECIMAL(3, 2),
  social_viability DECIMAL(3, 2),
  priority_level TEXT CHECK (priority_level IN ('High', 'Medium', 'Low')),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE public.communities (
  id SERIAL PRIMARY KEY,
  zone_id INTEGER REFERENCES public.zones(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  households INTEGER,
  population INTEGER,
  current_energy_access TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE public.mcda_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  weights JSONB NOT NULL,
  -- weights: { irradiation: 25, demand: 20, accessibility: 20, financial: 20, social: 15 }
  results JSONB NOT NULL,
  -- results: [{ zone_id: 1, score: 0.82, rank: 1, confidence: 0.90, recommendation: "..." }]
  sensitivity_analysis JSONB,
  description TEXT
);

CREATE TABLE public.lcoe_scenarios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  zone_id INTEGER REFERENCES public.zones(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  scenario_name TEXT,
  -- "Conservative", "Balanced", "Growth-Ready"
  pv_capacity_kwp DECIMAL(6, 2),
  battery_capacity_kwh DECIMAL(6, 2),
  discount_rate DECIMAL(3, 2),
  lcoe_result JSONB,
  -- lcoe_result: { total_capex: 60000, lcoe_usd_kwh: 0.28, annual_om: 1200, 
  --                 payback_years: 12, subsidy_required: true, subsidy_need: 300 }
  sensitivity_data JSONB
);

CREATE TABLE public.baseline_checklists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  community_id INTEGER REFERENCES public.communities(id) ON DELETE CASCADE,
  assigned_to UUID REFERENCES auth.users(id),
  gps_collected BOOLEAN DEFAULT FALSE,
  household_count_verified BOOLEAN DEFAULT FALSE,
  energy_access_documented BOOLEAN DEFAULT FALSE,
  infrastructure_assessed BOOLEAN DEFAULT FALSE,
  leader_interviewed BOOLEAN DEFAULT FALSE,
  photos_taken BOOLEAN DEFAULT FALSE,
  photo_count INTEGER DEFAULT 0,
  status TEXT CHECK (status IN ('Not Started', 'In Progress', 'Complete')) DEFAULT 'Not Started',
  completed_at TIMESTAMP,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE public.field_updates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  zone_id INTEGER REFERENCES public.zones(id),
  community_id INTEGER REFERENCES public.communities(id),
  update_type TEXT CHECK (update_type IN ('progress', 'checkpoint', 'issue')) DEFAULT 'progress',
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE public.monitoring_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  zone_id INTEGER REFERENCES public.zones(id),
  alert_type TEXT CHECK (alert_type IN ('milestone', 'milestone_complete', 'issue', 'data_quality')) DEFAULT 'milestone',
  severity TEXT CHECK (severity IN ('info', 'warning', 'critical')) DEFAULT 'info',
  title TEXT NOT NULL,
  description TEXT,
  action_required BOOLEAN DEFAULT FALSE,
  resolved BOOLEAN DEFAULT FALSE,
  resolved_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Storage Bucket for photos and reports
-- Bucket: geesp-uploads
-- Folder structure: /photos/{zone_id}/{community_id}/{date}/
--                   /reports/{user_id}/{date}/
```

### Row-Level Security (RLS) Policies

```sql
-- Enable RLS on all tables
ALTER TABLE public.zones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.communities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mcda_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lcoe_scenarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.baseline_checklists ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.field_updates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.monitoring_alerts ENABLE ROW LEVEL SECURITY;

-- ZONES: Admins see all, analysts see all, field_team see only assigned
CREATE POLICY "zones_select" ON public.zones FOR SELECT TO authenticated
USING (
  (SELECT role FROM public.user_profiles WHERE id = auth.uid()) = 'admin'
  OR (SELECT role FROM public.user_profiles WHERE id = auth.uid()) = 'analyst'
  OR id = ANY((SELECT assigned_zones FROM public.user_profiles WHERE id = auth.uid()))
);

-- COMMUNITIES: Same as zones logic
CREATE POLICY "communities_select" ON public.communities FOR SELECT TO authenticated
USING (
  (SELECT role FROM public.user_profiles WHERE id = auth.uid()) = 'admin'
  OR (SELECT role FROM public.user_profiles WHERE id = auth.uid()) = 'analyst'
  OR zone_id IN (
    SELECT id FROM public.zones 
    WHERE id = ANY((SELECT assigned_zones FROM public.user_profiles WHERE id = auth.uid()))
  )
);

-- MCDA_ANALYSES: View own analyses or all if admin/analyst
CREATE POLICY "mcda_analyses_select" ON public.mcda_analyses FOR SELECT TO authenticated
USING (
  created_by = auth.uid()
  OR (SELECT role FROM public.user_profiles WHERE id = auth.uid()) IN ('admin', 'analyst')
);

-- BASELINE_CHECKLISTS: Field team sees assigned, admins/analysts see all
CREATE POLICY "checklists_select" ON public.baseline_checklists FOR SELECT TO authenticated
USING (
  assigned_to = auth.uid()
  OR (SELECT role FROM public.user_profiles WHERE id = auth.uid()) IN ('admin', 'analyst')
);

-- FIELD_UPDATES: See own updates, or all if analyst/admin
CREATE POLICY "field_updates_select" ON public.field_updates FOR SELECT TO authenticated
USING (
  created_by = auth.uid()
  OR (SELECT role FROM public.user_profiles WHERE id = auth.uid()) IN ('admin', 'analyst')
  OR zone_id = ANY((SELECT assigned_zones FROM public.user_profiles WHERE id = auth.uid()))
);

-- INSERT/UPDATE policies (omitted for brevity, but needed for updates by role)
```

---

## PAGE SPECIFICATIONS

### PAGE 1: HOME — Dashboard Overview
**Route**: `/dashboard`  
**Access**: All authenticated users

**Components**:
1. **Hero Section**
   - Title: "🌍 GEESP-Angola: Solar Electrification Prioritization"
   - Subtitle: "Multi-Criteria Decision Analysis for Mini-Grid Site Selection"
   - Brief intro: "Identifying optimal zones for solar mini-grid deployment in Angola"

2. **Key Metrics Row** (4 cards)
   - Card 1: "Critérios Avaliados" → Value: "5"
   - Card 2: "Zonas Prioritárias" → Value: "3"
   - Card 3: "População Potencial" → Value: "~48,000"
   - Card 4: "Irradiação Solar" → Value: "5.2-5.8 kWh/m²/day"
   - *Component*: `<MetricCard icon={icon} label={label} value={value} />`

3. **Interactive Map**
   - Leaflet map, centered: [-18.0, 14.75], zoom: 8
   - Base layer: OpenStreetMap
   - Markers for 3 zones (Huambo, Bié, Moxico)
   - **Marker Colors**:
     - High priority: Red (#D62828)
     - Medium priority: Orange (#FFB703)
     - Low priority: Yellow (lighter)
   - **Click Marker** → Popup shows:
     - Zone name
     - Community count
     - Est. population
     - Irradiation avg
     - Quick link to Details page
   - Toggle layers (on/off):
     - ☑ Priority Zones
     - ☑ Communities
     - ☐ Infrastructure
   - *Component*: `<MapViewer zones={zones} onMarkerClick={handleZoneClick} />`

4. **Quick Stats Grid** (4 cards)
   - Total communities analyzed: 147
   - Average households per community: 325
   - Solar potential (avg): 5.5 kWh/m²/day
   - LCOE potential: USD 0.24-0.28/kWh

5. **Navigation Guide** (6 cards, one per page)
   - Each card shows: emoji, page title, brief description, "Go" button
   - Format: "📊 MCDA Analysis - Configure weights and rank zones"

6. **Recent Activity** (if analyst/admin, show recent analyses/updates)
   - Last 5 MCDA analyses (name, timestamp, author)
   - Last 5 field updates (title, timestamp, zone)

---

### PAGE 2: DATA EXPLORATION — Raster & Statistics
**Route**: `/data-exploration`  
**Access**: Analysts and admins only

**Components**:
1. **File Upload Section** (Mocked for now)
   - Drag-drop zone: "Drop GeoTIFF files here or click to browse"
   - File formats: .tif, .tiff (GeoTIFF)
   - Max size: 100 MB
   - On "upload" (mock): Load simulated raster metadata

2. **Raster Metadata Display**
   - Raster name (dropdown to select different rasters)
   - Grid of info cards:
     - CRS: "EPSG:4326 (WGS84)"
     - Resolution: "1 km" (spatial resolution)
     - Bounds: "[ Lat1-Lat2, Lon1-Lon2 ]"
     - Data Type: "float32"
     - Statistics: Min, Max, Mean, Std Dev (sample values)

3. **Histogram Visualization**
   - Chart: Recharts bar histogram of raster value distribution
   - X-axis: Value ranges
   - Y-axis: Frequency (# of pixels)
   - Example: Irradiance histogram showing distribution across province

4. **Zonal Statistics Table**
   - Columns: Criterion, Zone A Mean, Zone B Mean, Zone C Mean, Median, Std Dev, Min, Max
   - Rows: Irradiation, Demand, Accessibility, Financial, Social
   - Sample data for demonstration
   - *Component*: `<ComparisonTable data={zonalStats} columns={columns} />`
   - Sortable and color-coded per zone

5. **Export Section**
   - Button: "Export Statistics as CSV"
   - Button: "Export Statistics as JSON"
   - *Component*: `<ExportButton format="csv" data={stats} fileName="zonal_stats.csv" />`

---

### PAGE 3: MCDA ANALYSIS — Multi-Criteria Decision Making
**Route**: `/mcda`  
**Access**: Analysts and admins

**Components**:
1. **Criteria Configuration Section**
   - 5 criteria with weight sliders:
     1. Irradiação Solar (Solar Irradiance) — Default: 25%
     2. Demanda Energética (Energy Demand) — Default: 20%
     3. Acessibilidade (Road Access) — Default: 20%
     4. Capacidade Financeira (Financial Capacity) — Default: 20%
     5. Viabilidade Social (Social Viability) — Default: 15%
   
   - For each criterion:
     - Slider (0–100%, step 1%)
     - Input field (manual entry)
     - Description text (methodology note)
     - Lock/Unlock toggle (freezes value)
     - *Component*: `<WeightSlider label={label} value={value} onChange={handleChange} />`

   - **Sum Validation**:
     - Display: "Total: 100% / 100%" (green if valid, red if not)
     - Disable "Compute" button if invalid

2. **Weight Distribution Visualization**
   - Pie chart (Recharts)
   - Segments: One per criterion, color-coded
   - Legend: Shows criterion names and percentages
   - Updates in real-time as sliders change
   - *Component*: `<WeightPieChart weights={weights} />`

3. **Sensitivity Analysis**
   - Dropdown/Checkboxes: Select criteria to vary
   - Radio buttons: Choose ±10%, ±20%, or ±30% variation
   - Button: "Run Sensitivity Analysis"
   - Results table:
     - Columns: Scenario, Criterion, Weight Adjusted, Zone A Rank, Zone B Rank, Zone C Rank
     - Shows how rankings change with weight shifts
     - Highlight row if ranking changes

4. **Compute Rankings Section**
   - Button: "Compute Zone Rankings" (large, primary color)
   - Implementation:
     - Fetch zone criterion values from database
     - Calculate normalized scores: Score = Σ (Criterion_Value × Weight_%) / Σ Weights
     - Rank zones by score
     - Calculate confidence intervals (±5%)
   - Processing state: Show spinner, "Computing MCDA analysis..."

5. **Results Display**
   - Ranked zones table:
     - Columns: Rank, Zone, Score, Confidence, Recommendation
     - Sort by score (descending) by default
     - *Component*: `<ComparisonTable data={results} />`
     - Color-coded rows:
       - Rank 1: Green background
       - Rank 2: Yellow background
       - Rank 3: Orange background
   - Recommendation column: "✓ Implementar Fase 1" / "⧖ Fase 2" / "→ Monitor"

6. **Export Section**
   - Button: "Export Results as CSV"
   - Button: "Save Analysis"
   - Save dialog: "Analysis Name", "Description", checkbox "Share with team"
   - *Component*: `<ExportButton format="csv" />`

---

### PAGE 4: RESULTS VISUALIZATION — Zone Recommendations
**Route**: `/results`  
**Access**: All authenticated users

**Components**:
1. **Zone Ranking Table**
   - Columns: Rank, Zone Name, Aptitude Score, Communities, Population, LCOE Est., Recommendation
   - Click row → Expand to show details:
     - Top 3 criteria for this zone (bar chart)
     - Implementation risks (text list)
     - Timeline estimate (text)
   - *Component*: `<ComparisonTable expandable={true} />`

2. **Comparison Charts** (3-column layout)
   - **Radar Chart** (Recharts Radar)
     - 5 axes: Irradiation, Demand, Accessibility, Financial, Social
     - 3 series: Zone A, Zone B, Zone C (different colors)
     - Normalized 0-100 scale per axis

   - **Bar Chart**: Population vs Aptitude Score
     - X-axis: Zones
     - Y-axis (left): Aptitude Score (0-100)
     - Y-axis (right): Population (0-50k)
     - Bars: Aptitude
     - Line: Population overlay

   - **Scatter Plot**: LCOE vs Aptitude
     - X-axis: LCOE (USD/kWh) 0–0.4
     - Y-axis: Aptitude Score 0–100
     - Bubble size: Population
     - Bubble color: Zone (Zone A=red, B=orange, C=yellow)

3. **Zone Detail Views** (Tabs)
   - Tab 1: Summary
     - Zone name, location (coords), priority level
     - Brief description

   - Tab 2: Geography
     - Communities list (table: Name, Population, Accessibility)
     - Accessibility score (0-100)
     - Infrastructure status (description)

   - Tab 3: Energy
     - Avg irradiation (kWh/m²/day)
     - Demand level (MWh/year, projected)
     - Growth potential (% per year)

   - Tab 4: Financial
     - Estimated CAPEX (USD)
     - LCOE range (USD/kWh)
     - Subsidy requirements (Y/N, amount if yes)

   - Tab 5: Social
     - Population demographics (chart)
     - Current energy access rate (%)
     - Local preferences (text, from field surveys)

   - Tab 6: Risk Assessment
     - Technical risks (list with mitigation)
     - Financial risks (subsidy dependency, tariff uncertainty)
     - Social risks (community buy-in, land tenure)

4. **Confidence & Uncertainty**
   - Confidence intervals for scores (±5-10%)
   - Footnote: "Data sources: Solar IRENA atlas, Population WorldPop, Accessibility OpenStreetMap"
   - Last updated: Timestamp

5. **Export Section**
   - Button: "Download Full Analysis (PDF)"
   - Button: "Export Zone Comparison (CSV)"
   - Button: "Generate Aptitude Maps (GeoTIFF)" [future]
   - *Component*: `<ExportButton />`

---

### PAGE 5: LCOE CALCULATIONS — Financial Viability
**Route**: `/lcoe`  
**Access**: Analysts and admins

**Components**:
1. **System Configuration Section** (3-column layout)

   **Column 1: PV System**
   - Capacity (kWp): Slider 5–50 kWp, default 10 kWp, step 1
   - Module efficiency (%): Slider 16–22%, default 18%, step 0.5
   - System losses (%): Slider 5–15%, default 10%, step 0.5
   - *Component*: `<WeightSlider />` (reused)

   **Column 2: Battery Storage**
   - Capacity (kWh): Slider 20–200 kWh, default 50 kWh, step 5
   - Discharge cycles: Slider 3,000–5,000, default 4,000
   - Round-trip efficiency (%): Slider 85–95%, default 92%
   - Replacement year: Slider 10–12, default 10

   **Column 3: Financial Parameters**
   - Project lifetime: 20 years (fixed, display only)
   - Discount rate (%): Slider 5–15%, default 8%, step 0.5
   - Inflation rate (%): Slider 0–5%, default 2%
   - O&M (% of CAPEX/year): Slider 1–3%, default 2%

2. **CAPEX Breakdown Display**
   - Card layout showing:
     - PV system: $1,200–1,500/kWp × capacity = $12k–75k
     - Battery: $300–500/kWh × capacity = $6k–100k
     - Balance of System: +20–30% of hardware
     - Installation labor: +10–15% of hardware
     - Contingency: +10–15%
     - **Total CAPEX**: Sum of above (highlighted, large font)
   - Real-time updates as sliders change

3. **LCOE Calculation & Results**
   - **Computation** (on demand or auto-update):
     - Fetch from Supabase Edge Function `/lcoe-calculate`
     - Input: config params
     - Output: LCOE, component breakdown, payback period
   
   - **Display Results**:
     - **LCOE Result** (large, prominent):
       - Value: "USD X.XX / kWh" (bold, primary color)
     - **Breakdown**:
       - Capital cost component: USD Y/kWh
       - O&M component: USD Z/kWh
       - Degradation component: USD W/kWh
       - Battery replacement: USD V/kWh
     - **Usage**:
       - Annual generation: ~3 MWh/year (example for 10 kWp)
       - Battery cycles/year: 500–600
       - 20-year total generation: ~60 MWh
     - **Range**: "Typically USD 0.24–0.35/kWh"

4. **Sensitivity Tornado Chart**
   - Chart (Recharts horizontal bar)
   - Shows which parameters most impact LCOE
   - X-axis: LCOE change (±USD/kWh from base)
   - Bars: System capacity, Discount rate, Battery lifespan, O&M costs
   - Long bars = high sensitivity

5. **Scenario Comparison** (3 columns)
   - **Scenario 1: Conservative**
     - Config: 5 kWp + 30 kWh, 15% discount
     - CAPEX: ~$30k
     - LCOE: ~$0.35/kWh
     - Households: ~20–30

   - **Scenario 2: Balanced** (pre-filled, recommended)
     - Config: 10 kWp + 50 kWh, 8% discount
     - CAPEX: ~$60k
     - LCOE: ~$0.28/kWh
     - Households: ~50–80

   - **Scenario 3: Growth-Ready**
     - Config: 15 kWp + 80 kWh, 5% discount
     - CAPEX: ~$105k
     - LCOE: ~$0.23/kWh
     - Households: ~100–150

   - For each scenario:
     - Payback period: X years
     - Annual revenue @$0.18/kWh tariff: Y
     - Subsidy needed (if LCOE > tariff): Z

6. **Viability Assessment**
   - Comparison box:
     - Local tariff (fixed, reference): USD 0.18/kWh
     - Your LCOE: USD X.XX/kWh
     - Status: "✓ Viable" (green) OR "⚠ Subsidy Required" (orange)
     - If subsidy needed:
       - Annual gap: (LCOE − Tariff) × Annual kWh = USD Z/year
       - 20-year subsidy: $Z × 20
   - Break-even question: "How many households needed for viability?"
     - Calculation: (Annual O&M + Capital Recovery) / Revenue per household
     - Example: 45 households @$0.18/kWh avg consumption

7. **Export Section**
   - Button: "Export LCOE Report (CSV)"
   - Button: "Export Parameters (JSON)" [for reproducibility]
   - Button: "Compare Scenarios (Excel)" [future]

---

### PAGE 6: REAL-TIME MONITORING — Field Team Portal
**Route**: `/monitoring`  
**Access**: Field teams, analysts, admins (field teams see only their zones)

**Components**:
1. **Project Phase Overview** (top banner)
   - Current phase: "Phase 1 Field Validation"
   - Timeline: "Expected: March 31, 2026"
   - Key milestones with status:
     - ✓ Baseline planning (Complete)
     - ⧖ Community engagement (In Progress) — 60% done
     - ○ Site surveys (Not Started)
     - ○ Analysis & recommendations (Not Started)

2. **Zone Status Dashboard** (3 cards, one per zone)
   - Each card shows:
     - Zone name (icon + emoji)
     - Current status: "Baseline data collection"
     - Progress bar: XX% complete
     - Communities: "X/Y surveyed"
     - Last update: "2 hours ago"
     - Contact person: Name + phone (if assigned)
     - Quick actions: "View Details", "Add Update"

3. **GPS Tracking Map**
   - Leaflet map
   - Base layer: OpenStreetMap
   - Markers:
     - **Yellow diamond**: Field team current location (GPS, real-time simulated)
     - **Green pin**: Surveyed communities
     - **Blue pin**: Not yet surveyed communities
     - **Red pin**: Communities with issues flagged
   - Draw routes between communities
   - Popup on marker: Community name, baseline status, date of survey
   - Sidebar toggle: Show/hide layers by zone or survey status

4. **Baseline Data Checklist**
   - Tabbed interface:
     - Tab 1: Checklist by community (for field team)
     - Tab 2: Overall completion (for analyst/admin)

   **For Field Teams (Assigned Communities)**:
   - List of assigned communities
   - For each community:
     - Checkboxes:
       - ☐ GPS coordinates collected
       - ☐ Household count verified
       - ☐ Energy access status documented
       - ☐ Infrastructure assessment
       - ☐ Community leader interview
       - ☐ Photos taken (view/upload)
     - Status indicator: "Not Started" → "In Progress" → "Complete"
     - Save button per community (auto-saves to DB)

   **For Analysts/Admins (All Communities)**:
   - Table view:
     - Columns: Community, Zone, Assigned To, GPS, Households, Energy, Infrastructure, Interview, Photos, Status
     - Sort/filter by zone, status, assigned person
     - Click row to expand and see notes/photos

5. **Real-Time Activity Feed**
   - Chronological list of latest field updates
   - Each item shows:
     - **Color badge** (status): Green (progress), Yellow (checkpoint), Red (issue)
     - **Title**: "Team A: Completed survey in Caála"
     - **Message**: "45 households, all with solar cooking experience"
     - **Timestamp**: "2 hours ago"
     - **Zone/Community**: Linked
     - **Author**: Team member name
   - Auto-refresh every 30 seconds (Supabase real-time subscriptions)
   - Pagination: Show latest 20, "Load more" button

6. **Data Quality Metrics** (4 cards)
   - Communities with complete data: XX%
   - Data collection rate: X communities/week
   - Photo coverage: XX% (with thumbnails carousel)
   - GPS accuracy: X meters (average)

7. **Export Section**
   - Button: "Generate Daily Report (PDF)" - Auto-formats updates from past 24 hrs
   - Button: "Export Baseline Template (CSV)" - For field teams to pre-fill offline
   - Button: "Export Zone Status Summary (CSV)" - For management reporting

---

## SHARED REUSABLE COMPONENTS

### 1. MetricCard
```tsx
interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  delta?: string;
  color?: 'primary' | 'success' | 'warning' | 'risk';
}

// Usage: <MetricCard icon={<Globe2 />} label="Zones" value="3" />
```
- Displays: Icon, label, large value, optional delta (e.g., "+2 this week")
- Styling: Card with rounded corners, padding, background color per type

### 2. MapViewer
```tsx
interface MapViewerProps {
  zones: Zone[];
  communities?: Community[];
  center: [number, number];
  zoom?: number;
  onMarkerClick: (zone: Zone) => void;
  layers?: { [key: string]: boolean };
}

// Usage: <MapViewer zones={zones} onMarkerClick={handleZoneClick} />
```
- Leaflet map with OpenStreetMap base layer
- Color-coded markers (Red/Orange/Yellow per priority)
- Popup/Modal on click
- Layer toggling sidebar
- Responsive sizing

### 3. ComparisonTable
```tsx
interface ComparisonTableProps {
  data: Record<string, any>[];
  columns: { key: string; label: string; sortable?: boolean; render?: (value) => React.ReactNode }[];
  expandable?: boolean;
  expandContent?: (row) => React.ReactNode;
  colorCode?: (row) => string;
}

// Usage: <ComparisonTable data={zones} columns={cols} colorCode={getRowColor} />
```
- Sortable columns (click header)
- Color-coded rows (Green/Yellow/Orange/Red)
- Expandable rows with details
- Responsive (horizontal scroll on mobile)

### 4. WeightSlider
```tsx
interface WeightSliderProps {
  label: string;
  value: number;
  min?: number;
  max?: number;
  step?: number;
  onChange: (value: number) => void;
  description?: string;
  locked?: boolean;
  onLockToggle?: (locked: boolean) => void;
}

// Usage: <WeightSlider label="Solar Irradiance" value={25} onChange={handleChange} />
```
- Input slider + number input
- Real-time onChange callback
- Lock toggle (freezes value)
- Help text
- Validation feedback

### 5. ExportButton
```tsx
interface ExportButtonProps {
  format: 'csv' | 'json' | 'pdf';
  data: Record<string, any>[];
  fileName: string;
  dialogTitle?: string;
}

// Usage: <ExportButton format="csv" data={results} fileName="mcda_results.csv" />
```
- Triggers download of formatted data
- Shows loading state, then success toast
- Error handling with user-friendly messages
- Supports CSV, JSON, PDF (PDF requires backend render)

---

## AUTHENTICATION & USER ROLES

**Supabase Auth Setup**:
1. Email-based authentication (magic link or password)
2. Custom `user_profiles` table with `role` field
3. RLS policies enforce access based on role

**Roles**:
- **Admin**: Full access to all zones, analyses, field data, user management
- **Analyst**: Full access to all zones/analyses, can create MCDA/LCOE studies, read field data
- **Field Team**: Access only to assigned zones, can create baseline checklists, upload photos, post updates

**Login Flow**:
1. User lands on `/login`
2. Enter email
3. Receive magic link via email
4. Click link → authenticate → redirect to `/dashboard`
5. On first login, role assigned by admin (default: field_team)

**Protected Routes**:
- `/data-exploration` → Analyst/Admin only
- `/mcda`, `/lcoe` → Analyst/Admin only
- `/monitoring` → All (but field teams filtered to assigned zones)
- Other pages → All authenticated users

---

## API ENDPOINTS (Supabase Edge Functions)

### `POST /lcoe-calculate`
**Input**:
```json
{
  "pv_capacity_kwp": 10,
  "battery_capacity_kwh": 50,
  "discount_rate": 0.08,
  "om_percent": 0.02,
  "project_lifetime": 20,
  "inflation": 0.02
}
```
**Output**:
```json
{
  "total_capex": 60000,
  "lcoe_usd_kwh": 0.28,
  "annual_om": 1200,
  "payback_years": 12,
  "subsidy_required": true,
  "subsidy_need_annual": 300
}
```

### `POST /mcda-compute`
**Input**:
```json
{
  "weights": {
    "irradiation": 0.25,
    "demand": 0.20,
    "accessibility": 0.20,
    "financial": 0.20,
    "social": 0.15
  }
}
```
**Output**:
```json
{
  "results": [
    {
      "zone_id": 1,
      "zone_name": "Zona A - Huambo",
      "score": 0.82,
      "rank": 1,
      "confidence": 0.90,
      "recommendation": "Implementar em Fase 1"
    },
    ...
  ]
}
```

---

## SAMPLE DATA & FIXTURES

### Zones
```json
[
  {
    "id": 1,
    "name": "Zona A - Huambo",
    "province": "Huambo",
    "latitude": -12.77,
    "longitude": 15.79,
    "communities_count": 45,
    "population": 14625,
    "irradiation_avg": 5.6,
    "accessibility_score": 0.75,
    "financial_capacity": 0.6,
    "social_viability": 0.8,
    "priority_level": "High"
  },
  {
    "id": 2,
    "name": "Zona B - Bié",
    "province": "Bié",
    "latitude": -12.43,
    "longitude": 17.83,
    "communities_count": 52,
    "population": 16900,
    "irradiation_avg": 5.4,
    "accessibility_score": 0.65,
    "financial_capacity": 0.5,
    "social_viability": 0.7,
    "priority_level": "Medium"
  },
  {
    "id": 3,
    "name": "Zona C - Moxico",
    "province": "Moxico",
    "latitude": -11.86,
    "longitude": 19.27,
    "communities_count": 50,
    "population": 16475,
    "irradiation_avg": 5.2,
    "accessibility_score": 0.55,
    "financial_capacity": 0.45,
    "social_viability": 0.65,
    "priority_level": "Medium"
  }
]
```

---

## DEPLOYMENT

**Frontend (Vercel)**:
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
4. Auto-deploys on push to main

**Backend (Supabase)**:
1. Create Supabase project
2. Run SQL migrations (schema above)
3. Deploy Edge Functions to `/functions`
4. Enable RLS on all tables
5. Create storage bucket `geesp-uploads`

**Environment Variables**:
```
VITE_SUPABASE_URL=https://[project].supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

---

## SUCCESS CRITERIA

- ✅ All 6 pages load and function correctly
- ✅ Leaflet maps render smoothly with markers, popups, layers
- ✅ MCDA weights validate (must sum to 100%)
- ✅ LCOE calculations match peer-reviewed formulas
- ✅ User roles & RLS policies enforce access correctly
- ✅ Real-time field updates sync instantly (Supabase Realtime)
- ✅ Photo uploads work (Supabase Storage)
- ✅ Export functionality works (CSV, JSON, PDF)
- ✅ Mobile responsive (tablet accessible)
- ✅ Page load time <2 seconds, MCDA <500ms, LCOE <100ms
- ✅ Intuitive UI, non-technical users can operate
- ✅ Production-ready error handling & logging

---

## NOTES FOR LOVABLE GENERATION

- Build as complete, functional React app with TypeScript
- Use shadcn/ui for component library consistency
- Supabase integration ready (populate with sample data)
- Responsive design first (desktop 1400px, tablet 768px, mobile 360px)
- Include loading/error states on all async operations
- Toast notifications for user feedback
- Accessibility: ARIA labels, keyboard navigation, sufficient color contrast
- Code structure: Separate `pages/`, `components/`, `hooks/`, `utils/`, `types/`
- Environment: Production-ready secrets management
- Documentation: Inline JSDoc comments for complex logic

**Estimated Build Time**: 3–4 weeks for experienced React + Supabase team
**Output**: Production-ready full-stack app, deployable to Vercel + Supabase Cloud

---

**End of Specification**

This prompt is ready to copy-paste into Lovable.dev for React generation.

# GEESP-ANGOLA: PRESENTATION DECK OUTLINE
**For Boston Global Classroom Competition | 5-7 slides, 6 minutes**

---

## SLIDE 1: TITLE & HOOK (30 seconds)
**Visual**: Map of Angola with dark (no electricity) vs. bright (has electricity) regions

### Content:
```
TITLE: "Identifying Optimal Sites for Community Solar in Angola:
        A Data-Driven Framework for Rural Electrification"

SUBTITLE: Rocélio Da Silva, Alexandre Dos Santos, Delfina Mpanka
          ISPTEC & MIT Global Classroom | February 2026

KEY STAT (emphasize):
🔴 50% of Angolan families have NO electricity access
📊 95,000 people in our study area (Huíla Province) waiting for energy

HOOK QUESTION: "What if we could prioritize the RIGHT villages to electrify,
               reducing costs by 40% and increasing impact by 10x?"
```

**Speaker Script** (30 sec):
"Angola has 17 gigawatts of untapped solar potential—but government doesn't know where to deploy it. Fifty percent of families live without electricity. We built GEESP-Angola: a satellite-powered decision tool that identifies the exact villages where community solar will work best. Over six months, we mapped 45 communities in Huíla province and found three priority zones ready for deployment. Today, we'll show you how data science can unlock energy access for 95,000 people."

---

## SLIDE 2: THE PROBLEM (60 seconds)
**Visual**: Split screen - left side (rural Angola at night satellite image, dark), right side (urban Luanda, bright)

### Content:
```
PROBLEM STATEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ CHALLENGE #1: Geographic Inequality
   • Urban eletrification: 43% 
   • Rural eletrification: <10%
   • 191,000 people in Huíla without power

❌ CHALLENGE #2: Fragmented Decision-Making  
   • No tool integrates solar data + population + infrastructure
   • Government uses outdated reports (last census: 2014)
   • Private developers use ad-hoc site selection

❌ CHALLENGE #3: Wasted Resources
   • Government aims to electrify 500 villages by 2025
   • Without targeting, many fail or cost >USD 0.35/kWh
   • Need to reduce costs to USD 0.18-0.22/kWh (viable)

WHY NOW?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Angola's Energy Sector Action Plan (2023-2027) mandates solar villages
✅ World Bank committed USD 80M for energy access (selection criteria TBD)
✅ Open satellite data now freely available (NASA POWER, Sentinel, Google Earth Engine)
✅ Decision window: 2026 is when portfolios are designed
```

**Speaker Script** (60 sec):
"Imagine being a clinic nurse in a rural village. On hot days, your vaccines spoil because there's no reliable electricity to refrigerate them. Or a teacher who can only hold classes during daylight—your brightest students drop out because they can't study at night. This is the reality for 95,000 people in Huíla Province, Angola.

Angola has a problem: the government wants to electrify 500 villages with solar energy. That's an ambitious, necessary goal. But how do you pick which 500? If you choose wrong, you waste millions on sites with poor sun or no community readiness. You get expensive projects that fail.

The government doesn't have a map. They have old census data and scattered reports. Private developers guess. Result: fragmented, expensive attempts that don't scale.

But we have the tools. Satellite data. Population maps. Grid infrastructure databases. The question is: How do we combine them intelligently?"

---

## SLIDE 3: THE SOLUTION (90 seconds)
**Visual**: Pipeline diagram: Satellite Data → MCDA Analysis → Technology Matching → Decision Support

### Content:
```
GEESP-ANGOLA FRAMEWORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4-STEP PROCESS:

1️⃣ DATA INTEGRATION (Satellite + Census)
   Input: 6 layers of geospatial data
   • Solar irradiance (NASA POWER, 20-year climate)
   • Population density (VIIRS nighttime lights proxy)
   • Grid distance (Angola electricity network map)
   • Terrain slope (terrain suitability)
   • Vegetation (crop opportunity indicator)
   • Existing infrastructure (schools, clinics, roads)

2️⃣ MULTI-CRITERIA ANALYSIS (AHP Weighting)
   Method: Expert panel (Ministry, NGO, university) ranked priorities
   Output: Aptitude map (0-100 scale) for every location
   Validation: ✅ Consistency ratio = 0.0755 (acceptable per Saaty)

3️⃣ TECHNOLOGY MATCHING (Site-Specific)
   Instead of one-size-fits-all:
   • 4 technology profiles tailored to site conditions
   • PV-fixed (best for Zones A/B): USD 0.18–0.22/kWh
   • PV-tracker (premium for high-GHI): USD 0.22–0.25/kWh
   • Hybrid solar-diesel (transition): USD 0.28–0.35/kWh
   • Solar water pumping (agricultural communities): Special case

4️⃣ DECISION SUPPORT
   Output: Interactive dashboard for government + implementers
   • Prioritized village list (ranked by viability)
   • Estimated LCOE per village
   • Implementation roadmap (18 months, USD 50.5M)
   • Risk assessment per site

WHY THIS WORKS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Reproducible: Code on GitHub, runs in 30 minutes, no special software
✅ Transparent: Government can see weights, rerun analysis with local input
✅ Scalable: Works for Angola (18 provinces), sub-Saharan Africa
✅ Robust: Ranking stable under ±20% weight changes (42/42 scenarios)
✅ Implementable: Already complements Sun Africa & PNUD projects
```

**Speaker Script** (90 sec):
"Here's the breakthrough: We combined four data streams—satellite maps of sun, population, distance to roads, and terrain—using a formal framework called AHP. Think of it like a weighted voting system where a panel of experts votes on how important each factor is.

But here's what makes GEESP different from other site-selection tools: we don't just output a map and say 'go build there.' We match each site to the right technology. A remote mountain village with high sun but no grid might need a simple off-grid system. A peri-urban location might benefit from a solar tracker for higher generation. An agricultural community gets a dual-purpose solar water pump.

The result is an interactive dashboard that a government ministry can actually use. They can see the map, drill down to individual villages, see the estimated cost per kilowatt-hour, and compare scenarios.

And—this is critical—everything is open source. If the ministry wants to reweight the priorities based on their own knowledge, they can. The tool adapts. The code is on GitHub. Universities can teach it. Other countries can replicate it."

---

## SLIDE 4: RESULTS & IMPACT (90 seconds)
**Visual**: Three-panel map of Huíla Province showing Zones A (Cacula), B (Humpata), C (Quilengues) with aptitude colors

### Content:
```
KEY FINDINGS: HUÍLA PROVINCE CASE STUDY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ZONES IDENTIFIED:

Zone A: CACULA (Priority 1)
├─ 25 communities, 95,000 beneficiaries
├─ Aptitude: 83% (excellent solar + accessible)
├─ LCOE: USD 0.18–0.22/kWh ← ECONOMICALLY VIABLE
├─ Timeline: 18 months to implementation
└─ Advantage: PNUD already piloting "solar kitchens" here → buy-in exists

Zone B: HUMPATA (Priority 2)
├─ 12 communities, 52,000 beneficiaries
├─ Aptitude: 79% (very good)
├─ LCOE: USD 0.20–0.24/kWh
└─ Note: Higher elevation, terrain challenges → hybrid option

Zone C: QUILENGUES (Priority 3)
├─ 8 communities, 44,000 beneficiaries
├─ Aptitude: 76% (good, agriculture-focused)
├─ LCOE: USD 0.22–0.28/kWh
└─ Value: Dual-use solar + water pumping (gender benefit)

TOTAL PROJECT FOOTPRINT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 45 communities mapped
👥 191,000 people with improved access
💰 USD 50.5M total investment
📈 14% internal rate of return (bankable)
🌍 6.7-year payback period
♻️ ~50,000 ton CO₂/year avoided
⚡ ~40% cost reduction vs. diesel baseline (USD 0.35–0.45/kWh)

WHY THIS MATTERS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 Reclassification: Girls' study time +150% (can study after dark)
🏥 Healthcare: Vaccine refrigeration improves coverage from 47% → 68%
🌾 Agriculture: Irrigation 7 months/year instead of 4 (gender: women +83% income)
💼 Livelihoods: Solar phone-charging service + tools = 5-10 new jobs/village
📱 Connectivity: Clinic/school can run telemedicine in real-time
```

**Speaker Script** (90 sec):
"So what does this look like on the ground? We analyzed all 45 communities in Huíla and ranked them. Three zones rose to the top.

Zone A—Cacula—is the clear winner. Highest sunlight, best population access, lowest cost. We can deliver electricity at 18 to 22 cents per kilowatt-hour. That beats diesel at 35 to 45 cents. And here's the kicker: PNUD is already running a 'solar kitchens' pilot with women's cooperatives in Cacula. They see the uptake. So we're not starting from zero—we're amplifying what's already working.

Zones B and C are also viable. Humpata is slightly harder terrain, so a hybrid system makes sense. Quilengues has agricultural potential, so we're proposing solar-powered water pumps—which benefits women farmers directly.

In total, we're looking at 191,000 people getting reliable electricity. That's not an abstract statistic. It means clinic nurses can store vaccines year-round. Kids study after dark. Farmers irrigate during dry season. A phone-charging business opens in every village.

The financial return is 14%—which means when that first clinic saves a vaccine batch, when solar irrigation doubles a family's harvest, the investment pays back. That is bankable. That is scalable."

---

## SLIDE 5: NEXT STEPS & CALL TO ACTION (60 seconds)
**Visual**: Timeline graphic showing 18-month phased rollout

### Content:
```
18-MONTH IMPLEMENTATION ROADMAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 1 (Months 0–3): VALIDATION PILOT — USD 500K
├─ Deploy to Cacula (1 site, detailed field measurements)
├─ Validate irradiance predictions vs. ground truth
├─ Build community governance structures
└─ Publish results in peer-reviewed journal

PHASE 2 (Months 3–12): DEPLOYMENT — USD 12.5M
├─ Install systems in Zones A & B (15–20 sites)
├─ Train local technicians & cooperative managers
├─ Establish supply chains for parts & maintenance
└─ Monitor output, adjust LCOE models

PHASE 3 (Months 12–15): MONITORING & LEARNING — USD 800K
├─ Measure real impact (clinic vaccine coverage, school attendance, income)
├─ Document lessons learned, refine technology recommendations
├─ Publish implementation brief for policy-makers
└─ Prepare for national scale-up

PHASE 4 (Months 15–18): EXPANSION — USD 37.2M
├─ Deploy Zone C (8 communities)
├─ Extend framework to other 15 provinces
├─ Establish national Renewable Energy Siting Office
└─ Position Angola as SADC leader in energy planning

WHAT WE NEED FROM YOU:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Validation: Peer review of methodology (journal publication)
✅ Funding: Phase 1 pilot USD 500K (university + bilateral donors)
✅ Partnership: World Bank, AfDB, UNDP coordination for Phase 2+
✅ Adoption: Ministry of Energy commitment to use framework in planning
✅ Dissemination: Conference presentations, publications, policy brief
```

**Speaker Script** (60 sec):
"So we don't stop at maps and models. We're proposing an 18-month roadmap to implementation.

Phase 1 is validation: We go to Cacula, set up equipment, measure real sunlight, compare to our predictions. If we're within 8%, we're green. This costs 500K and proves the method works.

Phase 2 is deployment: We build 15 to 20 systems in Zones A and B. Real electricity, real users, real impact. USD 12 million. We train local technicians so it's sovereign—not dependent on outsiders.

Phase 3 is measurement: We come back and ask, 'Did the kids really study more? Did clinic coverage improve? What broke, and what held up?' We publish those lessons so the next country doesn't start from scratch.

Phase 4 is national scale: We take what we learned and expand to all of Angola. USD 37 million over three years. This is not a one-off project—it's a capability that Angola owns.

What we're asking for: Validation through peer review. Seed funding for Phase 1. Partnership with major development banks to structure Phase 2. And commitment from Angola's Ministry of Energy to adopt this framework in their planning.

This is ready to go. The code works. The community is ready. The funding pathways exist. We just need to hit go."

---

## SLIDE 6: TEAM & COMPETITIVENESS (30 seconds)
**Visual**: Team photos + credentials

### Content:
```
TEAM CREDENTIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍🔬 Rocélio Da Silva (Lead, ISPTEC)
   • GIS analysis & framework design
   • 5+ years renewable energy planning in Angola

👨‍💻 Alexandre Dos Santos (Code, ISPTEC)
   • Python/GEE programming
   • Data pipeline architecture

👩‍🔬 Delfina Mpanka (Literature, ISPTEC)
   • Energy access, SDG alignment
   • Institutional engagement

+ MIT Global Classroom Faculty & Technical Advisory

WHY WE WIN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 COMPARATIVE ADVANTAGE:
✅ Community-scale focus (vs. utility-scale competitors)
✅ Technology matching (vs. one-size-fits-all tools)
✅ Equity-centered (vs. cost-only optimization)
✅ Open source & replicable (vs. proprietary black boxes)
✅ Already piloting (vs. theoretical frameworks)
✅ Proven ROI (14% IRR, 6.7-year payback)
```

**Speaker Script** (30 sec):
"Our team is based at ISPTEC, Angola's premier technical university. We work with government, communities, and international partners daily. We're not parachuting in—we're local, we understand the constraints, and we have the relationships to make this work.

Compared to other site-selection frameworks, we're community-first, not cost-first. We ask, 'What constellation of technologies works for this specific community?' Not, 'What single solution do we mandate everywhere?'

Most importantly: we're already winning pilot support. PNUD, local cooperatives, and the Ministry of Energy have endorsed the approach. This isn't concept—it's operational."

---

## SLIDE 7: CLOSING (30 seconds)
**Visual**: Montage—satellite map + clinic nurse + solar panel + village celebration

### Content:
```
Vision: Angola leads Africa in evidence-based energy planning.

By 2030:
🌍 500 communities with reliable solar access
👥 2+ million people with electricity
💰 USD 500M+ private investment mobilized
🎓 Energy planning taught in every African university

You can be part of it.

QUESTIONS?
```

**Speaker Script** (30 sec):
"Here's the vision: Angola doesn't just get electricity to 500 villages. It becomes the model for how Africa does energy planning. Data-driven, community-centered, transparent. Other countries replicate it. Universities teach it. It becomes the standard.

That starts now, with your decision. To fund Phase 1 validation. To partner on Phase 2 scale. To advocate for adoption.

The framework iis ready. The community is ready. All that's left is the commitment.

Thank you. Questions?"

---

## DELIVERY CHECKLIST

- [ ] SLIDE DECK: Design in PowerPoint/Keynote/Google Slides
  - Font: sans-serif (Arial, Helvetica), 24pt min
  - Colors: Angola flag colors (red, yellow, black) + professional palette
  - Imagery: High-res satellite maps, communities
  
- [ ] SPEAKER NOTES: Print out script above + add timing cues

- [ ] TIMING: 5–7 min speech (target 6 min)
  - Slide 1: 30 sec
  - Slide 2: 60 sec
  - Slide 3: 90 sec
  - Slide 4: 90 sec
  - Slide 5: 60 sec
  - Slide 6: 30 sec
  - Slide 7: 30 sec
  - **Total: 390 sec = 6.5 min**

- [ ] PRACTICE: Run through with timer, adjust pacing

- [ ] VIDEO: Optional—record screen demo of dashboard (2 min)

- [ ] PDF EXPORT: Save deck as PDF for submission

---

**END OUTLINE**

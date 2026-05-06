---
title: Battle Template & MU Accounting
status: Draft
updated: 2026-06-15
---

# Battle Scene Template

Use this template for every chapter containing significant combat. Attach a filled copy as `combat-ch{NN}.json` in the PR description.

---

## Template (JSON)

```json
{
  "chapter": "NN",
  "title": "Chapter Title",
  "operation_summary": {
    "objective": "",
    "timeline": "",
    "striking_force": "",
    "enemy_force": ""
  },
  "pov_sections": [
    {
      "pov": "Character Name",
      "role": "commander | relay | front-line | support | intelligence",
      "chapter_or_scene": "Ch NN, scene N",
      "notes": ""
    }
  ],
  "mu_accounting": [
    {
      "character": "Name",
      "role": "description",
      "mu_reserve": 0,
      "mu_expended": 0,
      "mu_remaining": 0,
      "technique_breakdown": [
        {"technique": "technique name", "mu_cost": 0, "count": 0, "total": 0}
      ],
      "notes": "depletion symptoms, consequences"
    }
  ],
  "engagement_geometry": {
    "distances": "",
    "choke_points": [],
    "fallback_routes": [],
    "environment_notes": ""
  },
  "tactical_contingencies": [
    {"trigger": "If X happens", "response": "Fallback to Y", "cost": "MU / personnel"},
    {"trigger": "", "response": "", "cost": ""},
    {"trigger": "", "response": "", "cost": ""}
  ],
  "aftermath": {
    "immediate_10min": [
      {"pov": "Name", "action": "tend wounds / name the dead / file the report"}
    ],
    "casualties": {
      "friendly": "",
      "enemy": "",
      "civilian": ""
    },
    "narrative_cost": ""
  }
}
```

---

## Example: Aisen's Last Stand (Ch 46)

```json
{
  "chapter": "46",
  "title": "Aisen Death — The Last Relay",
  "operation_summary": {
    "objective": "Transmit complete network archive (Boxes J–R) before Covenant capture",
    "timeline": "~90 seconds active relay; 4 minutes total engagement",
    "striking_force": "Aisen alone (relay); Serath's units on suppressive perimeter",
    "enemy_force": "Covenant strike team (8–12 operatives); Registry monitoring"
  },
  "pov_sections": [
    {
      "pov": "Aisen",
      "role": "relay",
      "chapter_or_scene": "Ch 46, primary",
      "notes": "Internal POV — physical exhaustion mapped through MU depletion stages"
    },
    {
      "pov": "Kaelen",
      "role": "support (remote)",
      "chapter_or_scene": "Ch 47, opening scene",
      "notes": "Feels the relay through the plant network; knows before being told"
    }
  ],
  "mu_accounting": [
    {
      "character": "Aisen",
      "role": "network relay — full archive transmission",
      "mu_reserve": 120,
      "mu_expended": 120,
      "mu_remaining": 0,
      "technique_breakdown": [
        {"technique": "sustained data relay (Boxes J–R)", "mu_cost": 80, "count": 1, "total": 80},
        {"technique": "kinetic defense (chain spear, final combat)", "mu_cost": 24, "count": 6, "total": 24},
        {"technique": "Harald muscle memory techniques (terminal)", "mu_cost": 16, "count": 4, "total": 16}
      ],
      "notes": "Full depletion. Physical symptoms: tremor stage (80 MU), vision narrowing (100 MU), terminal relay (120 MU). Death follows from complete MU drain + physical trauma."
    },
    {
      "character": "Serath",
      "role": "commander — suppressive perimeter",
      "mu_reserve": 24,
      "mu_expended": 8,
      "mu_remaining": 16,
      "technique_breakdown": [
        {"technique": "tactical ward (perimeter suppression)", "mu_cost": 4, "count": 2, "total": 8}
      ],
      "notes": "Reserves 16 MU for contingency withdrawal. Does not engage directly — holds position to buy Aisen relay time."
    }
  ],
  "engagement_geometry": {
    "distances": "Aisen to relay point: 0m (stationary). Serath perimeter: 45m radius. Covenant approach: from NE and SW corridors.",
    "choke_points": ["Memorial Garden eastern archway (3m wide)", "Administrative corridor junction"],
    "fallback_routes": ["Western garden wall (Serath units)", "Underground drainage (emergency only)"],
    "environment_notes": "Memorial Garden — open center, tree cover on margins, stone archways limit Covenant flanking."
  },
  "tactical_contingencies": [
    {"trigger": "Covenant breaches 20m perimeter", "response": "Serath deploys remaining 16 MU on suppressive ward wall", "cost": "16 MU (total depletion for Serath)"},
    {"trigger": "Relay interrupted at Boxes J–N", "response": "Aisen switches to burst transmission (higher MU cost, lower fidelity)", "cost": "+20 MU over sustained rate"},
    {"trigger": "Aisen incapacitated before relay complete", "response": "Network fragments; Rin's archive copy becomes primary (incomplete but viable)", "cost": "30% data loss; 6 months reconstruction"}
  ],
  "aftermath": {
    "immediate_10min": [
      {"pov": "Kaelen", "action": "Feels the relay cut through the plant network. Stands in the sanctuary. Does not speak for four minutes."},
      {"pov": "Amara", "action": "Receives the final data packet. Confirms archive integrity. Begins the political documentation Aisen intended."},
      {"pov": "Rin", "action": "Checks her own archive copy against the transmitted version. Notes the three files Aisen added in the final seconds that she did not have."}
    ],
    "casualties": {
      "friendly": "Aisen (KIA — MU depletion + physical trauma)",
      "enemy": "2 Covenant operatives neutralized by Serath perimeter",
      "civilian": "None (Memorial Garden was evacuated)"
    },
    "narrative_cost": "The network loses its central intelligence node. Aisen's death is the cost of ensuring the network can survive without him — which was always his intention and his Lie's final test."
  }
}
```

---

## Rules Enforcement Checklist

For every combat chapter PR:

- [ ] MU costs stated inline in prose (e.g., "4 MU kinetic pulse")
- [ ] Combat window ≤ 3 minutes narrative time
- [ ] 10-minute aftermath scene follows the combat
- [ ] Tactical specificity: distances in meters, named choke points, force counts
- [ ] At least 2 POVs shown for primary battles
- [ ] combat-chNN.json attached to PR or included in commit
- [ ] MU table reviewed for consistency with HARD-MAGIC-RULES.md
- [ ] Depletion symptoms match MU thresholds (see magic system docs)

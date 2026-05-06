# CHARACTER INTERACTION — Spreadsheet Template

Purpose
-------
Template for tracking first‑appearance, seed scenes, recurrence, micro‑scene hooks, and limit‑break risk for each character. Exportable to CSV for tooling.

Field definitions
-----------------
- `ID` — numeric unique identifier.
- `Name` — canonical character name.
- `Role` — protagonist / ally / antagonist / mentor / side / family.
- `Alias` — common epithets or call signs.
- `FirstSeenAge` — age when introduced in timeline.
- `SeedScene` — file or scene reference (relative path).
- `Recurrence` — Y/N (three‑appearance recurrence rule flag).
- `MicroScenes` — tags or links into `structure/SIDE-CHARACTER-MOMENTS.md`.
- `LimitBreakRisk` — Low/Medium/High (likelihood to attempt/need limit‑breaking).
- `Notes` — short freeform notes.

Seeded entries
----------------------
| ID | Name | Role | Alias | FirstSeenAge | SeedScene | Recurrence | MicroScenes | LimitBreakRisk | Notes |
|---:|---|---|---|---:|---|:---:|---|---|---|
| 1 | Aisen | Protagonist | — | 5 | structure/PRE-ACADEMY-TIMELINE.md#aisen | Y | tavern/rescue | High | Chain spear; learning curve |
| 2 | Caspian Vane | Antagonist (Covenant) | Lord Caspian | 28 | story-overview.md#caspian | Y | council/duel | High | Political antagonist, limit-break ambition |
| 3 | Seraphine Moroz | Antagonist (proxy) | Seraphine | 24 | story-overview.md#seraphine | Y | academy/temptation | Medium | Charismatic, manipulates bargains |
| 4 | Ser Corvin Ashford | Mentor/Antagonist | Corvin | 40 | structure/PRE-ACADEMY-TIMELINE.md#corvin | Y | library/lesson | Medium | Old debts; complex loyalty |
| 5 | Lucius Varro | Antagonist lieutenant | Varro | 30 | structure/SIDE-CHARACTER-MOMENTS.md#varro | N | border/raid | Low | Brutal enforcer |
| 6 | Lysandra Windbreaker | Ally | Lysandra | 12 | structure/PRE-ACADEMY-TIMELINE.md#lysandra | Y | childhood/friend | Low | Aisen's childhood friend; earth magic |
| 7 | Harald Greyson | Mentor | Harald | 55 | characters/TIER-SECONDARY/HARALD-GREYSON-profile.md | Y | academy/instructor | Low | Stoic trainer; sacrifices Ch.38 |
| 8 | Aisen's Father | Family | — | 5 | story/001-tavern-opening.md | Y | tavern/father | Low | Protective; tends bar at The Crossing |
| 9 | Marta | Side | Marta | 5 | story/001-tavern-opening.md | Y | tavern/economy | Low | Barmaid; small kindness to Aisen |
| 10 | Thorne | Merchant | Thorne | 28 | story/003-the-robbery.md | Y | market/merchant | Medium | Merchant; target of robbery; links to networks |
| 11 | Local Guard | Side | Guard | 30 | story/003-the-robbery.md | N | civic/guard | Low | Local watchman; enforces order |
| 12 | Elara Valorin | Ally | — | 8 | characters/TIER-SECONDARY/ELARA-VALORIN-profile.md | Y | forest/leadership | Medium | Political heir; becomes post-Aisen leader |
| 13 | Kaelen Blackwood | Ally (Network) | — | 11 | characters/TIER-SECONDARY/KAELEN-BLACKWOOD-profile.md | Y | grove/healing | Medium | Forest mage; philosophical counter to Meridian |
| 14 | Rin Celestara | Ally (Network) | — | 17 | characters/TIER-SECONDARY/RIN-CELESTARA-profile.md | Y | academy/espionage | Medium | Celestial spy; intelligence node |
| 15 | Amara Okafor | Ally (Network) | — | 15 | characters/TIER-SECONDARY/AMARA-OKAFOR-profile.md | Y | caravan/intelligence | Medium | Intelligence operative; Sahelian trader |
| 16 | Tarovin Blacksun | Mentor | — | 13 | characters/TIER-SECONDARY/TAROVIN-profile.md | Y | tavern/candle | High | Teaches telekinesis; sacrifices Ch.38 |
| 17 | Vex | Ally (Network) | — | 17 | characters/VEX-PROFILE-EXPANDED.md | Y | academy/wildcard | Medium | Network wildcard; flexible specialist |
| 18 | Hendrick | Ally (Network) | — | 17 | characters/HENDRICK-PROFILE-EXPANDED.md | Y | academy/support | Low | Intelligence support; distributed networks |
| 19 | Serath | Ally (Network) | — | 17 | characters/SERATH-PROFILE-EXPANDED.md | Y | academy/combat | Medium | Combat specialist; tactical network member |
| 20 | Meridian Nightwhisper | Antagonist | — | 28 | characters/antagonists/meridian-nightwhisper.md | Y | hunt/decay | High | Weaponized healing; Kaelen's philosophical opposite |
| 21 | Renard | Ally | — | 20 | story/scene-aftermath-renard-finds-aisen.md | Y | border/vigil | Low | Fox-kin scout; finds Aisen after final stand |
| 22 | Master Wei | Mentor | — | 55 | Chapters/04-Frostfang-Incident.md | Y | academy/inquiry | Low | Academy instructor; defends Aisen at inquiry |
| 23 | Mira Voss | Family/Ally | Mira | 5 | duplicates_for_review/characters/supporting-cast/MIRA-VOSS.md | Y | tavern/family | Low | Tavern connection; emotional anchor |

CSV export (example)
--------------------
```csv
ID,Name,Role,Alias,FirstSeenAge,SeedScene,Recurrence,MicroScenes,LimitBreakRisk,Notes
1,Aisen,Protagonist,,5,structure/PRE-ACADEMY-TIMELINE.md#aisen,Y,tavern/rescue,High,"Chain spear; learning curve"
2,Caspian Vane,Antagonist,"Lord Caspian",28,story-overview.md#caspian,Y,council/duel,High,"Political antagonist, limit-break ambition"
3,Seraphine Moroz,Antagonist,Seraphine,24,story-overview.md#seraphine,Y,academy/temptation,Medium,"Charismatic, manipulates bargains"
12,Elara Valorin,Ally,,8,characters/TIER-SECONDARY/ELARA-VALORIN-profile.md,Y,forest/leadership,Medium,"Political heir; post-Aisen leader"
13,Kaelen Blackwood,Ally,,11,characters/TIER-SECONDARY/KAELEN-BLACKWOOD-profile.md,Y,grove/healing,Medium,"Forest mage; philosophical counter to Meridian"
15,Amara Okafor,Ally,,15,characters/TIER-SECONDARY/AMARA-OKAFOR-profile.md,Y,caravan/intelligence,Medium,"Intelligence operative; Sahelian trader"
```

How to use
----------
- Add new rows as characters are introduced. Keep `SeedScene` as a relative link to the canonical scene file.
- Use `LimitBreakRisk` to prioritize which characters to monitor when running the Verification Checklist.

Next actions
------------
- I can populate the spreadsheet with the top 50 side characters from `structure/SIDE-CHARACTER-MOMENTS.md` if you want.

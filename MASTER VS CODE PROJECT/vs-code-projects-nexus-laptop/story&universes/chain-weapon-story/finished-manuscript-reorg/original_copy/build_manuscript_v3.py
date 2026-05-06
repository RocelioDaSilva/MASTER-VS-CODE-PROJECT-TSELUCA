#!/usr/bin/env python3
"""
Build Manuscript v4: Regional Landscapes + Regional Character Glyphs
Generates integrated manuscript with character glyphs that vary by region AND emotional state
52 chapters × 9 characters × 5 regions × 4 emotions = 180+ unique glyph variations
"""

import json
import os
from pathlib import Path

# Configuration
CONFIG_FILE = "chapter-config-regional-emotional.json"
TEMPLATE_FILE = "manuscript.tex"
OUTPUT_FILE = "manuscript-final.tex"
CHAPTER_DIR = "cwbook_minimal_package"

# Define landscapes, regions, and emotional states for distribution
LANDSCAPES = ["Cavern", "Desert", "Jungle", "Swamp", "Plains", "Tundra", "UndergroundCity", "Volcanic"]
REGIONS = ["North", "South", "East", "West", "Central"]
TIMES = ["Dawn", "Morning", "Noon", "Afternoon", "Sunset", "Dusk", "Night"]
EMOTIONS = ["Calm", "Intense", "Vulnerable", "Resolute"]

def generate_chapter_config():
    """
    Auto-generate chapter configuration with region + emotional state assignments.
    Distributes chapters evenly across all dimensions for rich variety.
    """
    chapters = []
    characters = ["Aisen", "Caspian", "Corvin", "Ryo", "Kael", "Kairos", "Orin", "Amara", "Renard"]
    
    for chapter_num in range(1, 53):
        # Auto-distribute across all dimensions
        landscape_idx = (chapter_num - 1) % len(LANDSCAPES)
        region_idx = ((chapter_num - 1) // len(LANDSCAPES)) % len(REGIONS)
        time_idx = (chapter_num - 1) % len(TIMES)
        emotion_idx = (chapter_num - 1) % len(EMOTIONS)
        character_idx = (chapter_num - 1) % len(characters)
        
        landscape = LANDSCAPES[landscape_idx]
        region = REGIONS[region_idx]
        time_of_day = TIMES[time_idx]
        emotional_state = EMOTIONS[emotion_idx]
        character = characters[character_idx]
        
        # Generate location based on landscape
        location_map = {
            "Cavern": "The Deep Stone Halls",
            "Desert": "The Endless Sands",
            "Jungle": "The Emerald Expanse",
            "Swamp": "The Sunken Marshes",
            "Plains": "The Windswept Grasslands",
            "Tundra": "The Frozen Wastes",
            "UndergroundCity": "The Forgotten Citadel",
            "Volcanic": "The Burning Peaks"
        }
        
        location = location_map.get(landscape, "Unknown Territory")
        
        chapter = {
            "num": chapter_num,
            "label": f"CHAPTER {chapter_num:02d}",
            "title": f"Journey Through the {landscape}",
            "character": character,
            "landscape": landscape,
            "region": region,
            "time_of_day": time_of_day,
            "emotional_state": emotional_state,
            "location": location,
            "character_glyph": f"{character}{region}{emotional_state}",
            "notes": f"{character} ({emotional_state}) in the {region} {location} at {time_of_day}"
        }
        chapters.append(chapter)
    
    return chapters

def load_or_create_config():
    """Load config from file, or generate fresh if not exists."""
    if os.path.exists(CONFIG_FILE):
        print(f"📖 Loading config from {CONFIG_FILE}")
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"📝 Generating fresh config: 52 chapters × 9 chars × 5 regions × 4 emotions")
        config = generate_chapter_config()
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✓ Created {CONFIG_FILE}")
        return config

def get_chapter_content(chapter_num):
    """Load chapter content from file."""
    chapter_file = f"{CHAPTER_DIR}/chapter{chapter_num:02d}.tex"
    if os.path.exists(chapter_file):
        with open(chapter_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"% Chapter {chapter_num:02d} file not found"

def generate_chapter_block(chapter_info, chapter_content):
    """Generate chapter block with regional landscape + regional character glyph."""
    num = chapter_info['num']
    character = chapter_info['character']
    landscape = chapter_info['landscape']
    region = chapter_info['region']
    time_of_day = chapter_info['time_of_day']
    emotional_state = chapter_info['emotional_state']
    location = chapter_info['location']
    notes = chapter_info.get('notes', '')
    character_glyph = chapter_info.get('character_glyph', f"{character}{region}{emotional_state}")
    
    # Construct the landscape+region+time combination
    landscape_region_time = f"{landscape}{region}{time_of_day}"
    
    # Build chapter block with all customizations
    block = f"""
% ═══════════════════════════════════════════════════════════════════════════
% CHAPTER {num:02d}: {location}
% Character: {character} ({emotional_state}) | Landscape: {landscape} ({region}) | Time: {time_of_day}
% Glyph: {character_glyph}
% {notes}
% ═══════════════════════════════════════════════════════════════════════════

\\renewcommand{{\\ActiveCharacter}}{{{character}}}
\\renewcommand{{\\CharacterRegionEmotion}}{{{character_glyph}}}
\\renewcommand{{\\ActiveLandscape}}{{{landscape_region_time}}}
\\renewcommand{{\\LandscapeRegionTime}}{{{landscape_region_time}}}
\\renewcommand{{\\ChapterLocation}}{{{location}}}
\\renewcommand{{\\ChapterEmotion}}{{{emotional_state}}}

{chapter_content}

"""
    return block

def build_manuscript():
    """Build the complete integrated manuscript."""
    print("\n🔨 BUILDING MANUSCRIPT v4 (Regional Landscapes + Regional Character Glyphs)\n")
    
    # Load configuration
    config = load_or_create_config()
    
    # Load template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate manuscript body (all chapters)
    manuscript_body = ""
    for chapter_info in config:
        chapter_num = chapter_info['num']
        chapter_content = get_chapter_content(chapter_num)
        chapter_block = generate_chapter_block(chapter_info, chapter_content)
        manuscript_body += chapter_block
        print(f"  ✓ Ch{chapter_num:02d}: {chapter_info['character']} ({chapter_info['emotional_state']}) @ {chapter_info['landscape']} ({chapter_info['region']}) - {chapter_info['time_of_day']}")
    
    # Assemble final manuscript
    final_manuscript = template + "\n% INTEGRATED CHAPTERS\n" + manuscript_body + "\n\\end{document}\n"
    
    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_manuscript)
    
    print(f"\n✓ Generated all 52 chapters with regional character glyphs + landscapes")
    print(f"✓ Manuscript generated: {OUTPUT_FILE}, Total chapters: {len(config)}")
    print(f"\nCharacter Glyph System:")
    print(f"  • Characters: {len(set(c['character'] for c in config))}")
    print(f"  • Regions: {len(REGIONS)} ({', '.join(REGIONS)})")
    print(f"  • Emotional States: {len(EMOTIONS)} ({', '.join(EMOTIONS)})")
    print(f"  • Total glyph variants: {len(set(c['character'] for c in config))} × {len(REGIONS)} × {len(EMOTIONS)} = {9 * len(REGIONS) * len(EMOTIONS)}")
    print(f"\nLandscape System:")
    print(f"  • Landscapes: {len(LANDSCAPES)} ({', '.join(LANDSCAPES)})")
    print(f"  • Total variants: {len(LANDSCAPES)} × {len(REGIONS)} × {len(TIMES)} = {len(LANDSCAPES) * len(REGIONS) * len(TIMES)}")

if __name__ == "__main__":
    build_manuscript()


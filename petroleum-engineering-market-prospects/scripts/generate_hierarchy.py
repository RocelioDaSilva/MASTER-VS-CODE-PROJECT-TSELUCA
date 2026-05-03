import os
import re
from pathlib import Path

# Configuration — paths relative to repo root (data/processed/ and data/raw/)
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DATA_PROC = _REPO_ROOT / "data" / "processed"
INPUT_FILE = str(_REPO_ROOT / "data" / "raw" / "fullinfobetteroorganized.md")
OUTPUT_DIR = str(_DATA_PROC / "company_hierarchy")

# Ensure output directory exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def sanitize_name(name):
    """Remove invalid characters from folder/file names."""
    # Replace problematic characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    # Trim leading/trailing spaces and dots
    name = name.strip('. ')
    # Limit length to avoid path too long errors (optional)
    if len(name) > 200:
        name = name[:200]
    return name

def parse_md_file(filepath):
    """Parse the markdown file and extract hierarchy with companies."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    services = []
    current_service = None
    current_niche = None
    current_type = None
    collecting_companies = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Service header: "## X. Service Name"
        if line.startswith('## ') and not line.startswith('### '):
            if current_service:
                services.append(current_service)
            service_name = line[3:].strip()
            current_service = {
                'name': service_name,
                'niches': []
            }
            current_niche = None
            current_type = None
            collecting_companies = False

        # Niche header: "### Niche Name (XX empresas)"
        elif line.startswith('### ') and current_service is not None:
            match = re.match(r'### (.+?) \((\d+) empresas\)', line)
            if match:
                niche_name = match.group(1).strip()
                niche_count = match.group(2)
                current_niche = {
                    'name': niche_name,
                    'types': []
                }
                current_service['niches'].append(current_niche)
                current_type = None
                collecting_companies = False

        # Type header: "#### Tipo: SCA (XX empresas)"
        elif line.startswith('#### Tipo: ') and current_niche is not None:
            match = re.match(r'#### Tipo: (.+?) \((\d+) empresas\)', line)
            if match:
                type_name = match.group(1).strip()
                type_count = match.group(2)
                current_type = {
                    'name': type_name,
                    'companies': []
                }
                current_niche['types'].append(current_type)
                collecting_companies = True  # Next lines are companies

        # Company line: "- NIF — Name — Status"
        elif line.startswith('- ') and collecting_companies and current_type is not None:
            # Company entry format: "- 5000222879 — 2césJ - Comercio e Servicos, Lda — Preferência"
            # Some have no NIF: "- — — — — Preferência"
            content = line[2:].strip()
            parts = content.split(' — ')
            if len(parts) >= 3:
                nif = parts[0].strip()
                name = parts[1].strip()
                status = parts[2].strip()
                current_type['companies'].append({
                    'nif': nif,
                    'name': name,
                    'status': status
                })
            else:
                # Handle malformed lines if any
                pass

        # If we encounter a blank line, we might still be collecting,
        # but continue. Only stop collecting when new header appears.
        i += 1

    if current_service:
        services.append(current_service)

    return services

def create_structure(services, base_path):
    """Create folders and company markdown files."""
    for service in services:
        service_name = sanitize_name(service['name'])
        service_path = base_path / service_name
        service_path.mkdir(exist_ok=True)
        print(f"Service: {service_name}")

        for niche in service['niches']:
            niche_name = sanitize_name(niche['name'])
            niche_path = service_path / niche_name
            niche_path.mkdir(exist_ok=True)
            print(f"  Niche: {niche_name}")

            for type_info in niche['types']:
                type_name = sanitize_name(type_info['name'])
                type_path = niche_path / type_name
                type_path.mkdir(exist_ok=True)
                print(f"    Type: {type_name}")

                for company in type_info['companies']:
                    # Create filename: use NIF if available and not empty, else company name
                    if company['nif'] and company['nif'] not in ('—', ''):
                        filename_base = sanitize_name(f"{company['nif']}")
                    else:
                        filename_base = sanitize_name(company['name'])
                        if not filename_base:
                            filename_base = "unknown"

                    filename = f"{filename_base}.md"
                    file_path = type_path / filename

                    # Avoid overwriting duplicate filenames (e.g., multiple "—")
                    if file_path.exists():
                        counter = 1
                        while True:
                            new_filename = f"{filename_base}_{counter}.md"
                            file_path = type_path / new_filename
                            if not file_path.exists():
                                break
                            counter += 1

                    # Write company details to markdown file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {company['name']}\n\n")
                        f.write(f"- **NIF:** {company['nif']}\n")
                        f.write(f"- **Nome:** {company['name']}\n")
                        f.write(f"- **Status:** {company['status']}\n")
                        f.write(f"- **Serviço:** {service['name']}\n")
                        f.write(f"- **Nicho:** {niche['name']}\n")
                        f.write(f"- **Tipo:** {type_info['name']}\n")

                print(f"      Created {len(type_info['companies'])} company files")

if __name__ == "__main__":
    if not Path(INPUT_FILE).exists():
        print(f"Error: {INPUT_FILE} not found in current directory.")
        print("Please ensure the markdown file is in the same folder as this script.")
        exit(1)

    print(f"Parsing {INPUT_FILE}...")
    data = parse_md_file(INPUT_FILE)
    print(f"Found {len(data)} services.")

    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    create_structure(data, output_path)

    print(f"\nDone! Hierarchy created in '{OUTPUT_DIR}' folder.")

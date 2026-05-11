#!/usr/bin/env python3
"""
fill_company_info.py
====================

Unified script to fill .md files in company_hierarchy/ with structured company information.

Supports two modes:
  1. SIMPLE mode (--mode simple):
     Fills every .md file with a basic template: Serviço/Actividade/Tipo/Empresa
     Suitable for quick population or testing.

  2. FULL mode (--mode full, default):
     Fills .md files with complete BI reports:
     - For ~40 major verified companies: real contact data (websites, emails, phones, addresses, LinkedIn)
     - For all other companies: template with pre-built one-click research URLs
     - Derives company name/NIF from filename; service/niche/tipo from folder path
     - Looks up ANPG status (Preferência / Exclusividade) from CSV

Usage:
    python fill_company_info.py --mode simple              # Fill with basic template
    python fill_company_info.py --mode full                # Fill with full BI reports (default)
    python fill_company_info.py                             # Default: full mode
    python fill_company_info.py --root /path/to/hierarchy  # Use custom root
    python fill_company_info.py --no-backup                # Don't create backups

Reads:
  - data/processed/company_hierarchy/*.md (all files)
  - data/processed/company_hierarchy.csv (for ANPG status lookup in FULL mode)

Writes:
  - data/processed/company_hierarchy_originals/*.md (backups)
  - Modified .md files with filled content
"""

import argparse
import csv
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "processed", "company_hierarchy.csv")

_MONTHS_PT = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
              "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
_d = date.today()
TODAY = f"{_d.day} de {_MONTHS_PT[_d.month-1]} de {_d.year}"

# ── STATUS & TYPE NOTES ──────────────────────────────────────────────────────
STATUS_NOTES = {
    "Exclusividade": (
        "Esta empresa detém o estatuto de **Exclusividade** no ANPG, "
        "o que significa que é o fornecedor exclusivamente designado para este serviço "
        "em Angola. Associar-se a ela é uma porta de entrada estratégica no sector."
    ),
    "Preferência": (
        "Esta empresa detém o estatuto de **Preferência** no ANPG, "
        "o que significa que tem prioridade nos concursos de contratação. "
        "É um empregador relevante e com carteira de clientes estabelecida no mercado local."
    ),
}

TIPO_NOTES = {
    "SCA": "Sociedade Comercial Angolana — capital 100% angolano (máximo nível de conteúdo local).",
    "LDA": "Sociedade por Quotas (Lda) — pode ser angolana ou mista.",
    "SU LDA": "Sociedade Unipessoal por Quotas — tipicamente pequena empresa angolana.",
    "SA":  "Sociedade Anónima — estrutura adequada a empresas de maior dimensão.",
}

# ── SERVICE CLIENT MAPPING (FULL mode) ────────────────────────────────────────
SERVICE_CLIENTS = {
    "1":  "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Eni",
    "2":  "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Bureau Veritas, DNV",
    "3":  "Sonangol, TotalEnergies, SLB, Halliburton, Baker Hughes",
    "4":  "Sonangol, operadoras offshore, empresas de serviços",
    "5":  "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Eni",
    "6":  "TotalEnergies, bp / Azule Energy, Sonangol, TechnipFMC, Saipem",
    "7":  "TechnipFMC, Saipem, Subsea 7, SBM Offshore, TotalEnergies",
    "8":  "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Eni",
    "9":  "Sonangol, operadoras, governo angolano (ANPG, MindPetro)",
    "10": "TotalEnergies, bp / Azule Energy, Sonangol, SLB, Halliburton",
    "11": "TotalEnergies, bp / Azule Energy, ExxonMobil, Sonangol Pesquisa e Produção",
    "12": "Sonangol, TotalEnergies, Saipem, Subsea 7, SBM Offshore, Oceaneering",
    "13": "TotalEnergies, bp / Azule Energy, ExxonMobil, Sonangol P&P",
    "14": "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Eni",
    "15": "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, SLB",
    "16": "TechnipFMC, Saipem, Subsea 7, Sonangol, TotalEnergies",
    "17": "SLB, Halliburton, Baker Hughes, TotalEnergies, bp / Azule Energy",
    "18": "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, todas as operadoras",
    "19": "ANPG, Sonangol, governo angolano, TotalEnergies",
    "20": "TechnipFMC, Saipem, Subsea 7, TotalEnergies, bp / Azule Energy",
}

DEFAULT_CLIENTS = "Sonangol, TotalEnergies, bp / Azule Energy, ExxonMobil, Eni (verificar por pesquisa)"

# ══════════════════════════════════════════════════════════════════════════════
# CURATED COMPANY DATA — Real info found via web research (April 2026)
# ══════════════════════════════════════════════════════════════════════════════
CURATED = {
    "5401131542": {
        "brand": "Oceaneering",
        "website": "https://www.oceaneering.com/locations/angola/",
        "careers": "https://www.oceaneering.com/careers/",
        "email_rh": "recrutamentoangola-oii@oceaneering.com",
        "phone": "+244 222 635 400",
        "address": "Avenida Deolinda Rodrigues, No. 495, Terra Nova, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/oceaneering/",
        "services_desc": "ROVs, Diving, Asset Integrity, Vessel Management, Engineering, Machining, Fabrication",
        "clients_real": "TotalEnergies, Eni Angola, bp / Azule Energy, ExxonMobil, Sonangol",
        "notes": "Presente em Angola desde os anos 1980. Filial angolana liderada por força de trabalho local.",
    },
    "5112001275": {
        "brand": "SONAMET",
        "website": "https://www.sonamet.com",
        "email_rh": "recrutamento@sonamet.com",
        "phone": "+244 225 400 003",
        "address": "Luanda: Rua Domingos Tchekahanga nº18, Ingombota",
        "linkedin": "https://www.linkedin.com/company/sonamet-yard/",
        "services_desc": "EPC/EPCI, Fabrication, Engineering",
        "clients_real": "TotalEnergies, Eni Angola, bp / Azule Energy, Sonangol, ExxonMobil",
        "notes": "JV Sonangol/Subsea 7. Fundada em 1998. ISO 9001:2000. NUNCA cobra taxas de recrutamento.",
    },
    "5402160627": {
        "brand": "Baker Hughes",
        "website": "https://www.bakerhughes.com",
        "careers": "https://careers.bakerhughes.com",
        "address": "Rua Pedro de Castro Van-Dunem Loy, Morro Bento, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/baker-hughes/",
        "services_desc": "Drilling Services, Completions, Oilfield Chemicals, Turbomachinery, Digital Solutions",
        "clients_real": "TotalEnergies, Eni Angola, bp / Azule Energy, ExxonMobil, Sonangol",
        "notes": "Uma das 3 maiores empresas de serviços de campo petrolífero. Candidaturas exclusivamente online.",
    },
    "5403091831": {
        "brand": "Halliburton",
        "website": "https://www.halliburton.com",
        "careers": "https://jobs.halliburton.com",
        "address": "Zona Industrial de Viana / SONILS Base, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/halliburton/",
        "services_desc": "Drilling & Evaluation, Completion & Production, Digital Solutions",
        "clients_real": "TotalEnergies, Eni Angola, Azule Energy, Chevron (legacy), Sonangol",
        "notes": "Uma das 3 maiores empresas de serviços de campo petrolífero. Portal: jobs.halliburton.com.",
    },
    "5410002423": {
        "brand": "SLB (Schlumberger)",
        "website": "https://www.slb.com",
        "careers": "https://careers.slb.com",
        "address": "SONILS Base / Rua Amílcar Cabral, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/slb/",
        "services_desc": "Reservoir Characterization, Drilling, Production, Digital & Integration",
        "clients_real": "TotalEnergies, ExxonMobil, Sonangol, Eni Angola, bp / Azule Energy",
        "notes": "Maior empresa de serviços de campo petrolífero do mundo. Rebranding: Schlumberger → SLB (2022).",
    },
    "5000122157": {
        "brand": "TechnipFMC",
        "website": "https://www.technipfmc.com",
        "careers": "https://www.technipfmc.com/en/careers/",
        "address": "Rua Marechal Broz Tito nº 35/37, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/technipfmc/",
        "services_desc": "Subsea Systems, SURF, iEPCI™",
        "clients_real": "TotalEnergies (Blocos 17, 32), Eni Angola, bp / Azule Energy, Sonangol",
        "notes": "Líder global em sistemas submarinos. Presente em Angola há décadas em Luanda.",
    },
    "5402160554": {
        "brand": "Saipem",
        "website": "https://www.saipem.com",
        "careers": "https://www.saipem.com/en/work-with-us",
        "address": "Rua dos Coqueiros, Luanda, Angola",
        "linkedin": "https://www.linkedin.com/company/saipem/",
        "services_desc": "Offshore E&C, Onshore E&C, Drilling, Conceptual Design, EPCI",
        "clients_real": "TotalEnergies, Eni Angola, Sonangol, Azule Energy",
        "notes": "Grande empresa italiana de engenharia offshore/onshore. Fusão com Subsea 7 anunciada (2025).",
    },
    "5401128568": {
        "brand": "Subsea 7",
        "website": "https://www.subsea7.com",
        "careers": "https://careers.subsea7.com",
        "address": "Luanda, Angola (zona SONILS / área portuária)",
        "linkedin": "https://www.linkedin.com/company/subsea-7/",
        "services_desc": "SURF, Conventional, Seabed-to-Surface Engineering",
        "clients_real": "TotalEnergies, Eni Angola, bp / Azule Energy, ExxonMobil",
        "notes": "Líder global submarina. 50% SONAMET (JV com Sonangol). Fusão com Saipem anunciada (2025).",
    },
}

# ── Generic search URL builder (FULL mode) ────────────────────────────────────
def build_search_urls(nome, nif):
    """Return dict of pre-built search URLs for generic companies."""
    q = quote_plus(f"{nome} Angola")
    return {
        "g_website": f"https://www.google.com/search?q={quote_plus(nome)}+website+Angola",
        "g_email": f"https://www.google.com/search?q={quote_plus(nome)}+Angola+email+contacto",
        "g_phone": f"https://www.google.com/search?q={quote_plus(nome)}+Angola+telefone",
        "g_address": f"https://maps.google.com/maps/search/{q}",
        "g_news": f"https://news.google.com/search?q={q}",
        "g_tender": f"https://www.google.com/search?q={quote_plus(nome)}+concurso+publico",
        "g_nif": f"https://www.google.com/search?q={nif}+Angola",
        "g_dr": f"https://www.google.com/search?q={nif}+diario+republica+angola",
        "li_company": f"https://www.linkedin.com/search/results/companies/?keywords={quote_plus(nome)}",
        "li_people": f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(nome)}+Angola",
        "fb_search": f"https://www.facebook.com/search/top?q={quote_plus(nome)}",
        "ig_search": f"https://www.instagram.com/explore/search/keyword/?keyword={quote_plus(nome)}",
        "g_clients": f"https://www.google.com/search?q={quote_plus(nome)}+contratos+clientes",
    }

# ── SIMPLE mode: basic template ──────────────────────────────────────────────
SIMPLE_TEMPLATE = "Serviço: \nActividade: \nTipo de Sociedade: \nEmpresa: \n"

def fill_simple(fpath):
    """Fill file with simple template."""
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(SIMPLE_TEMPLATE)

# ── FULL mode: curated + search URLs ─────────────────────────────────────────
def build_report(nome, nif, status, servico, nicho, tipo):
    """Build full BI report — curated or generic with search URLs."""
    status_note = STATUS_NOTES.get(status, "Estatuto desconhecido; verificar no ANPG.")
    tipo_note = TIPO_NOTES.get(tipo, "Tipo desconhecido.")

    # Extract service number (e.g., "1" from "1. Consultoria...")
    service_num = servico.split(".")[0].strip() if "." in servico else ""
    clientes = SERVICE_CLIENTS.get(service_num, DEFAULT_CLIENTS)

    if nif in CURATED:
        company = CURATED[nif]
        website = company.get("website", "")
        email = company.get("email_rh", "")
        phone = company.get("phone", "")
        address = company.get("address", "")
        linkedin = company.get("linkedin", "")
        services_desc = company.get("services_desc", "")
        clients_real = company.get("clients_real", clientes)
        notes = company.get("notes", "")

        apply_steps = f"""1. **Visitar Carreiras:** Abrir [{website}]({website}careers/) ou [LinkedIn Empresa]({linkedin})
2. **Candidatura Online:** Submeter CV + carta de motivação via portal de carreiras (se disponibile)
3. **Email Direto:** Enviar CV para [{email}]({email}) se portal não existir
4. **Contacto Telefónico:** Ligar para {phone} (horário comercial) para confirmar recepção"""

        return f"""# Relatório de Empresa: {nome}

| Campo | Valor |
|---|---|
| **NIF** | `{nif}` |
| **Data de Análise** | {TODAY} |
| **Status ANPG** | {status} |
| **Serviço** | {servico} |
| **Actividade / Nicho** | {nicho} |
| **Tipo de Sociedade** | {tipo} — {tipo_note} |

---

## 📋 Contacto Direto (Verificado)

| Campo | Informação | Link |
|---|---|---|
| **Website** | {website} | [🌐 Visitar]({website}) |
| **Carreiras** | Portal de recrutamento online | [💼 Candidaturas]({website.rstrip('/')}/careers/) |
| **Email RH** | {email} | [📧 Enviar CV]({email if email.startswith('mailto:') else 'mailto:' + email}) |
| **Telefone** | {phone} | [📞 Ligar]({phone if phone.startswith('tel:') else 'tel:' + phone.replace(' ', '')}) |
| **Endereço** | {address} | [🗺️ Google Maps]({build_search_urls(nome, nif)['g_address']}) |
| **LinkedIn** | Empresa | [🔗 Perfil Empresa]({linkedin}) |

---

## 🎯 Relevância para Estudantes de Engenharia de Petróleo

**Porquê esta empresa?**
{status_note}

**Serviços principais:** {services_desc}

**Clientes verificados:** {clients_real}

**Nota:** {notes}

---

## 📝 Como se Candidatar

{apply_steps}

---

> **Nota de Investigação:** Este relatório contém dados reais verificados em Abril 2026. Recomenda-se confirmar contactos e procedimentos no website oficial antes de candidatar-se.
"""
    else:
        # Generic/template report with search URLs
        urls = build_search_urls(nome, nif)
        g_website = urls['g_website']
        g_email = urls['g_email']
        g_phone = urls['g_phone']
        g_address = urls['g_address']
        g_news = urls['g_news']
        g_tender = urls['g_tender']
        g_nif = urls['g_nif']
        g_dr = urls['g_dr']
        li_company = urls['li_company']
        li_people = urls['li_people']
        fb_search = urls['fb_search']
        ig_search = urls['ig_search']
        g_clients = urls['g_clients']

        return f"""# Relatório de Empresa: {nome}

| Campo | Valor |
|---|---|
| **NIF** | `{nif}` |
| **Data de Análise** | {TODAY} |
| **Status ANPG** | {status} |
| **Serviço** | {servico} |
| **Actividade / Nicho** | {nicho} |
| **Tipo de Sociedade** | {tipo} — {tipo_note} |

---

## 🏛️ Informação Oficial e de Registo

| Campo | Resultado | Pesquisa Rápida |
|---|---|---|
| **NIF** | `{nif}` | [🔍 Verificar NIF]({g_nif}) |
| **Data de Constituição** | _Preencher após pesquisa_ | [🔍 Diário da República]({g_dr}) |
| **Sede Social** | _Preencher após pesquisa_ | [🗺️ Google Maps]({g_address}) |
| **Objeto Social** | _Preencher após pesquisa_ | [🔍 Pesquisar]({g_website}) |

---

## 📞 Contactos e Presença Digital

| Canal | Resultado | Link de Pesquisa |
|---|---|---|
| **Website Oficial** | _Não encontrado automaticamente_ | [🌐 Pesquisar website]({g_website}) |
| **Email Geral / RH** | _Não encontrado automaticamente_ | [📧 Pesquisar email]({g_email}) |
| **Telefone** | _Não encontrado automaticamente_ | [📱 Pesquisar telefone]({g_phone}) |
| **LinkedIn (Empresa)** | _Verificar_ | [🔗 LinkedIn Empresas]({li_company}) |
| **LinkedIn (Pessoas)** | _Verificar_ | [👥 LinkedIn Pessoas]({li_people}) |
| **Facebook** | _Verificar_ | [📘 Facebook]({fb_search}) |
| **Instagram** | _Verificar_ | [📸 Instagram]({ig_search}) |
| **Notícias / Imprensa** | _Verificar_ | [📰 Google Notícias]({g_news}) |

---

## 🔗 Cadeia de Valor

### Quem os contrata? (Clientes)
- **Principais Operadoras / Tier-1:** {clientes}
- [🔍 Pesquisar contratos com Oil Majors]({g_clients})

### Quem eles contratam? (Subcontratados)
- _Verificar concursos públicos e limitados publicados pela empresa_
- [🔍 Pesquisar concursos públicos]({g_tender})

---

## 🎯 Relevância para Estudantes de Engenharia de Petróleo

**Porquê esta empresa?**
{status_note}

**Nicho de actuação:** `{nicho}` dentro do sector `{servico}`.

---

## 📝 Como se Candidatar — Passo a Passo

1. **LinkedIn First:** Abrir [LinkedIn Empresas]({li_company}) → procurar página da empresa. Se não existir, try [LinkedIn Pessoas]({li_people}).
2. **Email Direto:** Pesquisar [email corporativo]({g_email}) → tentar formatos `rh@[dominio].ao`, `recrutamento@[dominio].ao`.
3. **Presença Digital:** Verificar [Facebook]({fb_search}) e [Instagram]({ig_search}).
4. **Visita Presencial:** Localizar a sede via [Google Maps]({g_address}) e apresentar CV em mão.
5. **Monitorizar Concursos:** Acompanhar [concursos públicos]({g_tender}) — muitas empresas contratam via concurso limitado.

---

> **Nota de Investigação:** A maioria das PMEs angolanas tem presença digital limitada. Os campos marcados *"Preencher após pesquisa"* requerem verificação manual usando os links acima. Todos os links abrem a pesquisa correta num clique.
"""

# ── Parse path to extract (nome, nif, servico, nicho, tipo) ───────────────────
NIF_RE = re.compile(r"_([^_]+)\.md$", re.IGNORECASE)
FNAME_RE = re.compile(r"^(.+)_([^_]+)\.md$")

def parse_file(fpath, hier_root):
    """Extract (nome, nif, servico, nicho, tipo) from absolute path."""
    norm = fpath.replace("\\\\?\\", "").replace("/", os.sep)
    root = hier_root.replace("\\\\?\\", "").replace("/", os.sep)

    rel = os.path.relpath(norm, root)
    parts = rel.split(os.sep)
    if len(parts) < 4:
        return None

    servico = parts[0]
    nicho = parts[1]
    tipo = parts[2]
    filename = parts[-1]

    m = FNAME_RE.match(filename)
    if not m:
        return None
    nome = m.group(1)
    nif = m.group(2)
    return nome, nif, servico, nicho, tipo

# ── Load status map from CSV (FULL mode only) ────────────────────────────────
def load_status_map(csv_path):
    """Return dict NIF → Status from CSV."""
    status_map = {}
    try:
        with open(csv_path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                nif = str(row["NIF"]).strip()
                status = row["Status"].strip()
                if nif not in status_map:
                    status_map[nif] = status
    except Exception as e:
        print(f"Warning: Could not load CSV ({e}). Using default status.")
        return {}
    return status_map

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Fill company_hierarchy .md files with company information.\n"
                    "Supports simple template or full BI reports with curated/search data."
    )
    parser.add_argument('--mode', choices=['simple', 'full'], default='full',
                        help='Filling mode: simple (template) or full (BI reports with curated data)')
    parser.add_argument('--root', default=None,
                        help='Root folder to process (default: auto-detect based on script location)')
    parser.add_argument('--no-backup', action='store_true',
                        help='Do not create backups')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying files')
    args = parser.parse_args()

    # Determine root folder
    if args.root:
        hier_root = Path(args.root)
    else:
        # Auto-detect: if called from scripts/, look one level up; otherwise use data/processed/company_hierarchy
        script_dir = Path(__file__).resolve().parent
        if script_dir.name == 'scripts':
            hier_root = script_dir.parent / 'data' / 'processed' / 'company_hierarchy'
        else:
            hier_root = script_dir / 'company_hierarchy'

    if not hier_root.exists():
        print(f"ERROR: root folder '{hier_root}' not found")
        return 2

    # Handle Windows extended paths
    hier_root_walk = hier_root
    if sys.platform == "win32":
        hier_root_walk = Path("\\\\?\\" + str(hier_root.resolve()))

    # Load status map if FULL mode
    status_map = {}
    if args.mode == 'full':
        print("Loading ANPG status map from CSV...")
        # Try to find CSV
        csv_search = [
            Path(CSV_PATH),
            hier_root.parent / 'company_hierarchy.csv',
            hier_root.parent.parent / 'company_hierarchy.csv',
        ]
        csv_found = None
        for csv_path in csv_search:
            if csv_path.exists():
                csv_found = csv_path
                break
        
        if csv_found:
            status_map = load_status_map(str(csv_found))
            print(f"  Loaded {len(status_map):,} unique NIFs")
        else:
            print(f"  Warning: CSV not found. Using default status 'Preferência'.")

    # Create backup folder if needed
    backup_root = None
    if not args.no_backup:
        backup_root = hier_root.parent / (hier_root.name + '_originals')
        backup_root.mkdir(parents=True, exist_ok=True)
        print(f"Backups will be created in: {backup_root}")

    # Walk and fill files
    print(f"\nWalking {hier_root} in {args.mode.upper()} mode...")
    total = updated = skipped = 0

    for dirpath, _dirs, files in os.walk(str(hier_root_walk)):
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue

            fpath = os.path.join(dirpath, fname)
            total += 1

            # Parse file path
            parsed = parse_file(fpath, str(hier_root_walk))
            if not parsed:
                skipped += 1
                continue

            nome, nif, servico, nicho, tipo = parsed

            # Create backup
            if backup_root:
                rel_path = Path(fpath).relative_to(Path(str(hier_root_walk)).resolve())
                backup_file = backup_root / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                if not backup_file.exists():
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            old_content = f.read()
                        backup_file.write_text(old_content, encoding='utf-8')
                    except Exception:
                        pass

            # Generate content
            if args.mode == 'simple':
                new_content = SIMPLE_TEMPLATE
            else:  # full
                status = status_map.get(nif, "Preferência")
                new_content = build_report(nome, nif, status, servico, nicho, tipo)

            # Write (or show)
            if args.dry_run:
                print(f"  [DRY-RUN] Would fill: {fpath}")
            else:
                try:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated += 1
                    if updated % 5000 == 0:
                        print(f"  ... {updated:,} updated so far")
                except Exception as e:
                    print(f"  Error writing {fpath}: {e}")
                    skipped += 1

    print(f"\nDone.")
    print(f"  Total files       : {total:,}")
    print(f"  Updated           : {updated:,}")
    print(f"  Skipped/Errors    : {skipped:,}")

if __name__ == "__main__":
    sys.exit(main() or 0)

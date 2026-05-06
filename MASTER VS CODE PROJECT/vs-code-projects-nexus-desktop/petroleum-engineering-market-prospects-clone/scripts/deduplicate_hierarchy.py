#!/usr/bin/env python3
"""
deduplicate_hierarchy.py
========================
Deduplicate company files across service hierarchy folders.

Strategy
--------
1. Walk every .md in company_hierarchy/ and group files by NIF.
2. For each NIF that appears in MORE THAN ONE folder:
   a. Build a canonical profile in company_hierarchy/_Profiles/CompanyName_NIF.md
      - Reads ONLY ONE file per company (first alphabetically by service)
      - Service/Niche rows replaced by a full "Serviços Registados" table
   b. Replace every folder-specific instance with a lightweight stub that:
      - Shows Service / Niche / Status for THAT folder
      - Wiki-links back to [[CompanyName_NIF]] (Obsidian-compatible)
3. Single-occurrence companies: left as-is.

Run from anywhere:
    python deduplicate_hierarchy.py [--dry-run] [--root PATH]
"""

import os
import re
import sys
import csv
import argparse
from collections import defaultdict

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data", "processed"))
HIER_ROOT  = os.path.join(BASE_DIR, "company_hierarchy")
CSV_PATH   = os.path.join(BASE_DIR, "company_hierarchy.csv")

# Windows extended-length prefix so paths >260 chars work
if sys.platform == "win32":
    def _wp(p):
        if not p.startswith("\\\\?\\"):
            return "\\\\?\\" + p
        return p
else:
    def _wp(p):
        return p

FNAME_RE = re.compile(r"^(.+)_([^_\\\/]+)\.md$")   # CompanyName_NIF.md

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_filepath(fpath, hier_root):
    """
    Extract (company_name, nif, service, niche, tipo) from an absolute path.
    Expected depth: hier_root / Service / Niche / Tipo / CompanyName_NIF.md
    """
    norm_root = hier_root.rstrip(os.sep) + os.sep
    if not fpath.startswith(norm_root):
        return None
    rel   = fpath[len(norm_root):]
    parts = rel.split(os.sep)
    if len(parts) < 4:
        return None
    if parts[0].startswith("_"):    # skip _Profiles and any other _-prefixed dirs
        return None

    service  = parts[0]
    niche    = parts[1]
    tipo     = parts[2]
    filename = parts[-1]

    m = FNAME_RE.match(filename)
    if not m:
        return None
    company_name = m.group(1)
    nif          = m.group(2)
    return company_name, nif, service, niche, tipo


def load_status_map(csv_path):
    """Return dict NIF -> Status from the CSV."""
    status_map = {}
    try:
        with open(csv_path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                nif    = str(row["NIF"]).strip()
                status = row["Status"].strip()
                if nif not in status_map:
                    status_map[nif] = status
    except FileNotFoundError:
        pass
    return status_map


def read_one_file(path):
    try:
        with open(_wp(path), encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:
        print(f"  [WARN] Cannot read {path}: {exc}", file=sys.stderr)
        return ""


def write_file(path, content, dry_run=False):
    if dry_run:
        return
    try:
        os.makedirs(_wp(os.path.dirname(path)), exist_ok=True)
        with open(_wp(path), "w", encoding="utf-8") as fh:
            fh.write(content)
    except Exception as exc:
        print(f"  [ERROR] Cannot write {path}: {exc}", file=sys.stderr)


def is_curated(content):
    return "✅ **DADOS VERIFICADOS**" in content


def build_canonical_profile(company_name, nif, instances, sample_content):
    """
    Build the canonical profile from ONE sample file.
    instances: list of dicts {service, niche, tipo, status}
    """
    # Build all-niches table (sorted)
    niche_rows = "\n".join(
        f"| {i['service']} | {i['niche']} | {i['tipo']} | {i['status']} |"
        for i in sorted(instances, key=lambda x: (x["service"], x["niche"]))
    )
    niche_table = (
        "## 🗂️ Serviços & Nichos Registados no ANPG\n\n"
        "| Serviço | Actividade / Nicho | Tipo | Status |\n"
        "|---|---|---|---|\n"
        f"{niche_rows}\n"
    )

    content = sample_content

    # Replace the single-niche header rows with a multi-niche summary
    content = re.sub(
        r"\| \*\*Serviço\*\* \|[^\n]+\n\| \*\*Actividade \/ Nicho\*\* \|[^\n]+\n",
        f"| **Serviços Registados** | {len(instances)} nichos — ver tabela abaixo |\n",
        content,
        count=1,
    )

    # Insert niche table right after the first "---" separator
    first_hr = content.find("\n---\n")
    if first_hr != -1:
        ins = first_hr + len("\n---\n")
        content = content[:ins] + "\n" + niche_table + "\n" + content[ins:]
    else:
        content = content.rstrip() + "\n\n" + niche_table

    # Strip any old Backlinks section
    bl = "\n---\n\n## 🔗 Backlinks"
    if bl in content:
        content = content[:content.rfind(bl)].rstrip() + "\n"

    return content


def build_stub(company_name, nif, service, niche, tipo, status, canonical_stem):
    """Lightweight stub that links to the canonical profile."""
    return (
        f"# {company_name}\n\n"
        f"> 📌 **Perfil Completo:** [[{canonical_stem}]]\n\n"
        f"| Campo | Valor |\n"
        f"|---|---|\n"
        f"| **NIF** | `{nif}` |\n"
        f"| **Status ANPG** | {status} |\n"
        f"| **Serviço** | {service} |\n"
        f"| **Actividade / Nicho** | {niche} |\n"
        f"| **Tipo de Sociedade** | {tipo} |\n\n"
        f"→ Consulte [[{canonical_stem}]] para informação completa sobre esta empresa "
        f"(contactos, website, LinkedIn, cadeia de valor, como se candidatar).\n"
    )


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deduplicate company_hierarchy .md files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show stats only, do not write files")
    parser.add_argument("--root", default=HIER_ROOT,
                        help=f"Root of company_hierarchy (default: {HIER_ROOT})")
    args = parser.parse_args()

    hier_root    = args.root.rstrip(os.sep)
    profiles_dir = os.path.join(hier_root, "_Profiles")
    dry_run      = args.dry_run

    print(f"{'[DRY RUN] ' if dry_run else ''}Scanning: {hier_root}")

    # Load status from CSV (fast fallback)
    status_map = load_status_map(CSV_PATH)
    print(f"Status map: {len(status_map):,} NIFs loaded from CSV")

    # ── Pass 1: index all .md files by NIF (NO file reads) ───────────────────
    nif_groups = defaultdict(list)
    total_scanned = 0

    for dirpath, dirs, files in os.walk(_wp(hier_root)):
        # Prune _Profiles and any _-prefixed dirs
        dirs[:] = [d for d in dirs if not d.startswith("_")]

        norm_dir = dirpath.replace("\\\\?\\", "")
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            fpath = os.path.join(norm_dir, fname)
            total_scanned += 1

            parsed = parse_filepath(fpath, hier_root)
            if parsed is None:
                continue
            company_name, nif, service, niche, tipo = parsed
            status = status_map.get(nif, "Preferência")

            nif_groups[nif].append({
                "fpath":        fpath,
                "company_name": company_name,
                "service":      service,
                "niche":        niche,
                "tipo":         tipo,
                "status":       status,
            })

    print(f"Scanned {total_scanned:,} files | {len(nif_groups):,} unique NIFs")

    solo      = sum(1 for v in nif_groups.values() if len(v) == 1)
    dup_nifs  = sum(1 for v in nif_groups.values() if len(v) > 1)
    dup_files = sum(len(v) for v in nif_groups.values() if len(v) > 1)
    print(f"  Solo companies       : {solo:,}")
    print(f"  Multi-folder NIFs    : {dup_nifs:,}  ({dup_files:,} files)")

    if dry_run:
        print("\n[DRY RUN] No files written. Re-run without --dry-run to apply.")
        return

    os.makedirs(_wp(profiles_dir), exist_ok=True)

    # ── Pass 2: build canonicals + stubs ─────────────────────────────────────
    canonicals_written = 0
    stubs_written      = 0
    errors             = 0

    for nif, entries in nif_groups.items():
        if len(entries) == 1:
            continue

        company_name   = entries[0]["company_name"]
        canonical_stem = f"{company_name}_{nif}"
        canonical_path = os.path.join(profiles_dir, canonical_stem + ".md")

        # Read ONE representative file (smallest service-number → highest priority)
        entries_sorted = sorted(entries, key=lambda e: e["service"])
        sample_content = read_one_file(entries_sorted[0]["fpath"])

        if not sample_content:
            errors += 1
            continue

        # Build and write canonical
        canonical_content = build_canonical_profile(
            company_name, nif, entries, sample_content
        )
        write_file(canonical_path, canonical_content)
        canonicals_written += 1

        # Build and write stubs for every folder instance
        for ent in entries:
            stub = build_stub(
                ent["company_name"], nif,
                ent["service"], ent["niche"], ent["tipo"], ent["status"],
                canonical_stem,
            )
            write_file(ent["fpath"], stub)
            stubs_written += 1

        if canonicals_written % 500 == 0:
            print(f"  … {canonicals_written:,} canonicals written")

    print(f"\nDone.")
    print(f"  Canonical profiles created : {canonicals_written:,}  →  {profiles_dir}")
    print(f"  Stub files written         : {stubs_written:,}")
    print(f"  Solo files unchanged       : {solo:,}")
    print(f"  Read errors                : {errors:,}")


if __name__ == "__main__":
    main()

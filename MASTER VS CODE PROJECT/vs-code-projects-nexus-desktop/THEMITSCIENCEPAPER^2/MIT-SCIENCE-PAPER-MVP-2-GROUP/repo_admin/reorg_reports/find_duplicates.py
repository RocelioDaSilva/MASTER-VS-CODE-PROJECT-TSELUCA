import os, json

root = r"c:\Users\PCGAME\Desktop\Master VS CODE PROJECTS\THEMITSCIENCEPAPER^2\MIT-SCIENCE-PAPER-MVP-2-GROUP"

dups = {}
for dirpath, dirs, files in os.walk(root):
    for f in files:
        dups.setdefault(f, []).append(os.path.join(dirpath, f))

# Keep only duplicates
dups = {k: v for k, v in dups.items() if len(v) > 1}

out_dir = os.path.join(root, 'repo_admin', 'reorg_reports')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'duplicates.json')
with open(out_path, 'w', encoding='utf-8') as fh:
    json.dump(dups, fh, indent=2)

# Print a short summary
sorted_dups = sorted(dups.items(), key=lambda x: -len(x[1]))
for name, paths in sorted_dups[:100]:
    print(f"{name}: {len(paths)}")

print('\nReport written to:', out_path)

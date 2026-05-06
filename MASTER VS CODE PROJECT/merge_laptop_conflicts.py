#!/usr/bin/env python3
import os, re, hashlib

ROOT = r"C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT\MASTER-VS-CODE-PROJECT-TSELUCA"
pattern = re.compile(r'^(?P<base>.*?)(?P<suffix>_LAPTOP(?:_\d+)?)(?P<ext>\..*)?$')


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def is_text_file(path):
    try:
        with open(path, 'rb') as f:
            sample = f.read(4096)
        if b'\0' in sample:
            return False
        try:
            sample.decode('utf-8')
            return True
        except Exception:
            try:
                sample.decode('latin1')
                return True
            except Exception:
                return False
    except Exception:
        return False

merged = []
renamed = []
removed = []
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fname in list(filenames):
        m = pattern.match(fname)
        if not m:
            continue
        base = m.group('base')
        ext = m.group('ext') or ''
        laptop_name = fname
        laptop_path = os.path.join(dirpath, laptop_name)
        base_name = base + ext
        base_path = os.path.join(dirpath, base_name)

        try:
            if os.path.exists(base_path):
                try:
                    if md5(base_path) == md5(laptop_path):
                        os.remove(laptop_path)
                        removed.append(laptop_path)
                        continue
                except Exception as e:
                    errors.append((laptop_path, str(e)))
                    continue

                # Both exist and are different
                if is_text_file(base_path) and is_text_file(laptop_path):
                    lowbase = base_name.lower()
                    # Merge .gitignore variants by unique-line union
                    if lowbase.startswith('.gitignore'):
                        def read_lines(p):
                            with open(p, 'r', encoding='utf-8', errors='replace') as fh:
                                return [line.rstrip('\n') for line in fh]
                        base_lines = read_lines(base_path)
                        lap_lines = read_lines(laptop_path)
                        seen = set()
                        merged_lines = []
                        for L in base_lines:
                            if L not in seen:
                                merged_lines.append(L)
                                seen.add(L)
                        added = 0
                        for L in lap_lines:
                            if L not in seen:
                                merged_lines.append(L)
                                seen.add(L)
                                added += 1
                        with open(base_path, 'w', encoding='utf-8') as fh:
                            fh.write('\n'.join(merged_lines) + ('\n' if merged_lines and not merged_lines[-1].endswith('\n') else ''))
                        os.remove(laptop_path)
                        merged.append((base_path, laptop_path, 'gitignore', added))
                    else:
                        # Generic text merge: append laptop content under marker if not already contained
                        with open(base_path, 'r', encoding='utf-8', errors='replace') as fh:
                            base_text = fh.read()
                        with open(laptop_path, 'r', encoding='utf-8', errors='replace') as fh:
                            lap_text = fh.read()
                        if lap_text.strip() == '':
                            # nothing to merge
                            os.remove(laptop_path)
                            removed.append(laptop_path)
                        elif lap_text in base_text:
                            os.remove(laptop_path)
                            removed.append(laptop_path)
                        else:
                            marker = "\n\n# ----- MERGED FROM LAPTOP VERSION -----\n\n"
                            merged_text = base_text + marker + lap_text
                            with open(base_path, 'w', encoding='utf-8') as fh:
                                fh.write(merged_text)
                            os.remove(laptop_path)
                            merged.append((base_path, laptop_path, 'append'))
                else:
                    # Binary or non-text -> keep both (do nothing)
                    continue
            else:
                # Base does not exist -> rename laptop to base (remove suffix)
                newpath = os.path.join(dirpath, base_name)
                os.rename(laptop_path, newpath)
                renamed.append((laptop_path, newpath))
        except Exception as e:
            errors.append((laptop_path, str(e)))

# Summary
print('MERGE CONFLICTS SUMMARY')
print('Merged (files updated by merge):', len(merged))
for item in merged:
    print(' -', item)
print('Renamed (no original present):', len(renamed))
for item in renamed:
    print(' -', item)
print('Removed (identical duplicates removed):', len(removed))
for item in removed:
    print(' -', item)
if errors:
    print('Errors:', len(errors))
    for e in errors:
        print(' -', e)

# Exit code 0

Scripts README
===============

`copy_finished_manuscript.py` — duplicates the original
`finished-manuscript/` folder into `finished-manuscript-reorg/original_copy/`.

Usage
-----
PowerShell
```
cd finished-manuscript-reorg\scripts
python copy_finished_manuscript.py
```

To overwrite an existing copy, add `--force`:
```
python copy_finished_manuscript.py --force
```

After the copy completes, you can test LaTeX builds from `src/tex/` using the
wrapper files. They reference the originals in `finished-manuscript/` until you
promote files into this reorg copy.

from pathlib import Path
import subprocess

BASE = Path(r"c:\Users\PCGAME\Desktop\reservatórios")
INPUT_TEX = BASE / "Estudar" / "matéria" / "revisão para a prova" / "compendio_revisao_prova.tex"
OUT_TEX = BASE / "Estudar" / "matéria" / "revisão para a prova" / "compendio_prova_topicos.tex"
OUT_DIR = OUT_TEX.parent

TARGET_FILES = [
    'cap1_transcription.md',
    'cap2_transcription.md',
    'cap3_transcription.md',
    'cap4_transcription.md',
]

EXAM_SECTION = r"""
\clearpage
\section{Tópicos para prova}
\begin{enumerate}
\item Verdadeiro ou falso — Capítulo 1. Responda Verdadeiro (V) ou Falso (F) para cada afirmação e justifique sucintamente.
\vspace{6mm}
\item Dissertação (Redação) — Capítulo 4. Desenvolva uma redação técnica (máx. 1 página) sobre um tema relacionado ao cálculo volumétrico e incertezas (explique metodologia e discuta fontes de erro).
\vspace{6mm}
\item Cálculo/prático — Capítulo 2. Resolva um problema prático de PVT/Conversões: calcule $B_o$ e converta $R_s$ para unidades SI, mostrando todos os passos.
\vspace{6mm}
\item Cálculo/prático — Capítulo 3. Resolva um problema de porosidade/permeabilidade (ex.: cálculo de porosidade por pesagem e método de Arquímedes). Mostre passos e unidades.
\vspace{6mm}
\end{enumerate}
"""


def main():
    if not INPUT_TEX.exists():
        print('Input .tex not found:', INPUT_TEX)
        return
    text = INPUT_TEX.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)

    # find all file markers
    markers = []  # list of (name, index)
    for i,ln in enumerate(lines):
        if ln.startswith('% ---- file: '):
            name = ln[len('% ---- file: '):].strip()
            markers.append((name, i))

    if not markers:
        print('No file markers found in input .tex')
        return

    # preamble is lines up to first marker
    first_marker_idx = markers[0][1]
    preamble = lines[:first_marker_idx]

    # build a mapping from name->start idx and compute end indices
    name_to_idx = {name: idx for name, idx in markers}
    sorted_markers = sorted(markers, key=lambda x: x[1])
    # compute end index for each marker as start of next marker, or len(lines)
    end_indices = {}
    for k in range(len(sorted_markers)):
        name, idx = sorted_markers[k]
        if k+1 < len(sorted_markers):
            end_indices[name] = sorted_markers[k+1][1]
        else:
            # up to before \end{document}
            # find \end{document}
            try:
                end_doc = next(i for i,l in enumerate(lines) if l.strip().startswith('\\end{document}'))
            except StopIteration:
                end_doc = len(lines)
            end_indices[name] = end_doc

    # collect sections for target files
    selected = []
    for t in TARGET_FILES:
        if t in name_to_idx:
            start = name_to_idx[t]
            end = end_indices.get(t, len(lines))
            selected.extend(lines[start:end])
        else:
            print('Warning: target file not present in .tex:', t)

    # compose output
    out_lines = []
    out_lines.extend(preamble)
    out_lines.extend(selected)
    out_lines.append(EXAM_SECTION)
    out_lines.append('\n\\end{document}\n')

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TEX.write_text(''.join(out_lines), encoding='utf-8')
    print('Wrote', OUT_TEX)

    # compile with xelatex twice
    cmd = ['xelatex', '-interaction=nonstopmode', str(OUT_TEX.name)]
    # run in OUT_DIR
    try:
        subprocess.run(cmd, cwd=str(OUT_DIR), check=True)
        subprocess.run(cmd, cwd=str(OUT_DIR), check=True)
        print('PDF generated:', OUT_TEX.with_suffix('.pdf'))
    except subprocess.CalledProcessError as e:
        print('xelatex failed with', e.returncode)


if __name__ == '__main__':
    main()

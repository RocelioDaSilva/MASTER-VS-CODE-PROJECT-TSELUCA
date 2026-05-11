\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cwbook_enhanced}[2026/04 Enhanced POV Book Class — Chain Weapon Story]

\LoadClass[12pt,openany]{book}

% ═══════════════════════════════════════════════════════
% CORE PACKAGES
% ═══════════════════════════════════════════════════════
\RequirePackage[paperwidth=6in,paperheight=9in,
  inner=0.9in,outer=0.8in,top=1.05in,bottom=0.95in,
  headsep=12pt,headheight=28pt]{geometry}
\RequirePackage{fontspec}
\defaultfontfeatures{Ligatures=TeX}
\setmainfont{TeX Gyre Pagella}
\setsansfont{TeX Gyre Heros}
\RequirePackage{microtype}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\usetikzlibrary{calc,decorations.pathmorphing}
\RequirePackage{fancyhdr}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
\RequirePackage{etoolbox}
\RequirePackage{eso-pic}
\RequirePackage{lettrine}

% ═══════════════════════════════════════════════════════
% COLOUR PALETTE
% ═══════════════════════════════════════════════════════
\definecolor{cwink}{RGB}{40,30,24}
\definecolor{cwinksoft}{RGB}{92,74,58}
\definecolor{PageBg}{HTML}{F8F3EC}
\definecolor{Ink}{HTML}{1C1812}
\definecolor{InkMid}{HTML}{3A3028}
\definecolor{Stone}{HTML}{9A8A78}
\definecolor{StoneLight}{HTML}{C8B8A8}

% Character accent colours
\definecolor{ColAisen}{HTML}{7A6A50}
\definecolor{ColCaspian}{HTML}{5A6A7A}
\definecolor{ColCorvin}{HTML}{4A4A4A}
\definecolor{ColRyo}{HTML}{6A7A5A}
\definecolor{ColKael}{HTML}{7A5A3A}
\definecolor{ColKairos}{HTML}{6A5A7A}
\definecolor{ColOrin}{HTML}{8A7A6A}
\definecolor{ColAmara}{HTML}{6A5A4A}
\definecolor{ColRenard}{HTML}{5A6A5A}
\definecolor{ColEmma}{HTML}{7A5A6A}
\definecolor{ColHistorian}{HTML}{6A6A6A}
\definecolor{ColMultiple}{HTML}{8A7A6A}

% ═══════════════════════════════════════════════════════
% COUNTERS & HOOKS
% ═══════════════════════════════════════════════════════
\newcommand{\CurrentChapterNum}{1}
\newcommand{\TotalChapters}{52}
\newcommand{\POVColor}{ColAisen}

% ═══════════════════════════════════════════════════════
% TIKZ LANDSCAPE SILHOUETTE SYSTEM
% ═══════════════════════════════════════════════════════
% Environment types: default, city, north, dungeon, wasteland
\newcommand{\cw@envtype}{default}
\newcommand{\cw@loctext}{}
\newcommand{\ENV}[1]{\renewcommand{\cw@envtype}{#1}}
\newcommand{\LOC}[1]{\renewcommand{\cw@loctext}{#1}}

% ─────────────────────────────────────────────────────────
% DEFAULT — Pastoral rolling hills, oak groves, smoke
% ─────────────────────────────────────────────────────────
\newcommand{\cw@land@default@top}{%
  % Warm sky wash
  \fill[\POVColor!5] (0,0) rectangle (1,1.1);
  \fill[\POVColor!3,opacity=0.6] (0,0) rectangle (1,0.35);
  % Far-distant haze ridge
  \fill[\POVColor!10,opacity=0.5] (0,0)
    .. controls (0.12,0.52) and (0.20,0.60) .. (0.32,0.55)
    .. controls (0.44,0.50) and (0.52,0.68) .. (0.64,0.60)
    .. controls (0.76,0.52) and (0.84,0.70) .. (0.95,0.58)
    -- (1,0.52) -- (1,0) -- (0,0) -- cycle;
  % Mid hills — undulating
  \fill[\POVColor!18] (0,0)
    .. controls (0.06,0.40) and (0.14,0.50) .. (0.24,0.42)
    .. controls (0.32,0.35) and (0.40,0.48) .. (0.50,0.40)
    .. controls (0.58,0.34) and (0.66,0.52) .. (0.76,0.44)
    .. controls (0.86,0.36) and (0.94,0.42) .. (1,0.35)
    -- (1,0) -- (0,0) -- cycle;
  % Near foreground ridge
  \fill[\POVColor!28] (0,0)
    .. controls (0.10,0.25) and (0.22,0.32) .. (0.35,0.26)
    .. controls (0.46,0.20) and (0.56,0.30) .. (0.68,0.24)
    .. controls (0.78,0.18) and (0.88,0.28) .. (1,0.20)
    -- (1,0) -- (0,0) -- cycle;
  % Tree cluster left — five conifers graded in size
  \fill[\POVColor!35]
    (0.03,0.22) -- (0.035,0.34) -- (0.04,0.22) -- cycle
    (0.045,0.26) -- (0.052,0.40) -- (0.059,0.26) -- cycle
    (0.065,0.23) -- (0.071,0.37) -- (0.077,0.23) -- cycle
    (0.085,0.24) -- (0.09,0.35) -- (0.095,0.24) -- cycle;
  % Tree cluster right — mixed sizes
  \fill[\POVColor!35]
    (0.90,0.22) -- (0.906,0.38) -- (0.912,0.22) -- cycle
    (0.92,0.20) -- (0.925,0.34) -- (0.93,0.20) -- cycle
    (0.935,0.22) -- (0.942,0.40) -- (0.949,0.22) -- cycle
    (0.955,0.21) -- (0.96,0.32) -- (0.965,0.21) -- cycle;
  % Scattered mid-field trees
  \fill[\POVColor!25]
    (0.36,0.27) -- (0.365,0.36) -- (0.37,0.27) -- cycle
    (0.62,0.25) -- (0.626,0.35) -- (0.632,0.25) -- cycle;
  % Chimney smoke wisps (tiny curving lines)
  \draw[\POVColor!15,line width=0.3pt,opacity=0.5]
    (0.37,0.36) .. controls (0.373,0.42) and (0.378,0.44) .. (0.376,0.50);
  \draw[\POVColor!12,line width=0.2pt,opacity=0.4]
    (0.372,0.36) .. controls (0.368,0.43) and (0.374,0.47) .. (0.370,0.52);
  % Birds — tiny v-shapes
  \draw[\POVColor!20,line width=0.25pt]
    (0.48,0.70) -- (0.484,0.72) -- (0.488,0.70)
    (0.50,0.74) -- (0.504,0.76) -- (0.508,0.74)
    (0.52,0.72) -- (0.524,0.74) -- (0.528,0.72);
}
\newcommand{\cw@land@default@bot}{%
  \fill[\POVColor!5] (0,0) rectangle (1,1.1);
  % Meadow ground — two layers
  \fill[\POVColor!12] (0,0)
    .. controls (0.10,0.28) and (0.22,0.34) .. (0.36,0.30)
    .. controls (0.50,0.26) and (0.62,0.36) .. (0.76,0.32)
    .. controls (0.88,0.28) and (0.96,0.34) .. (1,0.30)
    -- (1,0) -- (0,0) -- cycle;
  \fill[\POVColor!18] (0,0)
    .. controls (0.08,0.18) and (0.16,0.22) .. (0.28,0.20)
    .. controls (0.40,0.18) and (0.52,0.24) .. (0.64,0.22)
    .. controls (0.76,0.18) and (0.88,0.22) .. (1,0.18)
    -- (1,0) -- (0,0) -- cycle;
  % Fence posts with cross-rail
  \fill[\POVColor!28]
    (0.10,0.22) rectangle (0.105,0.40)
    (0.092,0.37) rectangle (0.113,0.39);
  \fill[\POVColor!28]
    (0.90,0.24) rectangle (0.905,0.42)
    (0.892,0.39) rectangle (0.913,0.41);
  \draw[\POVColor!22,line width=0.3pt]
    (0.105,0.34) -- (0.90,0.36);
  \draw[\POVColor!20,line width=0.2pt]
    (0.105,0.30) -- (0.90,0.32);
  % Wildflower dots
  \fill[\POVColor!20,opacity=0.5]
    (0.30,0.22) circle (0.003)
    (0.34,0.24) circle (0.002)
    (0.44,0.21) circle (0.003)
    (0.56,0.24) circle (0.002)
    (0.66,0.22) circle (0.003)
    (0.72,0.23) circle (0.002);
}

% ─────────────────────────────────────────────────────────
% CITY — Layered skyline with spires, windows, smoke
% ─────────────────────────────────────────────────────────
\newcommand{\cw@land@city@top}{%
  % Warm dusk sky
  \fill[\POVColor!6] (0,0) rectangle (1,1.1);
  \fill[\POVColor!3,opacity=0.4] (0,0) rectangle (1,0.20);
  % Distant silhouette layer (faint, wide)
  \fill[\POVColor!14,opacity=0.6]
    (0,0.18) -- (0.04,0.18) -- (0.04,0.38) -- (0.08,0.38)
    -- (0.08,0.26) -- (0.16,0.26) -- (0.16,0.42) -- (0.20,0.42)
    -- (0.20,0.30) -- (0.32,0.30) -- (0.32,0.36) -- (0.40,0.36)
    -- (0.40,0.24) -- (0.52,0.24) -- (0.52,0.40) -- (0.58,0.40)
    -- (0.58,0.28) -- (0.70,0.28) -- (0.70,0.38) -- (0.78,0.38)
    -- (0.78,0.22) -- (0.88,0.22) -- (0.88,0.32) -- (0.96,0.32)
    -- (0.96,0.18) -- (1,0.18)
    -- (1,0) -- (0,0) -- cycle;
  % Main buildings — foreground
  \fill[\POVColor!30]
    (0.025,0) rectangle (0.055,0.68)        % narrow tower L
    (0.07,0) rectangle (0.09,0.80)          % thin spire
    (0.105,0) rectangle (0.145,0.88);       % wide tower
  % Peaked roof 1
  \fill[\POVColor!30]
    (0.20,0) -- (0.24,0.52) -- (0.28,0) -- cycle;
  % Central cluster
  \fill[\POVColor!30]
    (0.34,0) rectangle (0.38,0.74)
    (0.40,0) rectangle (0.42,0.92);
  \fill[\POVColor!30]
    (0.46,0) rectangle (0.50,0.68);
  % Peaked roof 2
  \fill[\POVColor!30]
    (0.56,0.08) -- (0.60,0.62) -- (0.64,0.08) -- cycle;
  % Right cluster
  \fill[\POVColor!30]
    (0.70,0) rectangle (0.74,0.85)
    (0.77,0) rectangle (0.80,0.70)
    (0.84,0) rectangle (0.87,0.58);
  % Window dots (life in the city)
  \fill[\POVColor!8,opacity=0.8]
    (0.115,0.72) circle (0.004)  (0.125,0.72) circle (0.004)
    (0.115,0.62) circle (0.004)  (0.125,0.62) circle (0.004)
    (0.115,0.52) circle (0.004)  (0.125,0.52) circle (0.004)
    (0.355,0.58) circle (0.004)  (0.365,0.58) circle (0.004)
    (0.355,0.48) circle (0.004)  (0.365,0.48) circle (0.004)
    (0.715,0.68) circle (0.004)  (0.725,0.68) circle (0.004)
    (0.715,0.58) circle (0.004)  (0.725,0.58) circle (0.004)
    (0.715,0.48) circle (0.004)  (0.725,0.48) circle (0.004);
  % Chimney smoke
  \draw[\POVColor!12,line width=0.25pt,opacity=0.5]
    (0.42,0.92) .. controls (0.425,0.98) and (0.43,1.02) .. (0.428,1.07);
  \draw[\POVColor!10,line width=0.2pt,opacity=0.35]
    (0.418,0.92) .. controls (0.415,0.97) and (0.42,1.00) .. (0.416,1.05);
}
\newcommand{\cw@land@city@bot}{%
  \fill[\POVColor!5] (0,0) rectangle (1,1.1);
  % Cobblestone ground layer
  \fill[\POVColor!14] (0,0)
    -- (0,0.20) -- (0.08,0.22) -- (0.20,0.18) -- (0.36,0.24)
    -- (0.50,0.20) -- (0.66,0.22) -- (0.80,0.18) -- (0.92,0.24) -- (1,0.20)
    -- (1,0) -- cycle;
  % Low walls/structures
  \fill[\POVColor!22]
    (0.06,0.18) rectangle (0.08,0.34)
    (0.05,0.32) rectangle (0.09,0.36)
    (0.12,0.18) rectangle (0.15,0.30);
  % Ground shadows — soft ellipses
  \fill[\POVColor!8,opacity=0.5]
    (0.30,0.14) ellipse [x radius=0.06, y radius=0.04]
    (0.55,0.15) ellipse [x radius=0.05, y radius=0.03]
    (0.78,0.16) ellipse [x radius=0.04, y radius=0.03];
  % Cobblestone texture — tiny rectangles
  \fill[\POVColor!18,opacity=0.3]
    (0.24,0.08) rectangle (0.255,0.10)
    (0.26,0.06) rectangle (0.275,0.08)
    (0.28,0.09) rectangle (0.29,0.11)
    (0.44,0.07) rectangle (0.455,0.09)
    (0.46,0.10) rectangle (0.47,0.12)
    (0.64,0.08) rectangle (0.655,0.10)
    (0.66,0.06) rectangle (0.675,0.08);
  % Cart wheel
  \draw[\POVColor!25,line width=0.3pt]
    (0.88,0.28) circle (0.025);
  \draw[\POVColor!25,line width=0.2pt]
    (0.88,0.255) -- (0.88,0.305)
    (0.855,0.28) -- (0.905,0.28);
}

% ─────────────────────────────────────────────────────────
% NORTH — Jagged peaks, snow veils, aurora wisps
% ─────────────────────────────────────────────────────────
\newcommand{\cw@land@north@top}{%
  % Cold pale sky
  \fill[\POVColor!5] (0,0) rectangle (1,1.1);
  % Distant haze ridge
  \fill[\POVColor!8,opacity=0.4] (0,0)
    .. controls (0.15,0.38) and (0.30,0.42) .. (0.50,0.35)
    .. controls (0.70,0.28) and (0.85,0.40) .. (1,0.32)
    -- (1,0) -- (0,0) -- cycle;
  % Main mountain range — sharp peaks polygon
  \fill[\POVColor!22]
    (0,0.08)
    -- (0.065,0.58) -- (0.13,0.30)
    -- (0.20,0.70) -- (0.265,0.38)
    -- (0.33,0.82) -- (0.395,0.28)
    -- (0.465,0.78) -- (0.53,0.35)
    -- (0.60,0.72) -- (0.665,0.30)
    -- (0.73,0.80) -- (0.80,0.40)
    -- (0.87,0.75) -- (0.935,0.32)
    -- (1,0.68)
    -- (1,0) -- (0,0) -- cycle;
  % Near foothills — darker
  \fill[\POVColor!32]
    (0,0.10)
    .. controls (0.08,0.24) and (0.16,0.20) .. (0.24,0.26)
    .. controls (0.32,0.32) and (0.40,0.18) .. (0.50,0.22)
    .. controls (0.60,0.28) and (0.68,0.16) .. (0.78,0.24)
    .. controls (0.86,0.30) and (0.94,0.18) .. (1,0.22)
    -- (1,0) -- (0,0) -- cycle;
  % Snow caps — white highlights on tallest peaks
  \fill[white,opacity=0.15]
    (0.20,0.70) -- (0.215,0.64) -- (0.185,0.64) -- cycle
    (0.33,0.82) -- (0.345,0.74) -- (0.315,0.74) -- cycle
    (0.465,0.78) -- (0.48,0.72) -- (0.45,0.72) -- cycle
    (0.73,0.80) -- (0.745,0.72) -- (0.715,0.72) -- cycle;
  % Atmospheric haze line at foothills
  \draw[\POVColor!10,line width=0.4pt,opacity=0.4]
    (0,0.32) .. controls (0.25,0.36) and (0.50,0.30) ..
    (0.75,0.34) .. controls (0.88,0.36) and (0.96,0.32) .. (1,0.34);
}
\newcommand{\cw@land@north@bot}{%
  \fill[\POVColor!4] (0,0) rectangle (1,1.1);
  % Snow field — gentle undulations
  \fill[\POVColor!12] (0,0)
    .. controls (0.06,0.20) and (0.14,0.24) .. (0.22,0.18)
    .. controls (0.30,0.12) and (0.38,0.22) .. (0.46,0.16)
    .. controls (0.54,0.10) and (0.62,0.24) .. (0.70,0.18)
    .. controls (0.78,0.12) and (0.86,0.22) .. (0.94,0.16)
    -- (1,0.14) -- (1,0) -- (0,0) -- cycle;
  % Deeper snow drifts
  \fill[\POVColor!8] (0,0)
    .. controls (0.10,0.12) and (0.20,0.16) .. (0.30,0.10)
    .. controls (0.40,0.06) and (0.50,0.14) .. (0.60,0.08)
    .. controls (0.70,0.04) and (0.80,0.14) .. (0.90,0.08)
    -- (1,0.06) -- (1,0) -- (0,0) -- cycle;
  % Snow patch highlights
  \fill[white,opacity=0.15]
    (0.18,0.12) ellipse [x radius=0.015, y radius=0.04]
    (0.42,0.10) ellipse [x radius=0.012, y radius=0.035]
    (0.66,0.12) ellipse [x radius=0.018, y radius=0.045]
    (0.88,0.10) ellipse [x radius=0.010, y radius=0.03];
  % Frozen puddle reflections
  \fill[\POVColor!6,opacity=0.3]
    (0.30,0.05) ellipse [x radius=0.020, y radius=0.02]
    (0.55,0.04) ellipse [x radius=0.015, y radius=0.015]
    (0.80,0.05) ellipse [x radius=0.018, y radius=0.018];
  % Wind-blown snow streaks
  \draw[white,opacity=0.08,line width=0.3pt]
    (0.10,0.18) -- (0.22,0.16)
    (0.40,0.14) -- (0.52,0.12)
    (0.70,0.16) -- (0.82,0.14);
}

% ─────────────────────────────────────────────────────────
% DUNGEON — Vaulted ceiling, stalactites, torch glow
% ─────────────────────────────────────────────────────────
\newcommand{\cw@land@dungeon@top}{%
  % Deep darkness
  \fill[\POVColor!30!black] (0,0) rectangle (1,1.1);
  % Subtle vault arch gradient (lighter at center-top)
  \fill[\POVColor!38!black,opacity=0.3]
    (0.30,1.1) .. controls (0.40,0.60) and (0.60,0.60) .. (0.70,1.1) -- cycle;
  % Rounded pillar L
  \fill[\POVColor!22!black]
    (0.03,0) rectangle (0.055,0.62);
  \fill[\POVColor!25!black]
    (0.055,0) rectangle (0.06,0.62);           % highlight edge
  % Rounded pillar L2
  \fill[\POVColor!20!black]
    (0.09,0) rectangle (0.115,0.74);
  \fill[\POVColor!24!black]
    (0.115,0) rectangle (0.12,0.74);
  % Stalactites — varied thickness
  \fill[\POVColor!18!black]
    (0.18,0) -- (0.195,0.60) -- (0.21,0) -- cycle
    (0.22,0) -- (0.24,0.72) -- (0.26,0) -- cycle;
  \fill[\POVColor!16!black]
    (0.30,0) -- (0.32,0.55) -- (0.34,0) -- cycle;
  % Wide cavern arch
  \fill[\POVColor!18!black]
    (0.42,0) -- (0.48,0.48) -- (0.54,0) -- cycle;
  % Right pillar
  \fill[\POVColor!22!black]
    (0.58,0) rectangle (0.60,0.54);
  \fill[\POVColor!25!black]
    (0.60,0) rectangle (0.605,0.54);
  % Right stalactites cluster
  \fill[\POVColor!18!black]
    (0.68,0) -- (0.70,0.74) -- (0.72,0) -- cycle
    (0.74,0) -- (0.76,0.58) -- (0.78,0) -- cycle;
  \fill[\POVColor!16!black]
    (0.82,0) -- (0.84,0.65) -- (0.86,0) -- cycle;
  % Far-right pillar
  \fill[\POVColor!20!black]
    (0.92,0) rectangle (0.945,0.48);
  % Torch glow — warm halos
  \fill[\POVColor!45!black,opacity=0.08]
    (0.30,0.30) circle (0.06);
  \fill[\POVColor!45!black,opacity=0.06]
    (0.70,0.35) circle (0.055);
}
\newcommand{\cw@land@dungeon@bot}{%
  % Dark floor
  \fill[\POVColor!25!black] (0,0) rectangle (1,1.1);
  % Stone floor texture — subtle uneven line
  \fill[\POVColor!20!black] (0,0)
    -- (0,0.08) .. controls (0.10,0.10) and (0.20,0.06) .. (0.30,0.09)
    .. controls (0.40,0.12) and (0.50,0.06) .. (0.60,0.10)
    .. controls (0.70,0.14) and (0.80,0.07) .. (0.90,0.11)
    -- (1,0.08) -- (1,0) -- cycle;
  % Puddle reflections — ellipses with subtle glow
  \fill[\POVColor!15!black]
    (0.15,0.14) ellipse [x radius=0.025, y radius=0.05]
    (0.28,0.12) ellipse [x radius=0.018, y radius=0.04]
    (0.42,0.13) ellipse [x radius=0.030, y radius=0.06]
    (0.58,0.11) ellipse [x radius=0.022, y radius=0.04]
    (0.72,0.14) ellipse [x radius=0.028, y radius=0.055];
  % Reflected light shimmer in largest puddle
  \draw[\POVColor!35!black,line width=0.2pt,opacity=0.4]
    (0.40,0.13) .. controls (0.42,0.17) and (0.43,0.17) .. (0.44,0.13);
  % Floor pillar base
  \fill[\POVColor!28!black]
    (0.85,0) rectangle (0.87,0.22);
  \fill[\POVColor!30!black]
    (0.84,0.18) rectangle (0.88,0.24);   % capital
  % Scattered pebbles
  \fill[\POVColor!18!black]
    (0.20,0.06) circle (0.004)
    (0.50,0.05) circle (0.003)
    (0.65,0.07) circle (0.004)
    (0.80,0.05) circle (0.003);
}

% ─────────────────────────────────────────────────────────
% WASTELAND — Scorched dunes, ruins, heat haze
% ─────────────────────────────────────────────────────────
\newcommand{\cw@land@wasteland@top}{%
  % Hot hazy sky
  \fill[\POVColor!6] (0,0) rectangle (1,1.1);
  \fill[\POVColor!4,opacity=0.5] (0,0) rectangle (1,0.40);
  % Far dune ridge (faint)
  \fill[\POVColor!12,opacity=0.5] (0,0)
    .. controls (0.10,0.38) and (0.25,0.40) .. (0.40,0.32)
    .. controls (0.55,0.24) and (0.70,0.42) .. (0.85,0.35)
    -- (1,0.30) -- (1,0) -- (0,0) -- cycle;
  % Main dune forms — flowing curves
  \fill[\POVColor!20] (0,0)
    .. controls (0.05,0.30) and (0.12,0.50) .. (0.22,0.42)
    .. controls (0.30,0.35) and (0.38,0.58) .. (0.48,0.46)
    .. controls (0.56,0.36) and (0.64,0.55) .. (0.74,0.44)
    .. controls (0.82,0.35) and (0.90,0.50) .. (1,0.38)
    -- (1,0) -- (0,0) -- cycle;
  % Near ground
  \fill[\POVColor!28] (0,0)
    .. controls (0.12,0.20) and (0.24,0.28) .. (0.38,0.22)
    .. controls (0.50,0.16) and (0.62,0.24) .. (0.76,0.18)
    .. controls (0.88,0.12) and (0.96,0.20) .. (1,0.16)
    -- (1,0) -- (0,0) -- cycle;
  % Ruin fragments — broken wall segments
  \fill[\POVColor!35]
    (0.16,0.22) rectangle (0.168,0.34)
    (0.172,0.22) rectangle (0.178,0.30)
    (0.182,0.22) rectangle (0.187,0.26);
  \fill[\POVColor!35]
    (0.82,0.14) rectangle (0.826,0.28)
    (0.83,0.14) rectangle (0.838,0.22);
  % Heat haze shimmer
  \draw[\POVColor!15,line width=0.2pt,opacity=0.3,decorate,
    decoration={snake,amplitude=0.3pt,segment length=3pt}]
    (0.10,0.36) -- (0.90,0.34);
  \draw[\POVColor!12,line width=0.15pt,opacity=0.2,decorate,
    decoration={snake,amplitude=0.2pt,segment length=2.5pt}]
    (0.05,0.42) -- (0.95,0.40);
}
\newcommand{\cw@land@wasteland@bot}{%
  \fill[\POVColor!5] (0,0) rectangle (1,1.1);
  % Cracked earth layers
  \fill[\POVColor!15] (0,0)
    .. controls (0.05,0.22) and (0.12,0.18) .. (0.20,0.24)
    .. controls (0.28,0.30) and (0.36,0.20) .. (0.46,0.26)
    .. controls (0.56,0.32) and (0.64,0.22) .. (0.74,0.28)
    .. controls (0.84,0.34) and (0.92,0.24) .. (1,0.28)
    -- (1,0) -- (0,0) -- cycle;
  \fill[\POVColor!20] (0,0)
    .. controls (0.08,0.14) and (0.16,0.10) .. (0.24,0.16)
    .. controls (0.34,0.22) and (0.42,0.12) .. (0.52,0.18)
    .. controls (0.62,0.24) and (0.70,0.14) .. (0.80,0.20)
    .. controls (0.90,0.26) and (0.96,0.16) .. (1,0.18)
    -- (1,0) -- (0,0) -- cycle;
  % Cracks — fine lines
  \draw[\POVColor!25,line width=0.2pt,opacity=0.4]
    (0.15,0.04) -- (0.18,0.14) -- (0.22,0.08) -- (0.26,0.16)
    (0.40,0.02) -- (0.44,0.12) -- (0.48,0.06)
    (0.60,0.04) -- (0.63,0.10) -- (0.68,0.06) -- (0.72,0.14)
    (0.82,0.03) -- (0.86,0.12);
  % Rubble debris
  \fill[\POVColor!28]
    (0.22,0.08) rectangle (0.226,0.13)
    (0.23,0.06) rectangle (0.238,0.12)
    (0.24,0.08) rectangle (0.245,0.11);
  % Bone fragment (subtle)
  \draw[\POVColor!22,line width=0.3pt,opacity=0.4]
    (0.56,0.08) -- (0.58,0.12) -- (0.59,0.09);
}

% ─────────────────────────────────────────────────────────
% LANDSCAPE RENDERER (dispatches by type)
% ─────────────────────────────────────────────────────────
\newcommand{\cw@renderLandscapeTop}{%
  \begin{tikzpicture}[x=\paperwidth,y=0.7cm,baseline]
    \ifstrequal{\cw@envtype}{city}{\cw@land@city@top}{%
    \ifstrequal{\cw@envtype}{north}{\cw@land@north@top}{%
    \ifstrequal{\cw@envtype}{dungeon}{\cw@land@dungeon@top}{%
    \ifstrequal{\cw@envtype}{wasteland}{\cw@land@wasteland@top}{%
    \cw@land@default@top}}}}%
    \ifx\cw@loctext\empty\else
      \node[anchor=south east,font=\sffamily\tiny\color{\POVColor!50},opacity=0.7]
        at (0.97,0.02) {\cw@loctext};
    \fi
  \end{tikzpicture}%
}
\newcommand{\cw@renderLandscapeBot}{%
  \begin{tikzpicture}[x=\paperwidth,y=0.5cm,baseline]
    \ifstrequal{\cw@envtype}{city}{\cw@land@city@bot}{%
    \ifstrequal{\cw@envtype}{north}{\cw@land@north@bot}{%
    \ifstrequal{\cw@envtype}{dungeon}{\cw@land@dungeon@bot}{%
    \ifstrequal{\cw@envtype}{wasteland}{\cw@land@wasteland@bot}{%
    \cw@land@default@bot}}}}%
  \end{tikzpicture}%
}

% Lettrine (drop cap) defaults
\setcounter{DefaultLines}{3}
\renewcommand{\DefaultLoversize}{0.1}
\renewcommand{\DefaultLhang}{0.15}
\renewcommand{\LettrineFontHook}{\color{\POVColor}\bfseries}

% ═══════════════════════════════════════════════════════
% POV SYSTEM
% ═══════════════════════════════════════════════════════
\newcommand{\cw@povglyph}{}
\newcommand{\cw@povname}{}
\newcommand{\POV}[2]{%
  \renewcommand{\cw@povglyph}{#1}%
  \renewcommand{\cw@povname}{#2}%
  \renewcommand{\POVColor}{ColAisen}% default
  \ifstrequal{#2}{Aisen}{\renewcommand{\POVColor}{ColAisen}}{}%
  \ifstrequal{#2}{Caspian}{\renewcommand{\POVColor}{ColCaspian}}{}%
  \ifstrequal{#2}{Corvin}{\renewcommand{\POVColor}{ColCorvin}}{}%
  \ifstrequal{#2}{Ryo}{\renewcommand{\POVColor}{ColRyo}}{}%
  \ifstrequal{#2}{Kael}{\renewcommand{\POVColor}{ColKael}}{}%
  \ifstrequal{#2}{Kairos}{\renewcommand{\POVColor}{ColKairos}}{}%
  \ifstrequal{#2}{Orin}{\renewcommand{\POVColor}{ColOrin}}{}%
  \ifstrequal{#2}{Amara}{\renewcommand{\POVColor}{ColAmara}}{}%
  \ifstrequal{#2}{Renard}{\renewcommand{\POVColor}{ColRenard}}{}%
  \ifstrequal{#2}{Emma}{\renewcommand{\POVColor}{ColEmma}}{}%
  \ifstrequal{#2}{Historian}{\renewcommand{\POVColor}{ColHistorian}}{}%
  \ifstrequal{#2}{Multiple}{\renewcommand{\POVColor}{ColMultiple}}{}%
}

% ═══════════════════════════════════════════════════════
% CHARACTER GLYPHS (TikZ runes)
% ═══════════════════════════════════════════════════════
\newcommand{\glyphAisen}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) -- (1,2) -- (2,0) -- cycle;
    \draw[line width=0.6pt,\POVColor] (1,2) -- (1,0.7);
  \end{tikzpicture}}
\newcommand{\glyphCaspian}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) circle (1);
    \draw[line width=0.6pt,\POVColor] (-1,0) -- (1,0);
  \end{tikzpicture}}
\newcommand{\glyphCorvin}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) rectangle (2,2);
    \draw[line width=0.6pt,\POVColor] (0,0) -- (2,2);
  \end{tikzpicture}}
\newcommand{\glyphRyo}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=1pt,\POVColor] (0,2) -- (1,1) -- (0.6,1) -- (2,0);
  \end{tikzpicture}}
\newcommand{\glyphKael}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (1,2) -- (2,0) -- (0,0) -- cycle;
    \fill[\POVColor] (1,0.6) circle (0.2);
  \end{tikzpicture}}
\newcommand{\glyphKairos}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) circle (1);
    \draw[line width=0.8pt,\POVColor] (1,0) -- (1.5,0.5);
  \end{tikzpicture}}
\newcommand{\glyphOrin}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) circle (1);
    \fill[\POVColor] (0,0) circle (0.3);
  \end{tikzpicture}}
\newcommand{\glyphAmara}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (0,0) -- (2,0) -- (1,2) -- cycle;
    \draw[line width=0.6pt,\POVColor] (0.6,0.6) -- (1.4,0.6);
  \end{tikzpicture}}
\newcommand{\glyphRenard}{%
  \begin{tikzpicture}[scale=0.16,baseline=-0.5ex]
    \draw[line width=0.8pt,\POVColor] (1,2) -- (1.3,1.3) -- (2,1) -- (1.3,0.7) -- (1,0) -- (0.7,0.7) -- (0,1) -- (0.7,1.3) -- cycle;
  \end{tikzpicture}}

% ═══════════════════════════════════════════════════════
% SCENE BREAK ORNAMENT (enhanced)
% ═══════════════════════════════════════════════════════
\newcommand{\scenebreak}{%
  \par\bigskip
  \begin{center}
    \begin{tikzpicture}[scale=0.7]
      \draw[Stone,line width=0.5pt] (-2.2,0) -- (-0.6,0);
      \draw[Stone,line width=0.5pt] (0.6,0) -- (2.2,0);
      \fill[Stone] (0,0) circle (1.4pt);
      \fill[Stone] (-0.35,0) circle (0.8pt);
      \fill[Stone] (0.35,0) circle (0.8pt);
    \end{tikzpicture}
  \end{center}
  \bigskip
}

% ═══════════════════════════════════════════════════════
% HEADER / FOOTER with TikZ landscape silhouettes
% ═══════════════════════════════════════════════════════
\newcommand{\cw@renderHeader}{%
  \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=north,inner sep=0pt] at (current page.north) {%
      \cw@renderLandscapeTop
    };
    \ifx\cw@povname\empty\else
      \node[anchor=north west] at ([xshift=0.8cm,yshift=-0.75cm]current page.north west) {%
        {\scriptsize\color{\POVColor}\cw@povglyph\ \textit{\cw@povname}}
      };
    \fi
  \end{tikzpicture}%
}

\newcommand{\cw@renderFooter}{%
  \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south,inner sep=0pt] at (current page.south) {%
      \cw@renderLandscapeBot
    };
  \end{tikzpicture}%
}

% ═══════════════════════════════════════════════════════
% CHAPTER PROGRESS STRIPE
% ═══════════════════════════════════════════════════════
\newcommand{\ChapterStripe}{%
  \begin{tikzpicture}[remember picture, overlay]
    \coordinate (TR) at (current page.north east);
    \coordinate (BR) at (current page.south east);
    \pgfmathsetmacro{\BarW}{0.45}
    \pgfmathsetmacro{\SlotH}{\paperheight / \TotalChapters}
    \pgfmathsetmacro{\BlockTop}{\paperheight - (\CurrentChapterNum - 1)*\SlotH}
    \pgfmathsetmacro{\BlockBot}{\paperheight - \CurrentChapterNum*\SlotH}
    \fill[\POVColor]
      ($(BR)-(\BarW cm,0)+(0,\BlockTop pt)$)
      rectangle
      ($(BR)+(0,\BlockBot pt)$);
  \end{tikzpicture}%
}
\AddToShipoutPictureBG{\ChapterStripe}

% ═══════════════════════════════════════════════════════
% PAGE STYLES
% ═══════════════════════════════════════════════════════
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[L]{\cw@renderHeader}
\fancyfoot[C]{\cw@renderFooter\vspace{0.2cm}\thepage}

\fancypagestyle{plain}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
  \fancyhead[L]{\cw@renderHeader}%
  \fancyfoot[C]{\cw@renderFooter\vspace{0.2cm}\thepage}%
}

% Clean page style for title/toc
\fancypagestyle{cleanpage}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
  \fancyfoot[C]{\thepage}%
}

% ═══════════════════════════════════════════════════════
% CHAPTER STYLING (enhanced with POV glyph & ornament)
% ═══════════════════════════════════════════════════════
\titleformat{\chapter}[display]
  {\centering\normalfont}
  {%
    \begin{tikzpicture}
      \draw[Stone,line width=0.4pt] (-2,0) -- (-0.5,0);
      \draw[Stone,line width=0.4pt] (0.5,0) -- (2,0);
      \node[inner sep=2pt] at (0,0) {%
        {\small\color{\POVColor}\cw@povglyph}%
      };
    \end{tikzpicture}%
  }
  {0.4em}
  {\Large\bfseries\color{cwink}}
\titleformat{\section}
  {\bfseries\color{cwink}}
  {}
  {0pt}
  {}

% ═══════════════════════════════════════════════════════
% ACT DIVIDER PAGE (enhanced with landscape band)
% ═══════════════════════════════════════════════════════
\newcommand{\actpage}[3]{%  #1=Act number, #2=Act title, #3=Subtitle/age range
  \clearpage
  \thispagestyle{empty}
  \null\vspace{2cm}
  \begin{center}
    \begin{tikzpicture}
      \draw[Stone,line width=0.4pt] (-2.8,0) -- (-0.5,0);
      \fill[Stone] (0,0) circle (1.2pt);
      \draw[Stone,line width=0.4pt] (0.5,0) -- (2.8,0);
    \end{tikzpicture}\\[1.2em]
    {\fontsize{14}{18}\selectfont\color{Stone}\textsc{act}}\\[0.3em]
    {\fontsize{42}{48}\selectfont\bfseries\color{cwink} #1}\\[0.8em]
    {\Large\color{InkMid}\textsc{#2}}\\[0.8em]
    {\normalsize\color{Stone}\textit{#3}}\\[1.2em]
    \begin{tikzpicture}
      \draw[Stone,line width=0.4pt] (-2.8,0) -- (-0.5,0);
      \fill[Stone] (0,0) circle (1.2pt);
      \draw[Stone,line width=0.4pt] (0.5,0) -- (2.8,0);
    \end{tikzpicture}
  \end{center}
  \vfill
  % Small landscape silhouette at bottom of act page
  \begin{center}
    \begin{tikzpicture}[x=8cm,y=1.2cm]
      \fill[Stone!25] (0,0)
        .. controls (0.10,0.35) and (0.25,0.15) .. (0.40,0.45)
        .. controls (0.55,0.70) and (0.70,0.20) .. (0.85,0.50)
        .. controls (0.92,0.60) and (0.97,0.25) .. (1,0.15)
        -- (1,0) -- (0,0) -- cycle;
      \fill[Stone!40] (0,0)
        .. controls (0.15,0.25) and (0.30,0.10) .. (0.50,0.30)
        .. controls (0.65,0.45) and (0.80,0.12) .. (1,0.20)
        -- (1,0) -- (0,0) -- cycle;
    \end{tikzpicture}
  \end{center}
  \vspace{1cm}
  \clearpage
}

% ═══════════════════════════════════════════════════════
% TYPOGRAPHY
% ═══════════════════════════════════════════════════════
\setlength{\parindent}{1.2em}
\setlength{\parskip}{0pt}
\addtolength{\textheight}{-5mm}
\AtBeginDocument{\frenchspacing}
\emergencystretch=2em
\raggedbottom

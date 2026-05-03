
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cwbook_minimal}[2026 Minimal POV Book Class]

\LoadClass[12pt,openany]{book}

\RequirePackage[paperwidth=6in,paperheight=9in,margin=0.8in]{geometry}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\usetikzlibrary{calc}
\RequirePackage{fancyhdr}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
\RequirePackage{etoolbox}
\RequirePackage{eso-pic}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% ensure header space for the environment strip + POV marker
\setlength{\headheight}{14.5pt}

\definecolor{cwink}{RGB}{40,30,24}
\definecolor{cwinksoft}{RGB}{92,74,58}

% --- Page / ink colours (shared with simplified template) ---
\definecolor{PageBg}    {HTML}{F8F3EC}
\definecolor{Ink}       {HTML}{1C1812}
\definecolor{InkMid}    {HTML}{3A3028}
\definecolor{Stone}     {HTML}{9A8A78}
\definecolor{StoneLight}{HTML}{C8B8A8}

% --- Character accent colours (tint glyph + chapter stripe) ---
\definecolor{ColAisen}  {HTML}{7A6A50}
\definecolor{ColCaspian}{HTML}{5A6A7A}
\definecolor{ColCorvin} {HTML}{4A4A4A}
\definecolor{ColRyo}    {HTML}{6A7A5A}
\definecolor{ColKael}   {HTML}{7A5A3A}
\definecolor{ColKairos} {HTML}{6A5A7A}
\definecolor{ColOrin}   {HTML}{8A7A6A}
\definecolor{ColAmara}  {HTML}{6A5A4A}
\definecolor{ColRenard} {HTML}{5A6A5A}

% --- Chapter counters / stripe colour hooks ---
\newcommand{\CurrentChapterNum}{1}
\newcommand{\TotalChapters}{52}
\newcommand{\POVColor}{ColAisen}

% ---------- ENVIRONMENT STRIPS ----------
\newcommand{\cw@envtop}{env-top.png}
\newcommand{\cw@envbottom}{env-bottom.png}
\newcommand{\ENV}[2]{%
  \renewcommand{\cw@envtop}{#1}%
  \renewcommand{\cw@envbottom}{#2}%
}

% ---------- POV SYMBOL ----------
\newcommand{\cw@povglyph}{}
\newcommand{\cw@povname}{}
\newcommand{\cw@useRegional}{0}  % Flag: use regional glyph if available
\newcommand{\POV}[2]{%
  % Check if we have a regional glyph available (CharacterRegionEmotion will be set by build script)
  \ifdefined\CharacterRegionEmotion
    \renewcommand{\cw@povglyph}{\POVGlyphRegional}%  Use regional dispatcher
    \renewcommand{\cw@useRegional}{1}%
  \else
    \renewcommand{\cw@povglyph}{#1}%  Fall back to passed-in glyph
    \renewcommand{\cw@useRegional}{0}%
  \fi%
  \renewcommand{\cw@povname}{#2}%
  % map the POV name to an accent colour immediately so overlays can use it
  \renewcommand{\POVColor}{ColAisen}% default fallback
  \ifstrequal{#2}{Aisen}{\renewcommand{\POVColor}{ColAisen}}{}%
  \ifstrequal{#2}{Caspian}{\renewcommand{\POVColor}{ColCaspian}}{}%
  \ifstrequal{#2}{Corvin}{\renewcommand{\POVColor}{ColCorvin}}{}%
  \ifstrequal{#2}{Ryo}{\renewcommand{\POVColor}{ColRyo}}{}%
  \ifstrequal{#2}{Kael}{\renewcommand{\POVColor}{ColKael}}{}%
  \ifstrequal{#2}{Kairos}{\renewcommand{\POVColor}{ColKairos}}{}%
  \ifstrequal{#2}{Orin}{\renewcommand{\POVColor}{ColOrin}}{}%
  \ifstrequal{#2}{Amara}{\renewcommand{\POVColor}{ColAmara}}{}%
  \ifstrequal{#2}{Renard}{\renewcommand{\POVColor}{ColRenard}}{}%
}

% ---------- RUNE GLYPHS (refined) ----------
\newcommand{\glyphAisen}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) -- (1,2) -- (2,0) -- cycle;\draw[line width=0.6pt] (1,2) -- (1,0.7);\end{tikzpicture}}
\newcommand{\glyphCaspian}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\draw[line width=0.6pt] (-1,0) -- (1,0);\end{tikzpicture}}

% Fallback for POVGlyphRegional (defined in character-glyphs-complete.tex if loaded)
\ifx\POVGlyphRegional\undefined
  \newcommand{\POVGlyphRegional}{\glyphAisen}  % Default if regional system not loaded
\fi
\newcommand{\glyphCorvin}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) rectangle (2,2);\draw[line width=0.6pt] (0,0) -- (2,2);\end{tikzpicture}}
\newcommand{\glyphRyo}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=1pt] (0,2) -- (1,1) -- (0.6,1) -- (2,0);\end{tikzpicture}}
\newcommand{\glyphKael}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (1,2) -- (2,0) -- (0,0) -- cycle;\fill (1,0.6) circle (0.2);\end{tikzpicture}}
\newcommand{\glyphKairos}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\draw[line width=0.8pt] (1,0) -- (1.5,0.5);\end{tikzpicture}}
\newcommand{\glyphOrin}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\fill (0,0) circle (0.3);\end{tikzpicture}}
\newcommand{\glyphAmara}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) -- (2,0) -- (1,2) -- cycle;\draw[line width=0.6pt] (0.6,0.6) -- (1.4,0.6);\end{tikzpicture}}
\newcommand{\glyphRenard}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (1,2) -- (1.3,1.3) -- (2,1) -- (1.3,0.7) -- (1,0) -- (0.7,0.7) -- (0,1) -- (0.7,1.3) -- cycle;\end{tikzpicture}}

% ---------- HEADER / FOOTER ----------
% Render header graphic and POV marker (reusable)
\newcommand{\cw@renderHeader}{%
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=north west] at (current page.north west) {%
    \includegraphics[width=\paperwidth,height=0.5cm]{\cw@envtop}
  };
  \node[anchor=north west] at ([yshift=-0.6cm]current page.north west) {%
    {\scriptsize\color{cwinksoft}\cw@povglyph\ \textit{\cw@povname}}
  };
\end{tikzpicture}%
}

\newcommand{\cw@renderFooter}{%
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=south west] at (current page.south west) {%
    \includegraphics[width=\paperwidth,height=0.5cm]{\cw@envbottom}
  };
\end{tikzpicture}%
}

% ══════════════════════════════════════════════════════════════════
% Chapter stripe: single coloured bar at right edge, vertical position
% maps to chapter number / total chapters. Uses \POVColor for the fill.
% ══════════════════════════════════════════════════════════════════
\newcommand{\ChapterStripe}{%
  \begin{tikzpicture}[remember picture, overlay]
    \coordinate (TR) at (current page.north east);
    \coordinate (BR) at (current page.south east);
    % Bar width in cm
    \pgfmathsetmacro{\BarW}{0.50}
    % Slot height = full page / total chapters
    \pgfmathsetmacro{\SlotH}{\paperheight / \TotalChapters}
    % Block top and bottom in pt
    \pgfmathsetmacro{\BlockTop}{\paperheight - (\CurrentChapterNum - 1)*\SlotH}
    \pgfmathsetmacro{\BlockBot}{\paperheight - \CurrentChapterNum*\SlotH}
    \fill[\POVColor]
      ($(BR)-(\BarW cm,0)+(0,\BlockTop pt)$)
      rectangle
      ($(BR)+(0,\BlockBot pt)$);
  \end{tikzpicture}%
}

% Add the stripe to every page background (eso-pic)
\AddToShipoutPictureBG{\ChapterStripe}

% Use the same header/footer for both 'fancy' and 'plain' pagestyles
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[L]{\cw@renderHeader}
\fancyfoot[C]{\cw@renderFooter\vspace{0.2cm}\thepage}

% ensure chapter openings (plain style) use same header/footer
\fancypagestyle{plain}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
  \fancyhead[L]{\cw@renderHeader}%
  \fancyfoot[C]{\cw@renderFooter\vspace{0.2cm}\thepage}%
}

% ---------- CHAPTER STYLE ----------
\titleformat{\chapter}
  {\centering\Large\bfseries\color{cwink}}
  {}
  {0pt}
  {}
\titleformat{\section}
  {\bfseries\color{cwink}}
  {}
  {0pt}
  {}

\setlength{\parindent}{1.2em}
\setlength{\parskip}{0pt}
% slightly raise body text away from the bottom strip (experiment)
\addtolength{\textheight}{-5mm}
\AtBeginDocument{\frenchspacing}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cwbook}[2026 Custom POV Book Class]

\LoadClass[12pt,openany]{book}

% ---------- PACKAGES ----------
\RequirePackage[paperwidth=6in,paperheight=9in,margin=2.2cm]{geometry}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{fancyhdr}
\RequirePackage{xcolor}
\RequirePackage{eso-pic}
\RequirePackage{titlesec}
\RequirePackage{lmodern}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% ---------- GLYPH SYSTEM (CUSTOM SYMBOLS) ----------
\newcommand{\glyphAisen}{\ensuremath{\blacktriangle}}
\newcommand{\glyphCaspian}{\ensuremath{\lozenge}}
\newcommand{\glyphCorvin}{\ensuremath{\square}}
\newcommand{\glyphRyo}{\ensuremath{\diamond}}
\newcommand{\glyphKael}{\ensuremath{\bigstar}}
\newcommand{\glyphKairos}{\ensuremath{\circlearrowleft}}
\newcommand{\glyphOrin}{\ensuremath{\bullet}}
\newcommand{\glyphAmara}{\ensuremath{\triangle}}
\newcommand{\glyphRenard}{\ensuremath{\star}}

% ---------- POV SYSTEM ----------
\newcommand{\currentpov}{}
\newcommand{\currentname}{}

\newcommand{\POV}[2]{
    \clearpage
    \renewcommand{\currentpov}{#1}
    \renewcommand{\currentname}{#2}
}

% ---------- ENVIRONMENT ----------
\newcommand{\envtop}{env-top.png}
\newcommand{\envbottom}{env-bottom.png}

\newcommand{\ENV}[2]{
    \renewcommand{\envtop}{#1}
    \renewcommand{\envbottom}{#2}
}

% ---------- HEADER (SUBTLE POV MARKER) ----------
\fancyhead[L]{
    \begin{tikzpicture}[remember picture,overlay]
        % Environment strip
        \node at (current page.north) [anchor=north] {
            \includegraphics[width=\paperwidth,height=0.8cm]{\envtop}
        };

        % Subtle POV marker
        \node at (current page.north west)
        [anchor=north west, xshift=0.5cm, yshift=-0.9cm] {
            \textcolor{black!50}{\scriptsize \currentpov\ \textit{\currentname}}
        };
    \end{tikzpicture}
}

% ---------- FOOTER ----------
\fancyfoot[C]{
    \begin{tikzpicture}[remember picture,overlay]
        \node at (current page.south) [anchor=south] {
            \includegraphics[width=\paperwidth,height=0.8cm]{\envbottom}
        };
    \end{tikzpicture}
    \vspace{0.3cm}
    \thepage
}

% ---------- SIDE STRIPE ----------
\AddToShipoutPictureBG{
    \begin{tikzpicture}[remember picture,overlay]
        \fill[black!20]
        (current page.north east) rectangle
        ([xshift=-0.6cm]current page.south east);
    \end{tikzpicture}
}

% ---------- CHAPTER STYLE ----------
\titleformat{\chapter}
  {\centering\Huge\bfseries}
  {}
  {0pt}
  {}

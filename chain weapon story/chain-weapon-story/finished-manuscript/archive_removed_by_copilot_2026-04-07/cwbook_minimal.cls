\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cwbook_minimal}[2026 Minimal POV Book Class]

\LoadClass[12pt,openany]{book}

\RequirePackage[paperwidth=6in,paperheight=9in,margin=0.8in]{geometry}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{fancyhdr}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
\RequirePackage{etoolbox}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\definecolor{cwink}{RGB}{40,30,24}
\definecolor{cwinksoft}{RGB}{92,74,58}

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
\newcommand{\POV}[2]{%
  \renewcommand{\cw@povglyph}{#1}%
  \renewcommand{\cw@povname}{#2}%
}

% ---------- RUNE GLYPHS ----------
\newcommand{\glyphAisen}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) -- (1,2) -- (2,0) -- cycle;\draw[line width=0.6pt] (1,2) -- (1,0.8);\end{tikzpicture}}
\newcommand{\glyphCaspian}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\draw[line width=0.6pt] (-1,0) -- (1,0);\end{tikzpicture}}
\newcommand{\glyphCorvin}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) rectangle (2,2);\draw[line width=0.6pt] (0.2,0.2) -- (1.8,1.8);\end{tikzpicture}}
\newcommand{\glyphRyo}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.9pt] (0,2) -- (1,1) -- (0.55,1) -- (2,0);\end{tikzpicture}}
\newcommand{\glyphKael}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (1,2) -- (2,0) -- (0,0) -- cycle;\fill (1,0.65) circle (0.16);\end{tikzpicture}}
\newcommand{\glyphKairos}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\draw[line width=0.8pt] (1,0) -- (1.45,0.45);\end{tikzpicture}}
\newcommand{\glyphOrin}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) circle (1);\fill (0,0) circle (0.26);\end{tikzpicture}}
\newcommand{\glyphAmara}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (0,0) -- (2,0) -- (1,2) -- cycle;\draw[line width=0.6pt] (0.55,0.65) -- (1.45,0.65);\end{tikzpicture}}
\newcommand{\glyphRenard}{\begin{tikzpicture}[scale=0.16,baseline=-0.5ex]\draw[line width=0.8pt] (1,2) -- (1.28,1.28) -- (2,1) -- (1.28,0.72) -- (1,0) -- (0.72,0.72) -- (0,1) -- (0.72,1.28) -- cycle;\end{tikzpicture}}

% ---------- HEADER / FOOTER ----------
\fancyhead[L]{%
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=north west] at (current page.north west) {%
    \includegraphics[width=\paperwidth,height=0.45cm]{\cw@envtop}
  };
  \node[anchor=north west] at ([yshift=-0.53cm]current page.north west) {%
    {\scriptsize\color{cwinksoft}\cw@povglyph\ \textit{\cw@povname}}
  };
\end{tikzpicture}%
}

\fancyfoot[C]{%
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=south west] at (current page.south west) {%
    \includegraphics[width=\paperwidth,height=0.45cm]{\cw@envbottom}
  };
\end{tikzpicture}%
\vspace{0.18cm}\thepage
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
\AtBeginDocument{\frenchspacing}

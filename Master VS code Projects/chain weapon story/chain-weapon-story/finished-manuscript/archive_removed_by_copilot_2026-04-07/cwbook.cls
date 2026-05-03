\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cwbook}[2026/04/07 Custom POV-driven fantasy book class]

\LoadClass[12pt,openany]{book}

% Core packages
\RequirePackage{geometry}
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\RequirePackage{eso-pic}
\RequirePackage{titlesec}
\RequirePackage{microtype}
\RequirePackage{fancyhdr}
\RequirePackage{etoolbox}
\RequirePackage{setspace}

% Page size: 6x9 trade paperback
\geometry{
  paperwidth=6in,
  paperheight=9in,
  inner=0.82in,
  outer=0.67in,
  \NeedsTeXFormat{LaTeX2e}
  \ProvidesClass{cwbook}[2026/04/07 Custom POV-driven fantasy book class]

  \LoadClass[12pt,openany]{book}

  % Core packages
  \RequirePackage{geometry}
  \RequirePackage{fontspec}
  \RequirePackage{xcolor}
  \RequirePackage{tikz}
  \RequirePackage{eso-pic}
  \RequirePackage{titlesec}
  \RequirePackage{microtype}
  \RequirePackage{fancyhdr}
  \RequirePackage{etoolbox}
  \RequirePackage{setspace}

  % Page size: 6x9 trade paperback
  \geometry{
    paperwidth=6in,
    paperheight=9in,
    inner=0.82in,
    outer=0.67in,
    top=0.82in,
    bottom=0.78in,
    headheight=18pt,
    headsep=10pt,
    footskip=18pt,
    includeheadfoot
  }

  % Fonts
  \setmainfont{TeXGyrePagella}
  \setsansfont{TeXGyreHeros}
  \setmonofont{TeXGyreCursor}
  \defaultfontfeatures{Ligatures=TeX}

  % Color palette
  \definecolor{CWInk}{HTML}{171717}
  \definecolor{CWGray}{HTML}{7C7C7C}
  \definecolor{CWLine}{HTML}{3A3A3A}
  \definecolor{CWGold}{HTML}{B08D57}
  \definecolor{CWAsh}{HTML}{E6E0D8}
  \definecolor{CWFog}{HTML}{D7D2C9}
  \definecolor{CWAccent}{HTML}{8B6B3D}

  \setlength{\parindent}{1.1em}
  \setlength{\parskip}{0pt}
  \onehalfspacing
  \setlength{\emergencystretch}{1.5em}
  \setcounter{secnumdepth}{0}
  \setcounter{tocdepth}{1}

  % Running state
  \newcommand{\cw@povsymbol}{}
  \newcommand{\cw@povname}{}
  \newcommand{\cw@env}{dungeon}
  \newcommand{\cw@chapterlabel}{CHAPTER}
  \newcommand{\cw@chaptertitle}{}


  % Character glyphs (custom vector sigils)
  \newcommand{\GlyphAisen}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (0,-0.28) -- (0,0.20);
      \draw[line width=1.1pt, color=CWFog] (-0.10,0.05) -- (0.10,0.05);
      \draw[line width=1.1pt, color=CWFog] (-0.06,0.20) -- (0,0.28) -- (0.06,0.20);
    }%
  }
  \newcommand{\GlyphCaspian}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (0.03,0) arc[start angle=310, end angle=50, radius=0.22];
      \fill[color=CWFog] (0.10,0.00) circle (0.03);
    }%
  }
  \newcommand{\GlyphCorvin}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog, rounded corners=0.03cm] (0,0.26) -- (-0.17,0.14) -- (-0.12,-0.18) -- (0,-0.28) -- (0.12,-0.18) -- (0.17,0.14) -- cycle;
      \draw[line width=0.9pt, color=CWFog] (0,-0.18) -- (0,0.14);
    }%
  }
  \newcommand{\GlyphRyo}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (-0.03,0.28) -- (0.12,0.02) -- (0.02,0.02) -- (0.13,-0.24) -- (-0.05,-0.02) -- (0.03,-0.02) -- cycle;
    }%
  }
  \newcommand{\GlyphKael}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (-0.14,0.14) .. controls (-0.10,0.28) and (-0.04,0.28) .. (-0.02,0.13) .. controls (0.00,0.28) and (0.06,0.28) .. (0.10,0.14);
      \draw[line width=1.1pt, color=CWFog] (-0.06,0.12) -- (0.00,-0.24) -- (0.06,0.12);
    }%
  }
  \newcommand{\GlyphKairos}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (-0.18,0) .. controls (-0.10,0.18) and (-0.02,0.18) .. (0,0) .. controls (0.02,-0.18) and (0.10,-0.18) .. (0.18,0);
      \draw[line width=1.1pt, color=CWFog] (-0.18,0) .. controls (-0.10,-0.18) and (-0.02,-0.18) .. (0,0) .. controls (0.02,0.18) and (0.10,0.18) .. (0.18,0);
    }%
  }
  \newcommand{\GlyphOrin}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (0,0) circle (0.18);
      \draw[line width=1.0pt, color=CWFog] (-0.02,0.18) -- (0.08,0.24);
      \draw[line width=1.0pt, color=CWFog] (0.00,0.02) -- (0.08,-0.08);
    }%
  }
  \newcommand{\GlyphAmara}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (-0.12,0.20) -- (0.12,0.20) -- (0.12,0.02) -- (0.00,-0.18) -- (-0.12,0.02) -- cycle;
      \draw[line width=0.9pt, color=CWFog] (0,0.02) -- (0,0.24);
      \draw[line width=0.9pt, color=CWFog] (0.00,0.10) -- (0.05,0.05);
    }%
  }
  \newcommand{\GlyphRenard}{%
    	ikz[baseline=-0.6ex,scale=0.95]{%
      \draw[line width=1.1pt, color=CWFog] (-0.14,0.10) -- (-0.05,0.22) -- (0,0.12) -- (0.05,0.22) -- (0.14,0.10) -- (0.05,-0.16) -- (-0.05,-0.16) -- cycle;
      \draw[line width=0.9pt, color=CWFog] (-0.04,0.02) -- (0.04,0.02);
    }%
  }

  % Environment names
  \newcommand{\cw@envdungeon}{dungeon}
  \newcommand{\cw@envcity}{city}
  \newcommand{\cw@envwasteland}{wasteland}
  \newcommand{\cw@envnorthern}{northernwastes}

  % User-facing commands
  \newcommand{\ENV}[1]{\gdef\cw@env{#1}}
  \newcommand{\POV}[2]{%
    \clearpage
    \gdef\cw@povsymbol{#1}%
    \gdef\cw@povname{#2}%
    \vspace*{1.1cm}%
    \begin{center}
      {\fontsize{28}{30}\selectfont\color{CWInk}#1}\\[0.25em]
      {\large\itshape\color{CWGray}#2}
    \end{center}
    \vspace{0.5em}
  }

  \newcommand{\ShiftCue}[1][The thread passes onward.]{%
    \begin{center}
      {\small\itshape\color{CWGray}#1}
    \end{center}
  }

  % Chapter styling
  	itleformat{\chapter}[display]
    {\centering\bfseries\color{CWInk}}
    {\Large\cw@chapterlabel\space\thechapter}
    {0.6em}
    {\Huge}
    []

  	itlespacing*{\chapter}{0pt}{-10pt}{22pt}

  % Headers/footers (minimal; decorations are drawn separately)
  \pagestyle{fancy}
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
  \fancyfoot[C]{\color{CWGray}\thepage}


  % Scenic strip helpers
  \newcommand{\cw@stripheight}{0.52in}
  \newcommand{\cw@stripheightbottom}{0.46in}

  \newcommand{\cw@dungeonstriptop}{%
    \begin{tikzpicture}[remember picture,overlay]
      \fill[CWInk] (current page.north west) rectangle ([yshift=-\cw@stripheight]current page.north east);
      \fill[CWGray!55!CWInk] ([xshift=0.08in,yshift=-0.18in]current page.north west) -- ([xshift=0.30in,yshift=-0.02in]current page.north west) -- ([xshift=0.50in,yshift=-0.22in]current page.north west) -- ([xshift=0.72in,yshift=-0.05in]current page.north west) -- ([xshift=1.0in,yshift=-0.20in]current page.north west) -- ([xshift=1.18in,yshift=-0.04in]current page.north west) -- ([xshift=1.48in,yshift=-0.24in]current page.north west) -- ([xshift=1.70in,yshift=-0.08in]current page.north west) -- ([xshift=2.00in,yshift=-0.26in]current page.north west) -- ([xshift=2.25in,yshift=-0.06in]current page.north west) -- ([xshift=2.55in,yshift=-0.18in]current page.north west) -- ([xshift=2.80in,yshift=-0.03in]current page.north west) -- ([xshift=3.10in,yshift=-0.23in]current page.north west) -- ([xshift=3.40in,yshift=-0.07in]current page.north west) -- ([xshift=3.70in,yhift=-0.20in]current page.north west) -- ([xshift=4.05in,yshift=-0.05in]current page.north west) -- ([xshift=4.30in,yshift=-0.24in]current page.north west) -- ([xshift=4.60in,yshift=-0.10in]current page.north west) -- ([xshift=4.95in,yshift=-0.21in]current page.north west) -- ([xshift=5.20in,yshift=-0.04in]current page.north west) -- ([xshift=5.55in,yshift=-0.19in]current page.north west) -- ([xshift=5.85in,yshift=-0.07in]current page.north west) -- cycle;
    \end{tikzpicture}%
  }

  \newcommand{\cw@dungeonstripbottom}{%
    \begin{tikzpicture}[remember picture,overlay]
      \fill[CWInk] (current page.south west) rectangle ([yshift=\cw@stripheightbottom]current page.south east);
      \fill[CWGray!45!CWInk] ([xshift=0.10in,yshift=0.14in]current page.south west) -- ([xshift=0.35in,yshift=0.02in]current page.south west) -- ([xshift=0.58in,yshift=0.16in]current page.south west) -- ([xshift=0.78in,yshift=0.03in]current page.south west) -- ([xshift=1.06in,yshift=0.18in]current page.south west) -- ([xshift=1.32in,yshift=0.05in]current page.south west) -- ([xshift=1.62in,yshift=0.17in]current page.south west) -- ([xshift=1.88in,yshift=0.04in]current page.south west) -- ([xshift=2.15in,yshift=0.19in]current page.south west) -- ([xshift=2.42in,yshift=0.06in]current page.south west) -- ([xshift=2.75in,yshift=0.15in]current page.south west) -- ([xshift=3.05in,yshift=0.03in]current page.south west) -- ([xshift=3.40in,yshift=0.18in]current page.south west) -- ([xshift=3.72in,yshift=0.05in]current page.south west) -- ([xshift=4.02in,yshift=0.16in]current page.south west) -- ([xshift=4.30in,yshift=0.04in]current page.south west) -- ([xshift=4.60in,yshift=0.17in]current page.south west) -- ([xshift=4.95in,yshift=0.06in]current page.south west) -- ([xshift=5.30in,yshift=0.19in]current page.south west) -- ([xshift=5.60in,yshift=0.05in]current page.south west) -- ([xshift=5.90in,yshift=0.15in]current page.south west) -- cycle;
    \end{tikzpicture}%
  }

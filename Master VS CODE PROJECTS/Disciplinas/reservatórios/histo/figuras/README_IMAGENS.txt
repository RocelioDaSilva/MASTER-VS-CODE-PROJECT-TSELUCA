INSTRUÇÕES PARA DOWNLOAD DE IMAGENS
====================================

O documento LaTeX já está preparado para incluir 3 imagens adicionais.
Debido a restrições de rede, faça o download manual seguindo estas instruções:

🖼️ IMAGENS NECESSÁRIAS:
========================

1. ENIAC (1946)
   URL: https://upload.wikimedia.org/wikipedia/commons/0/07/Classic_shot_of_the_ENIAC_%28full_resolution%29.jpg
   Nome local: eniac_1946.jpg
   Tamanho: ~1-2 MB
   License: Public Domain (U.S. Army)

2. CDC 7600 (1969)
   URL: https://upload.wikimedia.org/wikipedia/commons/6/6c/CDC_7600.jc.jpg
   Nome local: cdc_7600_1969.jpg
   Tamanho: ~3-4 MB
   License: CC-BY 2.0 (Jitze Couperus)

3. Balakhani Oil Wells (1904)
   URL: https://upload.wikimedia.org/wikipedia/commons/6/65/Balakhani_oil_wells.png
   Nome local: balakhani_1904.png
   Tamanho: ~2-3 MB
   License: Public Domain (pré-1931)

📥 COMO FAZER O DOWNLOAD:
==========================

Opção A: Navegador Web
1. Clique na URL acima
2. Clique com botão direito na imagem → "Guardar imagem como..."
3. Salve na pasta: c:\Users\PCGAME\Desktop\reservatórios\histo\figuras\
4. Renomeie conforme "Nome local" acima

Opção B: Direto (wget/curl se disponível)
cd c:\Users\PCGAME\Desktop\reservatórios\histo\figuras
wget https://upload.wikimedia.org/wikipedia/commons/0/07/Classic_shot_of_the_ENIAC_%28full_resolution%29.jpg -O eniac_1946.jpg
[etc...]

✅ APÓS FAZER DOWNLOAD:
=======================

1. Coloque os 3 ficheiros nesta pasta (figuras/)
2. Recompile o PDF:
   cd c:\Users\PCGAME\Desktop\reservatórios\histo
   pdflatex -interaction=nonstopmode tcc_historia_eng_reservatorios.tex
3. Abra tcc_historia_eng_reservatorios.pdf

🎓 RESULTADO:
==============

Após integração, o documento terá:
- ✓ 4 imagens com text-wrapping (Afloramento, Darcy, Darcy Apparatus, Muskat)
- ✓ 3 novas imagens adicionadas (ENIAC, CDC 7600, Balakhani Oil Wells)
- ✓ Total: 7 imagens contextualizadas historicamente
- ✓ texto fluindo organicamente ao redor das imagens
- ✓ PDF profissional e pronto para publicação

❓ DÚVIDAS?
===========

Se o download não funcionar via navegador:
1. Tente aceder diretamente via VPN/proxy
2. Ou use ferramentas online como: https://commons.wikimedia.org/wiki/Tools  
3. Ou contacte o gestor de rede para desbloquear acesso a Wikimedia

Sucesso! 🚀

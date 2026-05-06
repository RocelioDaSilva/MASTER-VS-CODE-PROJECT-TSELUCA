Instruções de exportação de slides — Projeto: História da Engenharia de Reservatórios

Arquivos incluídos neste zip:
- Historia_Eng_Reservatorios_ISPTEC.pptx
- export_slides_to_png.py  (script opcional para export via PowerPoint COM)
- slide_images/ (imagens geradas via LibreOffice)

Como gerar PNGs localmente (opções):

1) Usando PowerPoint (Windows + PowerPoint instalado):
   - Ative o venv e instale pywin32:
     . ".venv\Scripts\Activate.ps1"
     pip install pywin32
   - Execute:
     python export_slides_to_png.py
   - As imagens serão escritas em `slide_images\slide_01.png`, `slide_02.png`, ...

2) Usando LibreOffice (Windows / Linux):
   - No terminal, execute:
     soffice --headless --convert-to png --outdir slide_images "Historia_Eng_Reservatorios_ISPTEC.pptx"
   - Isso gera imagens em `slide_images/` (nome base depende da versão do LibreOffice).

Observações:
- O script `export_slides_to_png.py` usa automação COM do PowerPoint; só funciona no Windows com PowerPoint instalado.
- Se preferir, posso criar um ZIP contendo apenas o PPTX e as instruções para você baixar.

Gerado automaticamente pelo gerador de apresentação.
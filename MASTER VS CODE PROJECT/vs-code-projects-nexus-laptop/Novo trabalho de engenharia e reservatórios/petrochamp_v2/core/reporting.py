"""
📄 Advanced Reporting - PetroChamp v2.0

Módulo de geração de relatórios em múltiplos formatos.
Suporta PDF, Excel, HTML, JSON e Markdown.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

import pandas as pd
import numpy as np
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


@dataclass
class ReportMetadata:
    """Metadados do relatório."""
    title: str = "Relatório PetroChamp"
    author: str = "PetroChamp v2.0"
    date: str = ""
    version: str = "1.0"
    description: str = ""
    confidential: bool = False
    
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AdvancedReportGenerator:
    """Gerador de relatórios avançados."""
    
    def __init__(self, metadata: Optional[ReportMetadata] = None):
        """
        Inicializa gerador de relatórios.
        
        Args:
            metadata: Metadados do relatório
        """
        self.metadata = metadata or ReportMetadata()
        self.sections: List[Dict[str, Any]] = []
        
        logger.info("Gerador de relatórios inicializado")
    
    def add_section(self, title: str, content: Any, section_type: str = "text") -> None:
        """
        Adiciona seção ao relatório.
        
        Args:
            title: Título da seção
            content: Conteúdo (texto, DataFrame, Figure, etc)
            section_type: Tipo de seção (text, table, figure, code)
        """
        self.sections.append({
            'title': title,
            'content': content,
            'type': section_type,
        })
        logger.info(f"Seção adicionada: {title}")
    
    def add_text(self, title: str, text: str) -> None:
        """Adiciona seção de texto."""
        self.add_section(title, text, "text")
    
    def add_table(self, title: str, dataframe: pd.DataFrame) -> None:
        """Adiciona seção com tabela."""
        self.add_section(title, dataframe, "table")
    
    def add_figure(self, title: str, figure: Figure) -> None:
        """Adiciona seção com gráfico."""
        self.add_section(title, figure, "figure")
    
    def add_code(self, title: str, code: str, language: str = "python") -> None:
        """Adiciona seção com código."""
        self.add_section(title, {'code': code, 'language': language}, "code")
    
    def add_metrics(self, title: str, metrics: Dict[str, Any]) -> None:
        """Adiciona seção com métricas."""
        self.add_section(title, metrics, "metrics")
    
    def to_html(self, include_toc: bool = True) -> str:
        """
        Converte relatório para HTML.
        
        Args:
            include_toc: Incluir table of contents
        
        Returns:
            String HTML
        """
        html = []
        
        # Header
        html.append("""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #f39c12; padding-left: 10px; }}
                h3 {{ color: #7f8c8d; }}
                table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                table, th, td {{ border: 1px solid #bdc3c7; padding: 10px; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #ecf0f1; }}
                pre {{ background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; }}
                .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }}
                .metric-card {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; }}
                .metric-card .value {{ font-size: 24px; font-weight: bold; color: #3498db; }}
                .metric-card .label {{ color: #7f8c8d; font-size: 12px; }}
                .footer {{ margin-top: 40px; text-align: center; color: #95a5a6; font-size: 12px; }}
                .metadata {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
        """.format(title=self.metadata.title))
        
        # Metadata
        html.append(f"""
        <div class="metadata">
            <h3>{self.metadata.title}</h3>
            <p><strong>Autor:</strong> {self.metadata.author}</p>
            <p><strong>Data:</strong> {self.metadata.date}</p>
            <p><strong>Versão:</strong> {self.metadata.version}</p>
            <p><strong>Descrição:</strong> {self.metadata.description}</p>
            {f'<p style="color: red; font-weight: bold;">⚠️ CONFIDENCIAL</p>' if self.metadata.confidential else ''}
        </div>
        """)
        
        # Table of Contents
        if include_toc and self.sections:
            html.append("<h2>Índice</h2>")
            html.append("<ul>")
            for i, section in enumerate(self.sections):
                html.append(f'<li><a href="#section-{i}">{section["title"]}</a></li>')
            html.append("</ul>")
        
        # Sections
        for i, section in enumerate(self.sections):
            html.append(f'<h2 id="section-{i}">{section["title"]}</h2>')
            
            if section['type'] == 'text':
                html.append(f'<p>{section["content"]}</p>')
            
            elif section['type'] == 'table':
                df = section['content']
                html.append(df.to_html(index=False))
            
            elif section['type'] == 'figure':
                # Salvar figura como base64
                fig = section['content']
                import io
                import base64
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode()
                html.append(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto;" />')
                buf.close()
            
            elif section['type'] == 'code':
                code_data = section['content']
                html.append(f'<pre><code class="{code_data.get("language", "python")}">{code_data["code"]}</code></pre>')
            
            elif section['type'] == 'metrics':
                metrics = section['content']
                html.append('<div class="metrics">')
                for key, value in metrics.items():
                    html.append(f"""
                    <div class="metric-card">
                        <div class="value">{value}</div>
                        <div class="label">{key}</div>
                    </div>
                    """)
                html.append('</div>')
        
        # Footer
        html.append(f"""
        <div class="footer">
            <p>Relatório gerado automaticamente por PetroChamp v2.0</p>
            <p>Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        </body>
        </html>
        """)
        
        return "\n".join(html)
    
    def to_json(self) -> str:
        """
        Converte relatório para JSON.
        
        Returns:
            String JSON
        """
        data = {
            'metadata': {
                'title': self.metadata.title,
                'author': self.metadata.author,
                'date': self.metadata.date,
                'version': self.metadata.version,
                'description': self.metadata.description,
            },
            'sections': []
        }
        
        for section in self.sections:
            section_data = {
                'title': section['title'],
                'type': section['type'],
            }
            
            if section['type'] == 'text':
                section_data['content'] = section['content']
            elif section['type'] == 'table':
                section_data['content'] = section['content'].to_dict(orient='records')
            elif section['type'] == 'metrics':
                section_data['content'] = section['content']
            elif section['type'] == 'figure':
                section_data['content'] = "[Binary data]"
            elif section['type'] == 'code':
                section_data['content'] = section['content']['code']
            
            data['sections'].append(section_data)
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def to_markdown(self) -> str:
        """
        Converte relatório para Markdown.
        
        Returns:
            String Markdown
        """
        md = []
        
        # Header
        md.append(f"# {self.metadata.title}\n")
        md.append(f"**Autor:** {self.metadata.author}\n")
        md.append(f"**Data:** {self.metadata.date}\n")
        md.append(f"**Versão:** {self.metadata.version}\n")
        md.append(f"**Descrição:** {self.metadata.description}\n")
        
        if self.metadata.confidential:
            md.append("⚠️ **CONFIDENCIAL**\n")
        
        # Table of Contents
        if self.sections:
            md.append("## Índice\n")
            for i, section in enumerate(self.sections):
                md.append(f"- [{section['title']}](#{i})\n")
        
        # Sections
        for i, section in enumerate(self.sections):
            md.append(f"\n## {section['title']} {{#{i}}}\n")
            
            if section['type'] == 'text':
                md.append(f"{section['content']}\n")
            
            elif section['type'] == 'table':
                df = section['content']
                md.append(df.to_markdown(index=False))
                md.append("\n")
            
            elif section['type'] == 'figure':
                md.append("[Gráfico incluído no relatório HTML]\n")
            
            elif section['type'] == 'code':
                code_data = section['content']
                md.append(f"```{code_data.get('language', 'python')}\n")
                md.append(f"{code_data['code']}\n")
                md.append("```\n")
            
            elif section['type'] == 'metrics':
                metrics = section['content']
                md.append("| Métrica | Valor |\n")
                md.append("|---------|-------|\n")
                for key, value in metrics.items():
                    md.append(f"| {key} | {value} |\n")
        
        # Footer
        md.append(f"\n---\n")
        md.append(f"*Relatório gerado automaticamente por PetroChamp v2.0*\n")
        md.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return "\n".join(md)
    
    def to_excel(self, filepath: str) -> None:
        """
        Exporta relatório para Excel.
        
        Args:
            filepath: Caminho do arquivo Excel
        """
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Metadata sheet
            metadata_df = pd.DataFrame({
                'Propriedade': ['Título', 'Autor', 'Data', 'Versão'],
                'Valor': [
                    self.metadata.title,
                    self.metadata.author,
                    self.metadata.date,
                    self.metadata.version
                ]
            })
            metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            # Sections sheets
            for i, section in enumerate(self.sections):
                sheet_name = f"Seção {i+1}"[:31]  # Excel limita a 31 caracteres
                
                if section['type'] == 'table':
                    section['content'].to_excel(writer, sheet_name=sheet_name, index=False)
                elif section['type'] == 'metrics':
                    df = pd.DataFrame(list(section['content'].items()), columns=['Métrica', 'Valor'])
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    # Para outros tipos, criar tabela com informações
                    df = pd.DataFrame({
                        'Campo': ['Título', 'Tipo', 'Conteúdo'],
                        'Valor': [
                            section['title'],
                            section['type'],
                            str(section['content'])[:100]
                        ]
                    })
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        logger.info(f"Relatório exportado para: {filepath}")
    
    def to_pdf(self, filepath: str) -> None:
        """
        Exporta relatório para PDF (requer reportlab ou similar).
        
        Args:
            filepath: Caminho do arquivo PDF
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
            from reportlab.lib import colors
            
            # Criar PDF
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=1*inch
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph(self.metadata.title, title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Metadata
            metadata_style = ParagraphStyle(
                'Metadata',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#7f8c8d'),
            )
            story.append(Paragraph(f"<b>Autor:</b> {self.metadata.author}", metadata_style))
            story.append(Paragraph(f"<b>Data:</b> {self.metadata.date}", metadata_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Sections
            for section in self.sections[:5]:  # Limitar a 5 seções no PDF
                story.append(Paragraph(section['title'], styles['Heading2']))
                
                if section['type'] == 'text':
                    story.append(Paragraph(section['content'], styles['Normal']))
                elif section['type'] == 'table':
                    df = section['content']
                    data = [df.columns.tolist()] + df.values.tolist()[:10]
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ]))
                    story.append(table)
                elif section['type'] == 'metrics':
                    metrics = section['content']
                    for key, value in list(metrics.items())[:10]:
                        story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
                
                story.append(Spacer(1, 0.2*inch))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF gerado: {filepath}")
        
        except ImportError:
            logger.error("Módulo reportlab não instalado. Use: pip install reportlab")
            raise
    
    def save(self, filepath: str, format: str = "html") -> None:
        """
        Salva relatório em arquivo.
        
        Args:
            filepath: Caminho do arquivo
            format: Formato (html, json, markdown, excel, pdf)
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == "html":
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.to_html())
        
        elif format.lower() == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.to_json())
        
        elif format.lower() in ["markdown", "md"]:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.to_markdown())
        
        elif format.lower() == "excel":
            self.to_excel(filepath)
        
        elif format.lower() == "pdf":
            self.to_pdf(filepath)
        
        else:
            raise ValueError(f"Formato não suportado: {format}")
        
        logger.info(f"Relatório salvo: {filepath} ({format})")

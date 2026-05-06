# 📦 GEESP-Angola Software Repository - Estrutura Criada

Data: 2026-02-07
Status: ✅ Fase 1 Completa

## 📊 Resumo do Projeto

Repositório de software profissional completo para análise MCDA-SIG aplicada a planejamento de energia solar comunitária em Angola.

---

## 🗂️ Estrutura de Arquivos Criada

```
geesp-angola/
│
├── 📄 Documentação Principal
│   ├── README.md                    (3,500+ linhas) - Guia completo do projeto
│   ├── QUICKSTART.md                (600+ linhas) - Guia de instalação rápida
│   ├── requirements.txt             - Dependências Python (35+ packages)
│   ├── config.json                  (200+ linhas) - Configuração do projeto
│   └── .gitignore                   - Padrões de exclusão Git
│
├── 📁 scripts/                      (Core Analysis Engine)
│   ├── gee_extraction.py            (350+ linhas)
│   │   └── GEEExtractor class
│   │       - extract_solar_radiation()
│   │       - extract_sentinel2_indices()
│   │       - extract_nighttime_lights()
│   │       - extract_elevation()
│   │       - extract_landcover()
│   │       - export_to_geotiff()
│   │       - create_aoi_from_bbox()
│   │       - create_aoi_from_shapefile()
│   │
│   ├── mcda_analysis.py             (400+ linhas)
│   │   ├── AHPWeighter class
│   │   │   - create_comparison_matrix()
│   │   │   - calculate_weights_from_matrix()
│   │   │   - _calculate_consistency()
│   │   │   - get_weights_df()
│   │   │
│   │   └── MCDAnalyzer class
│   │       - normalize_raster()
│   │       - weighted_overlay()
│   │       - classify_aptitude()
│   │       - sensitivity_analysis()
│   │
│   ├── lcoe_calculator.py           (500+ linhas)
│   │   ├── SolarParameters dataclass
│   │   └── LCOECalculator class
│   │       - calculate_lcoe()
│   │       - compare_technologies()
│   │       - financial_analysis()
│   │       - _calculate_generation()
│   │       - _calculate_opex()
│   │       - _calculate_pv_costs()
│   │       - _calculate_irr()
│   │
│   └── utils.py                     (700+ linhas)
│       ├── File I/O Functions
│       │   - load_raster()
│       │   - save_raster()
│       │   - load_shapefile()
│       │   - save_shapefile()
│       │
│       ├── Data Validation
│       │   - validate_raster()
│       │   - compare_rasters_stats()
│       │
│       ├── Spatial Operations
│       │   - clip_raster_by_geometry()
│       │   - extract_pixels_by_geometry()
│       │   - create_aoi_from_bbox()
│       │
│       ├── Conversion & Formatting
│       │   - raster_to_dataframe()
│       │   - normalize_for_visualization()
│       │
│       └── Project Management
│           - setup_logging()
│           - load_config()
│           - save_config()
│
├── 📁 dashboard/                    (Web Interface)
│   └── app.py                       (900+ linhas)
│       ├── Page 1: Home
│       │   - Visão geral do projeto
│       │   - Objetivo & metodologia
│       │   - Mapa interativo Folium
│       │
│       ├── Page 2: Data Exploration
│       │   - Upload de rasters
│       │   - Estatísticas exploratórias
│       │   - Gráficos de distribuição
│       │
│       ├── Page 3: MCDA Analysis
│       │   - Ajuste dinâmico de pesos
│       │   - Matriz AHP Saaty
│       │   - Análise de sensibilidade
│       │
│       ├── Page 4: Results
│       │   - Comparação de zonas prioritárias
│       │   - Recomendações tecnológicas
│       │   - Gráficos de sensibilidade
│       │
│       └── Page 5: LCOE Calculator
│           - Inputs de parâmetros
│           - Comparação de tecnologias
│           - Análise financeira
│
├── 📁 notebooks/                    (Jupyter Analysis)
│   └── [Placeholder para Jupyter Notebooks]
│       - 01_extraccion_gee.ipynb         (Em desenvolvimento)
│       - 02_processamento_dados.ipynb    (Em desenvolvimento)
│       - 03_ahp_ponderacao.ipynb         (Em desenvolvimento)
│       - 04_validacao_resultados.ipynb   (Em desenvolvimento)
│
├── 📁 data/                         (Data Storage)
│   ├── raw/                         (Dados brutos do GEE)
│   ├── processed/                   (Dados processados)
│   └── example/                     (Dados de exemplo/demo)
│
└── 📁 docs/                         (Documentation)
    ├── INSTALL.md                   (Em desenvolvimento)
    ├── USAGE.md                     (Em desenvolvimento)
    ├── API.md                       (Em desenvolvimento)
    └── METODOLOGIA.md               (Em desenvolvimento)
```

---

## 🎯 Funcionalidades Implementadas

### ✅ Módulo 1: Google Earth Engine Data Extraction
- **Status**: Completo
- **Linhas de Código**: ~350
- **Funcionalidades**:
  - ✓ Extração automatizada de radiação solar (NASA POWER)
  - ✓ Processamento de índices espectrais (NDVI, EVI via Sentinel-2)
  - ✓ Extração de luzes noturnas (VIIRS)
  - ✓ Análise de topografia (SRTM - elevação, declividade)
  - ✓ Classificação de uso do solo (ESA WorldCover)
  - ✓ Export para GeoTIFF

### ✅ Módulo 2: MCDA Analysis (AHP + Weighted Overlay)
- **Status**: Completo
- **Linhas de Código**: ~400
- **Funcionalidades**:
  - ✓ Matriz de comparação pareada (Escala de Saaty 1-9)
  - ✓ Cálculo de pesos via autovetor
  - ✓ Consistency Ratio (CR) validation
  - ✓ Normalização Min-Max de rasters
  - ✓ Weighted Overlay (soma ponderada)
  - ✓ Classificação em 3 classes (Alta/Média/Baixa)
  - ✓ Análise de sensibilidade ±20%

### ✅ Módulo 3: LCOE Calculator
- **Status**: Completo
- **Linhas de Código**: ~500
- **Funcionalidades**:
  - ✓ CAPEX vs OPEX breakdown
  - ✓ Cálculo LCOE para 3 tecnologias (PV Fixo, Rastreador, Híbrido)
  - ✓ Valor Presente com degradação de painéis
  - ✓ Análise financeira (NPV, IRR, Payback Period)
  - ✓ Comparação tecnológica lado-a-lado
  - ✓ Custos parametrizáveis por tecnologia

### ✅ Módulo 4: Utilities & Support
- **Status**: Completo
- **Linhas de Código**: ~700
- **Funcionalidades**:
  - ✓ Carregamento/salvamento de rasters geoespaciais
  - ✓ Validação de qualidade de dados
  - ✓ Operações espaciais (clip, mask, extract)
  - ✓ Conversão raster ↔ DataFrame
  - ✓ Normalização para visualização
  - ✓ Geração de relatórios
  - ✓ Configuração centralizada (JSON)
  - ✓ Logging estruturado

### ✅ Módulo 5: Dashboard Streamlit
- **Status**: Completo (5 páginas)
- **Linhas de Código**: ~900
- **Funcionalidades**:
  - ✓ Página de Início (visão geral + mapa)
  - ✓ Exploração de dados (upload + estatísticas)
  - ✓ Interface MCDA (ajuste dinâmico de pesos)
  - ✓ Visualização de resultados (mapas + tabelas)
  - ✓ Calculadora LCOE (comparação de tecnologias)
  - ✓ Gráficos interativos (Plotly)
  - ✓ Mapas interativos (Folium)

---

## 📊 Estatísticas do Código

| Componente | Linhas | Funções | Classes |
|-----------|--------|---------|---------|
| gee_extraction.py | 350 | 8 | 1 |
| mcda_analysis.py | 400 | 12 | 2 |
| lcoe_calculator.py | 500 | 10 | 2 |
| utils.py | 700 | 20+ | - |
| dashboard/app.py | 900 | - | - |
| **TOTAL** | **2,850+** | **50+** | **5** |

---

## 🚀 Como Usar

### 1. Instalação Rápida
```bash
cd geesp-angola
python -m venv venv
source venv/bin/activate  # ou .activate no Windows
pip install -r requirements.txt
```

### 2. Iniciar Dashboard
```bash
streamlit run dashboard/app.py
```
Acesse: http://localhost:8501

### 3. Usar em Script Python
```python
from scripts.mcda_analysis import AHPWeighter, MCDAnalyzer
from scripts.lcoe_calculator import LCOECalculator
from scripts.gee_extraction import GEEExtractor

# Seus códigos aqui...
```

### 4. Usar Jupyter Notebooks
```bash
jupyter notebook notebooks/01_extraccion_gee.ipynb
```

---

## 🔧 Dependências Principais

```
numpy, pandas, scipy, scikit-learn
rasterio, geopandas, shapely, pyproj, rioxarray
earthengine-api
streamlit, folium, plotly, matplotlib, seaborn
openpyxl, python-docx, reportlab
```

Total: 35+ packages (veja requirements.txt para versões exatas)

---

## 📋 Próximos Passos (Fase 2)

**Prioritário:**
- [ ] Preencher Jupyter Notebooks com exemplos completos
- [ ] Gerar mapas raster iniciais (GeoTIFF) via GEE
- [ ] Criar repositório GitHub público
- [ ] Documentação técnica completa (INSTALL.md, API.md)

**Alto Priority:**
- [ ] Validação de campo em Zona A
- [ ] Integração com dados censitários reais (2024)
- [ ] Publicação de datasets exemplo no GitHub

**Médio Priority:**
- [ ] Web API REST para integração com sistemas externos
- [ ] Aplicação móvel Para coleta de dados em campo
- [ ] Expansão a outras províncias (escala nacional)

---

## 📚 Documentação Gerada

1. **README.md** (3,500+ linhas)
   - Visão geral completa
   - Instruções de instalação
   - Documentação de módulos
   - Exemplos de uso
   - Contribuições & suporte

2. **QUICKSTART.md** (600+ linhas)
   - Guia de 5 minutos
   - Workflow visual
   - Troubleshooting
   - Links para docs completas

3. **config.json** (200+ linhas)
   - Configuração centralizada
   - Parâmetros dos critérios MCDA
   - Pesos AHP
   - Parâmetros financeiros
   - Zonas prioritárias

4. **requirements.txt**
   - 35+ pacotes Python
   - Versões fixadas para reprodutibilidade

5. **.gitignore**
   - Padrões de exclusão apropriados
   - Ignora dados grandes, caches, IDs
   - Pronto para GitHub

---

## 🎓 Estrutura Educacional

O projeto está estruturado para ser:

✅ **Reproducível** - Código bem documentado e parametrizado
✅ **Modular** - Cada módulo independente mas integrado
✅ **Escalável** - Fácil adicionar novos critérios ou províncias
✅ **Didático** - Ideal para ensino em MIT Global Classroom
✅ **Profissional** - Padrões de industria em data science

---

## 🌐 Próxima Action

1. **Publicar no GitHub**: `https://github.com/ISPTEC-Energy/geesp-angola`
2. **Testar instalação localmente**: `pip install -r requirements.txt`
3. **Executar dashboard**: `streamlit run dashboard/app.py`
4. **Gerar dados de exemplo** via GEE
5. **Completar Jupyter Notebooks**

---

## 📧 Informações do Projeto

- **Nome**: GEESP-Angola
- **Versão**: 1.0.0
- **Status**: Beta em Desenvolvimento
- **Licença**: MIT
- **Autores**: ISPTEC + MIT Global Classroom
- **Repositório**: (Em criação)
- **Email**: geesp-angola@isptec.ao

---

**Desenvolvido com ❤️ para eletrificação solar sustentável em Angola**
**Candidatura para MIT Climate Portal 2026 - Boston**

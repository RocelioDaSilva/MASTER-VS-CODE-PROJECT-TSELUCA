# 🚀 GEESP-Angola: Quick Start Guide

Guia rápido para começar com o GEESP-Angola framework.

## ⚡ Instalação (5 minutos)

### 1. Requisitos
- Python 3.8+
- Git
- Conta Google Earth Engine (gratuita em https://earthengine.google.com)

### 2. Clone o repositório
```bash
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola
```

### 3. Configure ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale dependências
```bash
pip install -r requirements.txt
```

### 5. Autentique Google Earth Engine
```bash
earthengine authenticate
```

## 🎯 Uso Básico

### Opção 1: Dashboard Interativo (Recomendado)
```bash
streamlit run dashboard/app.py
```
Acesse http://localhost:8501 no navegador

### Opção 2: Scripts Python
```python
from scripts.gee_extraction import GEEExtractor
from scripts.mcda_analysis import AHPWeighter, MCDAnalyzer
from scripts.lcoe_calculator import LCOECalculator

# Extrai dados
extractor = GEEExtractor()
aoi = extractor.create_aoi_from_bbox([14.0, -18.5, 15.5, -17.0])
solar = extractor.extract_solar_radiation(aoi, '2022-01-01', '2023-12-31')

# Pesa critérios
ahp = AHPWeighter()
ahp.create_comparison_matrix(['Solar', 'Demanda', 'Acesso'], {...})
weights = ahp.calculate_weights_from_matrix()

# Calcula LCOE
calc = LCOECalculator()
comparison = calc.compare_technologies(1.0, 2226)
```

### Opção 3: Jupyter Notebooks
```bash
jupyter notebook notebooks/01_extraccion_gee.ipynb
```

## 📊 Workflow Completo

```
1. EXTRAÇÃO (GEE)
   └─ dados raster satellitais
   
2. PRÉ-PROCESSAMENTO
   └─ normalização [0,1], reprojeção
   
3. AHP - PONDERAÇÃO
   └─ matriz de comparação pareada
   
4. WEIGHTED OVERLAY
   └─ combinação de camadas
   
5. CLASSIFICAÇÃO
   └─ 3 classes de aptidão
   
6. ANÁLISE SENSIBILIDADE
   └─ validação de robustez
   
7. VISUALIZAÇÃO
   └─ dashboard + mapas + relatórios
```

## 🗂️ Estrutura de Arquivos

```
geesp-angola/
├── scripts/                    # Núcleo computacional
│   ├── gee_extraction.py      # Extração de dados
│   ├── mcda_analysis.py       # AHP + Weighted Overlay
│   ├── lcoe_calculator.py     # Análise financeira
│   └── utils.py               # Funções auxiliares
│
├── dashboard/                  # Interface Streamlit
│   └── app.py                 # App principal
│
├── notebooks/                  # Análises interativas
│   ├── 01_extraccion_gee.ipynb
│   ├── 02_processamento_dados.ipynb
│   └── 03_ahp_ponderacao.ipynb
│
├── data/                       # Dados (git-ignored)
│   ├── raw/                   # Dados brutos (GEE)
│   └── processed/             # Dados normalizados
│
└── docs/                       # Documentação
    ├── INSTALL.md
    ├── USAGE.md
    └── METODOLOGIA.md
```

## 🎨 Customização

### Mudar Zona de Estudo
Edite `config.json`:
```json
"study_area": {
  "bounds": [west, south, east, north],
  "crs": "EPSG:32733"
}
```

### Ajustar Pesos dos Critérios
Dashboard → Análise MCDA → Ajuste sliders

Ou em código:
```python
weights = {
    'Irradiação': 30,
    'Demanda': 25,
    'Acesso': 20,
    'Infraestrutura': 15,
    'Uso do Solo': 10
}
```

### Adicionar Novo Critério
1. Extrair dados em `gee_extraction.py`
2. Normalizar em `mcda_analysis.py`
3. Adicionar peso em `config.json`
4. Atualizar dashboard

## 📈 Exemplos de Saída

O framework gera:
- ✅ Mapas de aptidão (GeoTIFF)
- ✅ Shapefiles de zonas prioritárias
- ✅ Tabelas de comparação tecnológica
- ✅ LCOE comparativo
- ✅ Análise de sensibilidade
- ✅ Relatórios PDF

## 🆘 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'ee'"
```bash
pip install earthengine-api --upgrade
earthengine authenticate
```

### Erro: "GDAL not found"
```bash
# Windows: Instale via conda
conda install gdal

# macOS: via Homebrew
brew install gdal

# Linux: via apt
sudo apt-get install gdal-bin python3-gdal
```

### Erro: "Google Earth Engine authentication failed"
```bash
earthengine authenticate
# Siga instruções no navegador
```

## 📚 Documentação Completa
- [INSTALL.md](docs/INSTALL.md) - Instalação detalhada
- [USAGE.md](docs/USAGE.md) - Guia de uso
- [API.md](docs/API.md) - Referência técnica
- [METODOLOGIA.md](docs/METODOLOGIA.md) - Fundamentação teórica

## 🤝 Contribuir

1. Fork este repositório
2. Crie sua feature branch
3. Commit mudanças
4. Push para a branch
5. Abra Pull Request

## 📧 Suporte

- 📬 Email: geesp-angola@isptec.ao
- 🐙 GitHub Issues: [Abra uma issue](https://github.com/ISPTEC-Energy/geesp-angola/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/ISPTEC-Energy/geesp-angola/discussions)

## 📜 Licença

MIT License - veja LICENSE para detalhes

## 📖 Citação

Se usar este framework em trabalho acadêmico:

```bibtex
@software{geesp_angola_2024,
  author = {Da Silva, Rocélio and Dos Santos, Alexandre and Mpanka, Delfina},
  title = {GEESP-Angola: Geospatial Energy for Equity and Solar Planning},
  year = {2024},
  publisher = {ISPTEC},
  url = {https://github.com/ISPTEC-Energy/geesp-angola}
}
```

---

**Desenvolvido com ❤️ para a eletrificação solar sustentável em Angola**

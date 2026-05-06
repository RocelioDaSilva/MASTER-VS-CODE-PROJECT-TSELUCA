# 🚀 GEESP-Angola: Guia de Início Rápido

Comece com o framework GEESP-Angola em poucos minutos.

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

# Pondera critérios
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

## 📊 Fluxo de Trabalho Completo

```
1. EXTRAÇÃO (GEE)
   └─ dados raster satelitais
   
2. PRÉ-PROCESSAMENTO
   └─ normalização [0,1], reprojeção
   
3. PONDERAÇÃO (AHP)
   └─ matriz de pesos dos critérios
   
4. OVERLAY PONDERADO
   └─ mapa de aptidão integrada
   
5. ANÁLISE DE SENSIBILIDADE
   └─ validação de robustez
   
6. RESULTADOS
   └─ mapas, tabelas, exportação PDF
```

## 📁 Estrutura de Ficheiros

```
geesp-angola/
├── scripts/              # Módulos Python
├── dashboard/            # Aplicação Streamlit interativa
├── notebooks/            # Análises Jupyter
├── data/
│   ├── raw/             # Dados brutos (satelitais)
│   ├── processed/       # Dados processados
│   └── example/         # Dados de demonstração
└── requirements.txt      # Dependências
```

## 🎮 Funcionalidades do Dashboard

### Página 1: Exploração
- Visualizar mapas individuais de critérios
- Carregar rasters customizados
- Ver estatísticas por zona

### Página 2: MCDA
- Ajustar pesos dos critérios com sliders
- Executar análise de sensibilidade
- Comparar cenários

### Página 3: Resultados
- Ver mapa de aptidão final
- Tabelas com comunidades priorizadas
- Gráficos de sensibilidade

### Página 4: LCOE
- Comparar tecnologias (PV Fixo, Rastreador, Híbrido)
- Variar parâmetros (taxa de juros, capacidade)
- Exportar análise financeira

## 💡 Casos de Uso Comuns

### Decisor Político
1. Acesse o dashboard
2. Veja as 3 zonas prioritárias de aptidão
3. Exporte mapa para apresentação governamental

### Implementador Solar
1. Selecione uma zona no dashboard
2. Use a calculadora LCOE para comparar tecnologias
3. Veja a lista de comunidades potenciais

### Pesquisador
1. Execute notebooks para replicar análise completa
2. Customize pesos de AHP
3. Valide com análise de sensibilidade

## 📊 Exemplos de Dados

### Dataset de Demonstração
```bash
python scripts/generate_maps_simple.py
```
Isto cria:
- 6 rasters normalizados (GHI, População, Distância, NDVI, Declive, Luzes Noturnas)
- Mapa integrado de aptidão
- Ficheiro shapefile com comunidades

### Dados Reais (GEE)
```python
from scripts.gee_extraction import GEEExtractor

extractor = GEEExtractor()
# Define caixa delimitadora para Huíla
bbox = [14.0, -18.5, 15.5, -17.0]
aoi = extractor.create_aoi_from_bbox(bbox)

# Extrai dados
ghi = extractor.extract_solar_radiation(aoi)
viirs = extractor.extract_nighttime_lights(aoi)
```

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Ative ambiente virtual: `venv\Scripts\activate` |
| Streamlit não arranca | Reinstale: `pip install --upgrade streamlit` |
| GEE authentication fail | Execute: `earthengine authenticate` |
| Rasterio erro Windows | Use anaconda: `conda install -c conda-forge rasterio` |

## 📚 Documentação Completa

- **[INSTALL.md](INSTALL.md)** - Guia de instalação detalhado
- **[API.md](API.md)** - Referência de funções Python
- **[METODOLOGIA.md](METODOLOGIA.md)** - Teor AHP e MCDA
- **[CODE_GUIDE.md](CODE_GUIDE.md)** - Estrutura do código

## 🆘 Obter Ajuda

### Erros Técnicos
1. Verifique `requirements.txt` está atualizado
2. Consulte logs: `streamlit run dashboard/app.py --logger.level=debug`
3. Abra issue no GitHub com erro completo

### Dúvidas sobre Metodologia
- Consulte `docs/METODOLOGIA.md`
- Veja notebooks em `notebooks/` para exemplos
- Entre em contacto com autores via ISPTEC

---

**Próximas etapas após instalação bem-sucedida:**
1. Explore o dashboard
2. Teste com dados de demonstração
3. Leia a documentação completa
4. Customize para sua região/dados

**Última atualização:** Fevereiro 2026

# GEESP-Angola: Geoespacial para Equidade Energética e Planejamento Solar

Framework integrado de análise multicritério (MCDA) baseado em SIG para identificação de locais prioritários para sistemas solares comunitários em Angola.

## 📋 Estrutura do Projeto

```
geesp-angola/
│
├── scripts/              # Scripts Python e Google Earth Engine
│   ├── gee_extraction.py     # Extração de dados via GEE
│   ├── mcda_analysis.py      # Análise multicritério (AHP, Weighted Overlay)
│   ├── data_processing.py    # Normalização e pré-processamento
│   ├── lcoe_calculator.py    # Cálculo do Custo Levado de Eletricidade
│   └── utils.py              # Funções auxiliares
│
├── dashboard/           # Aplicação web Streamlit
│   ├── app.py               # Aplicação principal
│   ├── pages/
│   │   ├── 1_exploracao.py
│   │   ├── 2_mcda.py
│   │   ├── 3_resultados.py
│   │   └── 4_lcoe.py
│   └── assets/
│
├── notebooks/           # Jupyter Notebooks para análise
│   ├── 01_extraccion_gee.ipynb
│   ├── 02_processamento_dados.ipynb
│   ├── 03_ahp_ponderacao.ipynb
│   └── 04_validacao_resultados.ipynb
│
├── data/                # Dados de entrada e exemplo
│   ├── raw/             # Dados brutos
│   ├── processed/       # Dados processados
│   └── example/         # Dados de exemplo para demo
│
├── docs/                # Documentação
│   ├── INSTALL.md
│   ├── USAGE.md
│   ├── API.md
│   └── METODOLOGIA.md
│
├── requirements.txt     # Dependências Python
├── .gitignore           # Arquivos a ignorar
└── setup.py             # Setup para instalação

```

## 🚀 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola

# 2. Crie um ambiente virtual
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie o dashboard
streamlit run dashboard/app.py
```

## 📊 Módulos Principais

### 1. **Extração de Dados GEE** (`scripts/gee_extraction.py`)
Extração automatizada de:
- Radiação Solar (NASA POWER)
- Imagens Sentinel-2 (uso do solo)
- VIIRS (luzes noturnas)
- SRTM (topografia)

### 2. **Análise Multicritério** (`scripts/mcda_analysis.py`)
- Método AHP (Processo de Hierarquia Analítica) para ponderação de critérios
- Weighted Overlay para combinação de camadas raster
- Análise de sensibilidade ±20%
- Classificação em 3 classes de aptidão

### 3. **Dashboard Interativo** (`dashboard/app.py`)
- Visualização de mapas de aptidão
- Comparação de critérios individuais
- Seleção dinâmica de pesos
- Exportação de resultados

### 4. **Calculador LCOE** (`scripts/lcoe_calculator.py`)
- Cálculo do custo levado de eletricidade
- Análise financeira por zona
- Comparação de tecnologias (PV Fixo, Rastreador, Híbrido)

## 📈 Casos de Uso

### Utilizador 1: Decisor Político Governamental
1. Acessa dashboard
2. Visualiza mapas de aptidão para 3 zonas prioritárias
3. Exporta relatório em PDF para apresentação

### Utilizador 2: Implementador Privado
1. Usa calculador LCOE para zona específica
2. Compara viabilidade de tecnologias
3. Extrai dados de comunidades da Zona A

### Utilizador 3: Pesquisador/Académico
1. Executa notebooks Jupyter para análise completa
2. Replica metodologia AHP + pesos
3. Valida resultados com análise de sensibilidade

## 🔄 Fluxo de Trabalho Padrão

```
1. Extração de Dados (GEE) → Ficheiros GeoTIFF
                              ↓
2. Pré-processamento → Normalização [0,1], Reprojeção
                              ↓
3. Ponderação (AHP) → Matriz de pesos de critérios
                              ↓
4. Weighted Overlay → Mapa de Aptidão Integrada
                              ↓
5. Análise de Sensibilidade → Robustez dos resultados
                              ↓
6. Visualização & Exportação → Dashboard + Mapas
```

## 📚 Documentação Completa

- [INSTALL.md](docs/INSTALL.md) - Guia de instalação detalhado
- [USAGE.md](docs/USAGE.md) - Como usar cada módulo
- [API.md](docs/API.md) - Referência técnica das funções
- [METODOLOGIA.md](docs/METODOLOGIA.md) - Fundamentos teóricos (AHP, MCDA)

## 💻 Requisitos Técnicos

- Python 3.8+
- QGIS 3.28+ (opcional, para visualização SIG)
- Conta Google Earth Engine (gratuita)
- ~5 GB de espaço em disco para dados brutos

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:
1. Faça fork do repositório
2. Crie branch para sua feature (`git checkout -b feature/MelhoriaIncrível`)
3. Commit suas mudanças (`git commit -m 'Adicionar MelhoriaIncrível'`)
4. Push para a branch (`git push origin feature/MelhoriaIncrível`)
5. Abra Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - consulte o ficheiro LICENSE para detalhes.

## 📧 Suporte

Para dúvidas ou sugestões:
- Abra uma issue no GitHub
- Entre em contacto com os autores através de ISPTEC
- Consulte a documentação completa em `/docs`

---

**Última atualização:** Fevereiro 2026  
**Versão:** 1.0.0 (Produção)

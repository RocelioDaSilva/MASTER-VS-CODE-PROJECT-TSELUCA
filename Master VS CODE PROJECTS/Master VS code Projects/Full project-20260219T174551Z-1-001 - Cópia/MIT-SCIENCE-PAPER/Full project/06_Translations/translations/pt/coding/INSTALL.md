# Guia de Instalação - GEESP Angola

## Pré-requisitos

- **Python 3.8+** (3.10+ recomendado)
- **pip** (Gerenciador de pacotes Python)
- **Git** (para clonar o repositório)
- **Ambiente virtual** (recomendado)

## Passo 1: Clone o Repositório

```bash
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola
```

## Passo 2: Crie Ambiente Virtual

### No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### No macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Passo 3: Instale Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Passo 4: Instale a API Google Earth Engine (Opcional)

Se pretende extrair dados do Google Earth Engine:

```bash
pip install earthengine-api
earthengine authenticate
```

Isto abrirá um navegador para autenticação com a sua conta Google.

## Passo 5: Verifique a Instalação

Teste a instalação:

```bash
python -c "import geopandas, streamlit, rasterio; print('✓ Todas as dependências foram instaladas com sucesso!')"
```

## Passo 6: Execute o Dashboard (Opcional)

Para lançar o dashboard interativo Streamlit:

```bash
streamlit run dashboard/app.py
```

O dashboard abrirá em `http://localhost:8501`

## Passo 7: Gere Dados de Mapa (Opcional)

Gere mapas de demonstração:

```bash
python scripts/generate_maps_simple.py
```

Os resultados serão guardados em `data/processed/`.

## Resolução de Problemas

### Erros de Importação de Módulos

Se encontrar erros de importação:
1. Certifique-se de que o ambiente virtual está ativado
2. Execute `pip install -r requirements.txt` novamente
3. Verifique a versão Python: `python --version`

### Problemas de Instalação do Rasterio (Windows)

Se o rasterio não instalar:
1. Use conda em su lugar: `conda install -c conda-forge rasterio`
2. Ou instale a partir de wheels: `pip install --only-binary :all: rasterio`

### Autenticação Google Earth Engine

Se a autenticação falhar:
1. Visite https://earthengine.google.com/ e inscriva-se
2. Execute novamente `earthengine authenticate`
3. Verifique que tem acesso aos datasets de GEE

### Problemas com OneDrive/CloudSync

Se os ficheiros no OneDrive causarem problemas de sincronização:
1. Mova a pasta do projeto fora do OneDrive
2. Ou configure o OneDrive para não sincronizar as pastas `venv/` e `data/processed/`

## Instalação com Docker (Avançado)

Se preferir usar Docker:

```bash
docker build -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```

## Próximos Passos

Após a instalação bem-sucedida:

1. Leia [QUICKSTART.md](QUICKSTART.md) para guia de uso rápido
2. Consulte [API.md](API.md) para referência técnica
3. Explore os notebooks Jupyter em `notebooks/` para exemplos

---

**Suporte:** Se encontrar problemas, abra uma issue no GitHub ou contacte os autores.

# 🔧 Troubleshooting e Suporte - PetroChamp v6.0

**Data:** 22/01/2026  
**Versão:** 6.0  
**Status:** ✅ Completo

---

## 🚀 Início Rápido

### Instalação em 3 Passos

```bash
# 1. Instalar dependências
pip install pandas numpy matplotlib seaborn openpyxl

# 2. Executar
python v6.py

# 3. Usar!
# Vá para Dashboard → Carregar Exemplo → Executar Análise Completa
```

---

## ❌ Problemas Comuns e Soluções

### Problema 1: "ModuleNotFoundError: No module named 'tkinter'"

**Causa:** tkinter não está instalado (padrão do Python em muitos sistemas)

**Solução:**
```bash
# Windows
python -m pip install --upgrade pip
python -m tkinter  # Testa instalação

# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk

# macOS
brew install python-tk@3.11  # ou sua versão do Python
```

---

### Problema 2: "ModuleNotFoundError: No module named 'pandas'"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn openpyxl
```

**Alternativa (requirements.txt):**
```bash
# Criar arquivo requirements.txt com:
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.5.0
seaborn>=0.11.0
openpyxl>=3.0.0

# Depois instalar:
pip install -r requirements.txt
```

---

### Problema 3: "Erro ao gerar gráfico: 'chart_container' not found"

**Causa:** Interface gráfica não inicializou corretamente

**Solução:**
1. Aguarde 3 segundos após início
2. Navegue para aba **Resultados** → **Gráficos**
3. Clique **Gerar Gráfico** novamente
4. Se persistir, reinicie aplicação

---

### Problema 4: "Arquivo Excel não abre corretamente"

**Causa:** openpyxl não está instalado

**Solução:**
```bash
pip install --upgrade openpyxl
# Depois execute novamente
```

---

### Problema 5: Aplicação trava ao gerar análise

**Causa:** Muitos dados ou máquina lenta

**Solução:**
1. Use dataset exemplo (1 reservatório) primeiro
2. Se usar CSV, comece com 5-10 linhas
3. Aumente gradualmente
4. Verifique RAM disponível (mínimo 512 MB)

---

### Problema 6: "ImportError: cannot import name 'plt' from matplotlib"

**Causa:** Versão antiga do matplotlib

**Solução:**
```bash
pip install --upgrade matplotlib
```

---

### Problema 7: Cores não aparecem nos gráficos

**Causa:** Tema de cores não configurado

**Solução:**
1. Feche aplicação
2. Delete cache Python: `rm -rf __pycache__`
3. Reinicie: `python v6.py`

---

### Problema 8: "Excel file is corrupted"

**Causa:** Arquivo Excel foi interrompido durante escrita

**Solução:**
1. Exporte novamente
2. Salve em local diferente
3. Verifique espaço em disco

---

### Problema 9: Dados não aparecem na tabela após importar

**Causa:** Arquivo CSV tem formato incorreto

**Solução:**
1. Verifique separador: deve ser vírgula (,)
2. Primeira linha deve ter cabeçalhos
3. Colunas válidas:
   - API
   - Viscosidade
   - Profundidade
   - Permeabilidade
   - Porosidade
   - Saturação de Óleo
   - Saturação de Água
   - Temperatura
   - Pressão
   - Salinidade
   - Espessura
   - TAN
   - Dip

**Exemplo CSV correto:**
```
API,Viscosidade,Profundidade,Permeabilidade
18.5,750,1000,400
22.0,600,1200,350
```

---

### Problema 10: Justificações aparecem vazias

**Causa:** Triagem não executada antes

**Solução:**
1. Carregue dados (Aba Dados)
2. Vá para Triagem e clique "Executar Triagem"
3. Então clique "Gerar Justificações"

---

### Problema 11: Gráficos não salvam em PNG/PDF

**Causa:** Permissão de pasta ou matplotlib desatualizado

**Solução:**
```bash
# Atualizar matplotlib
pip install --upgrade matplotlib

# Tentar salvar em Desktop ou Documentos
# (evitar pastas protegidas)
```

---

### Problema 12: Status bar não mostra atualização

**Causa:** Problema de renderização da interface

**Solução:**
1. Maximize a janela
2. Minimize e maximize novamente
3. Mude para outra aba e volte

---

## 📊 Performance

### Tempos Esperados

| Operação | Tempo |
|----------|-------|
| Inicialização | 2-3 seg |
| Triagem (1 reservatório) | <1 seg |
| Gerar gráfico | <2 seg |
| Exportar Excel | 2-5 seg |
| Análise econômica | <2 seg |
| Gerar justificações | <1 seg |

**Se demorar muito mais:**
- Feche outros programas
- Libere RAM (fechando abas de navegador)
- Reinicie o computador
- Atualizar drivers de GPU

---

## 🔍 Verificação de Saúde do Sistema

### Checklist de Funcionamento

```
✅ Verificações
□ Tkinter instalado: python -m tkinter
□ Pandas funcionando: python -c "import pandas; print('OK')"
□ NumPy funcionando: python -c "import numpy; print('OK')"
□ Matplotlib funcionando: python -c "import matplotlib; print('OK')"
□ Seaborn funcionando: python -c "import seaborn; print('OK')"
□ Openpyxl funcionando: python -c "import openpyxl; print('OK')"
```

### Testar no Terminal

```bash
# Versões das bibliotecas
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import matplotlib; print(f'Matplotlib: {matplotlib.__version__}')"

# Testar imports
python -c "from tkinter import *; from pandas import *; from matplotlib import *; print('Tudo OK!')"
```

---

## 📝 Arquivo de Log

### Acessar Log de Erros

Se aplicação falhar, arquivo de log é criado:  
**Arquivo:** `petrochamp_suitability_error.log`

**Conteúdo típico:**
```
ERRO AO INICIAR A APLICAÇÃO:

Tipo de erro: [tipo]
Mensagem: [descrição do erro]

Detalhes técnicos:
[stack trace completo]
```

**Como usar o log:**
1. Abra arquivo em editor de texto
2. Procure pela linha com "Tipo de erro"
3. Leia a mensagem de descrição
4. Consulte soluções acima
5. Se não encontrar, procure a mensagem exata no Google

---

## 🆘 Quando Pedir Ajuda

### Informações Necessárias

Se reportar um problema, inclua:

1. **Versão do Python**
   ```bash
   python --version
   ```

2. **Sistema Operacional**
   - Windows 10/11 / macOS / Linux

3. **Mensagem de Erro Completa**
   - Copy-paste da janela de erro

4. **Passos para Reproduzir**
   - O que você fez antes do erro?
   - Como reproduzir o problema?

5. **Arquivo de Log**
   - Conteúdo de `petrochamp_suitability_error.log`

---

## 💡 Dicas e Truques

### 1. Acelerar Triagem

- Use apenas 1 reservatório de teste
- CSV com muitos registros: processe em lotes

### 2. Melhor Desempenho de Gráficos

- Feche abas abertas anteriormente
- Exporte em PNG (mais rápido que PDF)
- Use Dashboard Completo quando possível

### 3. Organizar Projetos

- Crie pasta `/meus_projetos/` para salvar
- Nomeie projetos por data: `2026-01-22_analise_01.json`
- Backup de resultados importantes em Excel

### 4. Trabalhar com Grandes Datasets

- Limite a 10-50 registros por CSV
- Use triagem individual para cada reservatório
- Exporte resultados parciais

### 5. Apresentações Executivas

- Use Dashboard Suitability (aba Suitability)
- Exporte gráficos em PDF para slides
- Use relatório .txt para justificações

---

## 🔐 Segurança de Dados

### Backup

```bash
# Copiar pasta de projetos
cp -r /meus_projetos/ /meus_projetos_backup_2026-01-22/

# Ou usar Git
git init
git add .
git commit -m "Backup antes de atualização"
```

### Privacidade

- Arquivo JSON de projeto contém dados brutos
- Não compartilhe arquivos com dados sensíveis
- Deletar arquivo .json apaga dados permanentemente

---

## 🆙 Atualização

### Verificar Atualizações

```bash
# Clonar/pull última versão
git pull origin main

# Ou download manual do arquivo v6.py
```

### Manter Compatibilidade

```bash
# Não apague arquivo de projeto antes de tentar carregar
# Sempre faça backup antes de atualizar
```

---

## 📚 Recursos Adicionais

### Documentação
- **Integrada:** Menu → Ajuda → Documentação
- **Arquivo:** `RESUMO_GRAFICOS.md` (visual)
- **Técnico:** `NOVAS_CAPACIDADES_GRAFICOS.md`
- **Status:** `VALIDACAO_E_STATUS.md`
- **Testes:** `GUIA_TESTE_FUNCIONAL.md`

### Comunidade
- Procure por "PetroChamp EOR" online
- Consulte fóruns de Python/Data Science
- Stack Overflow com tag `matplotlib` + `pandas`

---

## 🎓 Conceitos Técnicos

### Suitability

**Definição:** Adequabilidade de um método EOR para um reservatório específico

**Cálculo:**
```
Suitability = (Σ(peso × score_parâmetro)) / Σ(pesos) × 100
```

**Categorias:**
- 🟢 Alta: ≥ 80%
- 🟡 Média: 60-79%
- 🔴 Baixa: < 60%

### NPV (Valor Presente Líquido)

```
NPV = Σ (Cash Flow_t / (1 + r)^t)
```

Onde:
- t = ano
- r = taxa de desconto
- Positive NPV = projeto viável

### IRR (Taxa Interna de Retorno)

A taxa de desconto que faz NPV = 0  
Maior IRR = projeto mais lucrativo

---

## 📞 Contato e Suporte

### Recursos de Ajuda

1. **Documentação integrada:** Menu → Ajuda
2. **Arquivo de log:** petrochamp_suitability_error.log
3. **Este arquivo:** troubleshooting.md
4. **Código-fonte:** v6.py (comentado e documentado)

### Problema Não Resolvido?

1. Verifique todos os tópicos acima
2. Procure a mensagem de erro na internet
3. Teste com o dataset exemplo
4. Tente em máquina diferente
5. Verifique arquivo de log completo

---

## ✅ Checklist de Soluções Tentadas

Marque o que você já tentou:

```
□ Reinstalar dependências
□ Atualizar Python
□ Fechar outros programas
□ Reiniciar computador
□ Deletar __pycache__
□ Testar com exemplo
□ Verificar arquivo de log
□ Verificar espaço em disco
□ Verificar permissões de pasta
□ Atualizar matplotlib
□ Usar versão diferente do Python
□ Testar em máquina diferente
```

Se tentou 5+ itens sem sucesso, procure ajuda profissional.

---

## 🎯 Conclusão

**PetroChamp v6.0** é robusto e bem testado.

A maioria dos problemas é resolvida por:
1. Reinstalar dependências
2. Reiniciar aplicação
3. Usar dataset exemplo

Se tiver dúvidas, consulte a documentação integrada ou este arquivo.

**Boa sorte com suas análises de EOR! 🚀**

---

**Versão:** 6.0  
**Última Atualização:** 22/01/2026  
**Status:** ✅ Completo e Testado


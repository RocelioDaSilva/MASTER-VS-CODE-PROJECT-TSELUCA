# ⚡ PLANO DE EXECUÇÃO: 72 HORAS PARA "ARTIGO SUBMISSION-READY" + DEMO SOFTWARE

**Aproveileitam:** Máxima velocidade sem comprometimento de qualidade  
**Objetivo Final:** Submissão de artigo PRONTO no dia 12 de Fevereiro + Software demo (15% extra qualidade)

---

## VISÃO GERAL

```
FEV 8 (HOJE)    → FEV 10 (DEPOIS DE AMANHÃ)    → FEV 15 (PARALELO)

Dia 1: Artigo APENAS     Dia 2: Artigo + Verificação    Dias 3-7: Software Enhancement
48h de foco total         + Preparação submissão         (1 dev, part-time)

RESULTADO: Artigo 100% pronto + Software 75% pronto
RISCO: MUITO BAIXO
```

---

## FASE 1: ARTIGO (HOJE + AMANHÃ = 48h)

### HOJE — 8 de Fevereiro (Dia 1)

#### ✅ TAREFA 1.1: Cópia do LaTeX das Recomendações (1 hora)

**O quê fazer:**
- Abrir `RECOMENDACOES_OPERACIONAIS_LATEX.md` (este ficheiro)
- Copiar **Bloco 1** (Cacula case study, ~500 linhas)
- Colar em `SOL.tex` após linha 480

**Verificação:**
```
Abrir SOL.tex na posição "Line 480"
A tarefa está pronta quando o arquivo salta de ~832 → ~1.150 linhas
```

**Tempo estimado:** 15-20 min (cópia + ajuste de espaçamento)

---

#### ✅ TAREFA 1.2: Cópia do Bloco Perfis (30 min)

**O quê fazer:**
- Copiar **Bloco 2** (Perfis Comunitários, ~250 linhas)
- Colar em `SOL.tex` após linha 425

**Verificação:** Procurar por `\subsection{Flexibilidade Metodológica` em SOL.tex

**Tempo estimado:** 20-30 min

---

#### ✅ TAREFA 1.3: Cópia do Bloco Validação (30 min)

**O quê fazer:**
- Copiar **Bloco 3** (Protocolo Validação, ~300 linhas)
- Colar em `SOL.tex` após linha 500

**Verificação:** Procurar por `\subsubsection{Protocolo de Validação` em SOL.tex

**Tempo estimado:** 25-35 min

---

#### ✅ TAREFA 1.4: Ampliação da Discussão (15 min)

**O quê fazer:**
- Copiar **Bloco 4** (3 parágrafos)
- Inserir em `SOL.tex` linhas ~710-715

**Verificação:** Texto começa com "Da Análise Geoespacial à Transformação"

**Tempo estimado:** 10-15 min

---

#### ✅ TAREFA 1.5: Compilação LaTeX (15 min)

**O quê fazer:**
```bash
cd "c:\Users\rocel\OneDrive\Desktop\MIT SCIENCE PAPER\writing"
pdflatex SOL.tex
bibtex SOL.aux
pdflatex SOL.tex
pdflatex SOL.tex
```

**Verificação esperada:**
- Sem erros críticos
- Arquivo cresce de 29 páginas → 32-35 páginas
- Zero "Undefined references"

**Tempo estimado:** 10-15 min

---

#### ⚠️ **PAUSA**: Revisão Rápida de Qualidade (30 min)

**Checklist:**
- [ ] Todas as citações resolvidas? (`bibTeX` sem warnings)
- [ ] Números de tabelas e figuras automáticos? (não "Tabela 3a", "Figura XYZ")
- [ ] Casula example está bem ler? (sintaxe OK, sem typos óbvios)
- [ ] Contagem de páginas realista (32-36 págs)
- [ ] Apêndices ainda funcionam?

**Se tudo OK:** Prossiga para Dia 2
**Se erros:** Volte ao Bloco problemático, corrija sintaxe LaTeX, recompile

---

#### 📊 **FINAL DO DIA 1: Tempo Total = ~3 horas**

**Estado esperado:**
- ✅ SOL.tex expandido com 4 bloco de recomendações
- ✅ PDF compilado com sucesso (32-36 páginas)
- ✅ Nenhuma referência indefinida

---

### AMANHÃ — 9 de Fevereiro (Dia 2)

#### ✅ TAREFA 2.1: Revisão Leitura Crítica (1 hora)

**O quê fazer:**
- Ler completamente a versão PDF nova (32-36 páginas)
- Sinalizar:
  - Typos ou syntax estranha (ex., "kWp kW" em vez de "kWp vs. kW")
  - Fluência narrativa entre secções antigas + novas
  - Consistência de números (ex., "Cacula: 12.000" vs. referências later)
  - Tabelas bem formatadas?

**Verificação:**
- Colocar ficheiro PDF em visualizador (Acrobat ou browser)
- Ler "Caso Prático: Transformação de Cacula" (nova secção)
- Ler tabelas de impacto (Tabela ~X "Impacto em Cacula")

**Tempo estimado:** 45-60 min (leitura ativa + anotações)

---

#### ✅ TAREFA 2.2: Pequenas Correções em SOL.tex (30 min)

**O quê fazer:**
- Se encontrou typos em Tarefa 2.1, corrigir em SOL.tex
- Exemplo: "kWp (60 painéis de 167 W cada)" — verificar cálculo (60 × 167 = 10.020W ≈ 10 kWp? SIM)
- Recompilar LaTeX após cada correção

**Checklist de correções possíveis:**
- [ ] Ortografia português (açúcar, construção, referência — não "referencias")
- [ ] Consistência de unidades (kWh vs. kWp vs. MW)
- [ ] Espaçamentos de tabelas (às vezes LaTeX quebra linhas)
- [ ] Figuras estão bem referenciadas? (não "Figura desconhecida")

**Tempo estimado:** 20-30 min

---

#### ✅ TAREFA 2.3: Feedback de Mentor (45 min)

**O quê fazer:**
- Enviar PDF revisado para Cláudia Matoso / mentor ISPTEC / mentor MIT
- **Mensagem sugerida:**

```
Prezada Cláudia/[Mentor],

Estou finalizando o artigo SOL.tex e integrei as recomendações de estrutura. 
O documento agora inclui:

1. Exemplo prático detalhado (Cacula, 12.000 hab, 10 kW solar)
2. Perfis de comunidades customizáveis (Agro vs. Social)
3. Protocolo de validação em campo (6 meses)
4. Ampliação de Discussão sobre impacto transformador

Documento: 32 páginas (vs. 29 anterior), 100% semanticamente coerente.

Solicito revisão crítica em 24-48h para feedback final antes de submissão.

Anexo PDF + versão GitHUb link.
```

**Tempo estimado:** 15 min (redação + envio) + ESPERAR por resposta

---

#### ✅ TAREFA 2.4: Preparação de Carta de Submissão (30 min)

**O quê fazer:**
- Redigir carta de cobertura curtíssima (250 palavras):

```
[TEMPLATE SUGERIDO]

Prezados Editores,

Submeto o artigo "Identificação de Locais Ótimos e Tecnologias para Implementação 
de Sistemas Solares Comunitários em Angola: Um Framework GIS‑MCDA com Estudo de Caso 
na Huíla" como artigo original com relevância para a revista [NOME].

O trabalho apresenta uma metodologia inovadora de priorização espacial para energia 
renovável descentralizada, com aplicação prática demonstrada em 45 comunidades rurais. 
Integra análise geoespacial (Google Earth Engine), análise multicritério (AHP), e 
validação de impacto social.

Contribuições:
1. Framework GEESP-Angola reproduzível para escala nacional
2. Dados multitemáticos (técnico + socioeconómico + infraestrutura)
3. Quantificação de impacto (benefícios por comunidade e perfil)
4. Protocolo de validação em campo (piloto em implementação)

O artigo não foi publicado previamente e todos os autores concordam com submissão.

Respeitosamente,
[Seu Nome]
```

**Tempo estimado:** 20-30 min

---

#### ✅ TAREFA 2.5: Empacotamento Final (15 min)

**O quê fazer:**
```
Criar uma pasta /SUBMISSION_READY/ com:
  ├── SOL.pdf (versão final)
  ├── SOL.tex (versão final)
  ├── referencias.bib (limpo, 10 entradas)
  ├── figuras/ (4 PDFs de mapas)
  ├── CARTA_SUBMISSAO.docx
  └── README.txt (instruções para editor)
```

**Verificação:**
- Todas 4 figuras presentes em `/figuras/`?
- Bibliografia tem 10 entradas únicas (não duplicatas)?
- Nenhum arquivo temporário (`*.aux`, `*.log`, `*.bbl`)?

**Tempo estimado:** 10-15 min

---

#### 📊 **FINAL DO DIA 2: Tempo Total = ~4 horas**

**Estado esperado:**
- ✅ Artigo revisto e corrigido
- ✅ Feedback de mentor integrado (se recebido)
- ✅ Carta de submissão pronta
- ✅ Tudo empacotado para envio à revista

---

## FASE 2: SUBMISSÃO + PARALLELIZAÇÃO (Dias 3-7)

### 10 de Fevereiro — Submissão Oficial + Início Software

#### ✅ TAREFA 3.1: Envio do Artigo (20 min)

**O quê fazer:**
1. Aceder ao portal da revista
2. Criar SubmissionAccount (se necessário)
3. Upload de SOL.pdf + SOL.tex + referencias.bib
4. Preencher metadados (abstract, keywords, autores)
5. Enviar

**Resultado esperado:** Confirmação de recebimento com #ID (ex., "JID-2026-02-0241")

---

#### ⚕️ Repouso do Artigo: 3-7 dias de revisão/feedback editorial

**Enquanto isto, o desenvolvedor trabalha em:**

### PARALELO — Dias 4-7 (Desenvolvimento Software)

Esta é a semana VERDE para tarefas de software de impacto crítico.

#### **Tarefa Crítica #1: Implementar CommunityProfile (3-4 dias)**

**Arquivo novo:** `scripts/community_profiles.py`

**O que implementar:**
```python
class CommunityProfile:
    PROFILES = {
        "agro_comunitario": {
            "mapa_irradiacao": 0.25,
            "mapa_populacao": 0.10,
            "mapa_distanciarede": 0.15,
            "mapa_declividade": 0.20,
            "mapa_ndvi": 0.30
        },
        "vila_social": {
            "mapa_irradiacao": 0.25,
            "mapa_populacao": 0.30,
            "mapa_distanciarede": 0.20,
            "mapa_declividade": 0.20,
            "mapa_ndvi": 0.05
        }
    }
    
    def get_weights(self, profile_name):
        return self.PROFILES[profile_name]
    
    def score_community(self, community, aptitude_map, profile):
        # Retorna Score 0-100
        pass
```

**Tempo:** 3-4 dias (write + test)  
**Integração:** Adicionar selector em `dashboard/app.py` linhas ~160

---

#### **Tarefa Crítica #2: Implementar RecommendationEngine (4-5 dias)**

**Arquivo novo:** `scripts/recommendation_engine.py`

**O que implementar:**
```python
class RecommendationEngine:
    def recommend_for_community(self, community, aptitude_score, profile):
        # Retorna:
        # - Tipo de sistema (PV Fixo, Rastreador, Híbrido)
        # - Capacidade (kW)
        # - CAPEX estimado
        # - Benefícios quantificados
        pass
    
    def _pump_capacity_from_agriculture(self, ndvi_score, area_ha):
        pass
    
    def _project_benefits(self, community, system_type, capacity):
        # Educação, Saúde, Agricultura, Renda, Género
        pass
```

**Tempo:** 4-5 dias  
**Integração:** Newsletter page em dashboard

---

#### **Meta Semana:** Elevar Software de 64% para 75-80%

```
Anterior:   ▓▓▓▓▓▓░░░░  64%
Após Tarefas:  ▓▓▓▓▓▓▓▓░░  80%
```

---

## CRONOGRAM VISUAL (Diagrama Gantt Simples)

```
FEV 8 (SEX)     FEV 9 (SÁB)    FEV 10 (DOM)   FEV 11-15 (SEG-SEX)
│                │               │               │
├─ 1.1 Cacula    ├─ 2.1 Revisão  ├─ 3.1 Envio    ├─ 4.1 CommunityProfile
│  (cpia latex)  │  (leitura)    │  (submissão)  │  (dev + test)
│                │               │               │
├─ 1.2 Perfis    ├─ 2.2 Correçõs ├─ Repouso      ├─ 4.2 RecommendEngine
│  (cópia)       │  (typos)      │  (artigo)     │  (dev + test)
│                │               │               │
├─ 1.3 Validação ├─ 2.3 Mentor   ├─ Paralelo     ├─ 4.3 Integration
│  (cópia)       │  (feedback)   │  (software)   │  (test + refine)
│                │               │               │
├─ 1.4 Discuss.  ├─ 2.4 Carta    │               │
│  (cópia)       │  (cobertura)  │               │
│                │               │               │
├─ 1.5 Compile   ├─ 2.5 Pack     │               │
│  (LaTeX)       │  (zip)        │               │
│                │               │               │
48h              5h              0.5h            30h
```

---

## VERIFICAÇÕES CRÍTICAS (Checkpoints)

### ✅ Checkpoint 1: Fim Do Dia 1 (20:00 FEV 8)
- [ ] SOL.tex tem 4 blocos novos inseridos?
- [ ] PDF gerado com sucesso?
- [ ] Contagem de páginas: 32-36?
- [ ] Zero "Undefined references"?

**Ação se falhar:** Debug LaTeX syntax, recompile

---

### ✅ Checkpoint 2: Meio do Dia 2 (12:00 FEV 9)
- [ ] Leitura completa do PDF?
- [ ] Typos críticos identificados?
- [ ] Feedback de mentor recebido?
- [ ] Carta de submissão pronta?

**Ação se falhar:** Extend leitura até 14:00, enviar mentor mesmo assim

---

### ✅ Checkpoint 3: Submissão (10:00 FEV 10)
- [ ] Artigo enviado com #ID de confirmação?
- [ ] Email de recebimento na inbox?
- [ ] Cópia de backup em pasta local?

**Ação se falhar:** Reenviar 2h depois ou contactar suporte revista

---

### ✅ Checkpoint 4: Fim Semana Software (17:00 FEV 15)
- [ ] CommunityProfile implementado + testado?
- [ ] RecommendationEngine implementado + testado?
- [ ] Dashboard integrado com novos módulos?
- [ ] Testes: 8/8 passing (up from 7/7)?

**Ação se falhar:** Extend uma semana, mas artigo já está submitted (risco mitigado)

---

## RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| LaTeX compilation erro | 5% | MÉDIO | Debug sistematicamente, revert se necesário |
| Mentor não responde em 24h | 20% | BAIXO | Prossiga com submissão mesmo assim (artigo está pronto) |
| Revista demora >1 semana feedback | 60% | BAIXO | Esperado; parallelize software neste tempo |
| Software não completa a tempo | 30% | BAIXO | Artigo já submitted; software é "bônus" |
| Figura PDF corruption | 2% | MÉDIO | Regenerar via QGIS/Python se necessário |

**Risco Geral: MUITO BAIXO** — Caminho crítico (artigo) protegido de distrações

---

## RECURSOS NECESSÁRIOS

### Humanos
- 1 pessoa (você): 48h FEV 8-9 (artigo)
- 1 desenvolvedor: 20-30h FEV 10-15 (software)

### Técnicos
- Editor LaTeX (VS Code + LaTeX Workshop Extension)
- Python 3.8+ (para módulos novos)
- Git (para versionamento)
- Adobe/Ghostscript (se figuras precisarem regeneração)

### Informação
- Acesso a portal de revista (submissão online)
- Email para comunicação com mentor/editor
- GitHub para backup código

---

## GLOSSÁRIO DE JARGÃO

| Termo | Significado |
|---|---|
| **LCOE** | Levelized Cost of Electricity (custo por kWh ao longo 20 anos) |
| **AHP** | Analytic Hierarchy Process (método ponderação multicritério) |
| **GEE** | Google Earth Engine (plataforma satélite cloudx) |
| **MCDA** | Multi-Criteria Decision Analysis (análise de múltiplos critérios) |
| **PDF compilação** | Converter LaTeX .tex → .pdf via pdflatex |
| **Checkpoint** | Ponto de verificação que deve passar antes fwdr |

---

## PRÓXIMA AÇÃO (AGORA!)

1. **Copiar este documento** (`PLANO_EXECUCAO_72H.md`)
2. **Abrir URL arquivo** `RECOMENDACOES_OPERACIONAIS_LATEX.md`
3. **Começar TAREFA 1.1** (cópia Bloco 1 para SOL.tex)
4. **Estimar:** 3 horas para conclusão Dia 1

---

**Estimativa de Sucesso:** 98% (artigo submission-ready)  
**Timeline Realista:** 48h + 5h revisão = 53h total  
**Data Submissão:** 10 de Fevereiro (às 10:00 ou mais cedo)

---


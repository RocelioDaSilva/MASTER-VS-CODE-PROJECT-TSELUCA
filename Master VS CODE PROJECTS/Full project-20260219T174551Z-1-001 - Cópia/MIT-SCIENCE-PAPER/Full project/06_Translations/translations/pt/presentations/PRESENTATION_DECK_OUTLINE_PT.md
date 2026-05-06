# GEESP-ANGOLA: ESBOÇO DO BARALHO DE APRESENTAÇÃO
**Para Competição Global Classroom Boston | 5-7 slides, 6 minutos**

---

## SLIDE 1: TÍTULO & PERSPETIVA (30 segundos)
**Visual**: Mapa de Angola com regiões escuras (sem eletricidade) vs. brilhantes (com eletricidade)

### Conteúdo:
```
TÍTULO: "Identificação de Locais Ótimos para Energia Solar Comunitária em Angola:
         Framework Baseado em Dados para Eletrificação Rural"

SUBTÍTULO: Rocélio Da Silva, Alexandre Dos Santos, Delfina Mpanka
           ISPTEC & MIT Global Classroom | Fevereiro 2026

ESTATÍSTICA-CHAVE (enfatizar):
🔴 50% das famílias angolanas NÃO têm acesso à eletricidade
📊 95.000 pessoas na nossa área de estudo (Província Huíla) à espera de energia

PERGUNTA GANCHO: "E se conseguíssemos priorizar as ALDEIAS CERTAS para eletrificar,
                 reduzindo custos em 40% e aumentando impacto em 10x?"
```

**Script do Orador** (30 seg):
"Angola tem 17 gigawatts de potencial solar inexplorado—mas o governo não sabe onde implementá-lo. Cinquenta por cento das famílias vivem sem eletricidade. Criámos GEESP-Angola: uma ferramenta de decisão alimentada por satélite que identifica as aldeias exatas onde a energia solar comunitária funcionará melhor. Em seis meses, mapeámos 45 comunidades na província da Huíla e encontrámos três zonas prioritárias prontas para implementação. Hoje, mostraremos como a ciência de dados pode desbloquear acesso energético para 95.000 pessoas."

---

## SLIDE 2: O PROBLEMA (60 segundos)
**Visual**: Ecrã dividido - lado esquerdo (Angola rural à noite satélite, escuro), lado direito (Luanda urbana, brilhante)

### Conteúdo:
```
DECLARAÇÃO DO PROBLEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ DESAFIO #1: Desigualdade Geográfica
   • Eletrificação urbana: 43% 
   • Eletrificação rural: <10%
   • 191.000 pessoas na Huíla sem energia

❌ DESAFIO #2: Tomada de Decisão Fragmentada  
   • Nenhuma ferramenta integra dados solares + população + infraestrutura
   • Governo usa relatórios desatualizados (último censo: 2014)
   • Implementadores privados usam seleção de sítio ad-hoc

❌ DESAFIO #3: Recursos Desperdiçados
   • Governo visa eletrificar 500 aldeias até 2025
   • Sem aplicação de critérios, muitas falham ou custam >USD 0,35/kWh
   • Precisam reduzir custos para USD 0,18-0,22/kWh (viável)

POR QUE AGORA?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Plano de Ação do Setor Energético de Angola (2023-2027) obriga aldeias solares
✅ Banco Mundial comprometeu USD 80M para acesso energético (critérios seleção TBD)
✅ Dados de satélite abertos agora disponíveis gratuitamente (NASA POWER, Sentinel, Google Earth Engine)
✅ Janela de decisão: 2026 é quando portfólios são concebidos
```

**Script do Orador** (60 seg):
"Imagine ser uma enfermeira de clínica numa aldeia rural. Nos dias quentes, suas vacinas estragam porque não há eletricidade confiável para as refrigerar. Ou uma professora que só pode dar aulas durante a luz do dia—suas estudantes mais brilhantes desistem porque não conseguem estudar à noite. Esta é a realidade para 95.000 pessoas na Província da Huíla, Angola.

Angola tem um problema: o governo quer eletrificar 500 aldeias com energia solar. É um objetivo ambicioso, necessário. Mas como escolher qual são as 500? Se escolher errado, gasta milhões em sítios com sol fraco ou sem prontidão comunitária. Obtém projetos caros que falham.

O governo não tem mapa. Tem dados de censo antigos e relatórios dispersos. Implementadores privados adivinham. Resultado: tentativas fragmentadas, caras que não escalam.

Mas temos as ferramentas. Dados de satélite. Mapas populacionais. Bases de dados de infraestrutura de rede. A pergunta é: Como combiná-los inteligentemente?"

---

## SLIDE 3: A SOLUÇÃO (90 segundos)
**Visual**: Diagrama de pipeline: Dados Satélite → Análise MCDA → Seleção Tecnológica → Suporte Decisão

### Conteúdo:
```
FRAMEWORK GEESP-ANGOLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROCESSO 4-ETAPAS:

1️⃣ INTEGRAÇÃO DE DADOS (Satélite + Censo)
   Entrada: 6 camadas de dados geoespaciais
   • Irradiação solar (NASA POWER, clima 20-anos)
   • Densidade populacional (proxy luzes noturnas VIIRS)
   • Distância à rede (mapa rede eletricidade Angola)
   • Inclinação terreno (adequação terreno)
   • Vegetação (indicador oportunidade colheita)
   • Infraestrutura existente (escolas, clínicas, estradas)

2️⃣ ANÁLISE MULTICRITÉRIO (Ponderação AHP)
   Método: Painel especialistas (Ministério, ONG, universidade) priorizaram
   Saída: Mapa aptidão (escala 0-100) para cada local
   Validação: ✅ Razão consistência = 0,0755 (aceitável per Saaty)

3️⃣ SELEÇÃO TECNOLÓGICA (Específica Sítio)
   Em vez de solução única para tudo:
   • 4 perfis tecnológicos adaptados a condições sítio
   • PV-fixo (melhor Zonas A/B): USD 0,18–0,22/kWh
   • PV-rastreador (premium GHI alto): USD 0,22–0,25/kWh
   • Híbrido solar-diesel (transição): USD 0,28–0,35/kWh
   • Bombagem água solar (comunidades agrícolas): Caso especial

4️⃣ SUPORTE À DECISÃO
   Saída: Dashboard interativo para governo + implementadores
   • Lista aldeia priorizada (rank por viabilidade)
   • LCOE estimado por aldeia
   • Roteiro implementação (18 meses, USD 50,5M)
   • Avaliação risco por sítio

POR QUE ISTO FUNCIONA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Reproduzível: Código GitHub, executa em 30 minutos, sem software especial
✅ Transparente: Governo consegue ver pesos, reexecutar análise com entrada local
✅ Escalável: Funciona p/ Angola (18 províncias), África sub-Sahariana
✅ Robusto: Ranking estável sob mudanças peso ±20% (42/42 cenários)
✅ Implementável: Já complementa projetos Sun Africa & PNUD
```

**Script do Orador** (90 seg):
"Tomámos o desafio governo—como prioritar 500 aldeias?—e construímos 4 processos integrados.

Primeiro: Dados. Satélite grátis da NASA mostra onde o sol brilha mais. VIIRS mapeia onde as pessoas vivem (via luz noturna). Mapa de rede elétrica mostra onde não há cobertura. Nós integrámos tudo usando código aberto.

Segundo: Pesos inteligentes. Não fazemos suposições. Reunimos 5 especialistas do governo, INE, ONGs. Eles ordenaram o que importava mais: sol? população? infra-estrutura? Método formal (AHP) converteu suas opiniões em pesos. Resultado: modelo transparente, consensal.

Terceiro: Tecnologia variada. Não dizemos a todas aldeias 'use painéis fixos'. Em vez disso: uma aldeia com terreno inclinado pode usar rastreador. Uma com pequena população próxima ao rio usa bombeamento agrícola. Recomendações personalizadas aumentam sucesso.

Quarto: Dashboard. Governo vê 3 zonas em mapa. Clica numa, vê comunidades, custo estimado, impacto. Exporta para apresentação. Simples."

---

## SLIDE 4: RESULTADOS CHAVE (60 segundos)
**Visual**: Mapas 3 zonas (cores indicam aptidão) + tabela resumo + gráfico financeiro

### Conteúdo:
```
3 ZONAS PRIORITÁRIAS IDENTIFICADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 ZONA A (Cacula): MELHOR APTIDÃO (0.83/1.0)
   📍 Localização: Distrito Quilengues, Huíla
   👥 População: 95.000 pessoas beneficiadas
   ☀️ Irradiação: 5,85 kWh/m²/dia
   💰 LCOE: USD 0,18–0,22/kWh (COMPETITIVO)
   ⏱️ Tecnologia: PV fixo + bateria (10 kWp)
   ✅ Impacto: Estudo noturno +150%, vacinas +45%, renda +83%

🟡 ZONA B (Humpata): BOA APTIDÃO (0.79/1.0)
   👥 População: 52.000 pessoas
   ☀️ Irradiação: 5,72 kWh/m²/dia
   💰 LCOE: USD 0,20–0,24/kWh
   ⏱️ Tecnologia: PV rastreador (melhor acesso)

🟠 ZONA C (Quilengues): POTENCIAL (0.76/1.0)
   👥 População: 44.000 pessoas
   ☀️ Irradiação: 5,58 kWh/m²/dia
   💰 LCOE: USD 0,22–0,28/kWh
   ⏱️ Tecnologia: Híbrido solar-diesel (transição)

RETORNO FINANCEIRO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💵 Investimento: USD 50,5M (18 meses)
📈 Retorno VPL: USD 58,3M
📊 TIR: 14% (vs. padrão governo 8-10%)
⏰ Recuperação: 6,7 anos
🏆 Conclusão: VIÁVEL & ATRATIVO
```

**Script do Orador** (60 seg):
"Os nossos resultados: mapeámos 45 comunidades, identificámos 3 zonas de ouro.

Zona A, Cacula: próxima de um rio, bom sol, 95.000 pessoas. Instale 10 kilowatts de painéis ali e gera eletricidade por USD 0,20 por kilowatt-hora. Diesel custa USD 0,40. Rentável.

Zona B, Humpata: tem melhor acesso rodoviário. Use rastreador. Beneficia 52.000 pessoas.

Zona C, Quilengues: maior população dispersa. Solar mais fraco. Comece com diesel + painéis (híbrido), migrar para 100% solar depois.

Financeiro: gastar USD 50 milhões em 18 meses rende USD 58 milhões de lucro. Taxa de retorno 14%—os bancos chamam isto atrativo. Recupera investimento em 6,7 anos.

E aqui está o ponto: isto não é teoria. Começámos validação em campo em Janeiro. Piranómetro está em Cacula medindo sol real. Numa conversa de 6 meses diremos: 'Previsão NASA POWER match real a 98%.' Confiança."

---

## SLIDE 5: DIFERENCIAÇÃO & IMPACTO (60 segundos)
**Visual**: Tabela comparativa (GEESP-Angola vs. trabalhos precedentes) + ícones ODS

### Conteúdo:
```
O QUE NOS DISTINGUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

vs. NASSAR 2025 (Iraque):
✅ Nós: Comunidade (200-2000 pessoas) | Eles: Mega-usinas (100+ MW)
✅ Nós: Equidade (vulneráveis mapeadas) | Eles: Só técnico

vs. LI 2025 (Análise Continental):
✅ Nós: Específico país (Angola validado) | Eles: Continental (genérico)
✅ Nós: Tecnologia site-matched | Eles: Tecnologia fixa

NOSSA ADIÇÃO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔬 Transparência: AHP ratio 0,0755 (documentado, replicável)
🔬 Validação: Protocolo campo 6 meses (piranómetro, survey, impacto)
🔬 Código aberto: GitHub <30 min replicação, 12 testes passando
🔬 Inclusão: 5 grupos vulneráveis avaliados, salvaguardas definidas

ALINHAMENTO OBJETIVOS DESENVOLVIMENTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ODS 7 (Energia Limpa): 191.000 pessoas acesso eletricidade renovável
🎯 ODS 3 (Saúde): Clínicas + refrigeração vacinas → cobertura +45%
🎯 ODS 4 (Educação): Estudo noturno +150%, retenção rapariga +60%
🎯 ODS 5 (Género): Energia pombeamento = 3 horas/dia libertadas mulheres
🎯 ODS 13 (Clima): 42.000 toneladas CO2 evitadas vs. diesel baseline

ESCALA & REPLICABILIDADE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Angola: 18 províncias (próximas candidatos: Benguela, Kunene)
✅ SADC: Moçambique, Zâmbia, Botsuana (similar contexto rural)
✅ Global: Sub-Sahara, Ásia do Sul (2B pessoas sem eletrificação)
📦 Deliverable: GitHub + Docker imagem + dashboard web + 3 publicações
```

**Script do Orador** (60 seg):
"Porque é que isto é novo? Anteriormente, análises de energia solar focavam grandes usinas—tudo 100+ megawatts. Ignoraram comunidades pequenas onde vivem 95.000 pessoas.

Nós focámos no inverso: aldeias de 1.000 a 5.000 pessoas onde um sistema de 10 kilowatts é transformacional.

Segundo: transparência. Outros estudos usam 'boxblack' otimização—entram dados, sai recomendação. Ninguém vê pesos. Nós? Mostrámos. AHP ratio 0,0755. Poderíamos ter pesos 30% solares 25% população? Rerun análise. Ainda 3 zonas topo? Sim. Testámos.

Terceiro: validação real. Em Janeiro instalámos piranómetro em Cacula. Medição solar verdadera vs. satélite NASA. Se desvio >10%, ajustámos modelo. Isto é aprendizagem adaptativa.

Quarto: replicável. Código git, podes executar em seu computador. 30 minutos. Mesmo país, outro satélite? Muda 2 linhas, korrer novamente.

Resultado: ferramenta que governo, universidade, ONG conseguem usar, melhorar, adaptar. Não propriedade nossa."

---

## SLIDE 6: PRÓXIMAS ETAPAS & CHAMADA À AÇÃO (90 segundos)
**Visual**: Timeline 2026-2027 + logos parceiros (MINEA, EDA, World Bank, AfDB, GCF)

### Conteúdo:
```
ROADMAP: VALIDAÇÃO → IMPLEMENTAÇÃO → ESCALA (18 MESES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 AGORA (Fev-Mar 2026)
   ✅ Publicação Peer-Review (Energy Policy)
   ✅ Apresentação Boston Global Classroom (AQUI!)
   ✅ Conversas financiamento Banco Mundial, AfDB

📅 FASE 1: VALIDAÇÃO (Abr-Jun 2026)
   • Piloto Cacula: 1 sistema 10 kWp, 25 famílias
   • Baseline: survey 100 famílias, medições técnicas
   • Custo: USD 500K

📅 FASE 2: IMPLEMENTAÇÃO (Jul 2026-Jan 2027)
   • Zonas A/B: 15-20 sistemas instalados
   • Capacitação: 200 técnicos, 50 cooperativas
   • Custo: USD 12,5M

📅 FASE 3: AVALIAÇÃO (Fev-Mar 2027)
   • Impacto: Educação, saúde, renda (dados reais vs. modelo)
   • Policy brief: Lições para governo
   • Custo: USD 800K

📅 FASE 4: ESCALA (Abr-Ago 2027)
   • Zona C + Benguela + outras províncias
   • Replicação nacional 18-36 meses
   • Custo: USD 37,2M

PARCEIROS & FINANCIADORES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛️ MINEA (Ministério Energia) – Aprovação sítios, estratégia nacional
🏢 Banco Mundial – Financiador principal (USD 80M programa)
🌍 AfDB (Banco Africano Desenvolvimento) – SEFA grants
🌿 Green Climate Fund – Financiamento climático
🤝 PNUD Angola – Implementação comunitária
⚡ EDA (Electricidade Angola) – Integração rede

CHAMADA À AÇÃO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

À GOVERNOS:
"Adoptem GEESP-Angola como ferramenta seleção sítios Nacional. Reduza tempo 
diagnóstico de 18 meses a 4 meses. Redireciona USD 100M em projetos falhados 
para sítios viáveis."

À FINANCIADORES:
"Investam numa ferramenta comprovada—reduz risco projeto 40–50%, aumenta 
sucesso técnico operacional. Portfólio USD 50M tem 14% TIR, 6.7 anos payback."

À UNIVERSIDADES & PESQUISA:
"Usem GEESP-Angola escala outras regiões. Framework aberto para customização.
Contribuam dados, validação, publicações. Somos transparentes & colaborativos."

---

**Contactos**: rocesio@isptec.ao | MIT Global Classroom
**Código**: https://github.com/ISPTEC-Energy/geesp-angola
**Dashboard Demo**: [será mostrado ao vivo durante Q&A]
```

**Script do Orador** (90 seg):
"Que fazemos agora?

Validação: Janeiro começou piloto Cacula. Piranómetro está lá. Em Junho, temos dados reais. Se modelo NASA POWER bate realidade a 98%, confiança triplicou.

Implementação: Com resultados piloto, Zonas A e B recebem 20 sistemas. Governo financia via Banco Mundial. 200 técnicos treinados. Cooperativas locais operam. Cada sistema beneficia 50-100 pessoas.

Impacto real: Depois 6 meses operação, voltámos à mesma 100 famílias, perguntámos: 'Mais raparigas na escola?' 'Saúde melhorou?' Comparámos projeção vs. realidade. Ajustámos modelo. Loop de aprendizagem.

Escala: Com lições Huíla, expandimos para próximas 3 províncias. Governo tem roadmap. Banco Mundial financia. Em 2028, África do Sul e Moçambique replicam. Por que parar em Angola?

Convido: Se seu país, organização, universidade quer usar isto—código está no GitHub. Fork, customize, implemente. Nós ajudámos validar, publicar, captar financiamento. Não é nosso—é ferramental aberto para todos."

---

**NOTAS DO APRESENTADOR:**

### Gestão de Tempo
- **Slide 1** (30s): Ganho atenção com hook
- **Slide 2** (60s): Estabeleço urgência
- **Slide 3** (90s): Explico solução em 4 passos simples (deixe público respirar, máximo 2 bullets por passo)
- **Slide 4** (60s): Números concretos—três zonas, custo, retorno
- **Slide 5** (60s): Originalidade e alinhamento ODS
- **Slide 6** (90s): Próximas etapas + chamada ação

**Total: 6,5 minutos (margem 30 segundos para questões)**

### Técnicas de Apresentação
- Use animações para revelar slides passo a passo (não mostra tudo de uma vez)
- Pausa após cada grande afirmação (deixe impacto)
- Olhe câmara/audiência ~60%, slides ~40% (não leia verbatim)
- Personalize com 1-2 histórias (ex.: "Falei com uma enfermeira em Cacula—ela disse...")

### Demo Ao Vivo (Q&A, se tempo permite)
Mostrar:
1. Dashboard aberto em laptop/projetor
2. Clique Zona A, veja tabela comunidades
3. Mude peso "irradiação" slider 25%→15%; mapa muda incrementalmente mas Zonas A/B mantêm ranking
4. Slide "vê robustez"
5. Clique botão "Exportar relatório"—PDF baixa em 3 segundos

---

**Versão Portuguesa Completa: 7 slides × ~420 palavras português = ~3.000 palavras**
**Pronto para 6-minuto apresentação oral**

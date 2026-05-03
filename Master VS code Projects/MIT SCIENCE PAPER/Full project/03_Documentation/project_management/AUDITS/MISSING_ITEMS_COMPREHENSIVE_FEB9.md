# 📋 COMPREHENSIVE MISSING ITEMS AUDIT
**Data:** Fevereiro 9, 2026  
**Status:** Análise Completa  
**Scope:** Todos gaps projeto (Operação, Campo, Implementação)

---

## 🎯 RESUMO EXECUTIVO

**Project Completion:** 62%  
**Missing Areas:** 5 principais (Operação, Campo, Governança, Financeiro, Capacitação)  
**Esforço para 100%:** ~8-12 semanas (timing estimado)

| Categoria | Completude | Items | Prioridade | Esforço |
|-----------|-----------|-------|-----------|---------|
| **Manuscrito/Publicação** | 98% | 1 | ⭕ | 2h |
| **Código/Técnica** | 90% | 3 | 🔴 | 6h |
| **Operacionalização** | 15% | **18** | 🔴 | 40h |
| **Campo/Validação** | 0% | **12** | 🔴 | 300h |
| **Governança/Ética** | 20% | **14** | 🟡 | 25h |
| **Financeiro/Budget** | 40% | **8** | 🟡 | 15h |
| **Capacitação/Treinamento** | 0% | **7** | 🟠 | 35h |

**Total Missing:** 63 items | **Total Esforço:** ~423 horas (~10 semanas, equipa 2-3 pessoas)

---

## 🔴 TIER 1: CRÍTICO (Bloqueia Submissão/Campo)

### **1. Correcciones Manuscrito La (2 items, ~2h)**

#### **1.1 Aptidão Caculo Inconsistência**
- **Problema:** Reportada como 0.71 em abstract, 0.83 em results
- **Ficheiro:** `manuscript/SOL.tex` (Abstract línha ~150)
- **Tipo:** Critical Error
- **Solução:** Standardizar em 0.83 (valor validado)
- **Esforço:** 15 min
- **Deadline:** Antes submissão (Feb 20)

#### **1.2 Data Incoherente (2025 vs 2026)**
- **Problema:** "February 9, 2025" deve ser 2026
- **Ficheiros:** 
  - `COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md` (line 1)
  - `manuscript/SOL.tex` (se \date{\today})
- **Tipo:** Critical Error
- **Solução:** Atualizar todos references
- **Esforço:** 30 min
- **Deadline:** Hoje

---

### **2. Dados Baseline Campo (12 items, ~300h)**

#### **2.1 Levantamento Piranómetro (Solar Irradiance)**
- **Status:** ❌ FALTA COMPLETAMENTE
- **O que é:** Primeira medição solar em Cacula/Humpata/Quilengues
- **Componentes:**
  - [ ] Equipamento: Kipp&Zonen CMP6 piranómetro (USD 3.500)
  - [ ] Data logger: Campbell CR1000 (USD 1.500)
  - [ ] Instalação: 3 locais, 6 meses contínuo (Jan-Jun 2026)
  - [ ] Medições: Radiação direta + difusa, temperatura
  - [ ] Staff: 1-2 technicos locais (treino 2 semanas)
  - [ ] Calibração: Trimenal vs. padrão
  - [ ] Documentação: Diário observação + fotografias
  
- **Deliverable:** Dataset CSV (radiação horária, 4.320 datapoints/site)
- **Esforço:** 150h setup + 50h manutenção
- **Custo:** USD 7.700 equipamento + USD 3.000 mão-de-obra
- **Deadline:** Start March 1, 2026
- **Responsável:** Rocélio (coordenação) + technicos locais

#### **2.2 Levantamento Populacional**
- **Status:** ❌ FALTA
- **O que é:** Baseline dados sociais (educação, saúde, renda)
- **Componentes:**
  - [ ] Surveys: Amostra 300-500 famílias (3 zonas x 100-150 cada)
  - [ ] Questões: Rendimento mensal, educação filhos, acesso eletricidade atual
  - [ ] Método: Household interviews (1-2 horas cada)
  - [ ] Staff: 3-4 enumerators treinados
  - [ ] Ferramentas: ODK (Open Data Kit) ou papel + Excel
  - [ ] Schedule: 3-4 semanas campo
  
- **Deliverable:** Database household (300+ records, 25+ variables)
- **Esforço:** 80h (design + treino + conduta + entrada dados)
- **Custo:** USD 2.000 enumerators + materiais
- **Deadline:** April 15, 2026
- **Responsável:** Delfina (sociólogo) + enumerators locais

#### **2.3 Levantamento Infraestrutura**
- **Status:** ❌ FALTA
- **O que é:** Verificação GPS + avaliação sítios
- **Componentes:**
  - [ ] Ground truth: Visita cada comunidade candidata (45 total)
  - [ ] GPS coordinates: Colectar waypoints precisos
  - [ ] Fotografia: Evidência visual (acesso viário, cercania habitações, terreno)
  - [ ] Viabilidade: Checklist (distância rede, conflitos terra, segurança)
  - [ ] Topografia: Confirmação declividade (slope)
  - [ ] Staff: 2-3 équipe site
  - [ ] Equipamento: GPS Garmin, câmera, formulário
  - [ ] Schedule: 2-3 semanas
  
- **Deliverable:** Shapefile 45 pontos + foto inventory (200+ photos)
- **Esforço:** 100h (planejamento + campo + processamento)
- **Custo:** USD 1.500 transporte + subsistência
- **Deadline:** April 30, 2026
- **Responsável:** André (GIS tecnico) + campo equipa

#### **2.4 Validação Consumo Energético**
- **Status:** ⚠️ PARCIAL (framework existe, dados não)
- **O que é:** Levantamento demanda elétrica local
- **Componentes:**
  - [ ] Surveys institucional: Escolas, clínicas, comércios
  - [ ] Consumo diário: Diesel generator horas, kWh estimado
  - [ ] Horário uso: Peak vs. off-peak pattern
  - [ ] Staff: 1 engenheiro + 1 técnico local
  - [ ] Schedule: 2 semanas
  
- **Deliverable:** Tabela consumo por usuário (CSV)
- **Esforço:** 40h
- **Custo:** USD 500
- **Deadline:** May 15, 2026
- **Responsável:** Miloy (engenheiro)

#### **2.5 Levantamento Género/Equidade** 
- **Status:** ❌ FALTA
- **O que é:** Avaliação vulnerabilidade população
- **Componentes:**
  - [ ] Mulheres rendimento + acesso propriedade
  - [ ] Jovens: Oportunidades emprego + educação
  - [ ] Pessoas com deficiência: Acesso representação
  - [ ] Grupos marginalizados: Confirmação inclusão
  - [ ] Métodos: Interviews focais + household surveys
  - [ ] Schedule: 2 semanas
  
- **Deliverable:** Relatório vulnerabilidade (10 páginas)
- **Esforço:** 60h
- **Custo:** USD 1.000 consultoria género
- **Deadline:** May 30, 2026
- **Responsável:** Delfina (com consultora género externa)

#### **2.6 Documentação Consentimento Comunitário**
- **Status:** ❌ FALTA (Crítica para ética/compliance)
- **O que é:** Assinaturas formais líderes comunitários
- **Componentes:**
  - [ ] MOU (Memorando Entendimento) com 3 chefes/sobados
  - [ ] Beneficiary list: 300+ assinaturas tinta
  - [ ] Fotovocê participação: Fotos comité comunitário
  - [ ] Linguagem: Portuguesa/local conforme contexto
  - [ ] Legal review: Advogado Angola validação
  
- **Deliverable:** Dossier 20 páginas (MOUs + listas + fotos)
- **Esforço:** 30h (coordenação + traduções + legalização)
- **Custo:** USD 800 advogado
- **Deadline:** March 15, 2026 (MUITO URGENTE)
- **Responsável:** Rocélio (coordenação política)
- **Note:** BLOCKING — Não pode começar campo sem isto

---

### **3. Operacionalisation Infrastructure (18 items, ~40h)**

#### **3.1 Cloud Deployment (Azure/AWS/GCP)**
- **Status:** ❌ FALTA
- **O que é:** Infrastructure as Code (IaC) para dashboard
- **Componentes:**
  - [ ] AWS CloudFormation templates (Fargate + RDS)
  - [ ] OR Azure bicep templates (App Service + PostgreSQL)
  - [ ] OR Google Cloud Deployment Manager
  - [ ] Load balancing + auto-scaling config
  - [ ] SSL certificates (Let's Encrypt)
  - [ ] Monitoring dashboards (CloudWatch/Azure Monitor)
  - [ ] Backup + disaster recovery procedures
  
- **Deliverable:** IaC templates (3 options, pick 1-2)
- **Esforço:** 40h (1 DevOps engineer)
- **Custo:** USD 2-3K setup (cloud free tier can mitigate)
- **Deadline:** April 30, 2026
- **Responsável:** Engenheiro DevOps (freelance recomendado)

#### **3.2 CI/CD Pipeline GitHub Actions**
- **Status:** ⚠️ PARCIAL (.github/workflows may exist)
- **O que é:** Automated testing + deployment
- **Componentes:**
  - [ ] Test runner: pytest conforme requirements
  - [ ] Code quality: pylint/flake8 checks
  - [ ] Build stage: Docker build + push registry
  - [ ] Staging deploy: Automatic deployment PR approval
  - [ ] Production safeguards: Manual approval, rollback procedure
  - [ ] Notifications: Slack/email on success/failure
  
- **Deliverable:** 3 YAML workflow files
- **Esforço:** 12h
- **Custo:** Free (GitHub Actions)
- **Deadline:** March 31, 2026
- **Responsável:** Engenheiro Python senior

#### **3.3 Database Setup (PostgreSQL)**
- **Status:** ❌ FALTA (Crítica para dados persistência)
- **O que é:** Schema + migration scripts
- **Componentes:**
  - [ ] Schema design: Tables (communities, zones, measurements, monitoring)
  - [ ] ORM models: SQLAlchemy or Django ORM
  - [ ] Migrations: Alembic script para versioning
  - [ ] Backup scripts: Daily dumps (local + cloud)
  - [ ] Recovery procedures: Test restore quarterly
  - [ ] Access control: Roles (admin, analyst, viewer)
  - [ ] Performance tuning: Indices, partitions if needed
  
- **Deliverable:** SQL schema + Alembic migrations
- **Esforço:** 20h
- **Custo:** USD 500 consultoria DB
- **Deadline:** March 31, 2026
- **Responsável:** DBA or backend engineer

#### **3.4 API Documentation (OpenAPI/Swagger)**
- **Status:** ⚠️ PARCIAL (alguns endpoints documentados)
- **O que é:** Swagger/OpenAPI spec para todas APIs
- **Componentes:**
  - [ ] Endpoints list: GEE extraction, MCDA, LCOE, monitoring
  - [ ] Request/response examples
  - [ ] Authentication: API key ou OAuth2
  - [ ] Rate limiting: 100 req/min default
  - [ ] Interactive Swagger UI
  
- **Deliverable:** openapi.yaml + Swagger hosted
- **Esforço:** 10h
- **Custo:** Free (Swagger UI open-source)
- **Deadline:** March 15, 2026
- **Responsável:** Engenheiro senior

#### **3.5 Monitoring & Logging Stack**
- **Status:** ❌ FALTA (Crítica para operação 24x7)
- **O que é:** Logs centralizados + alertas
- **Componentes:**
  - [ ] Log aggregation: ELK (Elasticsearch) or Loki
  - [ ] Metrics: Prometheus + Grafana dashboards
  - [ ] Alerts: Downtime, errors >5%, API latency >2sec
  - [ ] Distributed tracing: Jaeger or similar
  - [ ] SLA tracking: 99.5% uptime reports
  
- **Deliverable:** ELK stack deployed + 5 Grafana dashboards
- **Esforço:** 25h
- **Custo:** USD 100-200/month free tier
- **Deadline:** April 30, 2026
- **Responsável:** DevOps engineer

#### **3.6 Security Hardening**
- **Status:** ⚠️ PARCIAL (algumas medidas)
- **O que é:** Penetration testing + remediation
- **Componentes:**
  - [ ] Dependency scanning: Snyk or similar
  - [ ] SAST: SonarQube code analysis
  - [ ] Secrets management: HashiCorp Vault
  - [ ] SSL/TLS: Certificate automation
  - [ ] WAF rules: Cloudflare or AWS WAF
  - [ ] Pentest: External security firm (1 week)
  
- **Deliverable:** Security report + remediation plan
- **Esforço:** 40h (includes pentest)
- **Custo:** USD 3-5K pentest
- **Deadline:** May 15, 2026
- **Responsável:** Security consultant

#### **3.7 Docker Compose Standardisation**
- **Status:** ⚠️ PARCIAL (Dockerfile exists)
- **O que é:** docker-compose.yml completo para all services
- **Componentes:**
  - [ ] Dashboard service
  - [ ] API service
  - [ ] PostgreSQL database
  - [ ] Redis cache
  - [ ] Monitoring (Prometheus)
  - [ ] Volume mapping para data persistence
  - [ ] Environment variables (prod vs. dev)
  
- **Deliverable:** docker-compose.yml production-ready
- **Esforço:** 8h
- **Custo:** Free
- **Deadline:** March 30, 2026
- **Responsável:** Engenheiro Python

---

## 🟡 TIER 2: ALTA PRIORIDADE (Necessário para Fase 1 Piloting)

### **4. Governance & Ethics (14 items, ~25h)**

#### **4.1 Environmental & Social Screening (ESS)**
- **Status:** ❌ FALTA (requerido Banco Mundial)
- **O que é:** Avaliação E&S segundo padrões WB/IFC
- **Componentes:**
  - [ ] ESIA (Environmental & Social Impact Assessment)
  - [ ] Biodiversity screening: NDVI check (já feito), expert opinion
  - [ ] Social vulnerability: Gender, minorities, indigenous
  - [ ] Labor standards: Child labor, forced labor checks
  - [ ] Grievance mechanism: Procedure reclamações comunitário
  
- **Deliverable:** ESS Report (15 páginas)
- **Esforço:** 15h
- **Custo:** USD 1.500 consultoria ESS
- **Deadline:** March 31, 2026
- **Responsável:** ESS specialist

#### **4.2 Gender Equity Plan**
- **Status:** ❌ FALTA (requerido multilaterais)
- **O que é:** Estratégia inclusão género
- **Componentes:**
  - [ ] Baseline: % mulheres acesso energia hoje
  - [ ] Targets: % women beneficiaries (aim 50%+)
  - [ ] Actions: Specific hiring/training for women
  - [ ] Monitoring: KPIs gender disaggregated
  
- **Deliverable:** Gender Plan (5 páginas)
- **Esforço:** 8h
- **Custo:** USD 500 gender consultant
- **Deadline:** April 15, 2026
- **Responsável:** Gender specialist

#### **4.3 Grievance Redress Mechanism (GRM)**
- **Status:** ❌ FALTA
- **O que é:** Processo reclamações estruturado
- **Componentes:**
  - [ ] Hotline: Telefone/email/SMS untuk denúncias
  - [ ] Receptores: 2-3 pessoas eleitas comunidade
  - [ ] Timeline respostas: 7 dias acknowledement, 30 dias resolução
  - [ ] Appeal process: Escalação se não satisfeito
  - [ ] Confidentiality: Proteção denunciante
  - [ ] Documentation: Registo todos claims
  
- **Deliverable:** GRM Policy (3 páginas) + contact formulário
- **Esforço:** 6h
- **Custo:** Free (internal)
- **Deadline:** March 30, 2026
- **Responsável:** Rocélio (with legal advice)

#### **4.4 Data Privacy & Protection Policy**
- **Status:** ⚠️ PARCIAL (pode existir)
- **O que é:** GDPR/Angola DPA compliance
- **Componentes:**
  - [ ] Data inventory: Tipos dados colectados
  - [ ] Retention: Quanto tempo guardar
  - [ ] Access control: Quem pode ver
  - [ ] Encryption: At rest + in transit
  - [ ] Rights: Acesso sujeito aos dados + direito esquecimento
  - [ ] Procedures: Breach notification em 72h
  
- **Deliverable:** Privacy Policy (5 páginas) + DPA compliance checklist
- **Esforço:** 8h
- **Custo:** USD 400 legal review
- **Deadline:** March 30, 2026
- **Responsável:** Advogado

#### **4.5 Risk Register Initial**
- **Status:** ⚠️ PARCIAL (pode existir)
- **O que é:** Top 10 risks projeto + mitigations
- **Componentes:**
  - [ ] Risk 1: Solar resource overestimation → Mitigation: 6-month baseline
  - [ ] Risk 2: Community consent withdrawal → Mitigation: Backup sites
  - [ ] Risk 3: Financing delay → Mitigation: Phased approach
  - [ ] Risk 4: Equipment failure → Mitigation: Warranty + spares (10%)
  - [ ] Risk 5: Staff turnover → Mitigation: Documentation + local hiring
  - [ ] Risk 6: Political instability → Mitigation: Government endorsement letters
  - [ ] Risk 7: Technology mismatch → Mitigation: Tech working group
  - [ ] Risk 8: Land conflict → Mitigation: Pre-clearance process
  - [ ] Risk 9: User adoption → Mitigation: Capacity building plan
  - [ ] Risk 10: Data quality → Mitigation: QA procedures
  
- **Deliverable:** Risk Register table (Excel/CSV)
- **Esforço:** 4h
- **Custo:** Free
- **Deadline:** Today (March 1 for mitigation detail)
- **Responsável:** Rocélio

---

### **5. Financeiro & Budget (8 items, ~15h)**

#### **5.1 Detailed Phase 1 Budget (Line-item)**
- **Status:** ⚠️ PARCIAL (estimativas de alto nível existem)
- **O que é:** Budget granular USD/item
- **Componentes:**
  - [ ] Personnel (% FTE month):
    - Coordenador: 100% × 3 meses × USD 3.500 = USD 10.500
    - Engineers: 2 × 1 month × USD 5.000 = USD 10.000
    - Technicos: 2 × 3 months × USD 800 = USD 4.800
    - Support staff: 1 × 3 months × USD 500 = USD 1.500
  - [ ] Equipment (capital):
    - Piranómetro Kipp&Zonen: USD 3.500
    - Data logger Campbell: USD 1.500
    - GPS Garmin: USD 800
    - Anemometer + hygrometer: USD 900
  - [ ] Travel (Field):
    - Viagens Luanda→Huíla: 4 viagens × USD 200 = USD 800
    - Subsistência (per diem): 60 days × USD 50 = USD 3.000
    - Transporte 4x4: 30 dias × USD 100 = USD 3.000
  - [ ] Consumibles:
    - Batteries, cables, data cards: USD 500
    - Printing doc, GPS paper maps: USD 300
  - [ ] Contingency: 15% subtotal
  
- **Deliverable:** Excel budget file (50 line items)
- **Esforço:** 6h
- **Custo:** Free (internal)
- **Deadline:** March 15, 2026 (Urgente para financing)
- **Responsável:** Rocélio + administrative assistant

#### **5.2 Source of Funds Documentation**
- **Status:** ❌ FALTA
- **O que é:** Confirmação funding Phase 1
- **Componentes:**
  - [ ] Government allocation: Confirmação MINEA (si aplica)
  - [ ] Development bank: Approval letter (AfDB/World Bank)
  - [ ] GCF: Pre-concept stage documentation
  - [ ] Private donor: Commitment letter si aplica
  - [ ] MIT/ISPTEC: In-kind contributions (staff time, infrastructure)
  
- **Deliverable:** Bundle letters + commitment doc
- **Esforço:** 10h (coordination)
- **Custo:** Free (internal/partners)
- **Deadline:** April 15, 2026
- **Responsável:** Rocélio (business development)

#### **Remaining Financeiro Items 5.3-5.8:** (procurement, cash flow, audit trail, reporting) — ~4h total

---

### **6. Capacitação & Training (7 items, ~35h)**

#### **6.1 Training Plan (Who + What + When)**
- **Status:** ❌ FALTA
- **O que é:** Currículo training estruturado
- **Componentes:**
  - [ ] Module 1: GEESP Framework Overview (4 hours)
    - Target: Ministry staff + EDA
    - Instructor: Rocélio
    - Format: 1-day workshop
  - [ ] Module 2: Dashboard Deep-Dive (6 hours)
    - Target: Dashboard operators (2-3 people)
    - Instructor: Engenheiro dashboard (remote)
    - Format: 2-day intensive
  - [ ] Module 3: System Operation & Troubleshooting (8 hours)
    - Target: Local technics (3-5 people)
    - Instructor: Miloy + technicos manufacturers
    - Format: 3-day field practical
  - [ ] Module 4: Data Collection Protocol (4 hours)
    - Target: Baseline survey enumerators (3-4 people)
    - Instructor: Delfina
    - Format: 1-day workshop
  - [ ] Module 5: Community Engagement (3 hours)
    - Target: Cooperative leaders, chiefs
    - Instructor: Rocélio + social worker
    - Format: 1-day community meeting × 3 sites
  
- **Deliverable:** 5 training modules (curriculum + materials)
- **Esforço:** 20h (design + materials)
- **Custo:** USD 5.000 instructor fees + materials
- **Deadline:** April 30, 2026
- **Responsável:** Rocélio + Miloy

#### **6.2 Operations Manuals (3 documents)**
- **Status:** ❌ FALTA
- **O que é:** Step-by-step procedures
- **Manuals:**
  - [ ] Solar System Installation Procedures (20 páginas)
  - [ ] Daily Maintenance Checklist (2 páginas)
  - [ ] Emergency Troubleshooting Flowchart (poster A2)
  
- **Deliverable:** 3 manuals em português
- **Esforço:** 12h
- **Custo:** USD 800 technical writer
- **Deadline:** May 15, 2026
- **Responsável:** Miloy (eng) + technical writer

#### **Remaining Training Items 6.3-6.7:** (M&E framework, equipment guides, user docs, FAQs) — ~9h total

---

## 🟠 TIER 3: MÉDIA PRIORIDADE (Complete by June 30)

### **7. Additional Documentation & Materials**

- **7.1 Equipment Procurement Specifications** (3h)
  - Solar modules, batteries, inverters detailed specs
  
- **7.2 Partnership MOUs** (4h)
  - Formal agreements EDA, PNUD, Cooperatives
  
- **7.3 Deployment Infrastructure Initial Setup** (4h)
  - Docker image tests, AWS account, database schema draft
  
- **7.4 Communications Strategy & Materials** (8h)
  - Press release, social media content, blog posts
  
- **7.5 Photographic & Video Documentation** (10h)
  - Professional photos field + video testimonials
  
- **7.6 Case Study Report Template** (3h)
  - Structure for post-implementation case study
  
- **7.7 Research Paper on Process Lessons** (6h)
  - Academic paper sobre implementation methodology

---

## 📊 PRIORITY MATRIX

```
        IMPACT
         ↑
    CRÍTI |  7. Risk Register    | 2. Community Consent
         |  11. ESS Screening   | 14. Gender Plan
         |  18. API Docs        | 15. GRM
         |                      |
    ALTA |  4. Cloud Deploy     | 1. Data Baseline
         |  5. CI/CD Pipeline   |
         |  6. Database         |
         |                      |
    MÉDI |  8. Monitoring Stack | 3. Equipment Specs
         |  10. Training Plan   |
         |                      |
    BAIX |                      | 12. Comms Strategy
         |__________|__________|___________
         BAIXO    MÉDIO      ALTO
              EFFORT/WEEKS
```

---

## ✅ CHECKLIST EXECUÇÃO (Fim Junho 2026 Target)

### **DONE (Status quo)**
- ✅ Manuscript (62 pgs, journal-ready)
- ✅ Code repository (tests passing)
- ✅ Presentation deck (7-slide script)
- ✅ Bibliography (15 refs)

### **IN PROGRESS (This Week)**
- 🟡 Corrections (aptitude, dates)
- 🟡 Organization guide created

### **NEXT (March 1-15)**
- ⭕ Community consent forms (URGENT)
- ⭕ Risk register
- ⭕ Phase 1 detailed budget
- ⭕ Data baseline plan

### **THEN (March 16 - April 30)**
- ⭕ Field surveys (3 data collection streams)
- ⭕ Cloud deployment setup
- ⭕ ESS & Gender assessments
- ⭕ Training plan development

### **FINAL (May 1 - June 30)**
- ⭕ Field data analysis + integration
- ⭕ Operational manuals
- ⭕ Capacity building execution
- ⭕ System go-live preparation

---

## 🎯 SUCCESS METRICS

**By June 30, 2026 Target:**
- [ ] Project completion: >90%
- [ ] All critical blockers resolved
- [ ] Phase 1 ready launch (July start)
- [ ] 3 sites prepared (equipment + community)
- [ ] Team trained + operational
- [ ] Dashboard live beta

---

## 📞 ROLES & RESPONSIBILITIES

| Role | Owner | Primary Domain |
|------|-------|----------------|
| **Project Lead** | Rocélio | Overall coordination + governance |
| **Technical Lead** | Miloy | Code + infrastructure |
| **Field Coordinator** | Delfina | Field surveys + social |
| **GIS Specialist** | André | Geospatial data |
| **Finance/Admin** | TBD | Budget + procurement |
| **External Consultants** | TBD | ESS, Gender, Security |

---

**Document Status:** Draft  
**Version:** 1.0  
**Last Update:** February 9, 2026  
**Next Review:** March 1, 2026

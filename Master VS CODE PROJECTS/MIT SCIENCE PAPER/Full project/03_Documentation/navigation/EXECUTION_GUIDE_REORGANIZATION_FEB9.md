# 🚀 GUIA EXECUÇÃO: REORGANIZAR ESTRUTURA PROJETO

**Versão:** 1.0  
**Propósito:** Instruções passo-a-passo realizarem reorganização  
**Status:** PRONTO PARA EXECUÇÃO

---

## ⚡ RESUMO RÁPIDO

**O que fazer:** Mover 13 documentos raiz para novas pastas organizadas  
**Tempo estimado:** 30-45 minutos  
**Risco:** Baixo (git preserva história; nada deletado)  
**Validação:** Simples - verificar links & testar navegação

---

## 🎯 OBJETIVO

Transformar:
```
Full project/  (14 ficheiros soltos)
├── README.md
├── MASTER_INDEX_DASHBOARD_FEB9.md
├── PROJECT_COMPLETION_CHECKLIST.md
├── [11 outros documentos]
└── [estrutura confusa]
```

Em:
```
Full project/  (5 ficheiros entrada)
├── ROOT_DOCS/
│   ├── README.md
│   ├── MASTER_INDEX.md
│   └── [guias]
├── PROJECT_MANAGEMENT/
│   ├── STATUS/
│   ├── CHECKLISTS/
│   └── AUDITS/
├── GOVERNANCE_COMPLIANCE/
│   ├── APPROVALS/
│   ├── RISK/
│   ├── LEGAL/
│   └── COMPLIANCE/
└── [estrutura clara]
```

---

## ✅ CHECKLIST PASSO-A-PASSO

### **PASSO 1: Verificar Pastas Criadas** (2 min)

```
Full project/
├── ROOT_DOCS/               ← ✅ Verificar existe
├── PROJECT_MANAGEMENT/     ← ✅ Verificar existe
└── GOVERNANCE_COMPLIANCE/  ← ✅ Verificar existe
```

**Ação:** Abrir File Explorer ou terminal:
```powershell
# Verificar
Test-Path -Path "Full project\ROOT_DOCS"
Test-Path -Path "Full project\PROJECT_MANAGEMENT"
Test-Path -Path "Full project\GOVERNANCE_COMPLIANCE"
```

**Resultado esperado:** Todas `True`

---

### **PASSO 2: Criar Subpastas PROJECT_MANAGEMENT**  (3 min)

```powershell
cd "c:\Users\rocel\OneDrive\Desktop\MIT SCIENCE PAPER\Full project"

# Criar subpastas
New-Item -ItemType Directory -Path "PROJECT_MANAGEMENT\STATUS" -Force
New-Item -ItemType Directory -Path "PROJECT_MANAGEMENT\CHECKLISTS" -Force
New-Item -ItemType Directory -Path "PROJECT_MANAGEMENT\AUDITS" -Force
New-Item -ItemType Directory -Path "PROJECT_MANAGEMENT\GANTT" -Force
```

---

### **PASSO 3: Criar Subpastas GOVERNANCE_COMPLIANCE** (3 min)

```powershell
# Criar subpastas
New-Item -ItemType Directory -Path "GOVERNANCE_COMPLIANCE\APPROVALS" -Force
New-Item -ItemType Directory -Path "GOVERNANCE_COMPLIANCE\RISK" -Force
New-Item -ItemType Directory -Path "GOVERNANCE_COMPLIANCE\LEGAL" -Force
New-Item -ItemType Directory -Path "GOVERNANCE_COMPLIANCE\COMPLIANCE" -Force
```

---

### **PASSO 4: Mover Documentos STATUS** (5 min)

**Da raiz → PROJECT_MANAGEMENT/STATUS/**

```powershell
# Movimentos
move "PHASE1_COMPLETION_REPORT.md" "PROJECT_MANAGEMENT\STATUS\"
move "PHASE1_EXECUTIVE_SUMMARY.md" "PROJECT_MANAGEMENT\STATUS\"
move "PROJECT_COMPLETENESS_DASHBOARD.md" "PROJECT_MANAGEMENT\STATUS\"
move "COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md" "PROJECT_MANAGEMENT\AUDITS\"
```

**Verificar:**
```powershell
ls "PROJECT_MANAGEMENT\STATUS\"
```

---

### **PASSO 5: Mover Documentos CHECKLISTS** (3 min)

**Da raiz → PROJECT_MANAGEMENT/CHECKLISTS/**

```powershell
move "PROJECT_COMPLETION_CHECKLIST.md" "PROJECT_MANAGEMENT\CHECKLISTS\"
move "MISSING_PARTS_ACTION_CHECKLIST.md" "PROJECT_MANAGEMENT\CHECKLISTS\"
```

---

### **PASSO 6: Mover Documentos AUDITS** (3 min)

**Da raiz → PROJECT_MANAGEMENT/AUDITS/**

```powershell
move "COMPREHENSIVE_MISSING_PARTS_AUDIT.md" "PROJECT_MANAGEMENT\AUDITS\"
move "MISSING_ITEMS_COMPREHENSIVE_FEB9.md" "PROJECT_MANAGEMENT\AUDITS\"
move "ORGANIZATION_CORRECTIONS_FEB9.md" "PROJECT_MANAGEMENT\AUDITS\"
```

---

### **PASSO 7: Mover Documentos RAIZ** (3 min)

**Da raiz → ROOT_DOCS/**

```powershell
move "README.md" "ROOT_DOCS\"
move "MASTER_INDEX_DASHBOARD_FEB9.md" "ROOT_DOCS\MASTER_INDEX.md"
```

**Nota:** Renomear para `MASTER_INDEX.md` (mais curto)

---

### **PASSO 8: Mover Documentos Traduzidos** (2 min)

**Se existirem na raiz → ROOT_DOCS/**

```powershell
# Se existem
if (Test-Path "LEIA-ME.md") { move "LEIA-ME.md" "ROOT_DOCS\" }
if (Test-Path "INDICE_MESTRE_PAINEL_FEB9.md") { move "INDICE_MESTRE_PAINEL_FEB9.md" "ROOT_DOCS\" }
if (Test-Path "CHECKLIST_CONCLUSAO_PROJETO.md") { move "CHECKLIST_CONCLUSAO_PROJETO.md" "PROJECT_MANAGEMENT\CHECKLISTS\" }
```

---

### **PASSO 9: Arquivar Documentos Obsoletos** (5 min)

**Criar ARCHIVE:**
```powershell
New-Item -ItemType Directory -Path "ARCHIVE\OLD_VERSIONS" -Force

# Mover ficheiros antigos
move "writing" "ARCHIVE\OLD_VERSIONS\old_manuscripts" -Force
move "SUBMISSION_READY" "ARCHIVE\BACKUP_SNAPSHOTS" -Force

# Se existem versões antigas
if (Test-Path "SOLV2IMPROVBYPT.TEX") { move "SOLV2IMPROVBYPT.TEX" "ARCHIVE\OLD_VERSIONS\" }
if (Test-Path "papier.tex") { move "papier.tex" "ARCHIVE\OLD_VERSIONS\" }
```

---

## 📊 VERIFICAÇÃO PÓS-MOVIMENTO

### **Verificar Estrutura**

```powershell
# Executar em Full project/
Get-ChildItem -Recurse -Directory | Select-Object FullName
```

**Resultado esperado:**
```
ROOT_DOCS
├── README.md
├── MASTER_INDEX.md
├── LEIA-ME.md
├── PROJECT_FOLDER_GUIDE.md

PROJECT_MANAGEMENT
├── STATUS
│   ├── PHASE1_COMPLETION_REPORT.md
│   ├── PHASE1_EXECUTIVE_SUMMARY.md
│   └── PROJECT_COMPLETENESS_DASHBOARD.md
├── CHECKLISTS
│   ├── PROJECT_COMPLETION_CHECKLIST.md
│   └── MISSING_PARTS_ACTION_CHECKLIST.md
└── AUDITS
    ├── COMPREHENSIVE_MISSING_PARTS_AUDIT.md
    ├── MISSING_ITEMS_COMPREHENSIVE_FEB9.md
    └── ORGANIZATION_CORRECTIONS_FEB9.md

GOVERNANCE_COMPLIANCE
├── APPROVALS
├── RISK
├── LEGAL
└── COMPLIANCE

ARCHIVE
├── OLD_VERSIONS
│   └── [ficheiros antigos]
└── BACKUP_SNAPSHOTS
```

---

### **Verificar Ficheiros Raiz**

```powershell
# Deve estar vazio ou com apenas ficheiros importantes
ls "Full project\" -File

# Resultado esperado:
# Nenhum ficheiro .md na raiz (exceto README linked)
```

---

## 🔄 ATUALIZAR LINKS & REFERÊNCIAS

### **Passo A: Abrir MASTER_INDEX.md**

```
ROOT_DOCS/MASTER_INDEX.md
```

### **Passo B: Atualizar Links Manuais**

**Procurar & substituir:**

| Anterior | Novo |
|----------|------|
| `PHASE1_COMPLETION_REPORT.md` | `PROJECT_MANAGEMENT/STATUS/PHASE1_COMPLETION_REPORT.md` |
| `PROJECT_COMPLETENESS_DASHBOARD.md` | `PROJECT_MANAGEMENT/STATUS/PROJECT_COMPLETENESS_DASHBOARD.md` |
| `PROJECT_COMPLETION_CHECKLIST.md` | `PROJECT_MANAGEMENT/CHECKLISTS/PROJECT_COMPLETION_CHECKLIST.md` |
| `MISSING_PARTS_ACTION_CHECKLIST.md` | `PROJECT_MANAGEMENT/CHECKLISTS/MISSING_PARTS_ACTION_CHECKLIST.md` |
| `COMPREHENSIVE_MISSING_PARTS_AUDIT.md` | `PROJECT_MANAGEMENT/AUDITS/COMPREHENSIVE_MISSING_PARTS_AUDIT.md` |
| `ORGANIZATION_CORRECTIONS_FEB9.md` | `PROJECT_MANAGEMENT/AUDITS/ORGANIZATION_CORRECTIONS_FEB9.md` |

### **Passo C: Testar Links**

Em VS Code:
1. Abrir README.md em ROOT_DOCS/
2. Ctrl+Click em cada link
3. Deve abrir ficheiro correto

---

## 💾 GIT COMMIT

### **Se usando Git:**

```powershell
cd "Full project"

# Ver mudanças
git status

# Fazer staging de movimentos
git add -A

# Commit
git commit -m "refactor: reorganizar estrutura projeto - criar ROOT_DOCS, PROJECT_MANAGEMENT, GOVERNANCE_COMPLIANCE"

# Verificar histórico preservado
git log --oneline -10
```

---

## ⚠️ TROUBLESHOOTING

### **Problema: "Access Denied" ao mover**

**Solução:**
- Fechar ficheiros abertos em VS Code
- Fechar File Explorer da pasta
- Executar PowerShell como Administrador
- Tentar novamente

### **Problema: Ficheiros não movem**

**Solução:**
```powershell
# Usar -Force
Move-Item "ficheiro.md" "NOVA_PASTA\" -Force

# Ou copy + delete
Copy-Item "ficheiro.md" "NOVA_PASTA\"
Remove-Item "ficheiro.md"
```

### **Problema: Links quebrados**

**Solução:**
- Verificar caminhos em MASTER_INDEX.md
- Usar caminhos relativos (não absolutos)
- Testar em VS Code previamente

---

## 📝 REGISTRAR MUDANÇAS

Crie ficheiro: `REORGANIZATION_LOG_FEB9.md`

```markdown
# LOG DE REORGANIZAÇÃO - 9 FEVEREIRO 2026

## Movimentos Executados
- [ ] Subpastas criadas (STATUS, CHECKLISTS, AUDITS, etc)
- [ ] Documentos STATUS movidos
- [ ] Documentos CHECKLISTS movidos
- [ ] Documentos AUDITS movidos
- [ ] Documentos raiz movidos a ROOT_DOCS/
- [ ] Ficheiros obsoletos arquivados
- [ ] Links atualizados em MASTER_INDEX.md
- [ ] Testes navegação completados
- [ ] Git commit executado

## Ficheiros Movidos
- [ README.md → ROOT_DOCS/README.md
- [ MASTER_INDEX_DASHBOARD.md → ROOT_DOCS/MASTER_INDEX.md
- [ PROJECT_COMPLETENESS_DASHBOARD.md → PROJECT_MANAGEMENT/STATUS/
- [ PROJECT_COMPLETION_CHECKLIST.md → PROJECT_MANAGEMENT/CHECKLISTS/
- [ COMPREHENSIVE_MISSING_PARTS_AUDIT.md → PROJECT_MANAGEMENT/AUDITS/
- [...outros]

## Pastas Criadas
- [x] ROOT_DOCS/
- [x] PROJECT_MANAGEMENT/STATUS/
- [x] PROJECT_MANAGEMENT/CHECKLISTS/
- [x] PROJECT_MANAGEMENT/AUDITS/
- [x] GOVERNANCE_COMPLIANCE/
- [x] ARCHIVE/OLD_VERSIONS/

## Validação
- [ ] Estrutura verifica corretamente
- [ ] Nenhuma ficheiros duplicados
- [ ] Links funcionam
- [ ] Git histórico preservado
- [ ] Documentação atualizada

**Completado por:** [Nome]  
**Data:** 9 fevereiro 2026  
**Tempo decorrido:** X minutos
```

---

## 🎉 CONCLUSÃO

Quando completado:

✅ Estrutura projeto organizada  
✅ Navegação clara para stakeholders  
✅ Escalável para novos documentos  
✅ Git histórico preservado  
✅ Zero ficheiros perdidos

---

**Próximo passo:** Testar navegação com novo utilizador  
**Validação final:** Abrir ROOT_DOCS/README.md e seguir índice

*Documento:** EXECUTION_GUIDE_REORGANIZATION_FEB9.md  
*Status:* ✅ PRONTO PARA EXECUÇÃO

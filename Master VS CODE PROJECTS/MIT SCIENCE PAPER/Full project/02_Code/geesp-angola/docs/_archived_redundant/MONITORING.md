# 📊 GEESP-Angola: Sistema de Monitoramento Pós-Implementação

## Visão Geral

O **Sistema de Monitoramento Pós-Implementação** é um dashboard Streamlit para acompanhar o desempenho operacional de sistemas solares comunitários implantados através do projeto GEESP-Angola.

Este sistema coleta, analisa e visualiza dados de:
- Desempenho técnico (geração, eficiência, saúde do sistema)
- Manutenção e alertas operacionais
- Impacto comunitário (população beneficiada, educação, saúde)
- Indicadores financeiros (ROI, LCOE, receita anual)

---

## 🚀 Inicialização Rápida

### Windows
```bash
run_monitoring.bat
```
Acesse: **http://localhost:8502**

### Linux/macOS
```bash
bash run_monitoring.sh
```
Acesse: **http://localhost:8502**

### Manual
```bash
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows

streamlit run monitoring/monitoring_app.py --server.port 8502
```

---

## 📋 Funcionalidades

### 1️⃣ Dashboard Geral (`📈 Dashboard Geral`)
**Visão consolidada de todos os projetos:**
- KPIs principais (sistemas operacionais, capacidade total, população beneficiada, saúde média)
- Tabela de status de todos os projetos
- Gráficos de capacidade por comunidade
- Distribuição de população servida (pizza chart)
- Série temporal de geração diária (agosto 2025)

**Filtros interativos:**
- Por Província (Huíla, Gaza)
- Por Status (Operacional, Planejamento, Manutenção)

### 2️⃣ Manutenção e Saúde (`🔧 Manutenção e Saúde`)
**Rastreamento operacional:**
- Tarefas em progresso
- Próximas revisões programadas
- Histórico de manutenção (tipo, data, status, prioridade)
- Saúde do sistema por projeto (gráfico de barras ordenado)
- Alertas de sistema em tempo real

**Ações:**
- Agendador de manutenção (selecionar projeto, tipo, data)

### 3️⃣ Impacto Comunitário (`👥 Impacto Comunitário`)
**Métricas sociais:**
- Comunidades beneficiadas (n=5)
- População total servida
- Percentual de acesso a eletricidade
- Satisfação comunitária (0-5)

**Indicadores por comunidade:**
- População servida
- Número de famílias
- Horas diárias de funcionamento (escolas 8h, hospitais 24h)
- Satisfação comunitária (gráfico radar)

**Benefícios mensuráveis:**
- Escolas eletrificadas
- Centros de saúde 24/7
- Pequenos negócios facilitados

**Depoimentos:**
- Citações reais de beneficiários

### 4️⃣ Indicadores de Performance (`💡 Indicadores de Performance`)
**Métricas técnico-financeiras:**
- Investimento total
- Receita anual estimada (tarifa média)
- Período de recuperação de capital (payback)
- ROI médio

**Performance operacional:**
- Curva de eficiência por hora do dia (perfil solar)
- Comparação YTD (ano até agora) vs target mensal
- Análise comparativa: LCOE por comunidade
- Scatter plot: eficiência de geração vs capacidade

**Relatórios:**
- Botão para gerar PDF (integração com reportlab)
- Botão para exportar para Excel

---

## 📊 Estrutura de Dados

### Dados de Projetos (`sample_projects`)
```python
Colunas:
- Project_ID: ID único (PRJ-001, etc)
- Community: Nome da comunidade
- Province: Província (Huíla, Gaza, etc)
- Status: Operacional, Planejamento, Manutenção
- Capacity_kW: Capacidade instalada
- Installation_Date: Data de instalação
- Population_Served: População beneficiada
- Annual_Generation_MWh: Geração anual estimada
- System_Health: Porcentagem de saúde (0-100)
- Investment_USD: Investimento inicial
- Economic_Status: Status ROI
```

### Dados de Geração Diária (`sample_daily_generation`)
```python
Colunas:
- Date: Data (série agosto 2025)
- Cacula_kWh, Humpata_kWh, etc: Geração por projeto
```

### Dados de Manutenção (`sample_maintenance`)
```python
Colunas:
- Project: Comunidade
- Type: Tipo de manutenção
- Date: Data
- Status: Concluído, Em progresso, Agendado
- Priority: Normal, Alta, Baixa
```

---

## 🔌 Integração com Sistema Real

### Substituir dados de exemplo por dados reais:

1. **Banco de Dados** (recomendado para produção):
   ```python
   # Em vez de DataFrame hardcoded:
   import sqlite3
   
   conn = sqlite3.connect('projects.db')
   projects_df = pd.read_sql_query("SELECT * FROM projects", conn)
   ```

2. **API REST**:
   ```python
   import requests
   
   response = requests.get('http://api.geesp/projects')
   projects_df = pd.DataFrame(response.json())
   ```

3. **Google Sheets** (simples):
   ```python
   import gspread
   
   gs = gspread.oauth()
   sheet = gs.open("GEESP-Angola Monitoring")
   projects_df = pd.DataFrame(sheet.sheet1.get_all_records())
   ```

4. **MQTT/IoT** (tempo real):
   ```python
   import paho.mqtt.client as mqtt
   
   # Subscrever a tópicos IoT para geração em tempo real
   ```

---

## ⚙️ Configurações

### Mudar porta
```bash
streamlit run monitoring/monitoring_app.py --server.port 9000
```

### Configurar em `~/.streamlit/config.toml`:
```toml
[server]
port = 8502
headless = true
runOnSave = true

[theme]
primaryColor = "#1f77b4"
```

### Executar em background (Linux):
```bash
nohup streamlit run monitoring/monitoring_app.py > monitoring.log 2>&1 &
```

---

## 📈 KPIs Monitorados

| Indicador | Fonte | Frequência | Ação se <Threshold |
|-----------|-------|------------|-------------------|
| **System Health** | IoT/SCADA | 15 min | Alerta email se <80% |
| **Daily Generation** | Inversor | 1 hora | Notif. se -20% vs histórico |
| **Maintenance Overdue** | DB | Diário | Bloco vermelho se >7 dias |
| **Satisfação Comunitária** | Survey | Mensal | Reunião se <3.5/5.0 |
| **Geração vs Target** | API | Diário | Dashboard aviso se -15% |

---

## 🔐 Segurança

⚠️ **Em produção**, adicionar:
- Autenticação (username/password)
- Rate limiting
- SSL/HTTPS
- Logging detalhado
- Backup automático de dados

Exemplo com autenticação:
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials, 'some_cookie_name', 'some_signature_key'
)
name, authentication_status, username = authenticator.login('Login', 'main')
```

---

## 🐛 Troubleshooting

### Dashboard não abre
```bash
# Verificar se Streamlit está instalado
pip list | grep streamlit

# Instalar se necessário
pip install streamlit>=1.0.0
```

### Porta ocupada
```bash
# Usar porta diferente
streamlit run monitoring/monitoring_app.py --server.port 8503
```

### Dados desatualizados
Atualmente usando dados de exemplo. Para integração real, conectar a banco de dados com sincronização automática (ex: a cada 15 minutos).

---

## 📚 Próximos Passos

1. **Conectar a dados reais**:
   - [ ] Integração com SCADA/Inversor via API
   - [ ] Configurar banco de dados (PostgreSQL/SQLite)
   - [ ] Sincronização automática de dados

2. **Alertas avançados**:
   - [ ] Email notifications
   - [ ] SMS alerts
   - [ ] Webhooks para integrações

3. **Funcionalidades adicionais**:
   - [ ] Previsões (ML) de geração vs consumo
   - [ ] Análise de causalidade (ex: chuva → ↓geração)
   - [ ] Comparativos entre sistemas
   - [ ] Exportação de relatórios em PDF/Excel

4. **Escalabilidade**:
   - [ ] Deploy em servidor (Heroku, AWS, Google Cloud)
   - [ ] Cache (Redis) para performance
   - [ ] Multi-user com permissões granulares

---

## 📞 Suporte

Para dúvidas ou sugestões:
- GitHub Issues: [geesp-angola/issues](https://github.com/ISPTEC-Energy/geesp-angola/issues)
- Email: research@isptec.ao

---

**Status**: ✅ Pronto para uso e customização  
**Última atualização**: 2025-08-20

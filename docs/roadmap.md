# 🗺️ Roadmap do Projeto

## Status Atual

```
✅ Fase 1 — Fundação de Dados
✅ Fase 2 — Segmentação de Clientes
✅ Fase 3 — Predição de Churn
✅ Fase 4 — Pipeline Automatizado
✅ Fase 5 — App de Demonstração
🔜 Fase 6 — Agente com IA
🔜 Fase 7 — Integrações e Produção
```

---

## ✅ Fase 1 — Fundação de Dados

**Objetivo:** garantir qualidade e confiabilidade dos dados antes de qualquer modelagem.

| Entrega | Status |
|---------|--------|
| EDA completo — 22 etapas de análise | ✅ |
| Pipeline de limpeza documentado | ✅ |
| Remoção de 296.656 registros inválidos | ✅ |
| Dataset limpo: 770.715 transações | ✅ |

**Decisões críticas:**
- Remoção de cancelamentos (Invoice 'C') antes da análise de receita
- Identificação de 13 StockCodes não-produto
- Tratamento de Customer IDs nulos (22,77% do dataset)

---

## ✅ Fase 2 — Segmentação de Clientes

**Objetivo:** agrupar clientes por comportamento de compra em perfis acionáveis.

| Entrega | Status |
|---------|--------|
| Feature engineering RFM | ✅ |
| Transformação log1p + StandardScaler | ✅ |
| K-Means com Método Elbow (k=4) | ✅ |
| Mapeamento dinâmico de segmentos | ✅ |
| 4 perfis com estratégias definidas | ✅ |

**Resultado:**
- VIP: 1.179 clientes → 70,66% da receita
- Promissor: 1.237 clientes → 6,96% da receita
- Em Risco: 1.432 clientes → 18,12% da receita
- Perdido: 1.968 clientes → 4,26% da receita

---

## ✅ Fase 3 — Predição de Churn

**Objetivo:** prever quais clientes estão em risco de churn antes que aconteça.

| Entrega | Status |
|---------|--------|
| Label de churn engenheirado | ✅ |
| Baseline — Regressão Logística (93%, AUC 0.9846) | ✅ |
| Modelo final — Random Forest (98%, AUC 0.9993) | ✅ |
| Análise de importância das features | ✅ |
| Probabilidade de churn por cliente | ✅ |

**Resultado:**
- Apenas 18 erros em 1.164 predições
- Recency: 73% de importância
- Em Risco: 98,81% com alto risco
- VIP: 0% com alto risco

---

## ✅ Fase 4 — Pipeline Automatizado

**Objetivo:** encapsular todo o processo em um sistema reproduzível e sustentável.

| Entrega | Status |
|---------|--------|
| src/preprocessing.py | ✅ |
| src/feature_engineering.py | ✅ |
| src/segmentation.py | ✅ |
| src/prediction.py | ✅ |
| src/evaluation.py | ✅ |
| src/pipeline.py — orquestração completa | ✅ |
| Teste de integração end-to-end | ✅ |

**Resultado:** `run_pipeline()` executa do Excel bruto ao relatório final com um único comando.

---

## ✅ Fase 5 — App de Demonstração

**Objetivo:** tornar os resultados acessíveis e interativos para qualquer usuário.

| Entrega | Status |
|---------|--------|
| Página Visão Geral — KPIs e gráficos | ✅ |
| Página Busca de Cliente — consulta por ID | ✅ |
| Simulador de novo cliente com predição | ✅ |
| Página Estratégias — ações por segmento | ✅ |
| Deploy no Streamlit Community Cloud | ✅ |

**App em produção:** [customer-segmentation-platform.streamlit.app](https://customer-segmentation-platform.streamlit.app)

---

## 🔜 Fase 6 — Agente com IA

**Objetivo:** adicionar inteligência conversacional ao sistema — o usuário descreve um cliente ou situação e o agente recomenda ações em linguagem natural.

| Entrega | Prioridade |
|---------|-----------|
| Integração com LLM (Claude API) | Alta |
| Agente que interpreta o perfil do cliente | Alta |
| Recomendação de estratégia em linguagem natural | Alta |
| Análise de tendências da base em tempo real | Média |
| Geração automática de relatórios executivos | Média |

**Exemplo de interação esperada:**
```
Usuário: "O cliente 12347 está comprando menos. O que devo fazer?"

Agente:  "O cliente 12347 é VIP com Recency de 45 dias —
          acima da média histórica de 27 dias para este segmento.
          Probabilidade de churn: 23%. Recomendo contato proativo
          com oferta exclusiva antes que passe dos 60 dias."
```

---

## 🔜 Fase 7 — Integrações e Produção

**Objetivo:** transformar o projeto de demonstração em sistema pronto para uso empresarial.

| Entrega | Prioridade |
|---------|-----------|
| Ingestão de dados via API ou banco de dados | Alta |
| Re-treino automático com novos dados | Alta |
| Alertas automáticos para clientes Em Risco | Alta |
| Dashboard executivo com métricas em tempo real | Média |
| Integração com CRM (Salesforce, HubSpot) | Média |
| Integração com plataformas de e-mail marketing | Baixa |
| Autenticação e controle de acesso | Baixa |

---

## Evolução Técnica Planejada

```
Hoje                          Próximos passos
─────────────────────         ──────────────────────────
Batch processing         →    Streaming / near real-time
CSV como fonte           →    Banco de dados (PostgreSQL)
Modelos fixos            →    Re-treino automático (MLflow)
App de demonstração      →    API REST (FastAPI)
Deploy manual            →    CI/CD automatizado
Sem autenticação         →    Multi-tenant com auth
```

---

## Métricas de Sucesso

| Métrica | Atual | Meta Fase 6 | Meta Fase 7 |
|---------|-------|-------------|-------------|
| Acurácia do modelo | 98% | 98%+ | 98%+ |
| Tempo do pipeline | ~5 min | ~2 min | < 30 seg |
| Clientes processados | 5.816 | Ilimitado | Ilimitado |
| Fonte de dados | Excel manual | API automática | Streaming |
| Intervenção humana | Necessária | Mínima | Zero |

---

*github.com/moises-rb | linkedin.com/in/moisesrsjr*

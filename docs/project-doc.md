# Customer Segmentation Prediction Platform
## Documentação de Setup e Decisões do Projeto

---

## 1. Objetivo do Projeto

Construir uma plataforma de segmentação de clientes que:
- Analisa dados históricos de e-commerce
- Segmenta clientes por comportamento de compra (modelo RFM)
- Prediz churn e conversão
- Evolui para um sistema "vivo" com pipeline automatizado
- Serve de base para agentes de IA no futuro

---

## 2. Dataset Escolhido

**UCI Online Retail II**
- URL: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- ~1 milhão de transações reais de e-commerce britânico (2009–2011)
- Colunas principais: `CustomerID`, `InvoiceDate`, `Quantity`, `UnitPrice`, `Country`, `Description`

### Por que esse dataset?
- Volume suficiente para treinar e validar modelos
- Estrutura que replica dados reais de e-commerce
- Suporta clusterização, classificação e evolução para pipeline

### Atenção aos 2 riscos principais do input:
1. **~25% de CustomerID nulos** — tratar na etapa de limpeza
2. **Devoluções misturadas com compras** — separar por quantidade negativa

### Aderência aos requisitos do projeto:
| Requisito | Status |
|-----------|--------|
| Clusterização | ✅ Perfeito |
| Classificação (churn/conversão) | ⚠️ Label precisa ser engenheirado |
| Narrativa de negócio | ✅ Perfeito |
| Evolução para pipeline | ✅ Perfeito |
| Evolução para agente | ⚠️ Depende da arquitetura |

---

## 3. Conceito Central — RFM

| Letra | Significado | Pergunta |
|-------|-------------|----------|
| **R** - Recency | Quando comprou pela última vez? | Faz quanto tempo? |
| **F** - Frequency | Quantas vezes comprou? | Com que frequência? |
| **M** - Monetary | Quanto gastou no total? | Qual o valor? |

---

## 4. Estrutura do Projeto

```
customer_segmentation_prediction_platform/
│
├── README.md
├── .env                          # variáveis de ambiente (API keys futuras)
├── .gitignore                    # proteger .env e dados sensíveis
├── requirements.in               # libs instaladas diretamente (edição manual)
├── requirements.txt              # gerado automaticamente pelo pip-tools
│
├── data/
│   ├── raw/                      # dataset original — nunca modificar
│   ├── processed/                # dados limpos
│   └── features/                 # RFM e features engineered
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_segmentation.ipynb
│   ├── 04_prediction.ipynb
│   └── 05_pipeline_test.ipynb
│
├── src/
│   ├── __init__.py               # transforma src em módulo Python
│   ├── preprocessing.py
│   ├── feature_engineering.py    # cálculo RFM
│   ├── segmentation.py
│   ├── prediction.py
│   ├── evaluation.py
│   └── pipeline.py               # orquestra tudo
│
├── models/                       # modelos treinados salvos (.pkl)
│   └── .gitkeep
│
└── reports/
    └── figures/
```

---

## 5. Setup do Ambiente Virtual

### Criar e ativar o ambiente
```bash
# Criar
python -m venv .venv

# Ativar (Windows PowerShell)
.venv\Scripts\activate

# Ativar (Mac/Linux)
source .venv/bin/activate
```

### Selecionar interpretador no VSCode
```
Ctrl+Shift+P → "Python: Select Interpreter" → selecionar .venv
```

### Instalar dependências
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter openpyxl python-dotenv
```

---

## 6. Gerenciamento de Dependências com pip-tools

### Conceito
- **`requirements.in`** → você edita manualmente, só suas libs diretas
- **`requirements.txt`** → nunca edite manualmente, sempre gerado pelo pip-compile
- As libs "extras" que aparecem no `.txt` são **dependências transitivas** (libs que suas libs precisam para funcionar)

### Instalar pip-tools
```bash
pip install pip-tools
```

### Criar o requirements.in (Windows PowerShell)
```powershell
@"
pandas
numpy
matplotlib
seaborn
scikit-learn
jupyter
openpyxl
python-dotenv
"@ | Out-File -FilePath requirements.in -Encoding utf8
```

### Compilar e sincronizar
```bash
# Gera o requirements.txt automaticamente
pip-compile requirements.in

# Sincroniza o ambiente com o requirements.txt
pip-sync requirements.txt
```

### Comandos do dia a dia
| Situação | Comando |
|----------|---------|
| Adicionou nova lib no `.in` | `pip-compile requirements.in` |
| Quer sincronizar o ambiente | `pip-sync requirements.txt` |
| Atualizar versões das libs | `pip-compile --upgrade requirements.in` |

---

## 7. .gitignore mínimo recomendado

```
.venv/
.env
data/raw/
__pycache__/
*.pkl
.ipynb_checkpoints/
```

---

## 8. Roadmap do Projeto

```
Etapa 1 — EDA                  → entender os dados
Etapa 2 — Limpeza              → tratar nulos e devoluções
Etapa 3 — Feature Engineering  → calcular RFM
Etapa 4 — Clusterização        → K-Means para segmentar clientes
Etapa 5 — Classificação        → predição de churn/conversão
Etapa 6 — Pipeline             → automatizar o fluxo completo
Etapa 7 — Agente               → sistema vivo com IA
```

---

*Documentação gerada durante o setup inicial do projeto.*

---

## 8. EDA — Principais Achados (01_eda.ipynb)

### 8.1 Visão geral do dataset
- **1.067.371 linhas** x **8 colunas**
- Duas abas no xlsx unificadas: Year 2009-2010 (525.461) + Year 2010-2011 (541.910)
- Período: Dezembro 2009 a Dezembro 2011

### 8.2 Problemas críticos identificados — a tratar no ETL

| # | Problema | Volume | Ação no ETL |
|---|----------|--------|-------------|
| 1 | Customer ID nulo | 243.007 linhas (22,77%) | Remover para análise RFM |
| 2 | Duplicatas verdadeiras | 34.335 linhas (3,22%) | Remover |
| 3 | Cancelamentos (Invoice com 'C') | 19.494 linhas (1,83%) | Remover ou análise separada |
| 4 | Ajustes contábeis (Invoice com 'A') | 5 linhas | Remover |
| 5 | StockCode não-produto (POST, DOT, M, etc.) | 6.093 linhas | Remover |
| 6 | Price zero (movimentações internas) | 6.202 linhas | Remover |
| 7 | Price negativo (bad debt) | 5 linhas | Remover |
| 8 | Outliers em Quantity | acima do p99 (>100) | Corte no percentil 99 |
| 9 | Customer ID como float | toda a coluna | Converter para string |

### 8.3 StockCodes não-produto identificados

| StockCode | Descrição | Ação |
|-----------|-----------|------|
| POST | Frete | Remover |
| DOT | Postagem interna | Remover |
| M | Ajuste manual | Remover |
| C2 | Custo de envio | Remover |
| D | Desconto | Remover |
| S | Amostra grátis | Remover |
| BANK CHARGES | Taxa bancária | Remover |
| ADJUST | Ajuste de estoque | Remover |
| AMAZONFEE | Taxa marketplace | Remover |
| CRUK | Doação | Remover |
| TEST001 | Registro de teste | Remover |
| gift_0001_* | Cartão presente | **Manter** |

### 8.4 Insights de negócio

**Perfil do negócio**
- Negócio **B2B confirmado** — compras em horário comercial, quantidades de caixa (6, 12, 24)
- 91,9% das transações são do Reino Unido
- Ticket médio baixo — 99% dos produtos entre £0,50 e £18,00

**Sazonalidade**
- Pico em Novembro (Black Friday + pré-Natal) — padrão consistente em 2010 e 2011
- Queda brusca em Janeiro/Fevereiro — maior risco de churn
- Retomada gradual a partir de Setembro

**Janela de compra**
- Dia da semana: Quinta-feira é o pico, Saturday/Sunday zerados
- Hora do dia: pico ao meio-dia, movimento entre 8h e 17h

**Concentração de receita — Lei de Pareto**

| Faixa de clientes | % da Receita |
|-------------------|--------------|
| Top 10% | 53,9% |
| Top 20% | 70,6% |
| Top 30% | 80,8% |
| Top 50% | 92,0% |

**Perfis geográficos**
- Reino Unido: mercado principal, alta frequência
- EIRE (Irlanda): apenas 5 clientes, comportamento atacadista — VIP B2B
- Europa: mercado secundário, comportamento similar entre si

**Perfis de clientes extremos**
- Cliente 14911: 398 pedidos, £57.753 — provável distribuidor
- Cliente 15760: 2 pedidos, £13.916 — alto valor unitário, investigar
- Mediana de 3 pedidos por cliente — maioria compra pouco

**Estratégias de negócio identificadas**
- Contato ideal: Quinta-feira entre 10h e 12h
- Campanhas de reativação: Janeiro (pós-churn sazonal)
- Ofertas antecipadas: Agosto (antes do pico)
- Proteção VIP: Top 10% de clientes = 53,9% da receita

---

## 9. Roadmap do Projeto

```
✅ Etapa 0 — Estrutura e ambiente
✅ Etapa 1 — EDA (01_eda.ipynb)
⏭️ Etapa 2 — Preprocessing / ETL (02_preprocessing.ipynb)
   Etapa 3 — Feature Engineering — RFM
   Etapa 4 — Clusterização — K-Means
   Etapa 5 — Classificação — churn/conversão
   Etapa 6 — Pipeline automatizado
   Etapa 7 — Agente com IA
```

---

## 10. Resultados do EDA — `01_eda.ipynb`

### Visão geral do dataset
- **Total de linhas:** 1.067.371 (Year 2009-2010: 525.461 + Year 2010-2011: 541.910)
- **Total de colunas:** 8
- **Clientes únicos identificados:** 5.878
- **Período:** Dezembro/2009 a Dezembro/2011

### Problemas críticos — a tratar no ETL

| # | Problema | Volume | Ação |
|---|----------|--------|------|
| 1 | Customer ID nulo | 243.007 linhas (22,77%) | Remover para análise RFM |
| 2 | Duplicatas verdadeiras | 34.335 linhas (3,22%) | Remover |
| 3 | Cancelamentos Invoice 'C' | 19.494 linhas (1,83%) | Remover / guardar separado |
| 4 | Ajustes contábeis Invoice 'A' | 5 linhas | Remover |
| 5 | StockCode não-produto (POST, DOT, M, etc.) | 6.093 linhas | Remover |
| 6 | Price zero — movimentações internas | 6.202 linhas | Remover |
| 7 | Price negativo — bad debt | 5 linhas | Remover |
| 8 | Outliers Quantity acima do p99 | acima de 100 unidades | Cortar no p99 |
| 9 | Customer ID como float | — | Converter para string |
| 10 | Description nulos | 4.382 linhas (0,41%) | Remover |

### Insights de negócio descobertos

**Perfil do negócio**
- B2B confirmado — compras em horário comercial, ausência total nos fins de semana
- 91,9% das transações são do Reino Unido
- Ticket médio baixo — 99% dos produtos entre £1 e £18
- Quantidades em múltiplos (6, 12, 24) — compras por caixa

**Sazonalidade**
- Pico absoluto em Novembro (Black Friday + pré-Natal)
- Queda brusca em Janeiro e Fevereiro — maior janela de risco de churn
- Padrão consistente e repetido em 2010 e 2011 — negócio previsível

**Janela de compra ideal**
- Dia: Quinta-feira
- Horário: entre 10h e 14h

**Concentração de receita — Pareto confirmado**
- Top 10% dos clientes → 53,9% da receita
- Top 20% dos clientes → 70,6% da receita
- Top 50% dos clientes → 92,0% da receita

**Perfis geográficos distintos**
- Reino Unido: mercado principal, alta frequência, 5.410 clientes
- EIRE (Irlanda): 5 clientes VIP, 806 pedidos — perfil distribuidor
- Europa: mercado secundário com comportamento homogêneo

**Produto estrela confirmado**
- WHITE HANGING HEART T-LIGHT HOLDER: 96.683 unidades, 5.455 pedidos

---

*Documentação atualizada após conclusão do EDA.*

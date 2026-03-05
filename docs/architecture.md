# 🏗️ Arquitetura do Projeto

## Visão Geral

A plataforma é construída em camadas — cada uma com responsabilidade única e interfaces bem definidas. O dado entra bruto e sai como inteligência acionável.

```
┌─────────────────────────────────────────────────────────┐
│                     FONTE DE DADOS                      │
│          UCI Online Retail II — 1.067.371 transações    │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                     CAMADA DE DADOS                     │
│                                                         │
│  data/raw/          → dataset original (.xlsx)          │
│  data/processed/    → dados limpos (.csv)               │
│  data/features/     → RFM + segmentos + predições       │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                   CAMADA DE PROCESSAMENTO               │
│                                                         │
│  src/preprocessing.py       → limpeza e validação       │
│  src/feature_engineering.py → cálculo RFM               │
│  src/segmentation.py        → K-Means                   │
│  src/prediction.py          → Random Forest             │
│  src/evaluation.py          → relatórios                │
│  src/pipeline.py            → orquestração              │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                     CAMADA DE MODELOS                   │
│                                                         │
│  models/kmeans_rfm.pkl          → segmentação           │
│  models/scaler_rfm.pkl          → normalização RFM      │
│  models/random_forest_churn.pkl → predição churn        │
│  models/scaler_prediction.pkl   → normalização predição │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    CAMADA DE INTERFACE                  │
│                                                         │
│  app.py → Streamlit                                     │
│  ├── 📊 Visão Geral      → KPIs e gráficos              │
│  ├── 🔍 Busca de Cliente → consulta + simulador         │
│  └── 🎯 Estratégias      → ações por segmento           │
└─────────────────────────────────────────────────────────┘
```

---

## Estrutura de Arquivos

```
customer-segmentation-platform/
│
├── app.py                          # App Streamlit
├── requirements.txt                # Dependências
├── README.md                       # Documentação principal
│
├── data/
│   ├── raw/                        # Dataset original (não versionado)
│   ├── processed/                  # Dados limpos (não versionado)
│   └── features/                   # Features engineered
│       ├── rfm_segmentado.csv
│       └── rfm_com_predicoes.csv
│
├── models/                         # Modelos treinados
│   ├── kmeans_rfm.pkl
│   ├── scaler_rfm.pkl
│   ├── random_forest_churn.pkl
│   └── scaler_prediction.pkl
│
├── notebooks/
│   ├── 01_eda.ipynb                # Exploração dos dados
│   ├── 02_preprocessing.ipynb      # Pipeline de limpeza
│   ├── 03_segmentation.ipynb       # RFM + K-Means
│   ├── 04_prediction.ipynb         # Random Forest
│   ├── 05_pipeline_test.ipynb      # Teste de integração
│   └── analysis.ipynb              # Notebook narrativo (vitrine)
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py            # Limpeza e validação
│   ├── feature_engineering.py      # Cálculo RFM
│   ├── segmentation.py             # K-Means + mapeamento dinâmico
│   ├── prediction.py               # Random Forest + churn
│   ├── evaluation.py               # Relatórios e visualizações
│   └── pipeline.py                 # Orquestração completa
│
└── reports/
    └── figures/                    # Gráficos exportados
```

---

## Fluxo de Dados

```
Excel bruto
    │
    ▼
preprocessing.py
    ├── remove duplicatas (34.335)
    ├── remove cancelamentos Invoice 'C' (19.104)
    ├── remove ajustes Invoice 'A' (6)
    ├── remove StockCodes não-produto (4.513)
    ├── remove Price ≤ 0 (5.987)
    ├── remove Customer ID nulo (226.843)
    └── remove outliers Quantity p99 (5.868)
    │
    ▼ 770.715 linhas válidas
    │
feature_engineering.py
    ├── calcula Recency  → dias desde última compra
    ├── calcula Frequency → pedidos únicos por cliente
    ├── calcula Monetary  → receita total por cliente
    └── aplica log1p nas 3 métricas
    │
    ▼ 5.816 clientes com RFM
    │
segmentation.py
    ├── StandardScaler nas features log
    ├── KMeans k=4 (Método Elbow)
    └── mapeamento dinâmico de clusters → segmentos
    │
    ▼ 5.816 clientes segmentados
    │
prediction.py
    ├── label engenheirado: Churn = Em Risco + Perdido
    ├── train_test_split 80/20 estratificado
    ├── StandardScaler nas features RFM originais
    ├── RandomForestClassifier 100 estimadores
    └── predict_proba → probabilidade de churn
    │
    ▼ 5.816 clientes com segmento + probabilidade de churn
    │
app.py / evaluation.py
    └── visualizações, relatórios, interface interativa
```

---

## Decisões de Design

| Decisão | Alternativa considerada | Motivo da escolha |
|---------|------------------------|-------------------|
| RFM como features | Features brutas de transação | Interpretabilidade de negócio |
| log1p antes do K-Means | Sem transformação | Comprime caudas longas sem perder ordem |
| StandardScaler | MinMaxScaler | Robusto a outliers residuais |
| K-Means k=4 | k=3 ou k=5 | Elbow + interpretabilidade de negócio |
| Mapeamento dinâmico | Mapeamento fixo por índice | Estabilidade em re-treinos |
| Label via segmentos | Label externo | Não havia ground truth disponível |
| Random Forest | Gradient Boosting, XGBoost | Melhor equilíbrio acurácia/interpretabilidade |
| Streamlit | Flask, FastAPI | Deploy imediato para demonstração |
| Módulos src/ | Notebooks em produção | Testabilidade e reutilização |

---

## Como Executar

```bash
# 1. Clonar o repositório
git clone https://github.com/moises-rb/customer-segmentation-platform.git
cd customer-segmentation-platform

# 2. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o pipeline completo
python3 -c "
from src.pipeline import run_pipeline
PATHS = {
    'raw':         'data/raw/online_retail_II.xlsx',
    'processed':   'data/processed/online_retail_clean.csv',
    'features':    'data/features/rfm_segmentado.csv',
    'predictions': 'data/features/rfm_com_predicoes.csv',
    'kmeans':      'models/kmeans_rfm.pkl',
    'scaler_seg':  'models/scaler_rfm.pkl',
    'rf_model':    'models/random_forest_churn.pkl',
    'scaler_pred': 'models/scaler_prediction.pkl',
}
run_pipeline(paths=PATHS)
"

# 5. Rodar o app
streamlit run app.py
```

---

*github.com/moises-rb | linkedin.com/in/moisesrsjr*

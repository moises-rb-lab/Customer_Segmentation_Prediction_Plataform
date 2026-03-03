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

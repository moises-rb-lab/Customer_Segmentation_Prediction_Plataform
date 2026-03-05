# 💼 Contexto de Negócio

## O Problema

E-commerces que atendem múltiplos clientes enfrentam um desafio silencioso: **tratam todo mundo igual**.

O cliente VIP que compra todo mês recebe o mesmo e-mail de marketing que o cliente que comprou uma vez há dois anos e nunca mais voltou. Isso desperdiça verba, queima relacionamento e deixa dinheiro na mesa.

Sem uma visão estruturada da base de clientes, as empresas:

- Não sabem quem são seus clientes mais valiosos
- Descobrem o churn depois que o cliente já foi
- Distribuem orçamento de marketing sem critério
- Perdem a janela de reativação dos clientes em risco

---

## O Dataset

**UCI Online Retail II** — transações reais de um e-commerce britânico B2B entre Dezembro/2009 e Dezembro/2011.

| Característica | Dado |
|----------------|------|
| Volume bruto | 1.067.371 transações |
| Volume limpo | 770.715 transações válidas |
| Clientes únicos | 5.816 |
| Pedidos únicos | 35.946 |
| Produtos únicos | 4.613 |
| Receita total | £14.332.363 |
| Período | Dez/2009 a Dez/2011 |

---

## Perfil do Negócio — Achados do EDA

### Comportamento B2B confirmado

- **Zero pedidos nos fins de semana** — clientes são empresas, não pessoas físicas
- **Pico às Quintas entre 10h e 14h** — janela de maior conversão
- **Concentração geográfica** — 91,9% do volume no Reino Unido

### Sazonalidade

- **Pico em Novembro** — Black Friday + pré-Natal
- **Queda em Janeiro e Fevereiro** — maior risco de churn pós-festas
- Essa sazonalidade orienta o **timing das campanhas de retenção**

### Concentração de receita

- **Top 10% dos clientes geram 53,9% da receita**
- **Top 20% geram 70,6%** — Pareto confirmado
- **Top 50% geram 92%**

> Isso significa que perder 1 cliente VIP pode ter o mesmo impacto financeiro que perder 50 clientes médios.

---

## Os 4 Segmentos de Clientes

### 👑 VIP — 1.179 clientes

| Métrica | Valor |
|---------|-------|
| Recency média | 27 dias |
| Frequency média | 19 pedidos |
| Monetary média | £8.589 |
| % da Receita | **70,66%** |
| Risco de Churn | 0% |

**O que fazer:** proteger a todo custo. Programa de fidelidade exclusivo, atendimento personalizado, acesso antecipado a novos produtos. O churn de um único cliente VIP pode representar uma perda desproporcional de receita.

---

### 🌱 Promissor — 1.237 clientes

| Métrica | Valor |
|---------|-------|
| Recency média | 29 dias |
| Frequency média | 3 pedidos |
| Monetary média | £807 |
| % da Receita | 6,96% |
| Risco de Churn | 0,24% |

**O que fazer:** desenvolver. Esses clientes estão engajados mas ainda não atingiram o potencial máximo. Incentivos de frequência, cross-sell e e-mail de engajamento semanal são as alavancas certas.

---

### ⚠️ Em Risco — 1.432 clientes

| Métrica | Valor |
|---------|-------|
| Recency média | 227 dias |
| Frequency média | 5 pedidos |
| Monetary média | £1.813 |
| % da Receita | 18,12% |
| Risco de Churn | **98,81%** |

**O que fazer:** reativar com urgência. Esses clientes já demonstraram valor — compraram com frequência razoável e geraram receita relevante. A janela de reativação ainda está aberta, mas não por muito tempo. Campanha personalizada com oferta especial de retorno.

---

### 💤 Perdido — 1.968 clientes

| Métrica | Valor |
|---------|-------|
| Recency média | 394 dias |
| Frequency média | 1 pedido |
| Monetary média | £310 |
| % da Receita | 4,26% |
| Risco de Churn | **99,75%** |

**O que fazer:** campanha de baixíssimo custo ou aceitar a perda. O custo de reativação provavelmente supera o valor gerado. Se houver ação, que seja automatizada — e-mail simples com desconto agressivo.

---

## Receita em Risco

```
Segmento Em Risco  → £2.596.629  (18,12% da receita total)
Segmento Perdido   → £610.793    (4,26%  da receita total)

Total em risco     → £3.207.422  (22,38% da receita total)
```

**Mais de £3,2 milhões em receita estão associados a clientes com alto risco de churn.**

---

## Perguntas que o Sistema Responde

Para o **gestor de marketing:**
- Quais clientes devo priorizar nessa campanha?
- Qual o melhor momento para acionar cada segmento?
- Quanto de receita estou em risco de perder?

Para o **gestor comercial:**
- Quais clientes merecem atendimento personalizado?
- Quais clientes posso desenvolver para o próximo nível?
- Quais já foram e não vale o esforço de reativar?

Para o **CEO:**
- Qual é a concentração de receita na base?
- Qual o risco de churn no curto prazo?
- Onde concentrar o orçamento de retenção?

---

## ROI Potencial

Uma campanha de reativação bem direcionada ao segmento **Em Risco** que converta apenas **10% dos clientes** de volta representa:

```
1.432 clientes × 10% × £1.813 (monetary média) = £259.662 recuperados
```

Com custo de campanha inferior a isso, o ROI já é positivo.

---

*github.com/moises-rb | linkedin.com/in/moisesrsjr*

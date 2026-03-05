import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Segmentation Platform",
    page_icon="🎯",
    layout="wide"
)

# ─── Cores dos segmentos ──────────────────────────────────────────────────────
CORES = {
    'VIP':       '#2ecc71',
    'Promissor': '#3498db',
    'Em Risco':  '#e67e22',
    'Perdido':   '#e74c3c'
}

ESTRATEGIAS = {
    'VIP': {
        'icon': '👑',
        'descricao': 'Clientes de altíssimo valor — proteger a todo custo.',
        'acoes': [
            'Programa de fidelidade exclusivo',
            'Atendimento personalizado e prioritário',
            'Acesso antecipado a novos produtos',
            'Desconto especial em datas comemorativas',
        ]
    },
    'Promissor': {
        'icon': '🌱',
        'descricao': 'Clientes recentes com potencial de crescimento.',
        'acoes': [
            'Campanha de aumento de frequência',
            'Sugestão de produtos complementares',
            'Cupom de desconto na próxima compra',
            'E-mail de engajamento semanal',
        ]
    },
    'Em Risco': {
        'icon': '⚠️',
        'descricao': 'Clientes que sumiram mas tinham bom valor — reativar urgente.',
        'acoes': [
            'Campanha de reengajamento imediata',
            'Oferta especial de retorno',
            'Pesquisa de satisfação para entender o afastamento',
            'Contato direto para clientes de alto valor',
        ]
    },
    'Perdido': {
        'icon': '💤',
        'descricao': 'Clientes inativos há muito tempo e de baixo valor.',
        'acoes': [
            'Campanha de baixo custo — e-mail automatizado',
            'Oferta de reativação com desconto agressivo',
            'Aceitar perda se custo de retenção superar o valor',
        ]
    }
}


# ─── Carregamento dos dados ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('data/features/rfm_com_predicoes.csv')


@st.cache_resource
def load_models():
    with open('models/random_forest_churn.pkl', 'rb') as f:
        rf = pickle.load(f)
    with open('models/scaler_prediction.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return rf, scaler


rfm = load_data()
rf, scaler = load_models()


# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=80)
st.sidebar.title("Customer Segmentation\nPlatform")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    ["📊 Visão Geral", "🔍 Busca de Cliente", "🎯 Estratégias"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**Dataset:** {len(rfm):,} clientes  \n"
    f"**Modelo:** Random Forest  \n"
    f"**Acurácia:** 98%  \n"
    f"**ROC-AUC:** 0.9993"
)


# ─── Página 1 — Visão Geral ───────────────────────────────────────────────────
if pagina == "📊 Visão Geral":
    st.title("📊 Visão Geral dos Segmentos")
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    for col, segmento in zip([col1, col2, col3, col4],
                              ['VIP', 'Promissor', 'Em Risco', 'Perdido']):
        dados = rfm[rfm['Segmento'] == segmento]
        col.metric(
            label=f"{ESTRATEGIAS[segmento]['icon']} {segmento}",
            value=f"{len(dados):,}",
            delta=f"£{dados['Monetary'].sum():,.0f} receita"
        )

    st.markdown("---")

    # Gráficos
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Clientes por Segmento")
        contagem = rfm['Segmento'].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(contagem.index, contagem.values,
               color=[CORES[s] for s in contagem.index])
        ax.set_ylabel("Clientes")
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Receita por Segmento")
        receita = rfm.groupby('Segmento')['Monetary'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(receita.index, receita.values,
               color=[CORES[s] for s in receita.index])
        ax.set_ylabel("Receita £")
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Tabela Resumo")
    resumo = rfm.groupby('Segmento').agg(
        Clientes=('Customer ID', 'count'),
        Recency_media=('Recency', 'mean'),
        Frequency_media=('Frequency', 'mean'),
        Monetary_media=('Monetary', 'mean'),
        Receita_total=('Monetary', 'sum'),
        Churn_medio=('Churn_Probability', 'mean')
    ).round(2)
    resumo['Pct_Receita'] = (
        resumo['Receita_total'] / resumo['Receita_total'].sum() * 100
    ).round(2)
    st.dataframe(resumo, use_container_width=True)


# ─── Página 2 — Busca de Cliente ─────────────────────────────────────────────
elif pagina == "🔍 Busca de Cliente":
    st.title("🔍 Busca de Cliente")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Consultar cliente existente")
        customer_id = st.text_input("Customer ID", placeholder="ex: 12347")

        if customer_id:
            cliente = rfm[rfm['Customer ID'].astype(str) == customer_id]
            if len(cliente) == 0:
                st.error("Cliente não encontrado.")
            else:
                c = cliente.iloc[0]
                segmento = c['Segmento']
                st.success(f"{ESTRATEGIAS[segmento]['icon']} Segmento: **{segmento}**")
                st.metric("Recency", f"{c['Recency']} dias")
                st.metric("Frequency", f"{c['Frequency']} pedidos")
                st.metric("Monetary", f"£{c['Monetary']:,.2f}")
                st.metric("Risco de Churn", f"{c['Churn_Probability']*100:.1f}%")

        st.markdown("---")
        st.subheader("Simular novo cliente")
        recency  = st.slider("Recency (dias)", 1, 730, 90)
        frequency = st.slider("Frequency (pedidos)", 1, 50, 5)
        monetary  = st.number_input("Monetary (£)", 10.0, 50000.0, 1000.0)

        if st.button("🎯 Classificar"):
            X = scaler.transform([[recency, frequency, monetary]])
            prob = rf.predict_proba(X)[0][1]
            pred = rf.predict(X)[0]
            churn_label = "🚨 Churn" if pred == 1 else "✅ Ativo"
            st.metric("Predição", churn_label)
            st.metric("Probabilidade de Churn", f"{prob*100:.1f}%")

    with col2:
        st.subheader("Distribuição de Risco de Churn")
        fig, ax = plt.subplots(figsize=(8, 4))
        for segmento, cor in CORES.items():
            dados = rfm[rfm['Segmento'] == segmento]['Churn_Probability']
            ax.hist(dados, bins=30, alpha=0.6, color=cor, label=segmento)
        ax.set_xlabel("Probabilidade de Churn")
        ax.set_ylabel("Clientes")
        ax.legend()
        st.pyplot(fig)
        plt.close()


# ─── Página 3 — Estratégias ───────────────────────────────────────────────────
elif pagina == "🎯 Estratégias":
    st.title("🎯 Estratégias por Segmento")
    st.markdown("---")

    for segmento, info in ESTRATEGIAS.items():
        dados = rfm[rfm['Segmento'] == segmento]
        with st.expander(
            f"{info['icon']} {segmento} — "
            f"{len(dados):,} clientes | "
            f"£{dados['Monetary'].sum():,.0f} receita",
            expanded=(segmento == 'VIP')
        ):
            st.markdown(f"**{info['descricao']}**")
            st.markdown("**Ações recomendadas:**")
            for acao in info['acoes']:
                st.markdown(f"- {acao}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Recency média", f"{dados['Recency'].mean():.0f} dias")
            col2.metric("Frequency média", f"{dados['Frequency'].mean():.1f} pedidos")
            col3.metric("Monetary média", f"£{dados['Monetary'].mean():,.0f}")
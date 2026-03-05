import pandas as pd
import numpy as np
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


NOMES_SEGMENTOS = {
    'VIP': {'recency_max': 100, 'frequency_min': 10},
}

MAPEAMENTO_SEGMENTOS = {
    0: 'Promissor',
    1: 'Perdido',
    2: 'Em Risco',
    3: 'VIP'
}


def scale_features(rfm_log: pd.DataFrame) -> tuple:
    """Normaliza as features RFM para uso no K-Means."""
    scaler = StandardScaler()
    features = ['Recency_log', 'Frequency_log', 'Monetary_log']
    rfm_scaled = scaler.fit_transform(rfm_log[features])
    return rfm_scaled, scaler


def train_kmeans(rfm_scaled: np.ndarray,
                 n_clusters: int = 4,
                 random_state: int = 42) -> KMeans:
    """Treina o modelo K-Means."""
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )
    kmeans.fit(rfm_scaled)
    return kmeans


def assign_segments(rfm: pd.DataFrame,
                    kmeans: KMeans,
                    rfm_scaled: np.ndarray) -> pd.DataFrame:
    """Atribui clusters e nomes de segmentos ao DataFrame RFM."""
    rfm = rfm.copy()
    rfm['Cluster'] = kmeans.predict(rfm_scaled)

    # Mapear clusters para nomes baseado no perfil RFM
    # Cluster com menor Recency e maior Frequency = VIP
    perfil = rfm.groupby('Cluster').agg(
        Recency_media=('Recency', 'mean'),
        Frequency_media=('Frequency', 'mean'),
        Monetary_media=('Monetary', 'mean')
    )

    # Ordenar por Frequency desc e Recency asc para nomear
    perfil['Score'] = (
        perfil['Frequency_media'].rank(ascending=True) +
        perfil['Monetary_media'].rank(ascending=True) +
        perfil['Recency_media'].rank(ascending=False)
    )

    ranking = perfil['Score'].sort_values(ascending=False)
    nomes = ['VIP', 'Em Risco', 'Promissor', 'Perdido']
    mapeamento = {cluster: nome
                  for cluster, nome in zip(ranking.index, nomes)}

    rfm['Segmento'] = rfm['Cluster'].map(mapeamento)
    return rfm


def save_models(kmeans: KMeans,
                scaler: StandardScaler,
                kmeans_path: str,
                scaler_path: str) -> None:
    """Salva o modelo K-Means e o scaler."""
    with open(kmeans_path, 'wb') as f:
        pickle.dump(kmeans, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Modelos salvos:")
    print(f"  → {kmeans_path}")
    print(f"  → {scaler_path}")


def load_models(kmeans_path: str,
                scaler_path: str) -> tuple:
    """Carrega modelos salvos do disco."""
    with open(kmeans_path, 'rb') as f:
        kmeans = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return kmeans, scaler
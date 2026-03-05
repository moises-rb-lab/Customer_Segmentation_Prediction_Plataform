import pandas as pd
import numpy as np


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula as métricas RFM por cliente."""

    data_referencia = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    recency = (
        df.groupby('Customer ID')['InvoiceDate']
        .max()
        .reset_index()
    )
    recency.columns = ['Customer ID', 'UltimaCompra']
    recency['Recency'] = (data_referencia - recency['UltimaCompra']).dt.days

    frequency = (
        df.groupby('Customer ID')['Invoice']
        .nunique()
        .reset_index()
    )
    frequency.columns = ['Customer ID', 'Frequency']

    monetary = (
        df.groupby('Customer ID')['TotalPrice']
        .sum()
        .reset_index()
    )
    monetary.columns = ['Customer ID', 'Monetary']

    rfm = (
        recency[['Customer ID', 'Recency']]
        .merge(frequency, on='Customer ID')
        .merge(monetary, on='Customer ID')
    )

    return rfm


def apply_log_transform(rfm: pd.DataFrame) -> pd.DataFrame:
    """Aplica transformação logarítmica nas métricas RFM."""
    rfm_log = rfm.copy()
    rfm_log['Recency_log']   = np.log1p(rfm['Recency'])
    rfm_log['Frequency_log'] = np.log1p(rfm['Frequency'])
    rfm_log['Monetary_log']  = np.log1p(rfm['Monetary'])
    return rfm_log


def save_rfm(rfm: pd.DataFrame, filepath: str) -> None:
    """Salva a tabela RFM em CSV."""
    rfm.to_csv(filepath, index=False)
    print(f"RFM salvo em {filepath} "
          f"— {rfm.shape[0]:,} clientes")
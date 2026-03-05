import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """Carrega o dataset bruto das duas abas do Excel."""
    df_0910 = pd.read_excel(filepath, sheet_name='Year 2009-2010')
    df_1011 = pd.read_excel(filepath, sheet_name='Year 2010-2011')
    df = pd.concat([df_0910, df_1011], ignore_index=True)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todo o pipeline de limpeza documentado no EDA."""

    STOCKCODES_NAO_PRODUTO = [
        'POST', 'DOT', 'M', 'C2', 'D', 'S',
        'BANK CHARGES', 'ADJUST', 'AMAZONFEE',
        'CRUK', 'TEST001', 'PADS', 'B'
    ]

    df = df.drop_duplicates()
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    df = df[~df['Invoice'].astype(str).str.startswith('A')]
    df = df[~df['StockCode'].astype(str).isin(STOCKCODES_NAO_PRODUTO)]
    df = df[df['Price'] > 0]
    df = df[df['Quantity'] > 0]
    df = df[df['Customer ID'].notna()]
    df = df[df['Description'].notna()]

    q99 = df['Quantity'].quantile(0.99)
    df = df[df['Quantity'] <= q99]

    df['Customer ID'] = df['Customer ID'].astype(int).astype(str)
    df['TotalPrice'] = df['Quantity'] * df['Price']

    return df.reset_index(drop=True)


def save_clean_data(df: pd.DataFrame, filepath: str) -> None:
    """Salva o dataset limpo em CSV."""
    df.to_csv(filepath, index=False)
    print(f"Dataset limpo salvo em {filepath} "
          f"— {df.shape[0]:,} linhas x {df.shape[1]} colunas")
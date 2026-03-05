import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from src.preprocessing import load_data, clean_data, save_clean_data
from src.feature_engineering import calculate_rfm, apply_log_transform, save_rfm
from src.segmentation import scale_features, train_kmeans, assign_segments, save_models
from src.prediction import (create_churn_label, prepare_features,
                             scale_features as scale_pred_features,
                             train_model, evaluate_model,
                             predict_churn, save_model)
from src.evaluation import segment_report, churn_report


# Caminhos padrão do projeto
PATHS = {
    'raw':            '../data/raw/online_retail_II.xlsx',
    'processed':      '../data/processed/online_retail_clean.csv',
    'features':       '../data/features/rfm_segmentado.csv',
    'predictions':    '../data/features/rfm_com_predicoes.csv',
    'kmeans':         '../models/kmeans_rfm.pkl',
    'scaler_seg':     '../models/scaler_rfm.pkl',
    'rf_model':       '../models/random_forest_churn.pkl',
    'scaler_pred':    '../models/scaler_prediction.pkl',
}


def run_preprocessing(paths: dict = PATHS) -> pd.DataFrame:
    """Etapa 1 — Carrega e limpa os dados brutos."""
    print("\n" + "="*55)
    print("ETAPA 1 — PREPROCESSING")
    print("="*55)
    df = load_data(paths['raw'])
    df = clean_data(df)
    save_clean_data(df, paths['processed'])
    return df


def run_feature_engineering(df: pd.DataFrame,
                             paths: dict = PATHS) -> tuple:
    """Etapa 2 — Calcula RFM e aplica transformação log."""
    print("\n" + "="*55)
    print("ETAPA 2 — FEATURE ENGINEERING (RFM)")
    print("="*55)
    rfm = calculate_rfm(df)
    rfm_log = apply_log_transform(rfm)
    save_rfm(rfm, paths['features'])
    print(f"RFM calculado para {len(rfm):,} clientes")
    return rfm, rfm_log


def run_segmentation(rfm: pd.DataFrame,
                     rfm_log: pd.DataFrame,
                     paths: dict = PATHS) -> pd.DataFrame:
    """Etapa 3 — Treina K-Means e segmenta os clientes."""
    print("\n" + "="*55)
    print("ETAPA 3 — SEGMENTAÇÃO (K-MEANS)")
    print("="*55)
    rfm_scaled, scaler = scale_features(rfm_log)
    kmeans = train_kmeans(rfm_scaled, n_clusters=4)
    rfm = assign_segments(rfm, kmeans, rfm_scaled)
    save_models(kmeans, scaler, paths['kmeans'], paths['scaler_seg'])

    print("\nDistribuição dos segmentos:")
    print(rfm['Segmento'].value_counts())
    return rfm


def run_prediction(rfm: pd.DataFrame,
                   paths: dict = PATHS) -> tuple:
    """Etapa 4 — Treina Random Forest e prediz churn."""
    print("\n" + "="*55)
    print("ETAPA 4 — PREDIÇÃO DE CHURN")
    print("="*55)
    rfm = create_churn_label(rfm)
    X, y = prepare_features(rfm)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train_scaled, X_test_scaled, scaler = scale_pred_features(
        X_train, X_test
    )

    rf = train_model(X_train_scaled, y_train)
    metrics = evaluate_model(rf, X_test_scaled, y_test)
    rfm = predict_churn(rfm, rf, scaler)

    save_model(rf, scaler, paths['rf_model'], paths['scaler_pred'])
    rfm.to_csv(paths['predictions'], index=False)
    print(f"Predições salvas em {paths['predictions']}")

    return rfm, metrics


def run_reports(rfm: pd.DataFrame) -> None:
    """Etapa 5 — Gera relatórios finais."""
    print("\n" + "="*55)
    print("ETAPA 5 — RELATÓRIOS")
    print("="*55)
    print("\nRelatório de Segmentos:")
    print(segment_report(rfm).to_string())
    print("\nRelatório de Churn:")
    print(churn_report(rfm).to_string())


def run_pipeline(paths: dict = PATHS) -> pd.DataFrame:
    """
    Executa o pipeline completo de ponta a ponta.
    Retorna o DataFrame final com segmentos e predições.
    """
    print("\n" + "="*55)
    print("CUSTOMER SEGMENTATION PREDICTION PLATFORM")
    print("Iniciando pipeline completo...")
    print("="*55)

    df = run_preprocessing(paths)
    rfm, rfm_log = run_feature_engineering(df, paths)
    rfm = run_segmentation(rfm, rfm_log, paths)
    rfm, metrics = run_prediction(rfm, paths)
    run_reports(rfm)

    print("\n" + "="*55)
    print("Pipeline concluído com sucesso!")
    print("="*55)

    return rfm


if __name__ == '__main__':
    rfm = run_pipeline()
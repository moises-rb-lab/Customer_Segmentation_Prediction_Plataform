import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score


FEATURES = ['Recency', 'Frequency', 'Monetary']
SEGMENTOS_CHURN = ['Perdido', 'Em Risco']


def create_churn_label(rfm: pd.DataFrame) -> pd.DataFrame:
    """Cria o label de churn baseado nos segmentos."""
    rfm = rfm.copy()
    rfm['Churn'] = rfm['Segmento'].isin(SEGMENTOS_CHURN).astype(int)
    return rfm


def prepare_features(rfm: pd.DataFrame) -> tuple:
    """Separa features e target para treino."""
    X = rfm[FEATURES]
    y = rfm['Churn']
    return X, y


def scale_features(X_train: pd.DataFrame,
                   X_test: pd.DataFrame) -> tuple:
    """Normaliza as features de treino e teste."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def train_model(X_train_scaled: np.ndarray,
                y_train: pd.Series,
                n_estimators: int = 100,
                random_state: int = 42) -> RandomForestClassifier:
    """Treina o modelo Random Forest."""
    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1
    )
    rf.fit(X_train_scaled, y_train)
    return rf


def evaluate_model(rf: RandomForestClassifier,
                   X_test_scaled: np.ndarray,
                   y_test: pd.Series) -> dict:
    """Avalia o modelo e retorna métricas."""
    y_pred = rf.predict(X_test_scaled)
    y_prob = rf.predict_proba(X_test_scaled)[:, 1]

    report = classification_report(
        y_test, y_pred,
        target_names=['Ativo', 'Churn'],
        output_dict=True
    )
    auc = roc_auc_score(y_test, y_prob)

    print("Resultado do modelo:")
    print('='*50)
    print(classification_report(y_test, y_pred,
          target_names=['Ativo', 'Churn']))
    print(f"ROC-AUC: {auc:.4f}")

    return {'report': report, 'roc_auc': auc}


def predict_churn(rfm: pd.DataFrame,
                  rf: RandomForestClassifier,
                  scaler: StandardScaler) -> pd.DataFrame:
    """Prediz churn e probabilidade para todos os clientes."""
    rfm = rfm.copy()
    X = scaler.transform(rfm[FEATURES])
    rfm['Churn_Predicted'] = rf.predict(X)
    rfm['Churn_Probability'] = rf.predict_proba(X)[:, 1]
    return rfm


def save_model(rf: RandomForestClassifier,
               scaler: StandardScaler,
               model_path: str,
               scaler_path: str) -> None:
    """Salva o modelo e scaler no disco."""
    with open(model_path, 'wb') as f:
        pickle.dump(rf, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Modelos salvos:")
    print(f"  → {model_path}")
    print(f"  → {scaler_path}")


def load_model(model_path: str,
               scaler_path: str) -> tuple:
    """Carrega modelo e scaler salvos do disco."""
    with open(model_path, 'rb') as f:
        rf = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return rf, scaler
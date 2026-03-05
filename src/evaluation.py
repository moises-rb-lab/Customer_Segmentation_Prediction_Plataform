import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, roc_curve,
                             roc_auc_score, classification_report)


def plot_segments(rfm: pd.DataFrame,
                  save_path: str = None) -> None:
    """Gera dashboard visual dos segmentos."""

    cores = {
        'VIP': '#2ecc71',
        'Promissor': '#3498db',
        'Em Risco': '#e67e22',
        'Perdido': '#e74c3c'
    }

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Clientes por segmento
    contagem = rfm['Segmento'].value_counts()
    axes[0, 0].bar(contagem.index, contagem.values,
                   color=[cores[s] for s in contagem.index])
    axes[0, 0].set_title('Clientes por Segmento')
    axes[0, 0].set_ylabel('Número de clientes')

    # Receita por segmento
    receita = (rfm.groupby('Segmento')['Monetary']
               .sum()
               .sort_values(ascending=False))
    axes[0, 1].bar(receita.index, receita.values,
                   color=[cores[s] for s in receita.index])
    axes[0, 1].set_title('Receita Total por Segmento')
    axes[0, 1].set_ylabel('Receita £')

    # Recency média
    recency = (rfm.groupby('Segmento')['Recency']
               .mean()
               .sort_values())
    axes[1, 0].bar(recency.index, recency.values,
                   color=[cores[s] for s in recency.index])
    axes[1, 0].set_title('Recency Média por Segmento')
    axes[1, 0].set_ylabel('Dias desde última compra')

    # Frequency média
    frequency = (rfm.groupby('Segmento')['Frequency']
                 .mean()
                 .sort_values(ascending=False))
    axes[1, 1].bar(frequency.index, frequency.values,
                   color=[cores[s] for s in frequency.index])
    axes[1, 1].set_title('Frequency Média por Segmento')
    axes[1, 1].set_ylabel('Número médio de pedidos')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo em {save_path}")

    plt.show()


def plot_confusion_matrix(y_test: pd.Series,
                          y_pred: np.ndarray,
                          save_path: str = None) -> None:
    """Plota a matriz de confusão do modelo."""
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=['Ativo', 'Churn'],
                yticklabels=['Ativo', 'Churn'])
    plt.title('Matriz de Confusão')
    plt.ylabel('Real')
    plt.xlabel('Previsto')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo em {save_path}")

    plt.show()


def plot_roc_curve(y_test: pd.Series,
                   y_prob: np.ndarray,
                   save_path: str = None) -> None:
    """Plota a curva ROC do modelo."""
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(8, 5))
    plt.plot(fpr, tpr, color='seagreen', linewidth=2,
             label=f'Random Forest (AUC={auc:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1)
    plt.title('Curva ROC')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo em {save_path}")

    plt.show()


def segment_report(rfm: pd.DataFrame) -> pd.DataFrame:
    """Gera relatório resumido dos segmentos."""
    report = rfm.groupby('Segmento').agg(
        Clientes=('Customer ID', 'count'),
        Recency_media=('Recency', 'mean'),
        Frequency_media=('Frequency', 'mean'),
        Monetary_media=('Monetary', 'mean'),
        Receita_total=('Monetary', 'sum')
    ).round(2)

    report['Pct_Receita'] = (
        report['Receita_total'] /
        report['Receita_total'].sum() * 100
    ).round(2)

    return report


def churn_report(rfm: pd.DataFrame) -> pd.DataFrame:
    """Gera relatório de risco de churn por segmento."""
    report = rfm.groupby('Segmento').agg(
        Clientes=('Customer ID', 'count'),
        Churn_medio=('Churn_Probability', 'mean'),
        Alto_risco=('Churn_Probability',
                    lambda x: (x >= 0.7).sum())
    ).round(2)

    report['Pct_Alto_Risco'] = (
        report['Alto_risco'] /
        report['Clientes'] * 100
    ).round(2)

    return report
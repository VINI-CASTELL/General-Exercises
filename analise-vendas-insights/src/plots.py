import matplotlib.pyplot as plt
import pandas as pd

def plot_receita_mensal(mensal: pd.DataFrame) -> None:
    # Plota receita ao longo do tempo pra enxergar sazonalidade e quedas
    plt.figure()
    plt.plot(mensal["mes"], mensal["receita"])
    plt.xticks(rotation=45)
    plt.title("Receita por mês")
    plt.ylabel("Receita")
    plt.tight_layout()
    plt.show()


def plot_top_barras(df_top: pd.DataFrame, label_col: str, value_col: str, titulo: str) -> None:
    # Bar chart pra ranking (produto/região) — fácil de entender rápido
    plt.figure()
    plt.bar(df_top[label_col], df_top[value_col])
    plt.xticks(rotation=45, ha="right")
    plt.title(titulo)
    plt.ylabel(value_col)
    plt.tight_layout()
    plt.show()

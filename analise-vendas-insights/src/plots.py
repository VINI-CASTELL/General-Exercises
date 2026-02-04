import os
import matplotlib.pyplot as plt
import pandas as pd

def _garantir_pasta_outputs():
    # Cria a pasta outputs/ se não existir (pra salvar os PNGs)
    os.makedirs("outputs", exist_ok=True)

def plot_receita_mensal(mensal: pd.DataFrame, salvar: bool = True) -> None:
    _garantir_pasta_outputs()

    plt.figure()
    plt.plot(mensal["mes"], mensal["receita"])
    plt.xticks(rotation=45)
    plt.title("Receita por mês")
    plt.ylabel("Receita")
    plt.tight_layout()

    if salvar:
        plt.savefig("outputs/receita_por_mes.png", dpi=150)

    plt.show()


def plot_top_barras(df_top: pd.DataFrame, label_col: str, value_col: str, titulo: str, nome_arquivo: str, salvar: bool = True) -> None:
    _garantir_pasta_outputs()

    plt.figure()
    plt.bar(df_top[label_col], df_top[value_col])
    plt.xticks(rotation=45, ha="right")
    plt.title(titulo)
    plt.ylabel(value_col)
    plt.tight_layout()

    if salvar:
        plt.savefig(f"outputs/{nome_arquivo}", dpi=150)

    plt.show()

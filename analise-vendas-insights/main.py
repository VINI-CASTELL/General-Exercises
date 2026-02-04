import pandas as pd

from src.metrics import (
    preparar_base,
    receita_por_regiao,
    receita_por_produto,
    crescimento_mensal,
    ticket_medio,
)

from src.plots import (
    plot_receita_mensal,
    plot_top_barras,
)


def main():
    # 1) Lê o CSV com os dados de vendas
    # IMPORTANTE: o arquivo precisa estar em data/vendas.csv
    df = pd.read_csv("data/vendas.csv")

    # 2) Limpa e prepara a base (corrige datas, tipos, cria receita e mes)
    df = preparar_base(df)

    # 3) KPIs principais (números “de cara”)
    receita_total = df["receita"].sum()
    tm = ticket_medio(df)

    print("=== KPIs principais ===")
    print(f"Receita total: {receita_total:,.2f}")
    print(f"Ticket médio (aprox.): {tm:,.2f}")
    print(f"Período: {df['data'].min().date()} -> {df['data'].max().date()}")
    print()

    # 4) Rankings
    reg = receita_por_regiao(df)
    prod = receita_por_produto(df, top_n=10)

    print("=== Top regiões por receita ===")
    print(reg.head(10).to_string(index=False))
    print()

    print("=== Top produtos por receita ===")
    print(prod.to_string(index=False))
    print()

    # 5) Série temporal
    mensal = crescimento_mensal(df)

    # 6) Gráficos (abre janelas com gráficos)
    plot_receita_mensal(mensal)
    plot_top_barras(prod, "produto", "receita", "Top 10 produtos por receita")
    plot_top_barras(reg.head(10), "regiao", "receita", "Top regiões por receita")

    # 7) “Insights” automáticos simples (pra já ter cara de projeto)
    mensal_sem_na = mensal.dropna(subset=["crescimento_mom"])
    if not mensal_sem_na.empty:
        pior = mensal_sem_na.sort_values("crescimento_mom").iloc[0]
        print("=== Insight automático ===")
        print(f"Pior variação MoM: {pior['mes']} com {pior['crescimento_mom']:.2%}")

    if not reg.empty:
        top_regiao = reg.iloc[0]
        print(f"Região que mais faturou: {top_regiao['regiao']} (receita = {top_regiao['receita']:,.2f})")


if __name__ == "__main__":
    main()

import pandas as pd

def preparar_base(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza a base para evitar erro bobo no resto do projeto.
    """
    # Converte a coluna de data para datetime (pra conseguir agrupar por mês)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Remove linhas sem data (sem data, não dá pra fazer série temporal)
    df = df.dropna(subset=["data"])

    # Normaliza texto (evita "Sudeste" vs "sudeste" virar duas regiões diferentes)
    df["regiao"] = df["regiao"].astype(str).str.strip().str.lower()
    df["produto"] = df["produto"].astype(str).str.strip()

    # Garante tipos numéricos
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")

    # Remove linhas inválidas (preço ou quantidade nulos/negativos costumam ser lixo)
    df = df.dropna(subset=["preco", "quantidade"])
    df = df[(df["preco"] > 0) & (df["quantidade"] > 0)]

    # Cria coluna de receita: KPI mais básico de vendas
    df["receita"] = df["preco"] * df["quantidade"]

    # Cria coluna mês (facilita agrupar e fazer gráfico de tendência)
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    return df


def receita_por_regiao(df: pd.DataFrame) -> pd.DataFrame:
    # Agrupa por região e soma receita (ranking de regiões)
    return (df.groupby("regiao", as_index=False)["receita"]
              .sum()
              .sort_values("receita", ascending=False))


def receita_por_produto(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    # Ranking de produtos por receita (top 10 por padrão)
    return (df.groupby("produto", as_index=False)["receita"]
              .sum()
              .sort_values("receita", ascending=False)
              .head(top_n))


def crescimento_mensal(df: pd.DataFrame) -> pd.DataFrame:
    # Série temporal de receita por mês
    mensal = (df.groupby("mes", as_index=False)["receita"].sum()
                .sort_values("mes"))

    # Crescimento mês a mês (MoM)
    mensal["crescimento_mom"] = mensal["receita"].pct_change()

    return mensal


def ticket_medio(df: pd.DataFrame) -> float:
    # Ticket médio aproximado = receita total / total de itens vendidos
    receita_total = df["receita"].sum()
    itens_total = df["quantidade"].sum()
    return receita_total / itens_total if itens_total else 0.0

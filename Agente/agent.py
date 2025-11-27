from google.adk.agents import Agent
import pandas as pd
import re


drive_link = "https://drive.google.com/uc?export=download)&id=1ncTVlw7uHRYOvGaGslOnuXW7Ou1QMDqu"

# Carrega o CSV externo
df = pd.read_csv(drive_link)

def consultar_csv(query: str) -> str:
    """
    Ferramenta que responde perguntas sobre o CSV.
    """
    q = query.lower()

    try:
         # --- Pergunta: "qual X teve mais acidentes?" ---
        if ("mais acidentes" in q) or ("teve mais" in q):
            palavras = q.split()

            # Lista de palavras-chave que representam categorias comuns
            possíveis_colunas = ["estado", "uf", "cidade", "municipio", "rodovia", "bairro", "regiao"]

            # Tenta encontrar uma coluna mencionada explicitamente
            col_encontrada = None

            for col in df.columns:
                col_lower = col.lower()

                # Comparar palavra por palavra
                if col_lower in palavras:
                    col_encontrada = col
                    break

                # Se a coluna é uma das categorias prováveis
                for p in possíveis_colunas:
                    if p in palavras and p in col_lower:
                        col_encontrada = col
                        break

            if col_encontrada is None:
                return "Não consegui identificar qual coluna representa o estado/categoria que você quer analisar."

            # Realiza a contagem por categoria
            counts = df[col_encontrada].value_counts()

            if counts.empty:
                return f"Não há dados suficientes para a coluna '{col_encontrada}'."

            top_value = counts.idxmax()
            top_count = counts.max()

            return (
                f"A categoria que teve mais acidentes na coluna '{col_encontrada}' "
                f"foi '{top_value}', com {top_count} registros."
            )
        
        if "quantas" in q and ("linhas" in q or "registros" in q):
            return f"O arquivo possui {len(df)} linhas."

        if "colunas" in q:
            return f"As colunas disponíveis são: {list(df.columns)}"

        if "info" in q or "tipos" in q or "dtype" in q:
            return str(df.dtypes)

        if "describe" in q or "estatística" in q:
            return str(df.describe(include='all'))

        
        for col in df.columns:
            col_lower = col.lower()

            
            if col_lower not in q:
                continue

            # Maior valor
            if "maior" in q or "max" in q:
                if pd.api.types.is_numeric_dtype(df[col]):
                    row = df.loc[df[col].idxmax()]
                    return f"Maior valor da coluna '{col}': {row.to_dict()}"
                else:
                    return f"A coluna '{col}' não é numérica."

            # Menor valor
            if "menor" in q or "min" in q:
                if pd.api.types.is_numeric_dtype(df[col]):
                    row = df.loc[df[col].idxmin()]
                    return f"Menor valor da coluna '{col}': {row.to_dict()}"
                else:
                    return f"A coluna '{col}' não é numérica."

            # Média
            if "média" in q or "media" in q:
                if pd.api.types.is_numeric_dtype(df[col]):
                    return f"A média da coluna '{col}' é {df[col].mean():.2f}"
                else:
                    return f"A coluna '{col}' não é numérica."

            # Soma
            if "soma" in q or "total" in q:
                if pd.api.types.is_numeric_dtype(df[col]):
                    return f"A soma da coluna '{col}' é {df[col].sum()}"
                else:
                    return f"A coluna '{col}' não é numérica."

            # Valores únicos
            if "valores únicos" in q or "unique" in q:
                return f"Valores únicos na coluna '{col}': {df[col].unique().tolist()}"

            # Contagem de valores únicos
            if "quantas vezes" in q or "contagem de" in q:
                return str(df[col].value_counts())

        # ---- "linhas onde X = Y" ----
        if "onde" in q or "igual a" in q:

            for col in df.columns:
                col_lower = col.lower()

                if col_lower in q:
                    # Tenta extrair valor após "=", "igual", etc.
                    import re

                    # padrões comuns
                    padroes = [
                        rf"{col_lower}\s*=\s*([\w\.-]+)",
                        rf"{col_lower}\s*igual a\s*([\w\.-]+)",
                        rf"{col_lower}\s*é\s*([\w\.-]+)"
                    ]

                    for p in padroes:
                        m = re.search(p, q)
                        if m:
                            valor = m.group(1)

                            # tenta converter para número, se aplicável
                            try:
                                valor_eval = float(valor)
                                filtro = df[df[col] == valor_eval]
                            except:
                                filtro = df[df[col].astype(str).str.lower() == valor.lower()]

                            return str(filtro.to_dict(orient="records"))

        # ---- Caso nada tenha sido detectado ----
        return "Ainda não tenho lógica para responder essa pergunta, tente ser mais específico."

    except Exception as e:
        return f"Erro ao consultar CSV: {e}"



root_agent = Agent(
    name="ijca",
    model="gemini-2.0-flash",
    description="Agente para analizar dados",
    instruction=f"""
        Você é um agente analista de dados.
        Use a ferramenta consultar_csv para responder perguntas sobre os dados.
        - Use a coluna 'uf' para perguntas sobre estados.
        - Use a coluna 'municipio' para perguntas sobre municípios.
        - Use a coluna 'tipo_acidente' para perguntas sobre tipos de acidentes.
        - Nunca invente valores.
        - Se a ferramenta não retornar nada útil, diga que não encontrou.
    """,
    tools=[consultar_csv],
)

from google.adk.agents import Agent
import pandas as pd

dados = pd.read_csv('dados_acidente.csv')

root_agent = Agent(
    name = "ijca",
    model = "gemini-2.0-flash",
    description = "Agente para analizar dados",
    instruction = f"""Você é um agente analista de dados que escaneia um arquivo CSV,{dados}, com base em perguntas e da uma resposta concisa
    baseada nestes dados.
    
    -Não halucine uma resposta caso não ache nada ou os dados não estiverem acessíveis.
    
    """

)
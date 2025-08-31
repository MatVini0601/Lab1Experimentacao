import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
from datetime import datetime, timedelta
import os


def salvar_grafico(nome_arquivo):
    """Salva o gráfico atual em PNG na pasta 'graficos'."""
    pasta = 'graficos'
    os.makedirs(pasta, exist_ok=True)  # Cria a pasta se não existir
    caminho = os.path.join(pasta, f'{nome_arquivo}.png')
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()  # Fecha a figura atual para liberar memória
    print(f'Gráfico salvo em: {caminho}')


def coletar_dados():
    df = pd.read_csv("repos_populares.csv")

    primary_language = "primary_language"
    pull_request_aceitas = "pull_requests_aceitas"

    resultado = df.groupby(primary_language).agg(
        Quantidade_Repositorios=(primary_language, "count"),
        Pulls_Aceitas=(pull_request_aceitas, "sum")
    ).reset_index()

    resultado = resultado.sort_values(by="Quantidade_Repositorios", ascending=False)
    resultado.to_csv("linguagens_com_pull_request.csv", index=False)



# GRÁFICOS BÁSICOS

def grafico_barras(df):
    plt.figure(figsize=(20, 12))
    sns.barplot(x='primary_language', y='Quantidade_Repositorios', data=df, estimator=sum, errorbar=None)
    plt.title('Quantidade Totais por Linguagem')
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico("grafico_barras")
    # plt.show()


# def grafico_pizza(df):
#     vendas_por_regiao = df.groupby('Regiao')['Vendas'].sum()
#     plt.figure(figsize=(6, 6))
#     plt.pie(vendas_por_regiao, labels=vendas_por_regiao.index, autopct='%1.1f%%', startangle=90)
#     plt.title('Distribuição das Vendas por Região')
#     plt.axis('equal')
#     salvar_grafico("grafico_pizza")
#     # plt.show()


# def grafico_linha(df):
#     df['Data'] = pd.to_datetime(df['Data'])
#     df_por_dia = df.groupby('Data')['Vendas'].sum().reset_index()

#     plt.figure(figsize=(10, 5))
#     sns.lineplot(x='Data', y='Vendas', data=df_por_dia)
#     plt.title('Evolução das Vendas ao Longo do Tempo')
#     plt.tight_layout()
#     salvar_grafico("grafico_linha")
#     # plt.show()


# def grafico_histograma(df):
#     plt.figure(figsize=(8, 5))
#     sns.histplot(df['Lucro'], bins=20, kde=True)
#     plt.title('Distribuição dos Lucros')
#     plt.tight_layout()
#     salvar_grafico("grafico_histograma")
#     # plt.show()


# GRÁFICOS AVANÇADOS

def grafico_dispersao(df):
    plt.figure(figsize=(8, 5))
    df['estrelas_milhares'] = df['stars'] / 1000
    sns.scatterplot(x='estrelas_milhares', y='idade_dias', hue='stars', data=df)
    plt.title('Estrelas vs Idade dos Repositórios')
    plt.tight_layout()
    salvar_grafico("grafico_dispersao")
#     # plt.show()


def grafico_boxplot(df):
    # Pull request por linguagem
    top_repos = df['stars'].head(5)

    df["pulls_centenas"] = df["pull_requests_aceitas"] / 100
    df['pulls_intervalo'] = pd.cut(df["pulls_centenas"], bins=[0, 100, 200, 300, 400, 500], right=False)

    plt.figure(figsize=(12, 8))
    sns.boxplot(
        x="pulls_intervalo", 
        y="stars",
        data=df[df["stars"].isin(top_repos)]
    )
    
    plt.title("Distribuição de Pull Requests Aceitas")
    plt.xlabel("Intervalo de pulls(Centenas)")
    plt.ylabel("Estrelas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_grafico("grafico_boxplot")
    # plt.show()


# def grafico_heatmap(df):
#     df['Data'] = pd.to_datetime(df['Data'])
#     df['Mes'] = df['Data'].dt.month
#     tabela = pd.pivot_table(df, values='Vendas', index='Produto', columns='Mes', aggfunc='sum')

#     plt.figure(figsize=(10, 6))
#     sns.heatmap(tabela, annot=True, fmt=".0f", cmap="YlGnBu")
#     plt.title('Heatmap de Vendas por Produto e Mês')
#     plt.tight_layout()
#     salvar_grafico("grafico_heatmap")
#     # plt.show()


# def grafico_pairplot(df):
#     df['estrelas_milhares'] = df['stars'] / 1000
#     sns.pairplot(df[['estrelas_milhares', 'dias_desde_ultima_atualizacao']], kind='scatter')
#     plt.suptitle('Correlação entre Stars e Dias desde a Última Atualização', y=1.02)
#     salvar_grafico("grafico_pairplot")
#     # plt.show()


# def grafico_violin(df):
#     plt.figure(figsize=(8, 5))
#     sns.violinplot(x='Produto', y='Lucro', data=df, hue='Produto', palette='Set2', legend=False)
#     plt.title('Distribuição dos Lucros por Produto (Violin Plot)')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     salvar_grafico("grafico_violin")
#     # plt.show()


# def grafico_barras_empilhadas(df):
#     vendas_por_produto_regiao = df.groupby(['Produto', 'Regiao'])['Vendas'].sum().unstack()
#     vendas_por_produto_regiao.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
#     plt.title('Vendas por Produto e Região (Barras Empilhadas)')
#     plt.ylabel('Vendas Totais')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     salvar_grafico("grafico_barras_empilhadas")
#     # plt.show()


def main():
    coletar_dados()

    # Leitura dos dados
    df = pd.read_csv('linguagens_com_pull_request.csv')
    populares = pd.read_csv('repos_populares.csv')

    # Gráficos básicos
    grafico_barras(df)
    # grafico_pizza(df)
    # grafico_linha(df)
    # grafico_histograma(df)

    # Gráficos avançados
    grafico_dispersao(populares)
    grafico_boxplot(populares)
    # grafico_heatmap(df)
    # grafico_pairplot(populares)
    # grafico_violin(df)
    # grafico_barras_empilhadas(df)

if __name__ == '__main__':
    main()
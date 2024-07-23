import abstra.tables as at
import pandas as pd
from abstra.messages import send_email
from sklearn.metrics.pairwise import cosine_similarity


def coletar_e_preparar_avaliacoes():
    avaliacoes = at.select("avaliacoes")
    avaliacoes_df = pd.DataFrame(avaliacoes)
    matriz_usuario_filme = avaliacoes_df.pivot_table(
        index='id_usuario', columns='id_filme', values='nota').fillna(0)
    return matriz_usuario_filme


def calcular_similaridade(matriz_usuario_filme):
    similaridade_usuarios = cosine_similarity(matriz_usuario_filme)

    # Convertendo para DataFrame
    similaridade_usuarios_df = pd.DataFrame(
        similaridade_usuarios, index=matriz_usuario_filme.index, columns=matriz_usuario_filme.index)

    return similaridade_usuarios_df


def calcular_similaridade(matriz_usuario_filme):
    # Preenchimento de NaNs com 0 para simplificação
    matriz_usuario_filme = matriz_usuario_filme.fillna(0)

    # Calculando similaridades
    similaridade_usuarios = cosine_similarity(matriz_usuario_filme)

    # Convertendo para DataFrame
    similaridade_usuarios_df = pd.DataFrame(
        similaridade_usuarios, index=matriz_usuario_filme.index, columns=matriz_usuario_filme.index)

    return similaridade_usuarios_df


def recomendar_filmes(usuario_alvo, matriz_aval, similaridade_usuarios_df, filmes_dict, num_recommendacoes=2):
    if usuario_alvo not in similaridade_usuarios_df.index:
        return pd.Series()
    # Similaridade do usuário alvo com outros usuários
    similaridades = similaridade_usuarios_df[usuario_alvo].sort_values(
        ascending=False)

    # Filmes que o usuário não assistiu
    filmes_nao_assistidos = matriz_aval.loc[usuario_alvo][matriz_aval.loc[usuario_alvo] == 0].index

    recomendacoes = {}

    for filme in filmes_nao_assistidos:
        soma_similaridades = 0
        sum_weighted_ratings = 0

        for usuario in similaridades.index:
            if matriz_aval.loc[usuario, filme] > 0:  # Usuário avaliou o filme
                similarity_score = similaridades[usuario]
                soma_similaridades += similarity_score
                sum_weighted_ratings += similarity_score * \
                    matriz_aval.loc[usuario, filme]

        if soma_similaridades != 0:
            recomendacoes[filme] = sum_weighted_ratings / soma_similaridades
        else:
            recomendacoes[filme] = 0

    # Pegando os nomes dos filmes ao invés dos IDs
    recomendacoes_nomes = {
        filmes_dict[filme]: avaliacao for filme, avaliacao in recomendacoes.items()}

    # Ordenar recomendações
    recomendacoes_nomes = pd.Series(recomendacoes_nomes).sort_values(
        ascending=False).head(num_recommendacoes)
    return recomendacoes_nomes


def formatar_recomendacoes(recomendacoes, usuario_alvo):
    message = f"Recomendações de filmes para o usuário {usuario_alvo}:\n"
    message += "-" * 40 + "\n"

    for i, (filme, avaliacao) in enumerate(recomendacoes.items(), 1):
        message += f"{i}. Filme: {filme} | Avaliação estimada: {avaliacao:.2f}\n"

    message += "-" * 40
    return message


matriz_usuario_filme = coletar_e_preparar_avaliacoes()
similaridade_usuarios_df = calcular_similaridade(matriz_usuario_filme)

# Recomendando filmes para um cada usuário
usuarios = at.select("usuarios")
filmes = at.select("filmes")
filmes_dict = {filme["id"]: filme["nome"] for filme in filmes}
for usuario in usuarios:
    recomendacoes = recomendar_filmes(
        usuario["id"], matriz_usuario_filme, similaridade_usuarios_df, filmes_dict)

    # substituir id_filme pelo nome do filme
    print(f"Recomendações para o usuário {usuario['nome']}:")
    if recomendacoes.empty:
        continue
    message = formatar_recomendacoes(recomendacoes, usuario["nome"])
    send_email(usuario["email"], title=f"Recomendação para {usuario['nome']}",
               message=message)

import abstra.forms as af
import abstra.tables as at
import abstra.workflows as aw
import random

informacoes = af.Page().display_markdown(
"""
## 👋 Olá! Seja bem vindo ao avaliador de Filmes Sciety\n 
### Antes de iniciar a avaliação precisamos de alguns dados.

""")\
                .read("Nome e sobrenome", key="name")\
                .read_email("Email", key="email")\
                .run("Próximo")

name, email = informacoes["name"], informacoes["email"]

# Salvar usuario no banco de dados
id_usuario = at.insert("usuarios", {"nome": name, "email": email})["id"]

# ler lista de filmes e randomizar
lista_filmes = at.select("filmes")
random.shuffle(lista_filmes)

nome_filmes = [filme["nome"] for filme in lista_filmes]

# Criar Pagina para avaliar os filmes
pagina_avaliacoes = af.Page()
for filme in nome_filmes[:8]:
    avaliacao = pagina_avaliacoes.read_rating(f"Qual sua nota para {filme}?")
    
avaliacoes = pagina_avaliacoes.run("Enviar")

# Salvar as avaliações no banco de dados
for filme, avaliacao in zip(nome_filmes, avaliacoes):
    nota = avaliacao["nota"]
    id_filme = [f["id"] for f in lista_filmes if f["nome"] == filme][0]
    at.insert("avaliacoes", {"id_usuario": id_usuario, 
                             "id_filme": id_filme, 
                             "nota": nota})


# Enviar informações do usuario e dos filmes não avaliados para o sistema de recomendação
aw.set_data("usuario", {"id": id_usuario, "nome": name, "email": email})
aw.set_data("filmes", [f for f in lista_filmes if f["nome"] not in nome_filmes])
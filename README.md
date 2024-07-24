# Sistema de Recomendação de Filmes

Este projeto implementa um sistema de recomendação de filmes personalizado. Utiliza avaliações de usuários para calcular a similaridade entre eles e recomendar filmes que usuários similares gostaram.

## Como Funciona

O sistema segue os seguintes passos para recomendar filmes:

1. **Coleta e Preparação de Avaliações:** Primeiramente, coleta-se as avaliações dos usuários sobre diversos filmes e prepara-se uma matriz de usuário-filme.
2. **Cálculo de Similaridade:** Calcula-se a similaridade entre os usuários com base nas suas avaliações utilizando esta matriz.
3. **Recomendação de Filmes:** Para cada usuário, o sistema recomenda filmes que usuários similares avaliaram positivamente.
4. **Formatação das Recomendações:** As recomendações são formatadas em uma mensagem amigável, indicando o nome do filme e a avaliação estimada.
5. **Envio de Recomendações:** Por fim, as recomendações são enviadas para o e-mail do usuário, personalizadas com o nome do usuário e os filmes recomendados.

## Tecnologias Utilizadas

- Python: Linguagem principal para o desenvolvimento do sistema.
- Abstra: Visualização, banco de dados e envio de emails.
- Bibliotecas de análise de dados (ex: pandas): Para manipulação e análise dos dados de avaliações.

## Como Usar

Para utilizar o sistema, siga os passos abaixo:

1. **Preparação do Conjunto de Dados:** É necessário ter um conjunto de dados de avaliações de filmes por usuários. Este conjunto de dados pode ser coletado através de formulários públicos onde os usuários avaliam os filmes que assistiram.
2. **Preenchimento dos Formulários:** Os formulários de avaliação são públicos e podem ser acessados por qualquer usuário que deseje avaliar um filme. As avaliações coletadas serão utilizadas para alimentar o sistema de recomendação.
3. **Agendamento do Sistema de Recomendação:** O sistema de recomendação é agendado para rodar automaticamente todo mês. Ele processará as novas avaliações recebidas para atualizar as recomendações de filmes.
4. **Execução do Script:** Execute o script `sistema_de_recomendacao.py` para gerar as recomendações com base nas avaliações mais recentes.
5. **Envio de Recomendações:** As recomendações serão formatadas e enviadas automaticamente para o e-mail dos usuários, personalizadas com o nome do usuário e os filmes recomendados.

Siga estes passos para garantir que o sistema de recomendação funcione corretamente e forneça recomendações atualizadas para os usuários.

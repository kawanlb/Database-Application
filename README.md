# Database-Application
Trabalho para AV1 da materia de Database Application.


# Visão geral do projeto
Neste projeto, foi selecionado um conjunto de dados disponível no Kaggle, sendo video_games_sales o escolhido, um dataset dos jogos mais vendidos.<br> 

O objetivo é construir um modelo lógico e normalizar o conjunto de dados de acordo com as regras normais. Posteriormente, os dados normalizados serão inseridos em um banco de dados relacional.<br> 

Iremos utilizar a tecnologia NoSQL Redis, extraindo os dados colocados no MySQL para o Redis. 
 <br>


Nosso projeto tem como principal os arquivos:
- import_data.py
- mysql_connection.py
- redis_connection.py
- mysql_to_redis.py

# Tecnologias utilizadas
- Python
- Bibliotecas do python: pandas, redis-python, mysqlconnector,
- Redis
- MySQL
- Docker: simplifica o processo de desenvolvimento, implantação e execução, de forma fácil, dos aplicativos em ambientes isolados.


# Dependências

Para rodar o repositório só é necessário o Docker Desktop instalado.

# Tecnologia Redis

O Redis é um banco de dados que utiliza o armazenamento de estrutura de dados de <b>chave-valor</b> na memória RAM do computador. <br>

Frequentemente utilizado como um armazenamento em cache de dados para melhorar o desempenho de aplicativos da web, mas também pode ser usado como um banco de dados principal para uma variedade de casos de uso.

## Exemplos de principais comandos
<h3><b>Tipo String:</b></h3> 
SET nome_jogos GTA V (chave-valor) <br>
GET nome_jogos <br>
/ GTA V<br>
<h3><b>Tipo Lista:</b></h3> 
LSET nome_editoras 1 Nintendo<br>
LSET nome_editoras 2 SEGA<br>
LRANGE nome_editoras 0 -1 <br> 
1) Nintendo 2) SEGA
<h3><b>Tipo Conjunto:</b></h3> 
SADD genero:acao Metal Gear Solid <br>
SADD genero:acao Resident Evil<br>
SMEMBERS genero:acao<br>
/ Metal Gear Solid <br>
/ Resident Evil


## Benefícios:
- <b>Desempenho muito rápido</b>:         

    Os dados do Redis residem na memória principal do seu servidor. Evita atrasos de tempo de busca, acessando dados com algoritmos mais simples. <br>

- <b>Estruturas de dados na memória</b>:                     

    Armazena chaves de vários tipos de dados. Aceita tipos como strings, listas, conjuntos não ordenados e ordenados, hashes que armazenam uma lista de campos. <br>
- <b>Replicação e persistência</b>:       

    Arquitetura no estilo mestre/subordinado. Replica os dados para os subordinados. Para durabilidade, podem ser feitos snapshots, armazenando as alterações no disco.

# Tutorial de Uso
Este tutorial fornecerá instruções sobre como executar o projeto em seu ambiente usando Docker. Siga os seguintes passos:

1. Clonar o repositório
2. Iniciar o Docker Desktop
3. Fechar programas como XAMPP, MySQL Workbench, qualquer que use a porta 3306, pois pode causar conflito.
4. Rodar no terminal do Visual Studio Code os comandos: <br>

     <b>docker-compose up -d mysql redis</b>   <br> (Cria os containers MySQL e redis em segundo plano) <br>

     <b>docker-compose up -d import_data</b>   <br> (Cria o container para importação de dados ao MySQL) <br>

     <b>docker-compose up mysql_to_redis</b>    <br>(Insere do MySQL os dados no redis)<br>

5. Abra o terminal do computador e rode o seguinte comando:<br>

    <b>docker exec -it redis redis-cli</b>    <br>(Entra no container de redis)
6. Para visualização dos dados no redis, utilize os seguintes comandos: <br>

    <b>LRANGE nomes_jogos 0 -1 <br>
    LRANGE nomes_editoras 0 -1 <br>
    ZRANGE ranking_vendas 0 -1 WITHSCORES REV <br>
    SMEMBERS genero:action <br>
    SMEMBERS genero:sports  </b>


# Equipe 
- [Kawan Leandro](https://github.com/kawanlb)
- [Matheus Paiva](https://github.com/Matheus-A-Paiva)
- [Eduardo Marinho](https://github.com/EduardoMarinho237)
- [Pedro Henrique](https://github.com/PedroHTLeal)
- [Kaio Vitor](https://github.com/KaioVitor18)


# Etapas do projeto
## Seleção do Dataset
Escolhemos o dataset video_games_sales, que reúne dados de um ranking de jogos, baseado nas vendas totais em milhões em todas as regiões. <br>
Dicionário de dados explicando as colunas do dataset:

![Dicionário de dados](/images/dicionario_de_dados.png)

## Criação de modelos
Foi criado o modelo lógico normalizando o dataset, para após isso ser possível fazer o script DDL.

![Modelo logico](/DataModel/modelologico.png)

Relação 1:N entre jogo e gênero <br>
Relação N:N entre jogo e editora <br>
Relação N:N entre a tabela jogo_editora e plataforma. Um determinado jogo de determinada editora pode ter mais de uma plataforma e vice-versa <br>
Relação 1:N entre a tabela jogo_plataforma e vendas

## Criação das tabelas (DDL)
Criação dos scripts DDL baseado no modelo lógico para serem usados no banco de dados relacional. 

![Criação das tabelas](/images/DDL.png)

(Pasta: /ScriptsMysql)


## Conexão com MySQL

Foi feito um arquivo para conexão com o mysql, assim permitindo uma melhor organização ao projeto.

![Conexão MySQL](/images/mysql_connection.png)

## Conexão com Redis

Foi feito um arquivo para conexão com o redis também, na ideia de organização e recursividade.

![Conexão MySQL](/images/redis_connection.png)

## Import_data.py

Foi criado o arquvio import_data.py. Esse arquivo é um dos principais, sendo responsável por inserir os dados vindos do dataset video_games_sales no banco relacional. É importado a conexão mysql e a biblioteca pandas para leitura do dataset e manipulação do mesmo.


## Mysql_to_redis.py

Arquivo responsável por inserir do banco MySQL para o Redis. O arquivo importa as conexões do mysql e do redis, além de utilizar a biblioteca redis do python.



# Uso do Docker

Utilizamos o docker-compose para criação dos 4 containers principais:

![docker-compose](/images/docker_compose.png)

- Container mysql:
Responsável por criar um servidor MySQL e na sua inicialização rodar o script de Criação de tabelas

- Container redis:
Cria uma instância do servidor Redis.

- Container import_data:
Responsável por rodar o arquivo import_data.py, juntamente com o download das bibliotecas utilizadas e também copiar os arquivos utilizados no import_data.py

- Container mysql_to_redis:
Roda o arquivo mysql_to_redis e também baixa as bibliotecas e copia os arquivos utilizados no mysql_to_redis



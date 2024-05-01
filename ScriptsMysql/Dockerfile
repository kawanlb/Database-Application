# Criação da imagem para usar no container mysql
FROM mysql:latest

# Copia o arquivo script.sql para o diretório /docker-entrypoint-initdb.d/ dentro do contêiner
# Este diretório é usado pelo MySQL para executar scripts SQL durante a inicialização do contêiner
COPY ./script.sql /docker-entrypoint-initdb.d/
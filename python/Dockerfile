# Criação da imagem para usar no container de python import_data
FROM python:latest

RUN pip install mysql-connector-python pandas redis

# Define o diretório de trabalho dentro do contêiner como /app/script
WORKDIR /app/script

# Copia o arquivo import_data.py e video_games_sales.csv para o diretório de trabalho dentro do contêiner
COPY import_data.py ./
COPY video_games_sales.csv ./ 
COPY mysql_to_redis.py ./
COPY mysql_connection.py ./
COPY redis_connection.py ./

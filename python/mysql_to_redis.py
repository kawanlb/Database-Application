from mysql_connection import connect_to_db
from redis_connection import connect_to_redis

def insert_data_redis_batch(chave_redis, data):
    r = connect_to_redis()
    
    if not r:
        print("Não foi possível conectar ao Redis.")
        return False

    # Verifica se a chave já existe no Redis
    if r.exists(chave_redis):
        print("A chave já existe no Redis.")
        return False

    # Insere os dados em lotes
    try:
        with r.pipeline() as pipe:
            for item in data:
                pipe.rpush(chave_redis, item)
            pipe.execute()
    except Exception as e:
        print("Erro ao inserir dados no Redis:", e)
        return False
    
    print("Dados inseridos com sucesso no Redis.")
    return True

def ranking_vendas():
    r = connect_to_redis()
    conn = connect_to_db()

    cursor = conn.cursor()
    cursor.execute(""" 
        SELECT CONCAT(j.titulo,' - ', p.plataforma_nome) AS jogo_plataforma,
        SUM(v.vendas_na+v.vendas_eu+v.vendas_jp+v.outras_vendas) AS total_vendas FROM jogo j
        INNER JOIN jogo_editora je ON j.jogo_id =je.jogo_id 
        INNER JOIN jogo_plataforma jp ON je.jogo_editora_id =jp.jogo_editora_id 
        INNER JOIN venda v ON jp.jogo_plataforma_id = v.jogo_plataforma_id 
        INNER JOIN plataforma p ON jp.plataforma_id = p.plataforma_id
        GROUP BY CONCAT(j.titulo, ' - ', p.plataforma_nome) 
        ORDER BY total_vendas ASC
    """)
    resultado = cursor.fetchall()
    cursor.close()

    if resultado:
        r.delete("ranking_vendas")
        for row in resultado:
            jogo_plataforma = row[0]
            total_vendas = float(row[1])  # Convertendo Decimal para float
            r.zadd("ranking_vendas", {jogo_plataforma: total_vendas})
        print("Ranking de vendas criado e armazenado no Redis.")    
    else:
        print("Não há dados de vendas para criar o ranking.")

def jogo_genero(genero_id):
    r = connect_to_redis()
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT j.titulo, g.genero_nome
            FROM jogo j
            INNER JOIN genero g ON j.genero_id = g.genero_id 
            WHERE g.genero_id = %s
        """, (genero_id,))
    
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        nome_genero = resultados[0][1].lower()  # Obtém o nome do gênero
        conjunto_key = f"genero:{nome_genero}"
        for jogo, _ in resultados:
            r.sadd(conjunto_key, jogo)
        print("adicionado com sucesso genero")
        
    else:
        print("Não há dados de jogos para inserir no Redis.")

try:
    conn = connect_to_db()
    if not conn:
        print("Não foi possível conectar ao banco de dados MySQL.")
        exit(1)

    cursor = conn.cursor()

    # Consultas ao MySQL
    cursor.execute("SELECT titulo FROM jogo")
    resultados_jogos = cursor.fetchall()

    cursor.execute("SELECT editora_nome FROM editora")
    resultados_editoras = cursor.fetchall()

    conn.close()

    # Inserção de dados no Redis
    if resultados_jogos:
        nomes_jogos = [resultado[0] for resultado in resultados_jogos]
        insert_data_redis_batch("nomes_jogos", nomes_jogos)

    if resultados_editoras:
        nomes_editoras = [editora[0] for editora in resultados_editoras]
        insert_data_redis_batch("nomes_editoras", nomes_editoras)


except Exception as e:
    print("Erro:", e)


ranking_vendas()
#Sports
jogo_genero(1)
#Action
jogo_genero(9)

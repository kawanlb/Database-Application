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
    cursor.execute("SELECT plataforma.plataforma_nome, jogo.titulo FROM jogo_plataforma INNER JOIN plataforma ON jogo_plataforma.plataforma_id = plataforma.plataforma_id INNER JOIN jogo ON jogo_plataforma.jogo_editora_id = jogo.jogo_id")
    resultados_plataformas_jogos = cursor.fetchall()
    cursor.execute("SELECT jogo.titulo, venda.vendas_na, venda.vendas_eu, venda.vendas_jp, venda.outras_vendas FROM venda INNER JOIN jogo_plataforma ON venda.jogo_plataforma_id = jogo_plataforma.jogo_plataforma_id INNER JOIN jogo ON jogo_plataforma.jogo_editora_id = jogo.jogo_id")
    resultados_vendas = cursor.fetchall()

    conn.close()

    # Inserção de dados no Redis
    if resultados_jogos:
        nomes_jogos = [resultado[0] for resultado in resultados_jogos]
        insert_data_redis_batch("nome_jogos", nomes_jogos)

    if resultados_editoras:
        nomes_editoras = [editora[0] for editora in resultados_editoras]
        insert_data_redis_batch("nomes_editoras", nomes_editoras)

    if resultados_plataformas_jogos:
        dados_plataformas_jogos = [(plataforma_jogo[0], plataforma_jogo[1]) for plataforma_jogo in resultados_plataformas_jogos]
        insert_data_redis_batch("plataformas_jogos", dados_plataformas_jogos)

    if resultados_vendas:
        vendas_na = [float(venda[1]) for venda in resultados_vendas]
        vendas_eu = [float(venda[2]) for venda in resultados_vendas]
        vendas_jp = [float(venda[3]) for venda in resultados_vendas]
        outras_vendas = [float(venda[4]) for venda in resultados_vendas]
        
        insert_data_redis_batch("vendas_na", vendas_na)
        insert_data_redis_batch("vendas_eu", vendas_eu)
        insert_data_redis_batch("vendas_jp", vendas_jp)
        insert_data_redis_batch("outras_vendas", outras_vendas)

except Exception as e:
    print("Erro:", e)

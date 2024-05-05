from mysql_connection import connect_to_db
from redis_connection import connect_to_redis

def insert_data_redis(chave_redis, data):
    r = connect_to_redis()
    
    if not r:
        print("Não foi possível conectar ao Redis.")
        return False

    # Verifica se a chave já existe no Redis
    if r.exists(chave_redis):
        print("A chave já existe no Redis.")
        return False

    # Insere os dados no Redis
    for item in data:
        r.rpush(chave_redis, item)
    
    print("Dados inseridos com sucesso no Redis.")
    return True

try:
    conn = connect_to_db()
    if not conn:
        print("Não foi possível conectar ao banco de dados MySQL.")
        exit(1)

    cursor = conn.cursor()

    # Consulta para obter os nomes dos jogos
    cursor.execute("SELECT titulo FROM jogo")
    resultados = cursor.fetchall()

    # Consulta para obter os nomes das editoras
    cursor.execute("SELECT editora_nome FROM editora")
    editoras = cursor.fetchall()

    # Consulta para obter os nomes das plataformas
    cursor.execute("SELECT plataforma_nome FROM plataforma")
    plataformas = cursor.fetchall()

    conn.close()

    if resultados:
        nomes_jogos = [resultado[0] for resultado in resultados]
        chave_nomes_jogos = "nome_jogos"
        
        if insert_data_redis(chave_nomes_jogos, nomes_jogos):
            print("Consulta ao MySQL realizada e nomes dos jogos inseridos no Redis.")
        else:
            print("Erro ao inserir nomes dos jogos no Redis.")
    else:
        print("Nenhum dado encontrado na consulta ao MySQL.")

    if editoras:
        nomes_editoras = [editora[0] for editora in editoras]
        chave_editoras = "nomes_editoras"
        
        if insert_data_redis(chave_editoras, nomes_editoras):
            print("Consulta ao MySQL realizada e nomes das editoras inseridos no Redis.")
        else:
            print("Erro ao inserir nomes das editoras no Redis.")
    else:
        print("Nenhum dado encontrado na consulta ao MySQL para editoras.")

    if plataformas:
        nomes_plataformas = [plataforma[0] for plataforma in plataformas]
        chave_plataformas = "nomes_plataformas"
        
        if insert_data_redis(chave_plataformas, nomes_plataformas):
            print("Consulta ao MySQL realizada e nomes das plataformas inseridos no Redis.")
        else:
            print("Erro ao inserir nomes das plataformas no Redis.")
    else:
        print("Nenhum dado encontrado na consulta ao MySQL para plataformas.")

except Exception as e:
    print("Erro:", e)

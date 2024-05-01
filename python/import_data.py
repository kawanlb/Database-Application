import pandas as pd
import mysql.connector


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='mysql',  # Nome do serviço no Docker Compose
            port="3306",     # Porta do MySQL
            user='root',
            password='root',
            database='games_sales'
        )
        print("Conexão com o banco de dados MySQL estabelecida com sucesso!")
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados MySQL: {e}")
        return None

#começa a adicionar os dados do dataset para o banco de dados
def insert_data(conn, table_name, data):
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(data.values()))
    conn.commit()
    return cursor.lastrowid

try:
    # alterar para o caminho do arquivo do dataset local
    df = pd.read_csv('video_games_sales.csv', nrows=50)

    # None para valores void
    df = df.where(pd.notnull(df), None)

    df['year'] = df['year'].astype(int)

    conn = connect_to_db()

    genres = df['genre'].unique()
    for genre in genres:
        insert_data(conn, 'genero', {'genero_nome': genre})

    publishers = df['publisher'].unique()
    for publisher in publishers:
        if publisher is not None:
            insert_data(conn, 'editora', {'editora_nome': publisher})

    platforms = df['platform'].unique()
    for platform in platforms:
        insert_data(conn, 'plataforma', {'plataforma_nome': platform})

    for index, row in df.iterrows():
        cursor = conn.cursor()
        cursor.execute("SELECT genero_id FROM genero WHERE genero_nome = %s", (row['genre'],))
        genero_id = cursor.fetchone()[0]
        cursor.close()
        
        jogo_id = insert_data(conn, 'jogo', {'genero_id': genero_id, 'titulo': row['name']})

        editora_id = None
        if row['publisher'] is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT editora_id FROM editora WHERE editora_nome = %s", (row['publisher'],))
            result = cursor.fetchone()
            cursor.close()
            if result:
                editora_id = result[0]
        if editora_id is not None:
            jogo_editora_id = insert_data(conn, 'jogo_editora', {'jogo_id': jogo_id, 'editora_id': editora_id})

            ano_lancamento = row['year']
            plataforma_id = platforms.tolist().index(row['platform']) + 1
            insert_data(conn, 'jogo_plataforma', {'jogo_editora_id': jogo_editora_id, 'plataforma_id': plataforma_id, 'ano_lancamento': ano_lancamento})

            insert_data(conn, 'venda', {'jogo_plataforma_id': jogo_editora_id, 'vendas_na': row['na_sales'], 
                                         'vendas_eu': row['eu_sales'], 'vendas_jp': row['jp_sales'], 
                                         'outras_vendas': row['other_sales']})

    print("Data inserted successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if 'conn' in locals():
        conn.close()

import pandas as pd
import mysql.connector


def connect_to_db():#alterar de acordo com o servidor sql:
    return mysql.connector.connect(
        host='172.17.0.2', 
        port=3306,
        user='root',
        password='1234',
        database='games_sales'
    )

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
    df = pd.read_csv('./video_games_sales.csv')

    # None para valores void
    df = df.where(pd.notnull(df), None)

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
        
            plataforma_id = platforms.tolist().index(row['platform']) + 1
            insert_data(conn, 'jogo_plataforma', {'jogo_editora_id': jogo_editora_id, 'plataforma_id': plataforma_id})

            insert_data(conn, 'venda', {'jogo_plataforma_id': jogo_editora_id, 'vendas_na': row['na_sales'], 
                                         'vendas_eu': row['eu_sales'], 'vendas_jp': row['jp_sales'], 
                                         'outras_vendas': row['other_sales']})

    print("Data inserted successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if 'conn' in locals():
        conn.close()

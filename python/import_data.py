import pandas as pd
from mysql_connection import connect_to_db

def insert_data(conn, table_name, data):
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(data.values()))
    conn.commit()
    return cursor.lastrowid

# Função para limpar valores não numéricos na coluna 'year' e converter para inteiro
def clean_year(year):
    try:
        return int(year)
    except (ValueError, TypeError):
        return None

try:
    print("Conectando ao banco de dados MySQL...")
    conn = connect_to_db()
    if conn:
        print("Conexão com o banco de dados MySQL estabelecida com sucesso!")

        # Alterar para o caminho do arquivo do dataset local
        df = pd.read_csv('video_games_sales.csv', nrows=500)

        # Remover valores não numéricos da coluna 'year' e converter para inteiro
        df['year'] = df['year'].apply(clean_year)

        # Remover linhas com valores ausentes em outras colunas
        df.dropna(subset=['year', 'genre', 'publisher', 'platform'], inplace=True)

        genres = df['genre'].unique()
        for genre in genres:
            insert_data(conn, 'genero', {'genero_nome': genre})

        publishers = df['publisher'].unique()
        for publisher in publishers:
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
                insert_data(conn, 'jogo_plataforma', {'jogo_editora_id': jogo_editora_id, 'plataforma_id': plataforma_id, 'ano_lancamento': row['year']})

                insert_data(conn, 'venda', {'jogo_plataforma_id': jogo_editora_id, 'vendas_na': row['na_sales'], 
                                             'vendas_eu': row['eu_sales'], 'vendas_jp': row['jp_sales'], 
                                             'outras_vendas': row['other_sales']})

        print("Dados inseridos com sucesso!")
    
    else:
        print("Não foi possível estabelecer conexão com o banco de dados MySQL.")

except Exception as e:
    print("Erro:", e)

finally:
    if 'conn' in locals():
        conn.close()

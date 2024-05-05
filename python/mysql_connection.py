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

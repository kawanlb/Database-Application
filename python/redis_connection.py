import redis

def connect_to_redis():
    try:
        r = redis.Redis(host='redis', port="6379", db=0)
        if r.ping():
            print("Conexão com o Redis estabelecida com sucesso!")
            return r
        else:
            print("Erro ao conectar ao Redis")
            return None
    except Exception as e:
        print(f"Erro ao conectar ao Redis: {e}")
        return None

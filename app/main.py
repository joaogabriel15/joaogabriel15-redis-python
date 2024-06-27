# Uncomment this to pass the first stage
import socket
import threading
from argparse import ArgumentParser


db = {}


def redis_encode(data, encoding="utf-8"):
    
    if not isinstance(data, list):
        data = [data]
   
    separador = "\r\n"
    size = len(data)
    encoded = []

    for item in data:
        encoded.append(f"${len(item)}")
        encoded.append(item)

    if size > 1:
        encoded.insert(0, f"*{size}")
    
    return (separador.join(encoded) + separador).encode(encoding=encoding)

def redis_set(data, time=None):
    key = data[3].decode("utf-8")
    inf = data[5].decode("utf-8")

    db[key] = inf

    if time is None:
        return
    print("tempo")
    threading.Timer(float(time.decode("utf-8")) / 1000, redis_remove,(key,)).start()

def redis_remove(key):
    del db[key]

def handle_connection(conn, addr, role):
    while True:
        data = conn.recv(1024)

        if not data:
            break

        arr_size, *arr = data.split(b"\r\n")
        
        if arr[1].lower() == b"ping":
            response = redis_encode("PONG")
            conn.sendall(response)

        elif arr[1].lower() == b"echo":
            response = redis_encode([el.decode("utf-8") for el in arr[3::2]])
            conn.sendall(response)

        elif arr[1].lower() == b"set":
            print(arr)
            if len(arr) > 7:
                if arr[7].lower() == b"px":
                    redis_set(arr, arr[9])
            else:
                redis_set(arr)
            
            response = redis_encode("OK")
            conn.sendall(response)

        elif arr[1].lower() == b"get":
            response = "$-1\r\n".encode("utf-8")

            if arr[3].decode("utf-8") in db.keys():
                response = redis_encode(db[arr[3].decode("utf-8")])
           
            conn.sendall(response)

        elif arr[1].lower() == b"info":
            print(role)
            response = redis_encode(f"role:{role}")
            conn.sendall(response)

        else:
            break

   

def main():
    parser = ArgumentParser("Redis Python")
    parser.add_argument("--port", type=int, default=6379)
    parser.add_argument("--replicaof",  default="master")

    server = socket.create_server(('localhost', parser.parse_args().port), reuse_port=True)


    role = parser.parse_args().replicaof

    while True:
        conn, client_addr = server.accept()

        try:
            threading.Thread(target=handle_connection, args=[conn, client_addr, role]).start()


        except Exception as e:
            print(e)
            conn.close()

   
            

    

if __name__ == "__main__":
    main()

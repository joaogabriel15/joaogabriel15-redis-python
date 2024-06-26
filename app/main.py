# Uncomment this to pass the first stage
import socket
import threading


def redis_encode(data, encoding="utf-8"):
    if not isinstance(data, list):
        data = [data]

    separador = "\r\n"
    size = len(data)
    encoded = []

    for item in data:
        encoded.append(f"${len(item)}")
        encoded.append(item)

    print(encoded)
    if size > 1:
        encoded.insert(0, f"*{size}")
    
    print(encoded)

    return (separador.join(encoded) + separador).encode(encoding=encoding)

def handle_connection(conn, addr):
    while True:
        data = conn.recv(1024)

        if not data:
            break

        arr_size, *arr = data.split(b"\r\n")
        print(f"Arr size: {arr_size}")
        print(f"Arr content: {arr}")
        
        if arr[1].lower() == b"ping":
            response = redis_encode("PONG")

            conn.sendall(response)
        elif arr[1].lower() == b"echo":
            response = redis_encode([el.decode("utf-8") for el in arr[3::2]])
            print(response)
            conn.sendall(response)
        else:
            break

    conn.close()


def main():
    server = socket.create_server(('localhost', 6379), reuse_port=True)
    clients = {}

    while True:
        conn, client_addr = server.accept()

        try:
            threading.Thread(target=handle_connection, args=[conn, client_addr]).start()


        except Exception as e:
            print(e)
            conn.close()

   
            

    

if __name__ == "__main__":
    main()

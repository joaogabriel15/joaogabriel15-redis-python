# Uncomment this to pass the first stage
import socket
import threading


def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data = request.decode().split(' ')
        command = data[0]

        if "ping" in command.lower():
            response = "+PONG\r\n"
            print(response)
            conn.send(response.encode())
        if "echo" in command.lower():
            if data[1] == None:
                conn.send("")
            response = data[1]
            print(response)
            conn.send(response.encode())

    conn.close()



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # server_socket.accept() # wait for client
    server_socket = socket.create_server(('localhost',6379), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_connection, args=[client_socket, client_address]).start()


   
            

    

if __name__ == "__main__":
    main()

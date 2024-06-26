# Uncomment this to pass the first stage
import socket
import threading


def response_template(data, fist_byte='+'):
    info = ""
    
    if len(data.rstrip().split()) > 1:
        info = data.rstrip().split()[1]

    match fist_byte:
        case '+' :
            print(f'{fist_byte}{info}\r\n')
            return f'{fist_byte}{info}\r\n'
        case '-':
            print(fist_byte)
            return f'{fist_byte}{info}\r\n'
        case ':':
            print(fist_byte)
        case '$':
            print(f'{fist_byte}{len(info)}\r\n{info}\r\n')
            return f'{fist_byte}{len(info)}\r\n{info}\r\n'
        case '*':
            print(fist_byte)
        case '_':
            print(fist_byte)
        case '#':
            print(fist_byte)
        case '(':
            print(fist_byte)
        case '!':
            print(fist_byte)
        case '=':
            print(fist_byte)
        case '%':
            print(fist_byte)
        case '~':
            print(fist_byte)
        case '>':
            print(fist_byte)
    


def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break

        data = request.decode()
        split_data = data.split("\r\n")
        
        print(data.split("\r\n"))

        command = split_data[0]

        if "ping" in command.lower():
            response = "+PONG\r\n"
            conn.send(response.encode())
        if "echo" in command.lower():
            response = response_template(data, '$')
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

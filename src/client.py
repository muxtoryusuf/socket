import socket
import threading


def handle_messages(connection: socket.socket):
    # print("handle_messages.....", connection)
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break
        except Exception as e:
            print(f'Error handle_messages from server: {e.args}')
            connection.close()
            break


def client() -> None:
    socket_instance = socket.socket()
    try:
        socket_instance.connect(('127.0.0.1', 12000))  # Instantiate socket and start connection with server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()  # Create a thread to handle messages sent by server
        print('Connected to chat!')
        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break
            socket_instance.send(msg.encode())  # Parse message to utf-8
        socket_instance.close()
    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":
    client()
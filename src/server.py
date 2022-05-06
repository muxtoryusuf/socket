import socket
import threading

connections = []


def handle_user_connection(connection: socket.socket, address: str) -> None:
    # print("handle_user_connection..", connection, address)
    while True:
        try:
            msg = connection.recv(1024)  # Get client message
            if msg:
                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                check_connection(msg_to_send, connection)
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e.args}')
            remove_connection(connection)
            break


def check_connection(message: str, connection: socket.socket) -> None:
    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                client_conn.send(message.encode())  # Sending message to client connection
            except Exception as e:
                print(f'Error connection message: {e.args}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    if conn in connections:
        conn.close()
        connections.remove(conn)


def server() -> None:
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance.bind(('127.0.0.1', 12000))
        socket_instance.listen(4)
        print('Server running!')

        while True:
            # Accept client connection
            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)  # append client connection
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e.args}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)
        socket_instance.close()


if __name__ == "__main__":
    server()
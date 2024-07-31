import socket
import select

LISTEN_IP = '0.0.0.0'  # Listen on all interfaces
LISTEN_PORT = 4444
TIMEOUT = 10  # Timeout in seconds


def handle_client(conn, addr):
    print(f"Connection from {addr}")

    try:
        while True:
            command = input("Shell> ")
            if command.lower() == 'exit':
                conn.sendall(b'exit')
                break

            conn.sendall(command.encode('utf-8'))

            data = b""
            while True:
                ready = select.select([conn], [], [], TIMEOUT)
                if ready[0]:
                    chunk = conn.recv(4096)
                    if not chunk:
                        print("Connection closed by client.")
                        return
                    data += chunk
                else:
                    break

            if data:
                print(data.decode('utf-8'), end='')
            else:
                print("No output received or command produces no output.")
    except (ConnectionResetError, ConnectionAbortedError):
        print("Connection was lost.")
    finally:
        conn.close()


def listen():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((LISTEN_IP, LISTEN_PORT))
        s.listen(1)
        print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}...")

        conn, addr = s.accept()
        handle_client(conn, addr)
        print("Waiting for new connection...")


if __name__ == "__main__":
    listen()


import socket

LISTEN_IP = '0.0.0.0'  # Listen on all interfaces
LISTEN_PORT = 4444


def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LISTEN_IP, LISTEN_PORT))
    s.listen(1)
    print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}...")

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    while True:
        command = input("Shell> ")
        if command.lower() == 'exit':
            conn.send(b'exit')
            break

        conn.send(command.encode('utf-8'))
        output = conn.recv(1024).decode('utf-8')
        print(output)

    conn.close()


if __name__ == "__main__":
    listen()

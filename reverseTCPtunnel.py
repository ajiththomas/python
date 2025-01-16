import socket
import threading

# Forward data between two sockets
def forward(src, dest):
    while True:
        try:
            data = src.recv(1024)
            if not data:
                break
            dest.sendall(data)
        except:
            break
    src.close()
    dest.close()

# Reverse tunnel server
def reverse_tunnel(local_port, remote_host, remote_port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("0.0.0.0", local_port))
    listener.listen(5)
    print(f"Listening on port {local_port}...")

    while True:
        client, _ = listener.accept()
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((remote_host, remote_port))

        # Start bidirectional forwarding
        threading.Thread(target=forward, args=(client, remote)).start()
        threading.Thread(target=forward, args=(remote, client)).start()

# Start the reverse tunnel
reverse_tunnel(8080, "remote.server.com", 80)

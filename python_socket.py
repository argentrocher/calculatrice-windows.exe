import socket
import threading

print("test client 3 pour (test) serveur 3")
print("ip récente : '192.168.0.13' du serveur")

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
        except Exception as e:
            print("Erreur réception :", e)
            client_socket.close()
            break

def main():
    global ip
    global port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((str(ip), int(port)))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("message :")
        client.send(message.encode('utf-8'))

ip = input("IP connexion : ('localhost')")
port = input("Port de connexion : (9999)")

main()

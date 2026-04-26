from socket import *
import time
print("Cliente iniciou")
serverName = "localhost"   # servidor local
serverPort = 12000         # mesma porta do servidor UDP

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # espera até 1 segundo

rtts = []
lost = 0

print("Iniciando testes de ping...\n")

for i in range(10):
    send_time = time.time()
    message = f"Ping {i} {send_time}"

    try:
        # envia mensagem
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # recebe resposta
        data, _ = clientSocket.recvfrom(1024)
        recv_time = time.time()

        rtt = (recv_time - send_time) * 1000
        rtts.append(rtt)

        print(f"Resposta: {data.decode()} | RTT = {round(rtt,2)} ms")

    except (timeout, ConnectionResetError):
        print("Timeout ou pacote perdido")
        lost += 1

# estatísticas finais
print("\n--- Estatísticas ---")

if rtts:
    media = sum(rtts) / len(rtts)
    print(f"RTT médio: {round(media,2)} ms")
else:
    print("Nenhuma resposta recebida")

loss_rate = (lost / 10) * 100
print(f"Taxa de perda: {loss_rate}%")

clientSocket.close()
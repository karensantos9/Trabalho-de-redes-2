from socket import *
import datetime
import os

print("Diretório atual:", os.getcwd())

serverPort = 8080

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print("Servidor Web rodando na porta", serverPort)

while True:
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(1024).decode()

        if not message:
            connectionSocket.close()
            continue

        try:
            filename = message.split()[1]
        except:
            connectionSocket.close()
            continue

        print(f"[{datetime.datetime.now()}] Cliente {addr} pediu {filename}")
        print(message)

        if filename == "/":
            filename = "/index.html"

        if filename == "/hora":
            body = f"<html><body><h1>Hora atual</h1><p>{datetime.datetime.now()}</p></body></html>"

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += "Content-Length: " + str(len(body.encode())) + "\r\n"
            response += "Connection: close\r\n"
            response += "\r\n"
            response += body

            connectionSocket.sendall(response.encode())
            connectionSocket.close()
            continue

        filename = filename[1:]

        with open(filename, "r", encoding="utf-8") as f:
            outputdata = f.read()

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += "Content-Length: " + str(len(outputdata.encode())) + "\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += outputdata

        connectionSocket.sendall(response.encode())

    except FileNotFoundError:
        body = "<h1>404 - Arquivo não encontrado</h1>"

        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: " + str(len(body.encode())) + "\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        connectionSocket.sendall(response.encode())
    
    connectionSocket.close()
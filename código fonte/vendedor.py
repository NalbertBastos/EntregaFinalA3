import socket
import json

class Vendedor:
    def __init__(self, server_address):
        self.server_address = server_address

    def informar_venda(self):
        vendedor = input("Nome do vendedor: ")
        loja = input("Identificação da loja: ")
        data = input("Data da venda (DD/MM/AAAA): ")
        valor = float(input("Valor da venda: "))

        venda = {
            "vendedor": vendedor,
            "loja": loja,
            "data": data,
            "valor": valor
        }

        message = json.dumps({"operation": "informar_venda", "data": venda})
        response = self.enviar_mensagem(message)
        print(response)

    def enviar_mensagem(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            sock.sendall(message.encode())
            response = sock.recv(1024).decode()
            return response

servidor_address = ('127.0.0.1', 5000)
vendedor = Vendedor(servidor_address)

while True:
    print("Escolha uma opção:")
    print("1 - Informar venda")
    print("0 - Sair")
    option = input("Opção: ")

    if option == '1':
        vendedor.informar_venda()
    elif option == '0':
        break
    else:
        print("Opção inválida. Tente novamente.")
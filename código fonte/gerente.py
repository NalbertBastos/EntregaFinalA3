import socket
import json

class Gerente:
    def __init__(self, server_address):
        self.server_address = server_address

    def consultar_vendas_vendedor(self):
        vendedor = input("Nome do vendedor: ")
        message = json.dumps({"operation": "consultar_vendas_vendedor", "data": vendedor})
        response = self.enviar_mensagem(message)
        print(f"Total de vendas do vendedor {vendedor}: {response}")

    def consultar_vendas_loja(self):
        loja = input("Identificação da loja: ")
        message = json.dumps({"operation": "consultar_vendas_loja", "data": loja})
        response = self.enviar_mensagem(message)
        print(f"Total de vendas da loja {loja}: {response}")

    def consultar_vendas_periodo(self):
        data_inicial = input("Data inicial (DD/MM/AAAA): ")
        data_final = input("Data final (DD/MM/AAAA): ")
        message = json.dumps({"operation": "consultar_vendas_periodo", "data": {"data_inicial": data_inicial, "data_final": data_final}})
        response = self.enviar_mensagem(message)
        print(f"Total de vendas no período de {data_inicial} a {data_final}: {response}")

    def consultar_melhor_vendedor(self):
        message = json.dumps({"operation": "consultar_melhor_vendedor"})
        response = self.enviar_mensagem(message)
        print(f"Melhor vendedor: {response}")

    def consultar_melhor_loja(self):
        message = json.dumps({"operation": "consultar_melhor_loja"})
        response = self.enviar_mensagem(message)
        print(f"Melhor loja: {response}")

    def enviar_mensagem(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            sock.sendall(message.encode())
            response = sock.recv(1024).decode()
            return response

servidor_address = ('127.0.0.1', 5000)
gerente = Gerente(servidor_address)

while True:
    print("Escolha uma opção:")
    print("1 - Consultar vendas de um vendedor")
    print("2 - Consultar vendas de uma loja")
    print("3 - Consultar vendas em um período")
    print("4 - Consultar melhor vendedor")
    print("5 - Consultar melhor loja")
    print("0 - Sair")
    option = input("Opção: ")

    if option == '1':
        gerente.consultar_vendas_vendedor()
    elif option == '2':
        gerente.consultar_vendas_loja()
    elif option == '3':
        gerente.consultar_vendas_periodo()
    elif option == '4':
        gerente.consultar_melhor_vendedor()
    elif option == '5':
        gerente.consultar_melhor_loja()
    elif option == '0':
        break
    else:
        print("Opção inválida. Tente novamente.")
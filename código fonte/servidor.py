import socket
import json
import sqlite3

class Servidor:
    def __init__(self, address):
        self.address = address
        self.database = 'vendas.db'
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vendas
                          (vendedor text, loja text, data text, valor real)''')
        conn.commit()
        conn.close()

    def incluir_venda(self, venda):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas VALUES (?, ?, ?, ?)", (venda['vendedor'], venda['loja'], venda['data'], venda['valor']))
        conn.commit()
        conn.close()

    def consultar_vendas_vendedor(self, vendedor):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(valor) FROM vendas WHERE vendedor = ?", (vendedor,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def consultar_vendas_loja(self, loja):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(valor) FROM vendas WHERE loja = ?", (loja,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def consultar_vendas_periodo(self, data_inicial, data_final):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(valor) FROM vendas WHERE data >= ? AND data <= ?", (data_inicial, data_final))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def consultar_melhor_vendedor(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT vendedor, SUM(valor) FROM vendas GROUP BY vendedor ORDER BY SUM(valor) DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def consultar_melhor_loja(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT loja, SUM(valor) FROM vendas GROUP BY loja ORDER BY SUM(valor) DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def iniciar_servidor(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen(1)
            print("Servidor iniciado. Aguardando conexões...")

            while True:
                conn, addr = sock.accept()
                with conn:
                    print(f"Conexão estabelecida com {addr[0]}:{addr[1]}")
                    while True:
                        data = conn.recv(1024).decode()
                        if not data:
                            break

                        message = json.loads(data)
                        operation = message.get('operation')

                        if operation == 'informar_venda':
                            venda = message.get('data')
                            self.incluir_venda(venda)
                            conn.sendall("OK".encode())
                        elif operation == 'consultar_vendas_vendedor':
                            vendedor = message.get('data')
                            total_vendas = self.consultar_vendas_vendedor(vendedor)
                            conn.sendall(str(total_vendas).encode())
                        elif operation == 'consultar_vendas_loja':
                            loja = message.get('data')
                            total_vendas = self.consultar_vendas_loja(loja)
                            conn.sendall(str(total_vendas).encode())
                        elif operation == 'consultar_vendas_periodo':
                            data_inicial = message.get('data').get('data_inicial')
                            data_final = message.get('data').get('data_final')
                            total_vendas = self.consultar_vendas_periodo(data_inicial, data_final)
                            conn.sendall(str(total_vendas).encode())
                        elif operation == 'consultar_melhor_vendedor':
                            melhor_vendedor = self.consultar_melhor_vendedor()
                            conn.sendall(str(melhor_vendedor).encode())
                        elif operation == 'consultar_melhor_loja':
                            melhor_loja = self.consultar_melhor_loja()
                            conn.sendall(str(melhor_loja).encode())
                        else:
                            conn.sendall("ERRO: Operação inválida".encode())
    
                   

servidor_address = ('127.0.0.1', 5000)
servidor = Servidor(servidor_address)
servidor.iniciar_servidor()

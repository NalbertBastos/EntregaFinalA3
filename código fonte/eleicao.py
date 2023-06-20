import socket
import threading

class EleicaoServidorTemporario:
    def __init__(self, servers):
        self.servers = servers
        self.election_in_progress = False
        self.elected_server = None

    def iniciar_eleicao(self):
        if not self.election_in_progress:
            self.election_in_progress = True
            self.elected_server = None
            print("Iniciando processo de eleição do servidor temporário...")

            # Envia uma mensagem de eleição para cada servidor na lista
            for server in self.servers:
                threading.Thread(target=self.enviar_mensagem_eleicao, args=(server,)).start()

    def enviar_mensagem_eleicao(self, server):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(server)
                sock.sendall(b"ELEICAO")
                response = sock.recv(1024).decode()

                # Se receber uma resposta do servidor, significa que ele já está ativo como primário
                if response == "ATIVO":
                    self.elected_server = server
                    print(f"Servidor {server} eleito como servidor temporário.")
            except:
                pass

    def verificar_eleicao_concluida(self):
        if self.election_in_progress:
            if self.elected_server:
                print("Eleição concluída. Servidor temporário ativo.")
            else:
                print("Eleição concluída. Nenhum servidor temporário eleito.")
            self.election_in_progress = False

servers = [('127.0.0.1', 5000), ('127.0.0.1', 5001), ('127.0.0.1', 5002)]

eleicao = EleicaoServidorTemporario(servers)
eleicao.iniciar_eleicao()
eleicao.verificar_eleicao_concluida()
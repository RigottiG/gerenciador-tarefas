from models.tarefa import Tarefa


class Projeto:
    contador_id = 1
    projetos = []

    def __init__(self, nome: str, descricao: str, usuario_id: int):
        self.id = Projeto.contador_id
        self.nome = nome
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.tarefas = []
        Projeto.contador_id += 1
        Projeto.projetos.append(self)

    def adicionar_tarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)

    def remover_tarefa(self, tarefa: Tarefa):
        if tarefa in self.tarefas:
            self.tarefas.remove(tarefa)
            tarefa.apagar()
            return True
        return False

    def listar_tarefas(self):
        return self.tarefas

    def criar_tarefa(self, titulo: str, descricao: str, data_limite: str, prioridade: str, usuario_id: int):
        tarefa = Tarefa(titulo, descricao, data_limite, prioridade, usuario_id)
        self.adicionar_tarefa(tarefa)
        return tarefa

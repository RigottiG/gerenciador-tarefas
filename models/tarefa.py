from models.etiqueta import Etiqueta
from models.notificacao import NotificacaoPopup


class Tarefa:
    contador_id = 1
    tarefas = []

    def __init__(self, titulo: str, descricao: str, data_limite: str, prioridade: str, usuario_id: int):
        self.id = Tarefa.contador_id
        self.titulo = titulo
        self.descricao = descricao
        self.data_limite = data_limite
        self.prioridade = prioridade
        self.usuario_id = usuario_id
        self.concluida = False
        self.subtarefas = []
        self.etiquetas = []
        self.notificacao = NotificacaoPopup(self)
        Tarefa.contador_id += 1
        Tarefa.tarefas.append(self)

    def adicionar_subtarefa(self, subtarefa):
        self.subtarefas.append(subtarefa)

    def adicionar_etiqueta(self, etiqueta: Etiqueta):
        self.etiquetas.append(etiqueta)

    def marcar_como_concluida(self):
        self.concluida = True
        self.notificacao.enviar_notificacao()

    def desmarcar_como_concluida(self):
        self.concluida = False

    def apagar(self):
        if self in Tarefa.tarefas:
            Tarefa.tarefas.remove(self)
        return True

    @staticmethod
    def listar_todas():
        return Tarefa.tarefas

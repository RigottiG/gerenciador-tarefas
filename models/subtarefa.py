from models.tarefa import Tarefa


class Subtarefa(Tarefa):
    def __init__(self, titulo, descricao, data_limite, prioridade, usuario_id, tarefa_pai):
        super().__init__(titulo, descricao, data_limite, prioridade, usuario_id)
        self.tarefa_pai = tarefa_pai
        tarefa_pai.adicionar_subtarefa(self)

    def get_tarefa_pai(self):
        return self.tarefa_pai
        
    def remover_da_tarefa_pai(self):
        if self.tarefa_pai and self in self.tarefa_pai.subtarefas:
            self.tarefa_pai.subtarefas.remove(self)
            self.tarefa_pai = None
            
    def transferir_para_tarefa(self, nova_tarefa_pai):
        self.remover_da_tarefa_pai()
        self.tarefa_pai = nova_tarefa_pai
        nova_tarefa_pai.adicionar_subtarefa(self)

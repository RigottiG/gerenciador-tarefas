from abc import ABC, abstractmethod
from tkinter import messagebox


class Notificacao(ABC):
    def __init__(self, tarefa):
        self.tarefa = tarefa

    @abstractmethod
    def enviar_notificacao(self):
        pass


class NotificacaoPopup(Notificacao):
    def enviar_notificacao(self):
        messagebox.showinfo(
            "Tarefa Concluída",
            f"A tarefa '{self.tarefa.titulo}' foi marcada como concluída!"
        )


class NotificacaoSMS(Notificacao):
    def enviar_notificacao(self):
        return f"SMS: Tarefa '{self.tarefa.titulo}' foi concluída!"


class NotificacaoEmail(Notificacao):
    def enviar_notificacao(self):
        return f"Email: Tarefa '{self.tarefa.titulo}' foi concluída!"

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.usuario import Usuario
from abc import ABC, abstractmethod


class Tela(ABC):
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = None

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    @abstractmethod
    def mostrar(self):
        pass


class TelaLogin(Tela):
    def mostrar(self):
        self.limpar_tela()
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Campos de login
        ttk.Label(self.frame, text="E-mail:").grid(row=0, column=0, pady=5)
        email = ttk.Entry(self.frame)
        email.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame, text="Senha:").grid(row=1, column=0, pady=5)
        senha = ttk.Entry(self.frame, show="*")
        senha.grid(row=1, column=1, pady=5)

        # Botões
        ttk.Button(self.frame, text="Login", 
                  command=lambda: self.fazer_login(email.get(), senha.get())).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame, text="Registrar", 
                  command=lambda: self.app.mudar_tela("registro")).grid(row=3, column=0, columnspan=2)

    def fazer_login(self, email, senha):
        try:
            self.app.usuario_atual = Usuario.autenticar(email, senha)
            self.app.mudar_tela("projetos")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


class TelaRegistro(Tela):
    def mostrar(self):
        self.limpar_tela()

        # Campos de registro
        ttk.Label(self.frame, text="Nome:").grid(row=0, column=0, pady=5)
        nome = ttk.Entry(self.frame)
        nome.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame, text="E-mail:").grid(row=1, column=0, pady=5)
        email = ttk.Entry(self.frame)
        email.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Senha:").grid(row=2, column=0, pady=5)
        senha = ttk.Entry(self.frame, show="*")
        senha.grid(row=2, column=1, pady=5)

        # Botões
        ttk.Button(self.frame, text="Registrar", 
                  command=lambda: self.fazer_registro(nome.get(), email.get(), senha.get())).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame, text="Voltar", 
                  command=lambda: self.app.mudar_tela("login")).grid(row=4, column=0, columnspan=2)

    def fazer_registro(self, nome, email, senha):
        try:
            self.app.usuario_atual = Usuario.registrar(nome, email, senha)
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.app.mudar_tela("login")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


class TelaProjetos(Tela):
    def mostrar(self):
        self.limpar_tela()

        # Título
        ttk.Label(self.frame, text=f"Bem-vindo(a), {self.app.usuario_atual.nome}!", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Lista de projetos
        ttk.Label(self.frame, text="Seus Projetos:", 
                 font=('Arial', 12)).grid(row=1, column=0, pady=5)
        
        # Frame para lista de projetos
        projetos_frame = ttk.Frame(self.frame)
        projetos_frame.grid(row=2, column=0, columnspan=2, pady=10)

        for i, projeto in enumerate(self.app.usuario_atual.get_projetos()):
            ttk.Label(projetos_frame, text=projeto.nome).grid(row=i, column=0, pady=2)
            ttk.Button(projetos_frame, text="Ver Tarefas", 
                      command=lambda p=projeto: self.app.mostrar_tarefas(p)).grid(row=i, column=1, padx=5)

        # Frame para novo projeto
        self.criar_form_novo_projeto()

        # Botão de logout
        ttk.Button(self.frame, text="Logout", 
                  command=lambda: self.app.mudar_tela("login")).grid(row=4, column=0, columnspan=2, pady=10)

    def criar_form_novo_projeto(self):
        novo_projeto_frame = ttk.Frame(self.frame)
        novo_projeto_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Label(novo_projeto_frame, text="Novo Projeto:").grid(row=0, column=0)
        nome_projeto = ttk.Entry(novo_projeto_frame)
        nome_projeto.grid(row=0, column=1, padx=5)

        ttk.Label(novo_projeto_frame, text="Descrição:").grid(row=1, column=0)
        desc_projeto = ttk.Entry(novo_projeto_frame)
        desc_projeto.grid(row=1, column=1, padx=5)

        ttk.Button(novo_projeto_frame, text="Criar Projeto", 
                  command=lambda: self.criar_projeto(nome_projeto.get(), desc_projeto.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def criar_projeto(self, nome, descricao):
        if nome and descricao:
            self.app.usuario_atual.adicionar_projeto(nome, descricao)
            messagebox.showinfo("Sucesso", "Projeto criado com sucesso!")
            self.mostrar()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")


class TelaTarefas(Tela):
    def __init__(self, root, app, projeto):
        super().__init__(root, app)
        self.projeto = projeto

    def mostrar(self):
        self.limpar_tela()

        # Título
        ttk.Label(self.frame, text=f"Projeto: {self.projeto.nome}", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)

        # Quadro de tarefas
        self.mostrar_quadro_tarefas()

        # Form nova tarefa
        self.criar_form_nova_tarefa()

        # Botões de navegação
        ttk.Button(self.frame, text="Voltar aos Projetos", 
                  command=lambda: self.app.mudar_tela("projetos")).grid(row=3, column=0, columnspan=3, pady=10)

    def mostrar_quadro_tarefas(self):
        tarefas_frame = ttk.Frame(self.frame)
        tarefas_frame.grid(row=1, column=0, columnspan=3, pady=10)

        colunas = ["A Fazer", "Em Andamento", "Concluídas"]
        for i, coluna in enumerate(colunas):
            col_frame = ttk.LabelFrame(tarefas_frame, text=coluna, padding="10")
            col_frame.grid(row=0, column=i, padx=10)

            for tarefa in self.projeto.listar_tarefas():
                if (coluna == "A Fazer" and not tarefa.concluida) or \
                   (coluna == "Concluídas" and tarefa.concluida):
                    self.criar_card_tarefa(col_frame, tarefa)

    def criar_card_tarefa(self, parent, tarefa):
        tarefa_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        tarefa_frame.pack(pady=5, fill="x", padx=5)
        
        ttk.Label(tarefa_frame, text=tarefa.titulo, 
                 font=('Arial', 10, 'bold')).pack(pady=2)
        ttk.Label(tarefa_frame, text=f"Prioridade: {tarefa.prioridade}").pack()
        ttk.Label(tarefa_frame, text=f"Data Limite: {tarefa.data_limite}").pack()
        
        botoes_frame = ttk.Frame(tarefa_frame)
        botoes_frame.pack(pady=5)
        
        if not tarefa.concluida:
            ttk.Button(botoes_frame, text="Concluir", 
                      command=lambda: self.concluir_tarefa(tarefa)).pack(side=tk.LEFT, padx=2)
        else:
            ttk.Button(botoes_frame, text="Desmarcar", 
                      command=lambda: self.desmarcar_tarefa(tarefa)).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(botoes_frame, text="Apagar", 
                  command=lambda: self.apagar_tarefa(tarefa)).pack(side=tk.LEFT, padx=2)

    def criar_form_nova_tarefa(self):
        nova_tarefa_frame = ttk.Frame(self.frame)
        nova_tarefa_frame.grid(row=2, column=0, columnspan=3, pady=20)

        # Título
        ttk.Label(nova_tarefa_frame, text="Nova Tarefa:").grid(row=0, column=0)
        titulo = ttk.Entry(nova_tarefa_frame)
        titulo.grid(row=0, column=1, padx=5)

        # Descrição
        ttk.Label(nova_tarefa_frame, text="Descrição:").grid(row=1, column=0)
        descricao = ttk.Entry(nova_tarefa_frame)
        descricao.grid(row=1, column=1, padx=5)

        # Data Limite com DatePicker
        ttk.Label(nova_tarefa_frame, text="Data Limite:").grid(row=2, column=0)
        data_limite = DateEntry(nova_tarefa_frame, width=12, background='darkblue',
                              foreground='white', borderwidth=2, locale='pt_BR',
                              date_pattern='dd/mm/yyyy')
        data_limite.grid(row=2, column=1, padx=5, sticky='w')

        # Prioridade
        ttk.Label(nova_tarefa_frame, text="Prioridade:").grid(row=3, column=0)
        prioridade = ttk.Combobox(nova_tarefa_frame, values=["Baixa", "Média", "Alta"])
        prioridade.grid(row=3, column=1, padx=5)

        # Botão criar tarefa
        ttk.Button(nova_tarefa_frame, text="Criar Tarefa", 
                  command=lambda: self.criar_tarefa(
                      titulo.get(), 
                      descricao.get(), 
                      data_limite.get_date().strftime('%d/%m/%Y'),
                      prioridade.get()
                  )).grid(row=4, column=0, columnspan=2, pady=10)

    def criar_tarefa(self, titulo, descricao, data_limite, prioridade):
        if all([titulo, descricao, data_limite, prioridade]):
            self.projeto.criar_tarefa(titulo, descricao, data_limite, prioridade, self.app.usuario_atual.id)
            messagebox.showinfo("Sucesso", "Tarefa criada com sucesso!")
            self.mostrar()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def concluir_tarefa(self, tarefa):
        tarefa.marcar_como_concluida()
        self.mostrar()

    def desmarcar_tarefa(self, tarefa):
        tarefa.desmarcar_como_concluida()
        self.mostrar()

    def apagar_tarefa(self, tarefa):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar esta tarefa?"):
            self.projeto.remover_tarefa(tarefa)
            messagebox.showinfo("Sucesso", "Tarefa apagada com sucesso!")
            self.mostrar()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("800x600")
        self.usuario_atual = None
        
        # Dicionário de telas
        self.telas = {
            "login": TelaLogin(root, self),
            "registro": TelaRegistro(root, self),
            "projetos": TelaProjetos(root, self)
        }
        
        self.mudar_tela("login")

    def mudar_tela(self, nome_tela):
        if nome_tela in self.telas:
            self.telas[nome_tela].mostrar()

    def mostrar_tarefas(self, projeto):
        tela_tarefas = TelaTarefas(self.root, self, projeto)
        tela_tarefas.mostrar()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

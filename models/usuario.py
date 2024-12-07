from models.projeto import Projeto
from typing import List

class Usuario:
    contador_id = 1
    usuarios = []

    def __init__(self, nome: str, email: str, senha: str):
        self.id = Usuario.contador_id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.projetos: List[Projeto] = []
        Usuario.contador_id += 1
        Usuario.usuarios.append(self)

    @staticmethod
    def registrar(nome, email, senha):
        for usuario in Usuario.usuarios:
            if usuario.email == email:
                raise ValueError("E-mail já cadastrado!")
        return Usuario(nome, email, senha)

    @staticmethod
    def autenticar(email, senha):
        for usuario in Usuario.usuarios:
            if usuario.email == email and usuario.senha == senha:
                return usuario
        raise ValueError("Credenciais inválidas!")

    def get_projetos(self):
        return self.projetos

    def adicionar_projeto(self, nome, descricao):
        projeto = Projeto(nome, descricao, self.id)
        self.projetos.append(projeto)
        return projeto

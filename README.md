# Sistema de Gestão de Tarefas

Este é um sistema de gestão de tarefas desenvolvido em Python para a cadeira de orientação a objetos, projetado para organizar e gerenciar usuários, projetos, tarefas e notificações. O projeto utiliza conceitos de **programação orientada a objetos**, como **herança**, **polimorfismo** e **associação**.

## 📋 Funcionalidades

- **Usuários**
  - Registro e autenticação.
  - Associação de múltiplos projetos.
- **Projetos**
  - Criação, listagem e exclusão de tarefas.
  - Organização das tarefas por projeto.
- **Tarefas**
  - Adicionar etiquetas, subtarefas e notificações.
  - Marcar/desmarcar como concluída.
  - Hierarquia entre tarefas e subtarefas.
- **Notificações**
  - Sistema de notificações com suporte a múltiplos formatos:
    - Popup.
    - SMS.
    - Email.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- Paradigma de Programação Orientada a Objetos (POO)
- **Biblioteca `tkinter`** (para notificações de popup)

---

## 📂 Estrutura do Projeto

```plaintext
models/
├── etiqueta.py       # Classe Etiqueta
├── notificacao.py    # Classe base Notificacao e subclasses (Popup, SMS, Email)
├── projeto.py        # Classe Projeto
├── subtarefa.py      # Classe Subtarefa (herda de Tarefa)
├── tarefa.py         # Classe Tarefa
└── usuario.py        # Classe Usuario

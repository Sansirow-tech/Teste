import sqlite3

# Conexão com banco SQLite
conn = sqlite3.connect("usuarios.db")
cur = conn.cursor()

# Criar tabela
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")
conn.commit()

def criar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    cur.execute("INSERT INTO usuarios (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone))
    conn.commit()
    print("Usuário criado com sucesso)")

def listar_usuarios():
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    if usuarios:
        print("\n--- Lista de Usuários ---")
        for u in usuarios:
            print(f"ID: {u[0]} | Nome: {u[1]} | Email: {u[2]} | Telefone: {u[3]}")
        print("--------------------------\n")
    else:
        print("\nNenhum usuário cadastrado.\n")

def editar_usuarios():
    listar_usuarios()
    id_user = input("Digite o ID do usuário para editar: ")
    nome = input("Novo Nome: ")
    email = input("Novo Email: ")
    telefone = input("Novo telefone: ")
    cur.execute("UPDATE usuarios SET nome=?, email=?, telefone=? WHERE id=?",
                (nome, email, telefone, id_user))
    print("Usuário criado com sucesso!\n")
    conn.commit()

def excluir_usuarios():
    listar_usuarios()
    id_user = input("Digite o ID do usuário para excluir: ")
    cur.execute("DELETE FROM usuarios WHERE id=?", (id_user,))
    conn.commit()
    print("Usuário Excluído!\n")

#Loop Principal
while True:
    print("===CRUD Usuários===")
    print("1 - Criar Usuários")
    print("2 - Listar Usuários")
    print("3 - Editar Usuários")
    print("4 - Excluir Usuários")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_usuario()
    elif opcao == "2":
        listar_usuarios()
    elif opcao == "3":
        editar_usuarios()
    elif opcao == "4":
        excluir_usuarios()
    elif opcao == "0":
        break

    else:
        print("Opção inválida! \n")

conn.close()
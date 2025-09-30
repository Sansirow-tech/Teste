from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"  # Para mensagens flash

DB_NAME = "usuarios.db"

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Página principal - lista usuários
@app.route("/")
def index():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return render_template("index.html", usuarios=usuarios)

# Criar usuário
@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]

        if not nome or not email or not telefone:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect(url_for("criar"))

        conn = get_db_connection()
        conn.execute("INSERT INTO usuarios (nome, email, telefone) VALUES (?, ?, ?)",
                     (nome, email, telefone))
        conn.commit()
        conn.close()
        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("criar.html")

# Editar usuário
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        conn.execute("UPDATE usuarios SET nome=?, email=?, telefone=? WHERE id=?",
                     (nome, email, telefone, id))
        conn.commit()
        conn.close()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("editar.html", usuario=usuario)

# Excluir usuário
@app.route("/excluir/<int:id>")
def excluir(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Usuário excluído!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

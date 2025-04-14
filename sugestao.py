import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Conexão com o banco de dados MySQL (XAMPP)
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="sugestoes_db"
    )

# Função para salvar sugestão
def salvar_sugestao():
    nome = entry_nome.get()
    email = entry_email.get()
    sugestao = text_sugestao.get("1.0", tk.END).strip()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not sugestao:
        messagebox.showwarning("Atenção", "Digite uma sugestão.")
        return

    if var_anonimo.get():
        nome = "Anônimo"
        email = ""

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO sugestoes (nome, email, sugestao, data_hora) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, email, sugestao, data_hora))
        conn.commit()
        conn.close()

        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        text_sugestao.delete("1.0", tk.END)
        var_anonimo.set(0)

        messagebox.showinfo("Sucesso", "Sugestão enviada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar: {e}")

# Função para exibir sugestões
def exibir_sugestoes():
    janela = tk.Toplevel(root)
    janela.title("Sugestões Enviadas")

    tree = ttk.Treeview(janela, columns=("Nome", "Sugestão", "Data/Hora"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Sugestão", text="Sugestão")
    tree.heading("Data/Hora", text="Data e Hora")
    tree.pack(fill=tk.BOTH, expand=True)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, sugestao, data_hora FROM sugestoes")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar sugestões: {e}")

# Interface Tkinter
root = tk.Tk()
root.title("Caixa de Sugestões")

tk.Label(root, text="Nome:").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(root, width=40)
entry_nome.grid(row=0, column=1, pady=5)

tk.Label(root, text="Email:").grid(row=1, column=0, sticky="w")
entry_email = tk.Entry(root, width=40)
entry_email.grid(row=1, column=1, pady=5)

var_anonimo = tk.IntVar()
check_anonimo = tk.Checkbutton(root, text="Enviar como anônimo", variable=var_anonimo)
check_anonimo.grid(row=2, column=1, sticky="w", pady=5)

tk.Label(root, text="Sugestão:").grid(row=3, column=0, sticky="nw")
text_sugestao = tk.Text(root, width=50, height=5)
text_sugestao.grid(row=3, column=1, pady=5)

btn_salvar = tk.Button(root, text="Enviar Sugestão", command=salvar_sugestao)
btn_salvar.grid(row=4, column=1, pady=10, sticky="e")

btn_ver = tk.Button(root, text="Ver Sugestões", command=exibir_sugestoes)
btn_ver.grid(row=4, column=0, pady=10, sticky="w")

root.mainloop()

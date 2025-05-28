import tkinter as tk
from PIL import Image, ImageTk

# Função chamada quando o botão é pressionado
def entrar():
    print("Entrar pressionado!")  # Aqui você pode redirecionar para outra tela

# Criação da janela principal
root = tk.Tk()
root.title("Home com Logo")
root.geometry("400x500")  # Define o tamanho da janela
root.configure(bg="white")

# Carrega e exibe a imagem do logo
try:
    imagem = Image.open("goku.jpg")
    imagem = imagem.resize((200, 200))  # Redimensiona a imagem
    imagem_tk = ImageTk.PhotoImage(imagem)

    label_imagem = tk.Label(root, image=imagem_tk, bg="white")
    label_imagem.pack(pady=30)
except Exception as e:
    print("Erro ao carregar imagem:", e)

# Título da Home
titulo = tk.Label(root, text="Bem-vindo ao App", font=("Helvetica", 18, "bold"), bg="white", fg="#333")
titulo.pack(pady=10)

# Botão de entrada
botao_entrar = tk.Button(root, text="Entrar", font=("Helvetica", 14), bg="#007bff", fg="white", padx=20, pady=10, command=entrar)
botao_entrar.pack(pady=20)

# Inicia a janela
root.mainloop()

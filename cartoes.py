import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from funcs import cadastrarCartao, listarCartoes, deletarCartao, listarCartoesSemCriptografia

def Cartao(root):
    def apagarTudo():
        frame_cadastro.pack_forget()
        frame_listar.pack_forget()
        frame_deletar.pack_forget()

    def handleCadastrarCartao():
        apagarTudo()
        frame_cadastro.pack(pady=10, ipadx=20)

    def handleListarCartao():
        apagarTudo()
        frame_listar.pack(pady=10, ipadx=20)

        for widget in frame_listar.winfo_children():
            widget.destroy()

        cartoes = listarCartoes()
        
        if not cartoes:
            ctk.CTkLabel(frame_listar, text="Nenhum cartão cadastrado.").pack(pady=10)
        else:
            for i, cartao in enumerate(cartoes, start=1):
                ctk.CTkLabel(frame_listar, text=f"Cartão {i}: {cartao['numero']} || Validade: {cartao['validade']}").pack(pady=5)

    def handleDeletarCartao():
        apagarTudo()
        frame_deletar.pack(pady=10, ipadx=20)
        cartoes = listarCartoes()
        if "status" in cartoes:
            CTkMessagebox(title="Erro", icon="cancel", message="Você só poderá deletar os cartões anteriores.", border_color="red", button_color="red", button_hover_color="darkred", title_color="red")
            cartoes = listarCartoesSemCriptografia()
            opcoes_cartoes = []
            for i in range(len(cartoes)):
                opcoes_cartoes.append(f"Cartão {i+1}")
                menu_deletar.configure(values=opcoes_cartoes)
                menu_deletar.set("Selecione o cartão") 
                btn_deletar_confirmar.configure(state="normal")  
            return
        
        if not cartoes: 
            menu_deletar.configure(values=["Nenhum cartão cadastrado"])
            menu_deletar.set("Nenhum cartão cadastrado")
            btn_deletar_confirmar.configure(state="disabled")  
        else:
            opcoes_cartoes = []
            for i in range(len(cartoes)):
                numeroDoCartao = cartoes[i]["numero"]
                opcoes_cartoes.append(f"Cartão {i+1}: {numeroDoCartao}")
                menu_deletar.configure(values=opcoes_cartoes)
                menu_deletar.set("Selecione o cartão") 
                btn_deletar_confirmar.configure(state="normal")  

    def Cadastrar(numero, cvv, validade):
        if cadastrarCartao(numero, cvv, validade) == True:
            entry_numero.delete(0, 'end')
            entry_cvv.delete(0, 'end')
            entry_validade.delete(0, 'end')

    def Deletar():
        selected_option = menu_deletar.get()
        if selected_option.startswith("Cartão "):
            indice = int(selected_option.split(" ")[1][0])  
            deletarCartao(indice)
    
    btn_cadastrar = ctk.CTkButton(root, text="Cadastrar Cartão", command=handleCadastrarCartao)
    btn_cadastrar.pack(pady=10)

    btn_listar = ctk.CTkButton(root, text="Listar Cartões", command=handleListarCartao)
    btn_listar.pack(pady=10)

    btn_deletar = ctk.CTkButton(root, text="Deletar Cartão", command=handleDeletarCartao)
    btn_deletar.pack(pady=10)

    frame_cadastro = ctk.CTkFrame(root)

    label_instrucoes = ctk.CTkLabel(frame_cadastro, text="Preencha os dados do cartão", font=("Arial", 18))
    label_instrucoes.pack(pady=10)

    entry_numero = ctk.CTkEntry(frame_cadastro, placeholder_text="Número do Cartão")
    entry_numero.pack(pady=10)

    entry_cvv = ctk.CTkEntry(frame_cadastro, placeholder_text="CVV")
    entry_cvv.pack(pady=10)

    entry_validade = ctk.CTkEntry(frame_cadastro, placeholder_text="Validade (mm/yy)")
    entry_validade.pack(pady=10)

    btn_cadastrar_confirmar = ctk.CTkButton(frame_cadastro, text="Cadastrar", command=lambda: Cadastrar(entry_numero.get(), entry_cvv.get(), entry_validade.get()))
    btn_cadastrar_confirmar.pack(pady=10)

    frame_listar = ctk.CTkFrame(root)

    frame_deletar = ctk.CTkFrame(root)

    label_selecao = ctk.CTkLabel(frame_deletar, text="Selecione o número do cartão a deletar:")
    label_selecao.pack(pady=10)

    menu_deletar = ctk.CTkOptionMenu(frame_deletar, values=["Carregando..."])
    menu_deletar.pack(pady=10)

    btn_deletar_confirmar = ctk.CTkButton(frame_deletar, text="Deletar", command=Deletar)
    btn_deletar_confirmar.pack(pady=10)

    root.mainloop()

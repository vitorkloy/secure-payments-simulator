import customtkinter as ctk
from funcs import listarCartoes, fazerPagamento, listarPagamentos

def Pagamento(root):
    def apagarTudo():
        frame_pagar.pack_forget()
        frame_listar.pack_forget()

    def handlePagar():
        apagarTudo()
        frame_pagar.pack(pady=10, ipadx=20)

        cartoes = listarCartoes()
        
        if not cartoes:  
            menu_pagar.configure(values=["Nenhum cartão cadastrado"])
            menu_pagar.set("Nenhum cartão cadastrado")
            btn_pagar_confirmar.configure(state="disabled")  
        else:
            opcoes_cartoes = []
            for i in range(len(cartoes)):
                numeroDoCartao = cartoes[i]["numero"]
                opcoes_cartoes.append(f"Cartão {i+1}: {numeroDoCartao}")
                menu_pagar.configure(values=opcoes_cartoes)
                menu_pagar.set("Selecione o cartão") 
                btn_pagar_confirmar.configure(state="normal")  

    def handleListarPags():
        apagarTudo()
        frame_listar.pack(pady=10, ipadx=20)

        pagamentos = listarPagamentos()

        for widget in frame_listar.winfo_children():
            widget.destroy()

        pagamentos = listarPagamentos()

        if not pagamentos:
            ctk.CTkLabel(frame_listar, text="Nenhum pagamento realizado.").pack(pady=10)
        else:
            for i, pagamento in enumerate(pagamentos):
                ctk.CTkLabel(frame_listar, text=f"Cartão {i+1}: {pagamento['numero']}\n Valor: {pagamento['valor']}\n Data: {pagamento['data']}", font=("Arial", 16)).pack(pady=5)

    def Pagar():
        selected_option = menu_pagar.get()
        valor = entry_valor.get()
        if selected_option.startswith("Cartão "):
            indice = int(selected_option.split(" ")[1][0])  
            fazerPagamento(indice, valor)
    
    btn_pagar = ctk.CTkButton(root, text="Pagar", command=handlePagar)
    btn_pagar.pack(pady=10)
    
    btn_listar = ctk.CTkButton(root, text="Extrato", command=handleListarPags)
    btn_listar.pack(pady=10)

    frame_pagar = ctk.CTkFrame(root)

    label_selecao = ctk.CTkLabel(frame_pagar, text="Selecione o número do cartão:")
    label_selecao.pack(pady=10)

    menu_pagar = ctk.CTkOptionMenu(frame_pagar, values=["Carregando..."])
    menu_pagar.pack(pady=10)

    entry_valor = ctk.CTkEntry(frame_pagar, placeholder_text="Valor")
    entry_valor.pack(pady=10)

    btn_pagar_confirmar = ctk.CTkButton(frame_pagar, text="Pagar", command=Pagar)
    btn_pagar_confirmar.pack(pady=10)

    frame_listar = ctk.CTkFrame(root)

    root.mainloop()
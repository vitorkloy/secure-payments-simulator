import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from funcs import cadastrarCartao, listarCartoes, deletarCartao, listarCartoesSemCriptografia
from PIL import Image, ImageTk

class CardWidget(ctk.CTkFrame):
    def __init__(self, master, card_data, index):
        super().__init__(master, corner_radius=12, fg_color=("#ffffff", "#2c2c2c"), border_width=1, border_color=("#e0e0e0", "#3a3a3a"))
        self.card_data = card_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # Ícone do cartão
        try:
            card_icon = ctk.CTkImage(light_image=Image.open("icons/credit-card.png"), size=(30, 30))
            ctk.CTkLabel(self, image=card_icon, text="").grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="nsew")
        except:
            pass
        
        # Número do cartão (com máscara)
        masked_number = f"**** **** **** {card_data['numero'][-4:]}" if len(card_data['numero']) > 4 else card_data['numero']
        ctk.CTkLabel(self, text=f"Cartão {index}", 
                    font=("Helvetica", 14, "bold")).grid(row=0, column=1, sticky="w", padx=5)
        ctk.CTkLabel(self, text=masked_number, 
                    font=("Helvetica", 13)).grid(row=1, column=1, sticky="w", padx=5)
        
        # Validade
        validity_frame = ctk.CTkFrame(self, fg_color="transparent")
        validity_frame.grid(row=0, column=2, rowspan=2, padx=15, sticky="e")
        ctk.CTkLabel(validity_frame, text="Validade:", font=("Helvetica", 10)).pack(anchor="e")
        ctk.CTkLabel(validity_frame, text=card_data['validade'], 
                    font=("Helvetica", 12, "bold")).pack(anchor="e")

def Cartao(root):
    # Estilos avançados
    frame_style = {
        "corner_radius": 15,
        "fg_color": ("#ffffff", "#2c2c2c"),
        "border_width": 1,
        "border_color": ("#e0e0e0", "#3a3a3a")
    }
    label_style = {"font": ("Helvetica", 14)}
    entry_style = {
        "font": ("Helvetica", 14),
        "height": 45,
        "width": 350,
        "corner_radius": 10,
        "border_width": 1
    }
    button_style = {
        "font": ("Helvetica", 14),
        "height": 45,
        "width": 180,
        "corner_radius": 10,
        "fg_color": "#2b8be0",
        "hover_color": "#1f6fb9",
        "border_width": 0
    }
    
    def apagarTudo():
        frame_cadastro.pack_forget()
        frame_listar.pack_forget()
        frame_deletar.pack_forget()

    def handleCadastrarCartao():
        apagarTudo()
        frame_cadastro.pack(pady=20, ipadx=20, ipady=20)

    def handleListarCartao():
        apagarTudo()
        frame_listar.pack(pady=20, ipadx=20, ipady=20)

        for widget in frame_listar.winfo_children():
            widget.destroy()

        cartoes = listarCartoes()
        
        if not cartoes:
            ctk.CTkLabel(frame_listar, text="Nenhum cartão cadastrado.", **label_style).pack(pady=20)
        else:
            for i, cartao in enumerate(cartoes, start=1):
                CardWidget(frame_listar, cartao, i).pack(pady=5, fill="x", padx=10)

    def handleDeletarCartao():
        apagarTudo()
        frame_deletar.pack(pady=20, ipadx=20, ipady=20)
        cartoes = listarCartoes()
        if "status" in cartoes:
            CTkMessagebox(title="Erro", icon="cancel", 
                         message="Você só poderá deletar os cartões anteriores.", 
                         border_color="red", button_color="red", 
                         button_hover_color="darkred", title_color="red")
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
                opcoes_cartoes.append(f"Cartão {i+1}: ****{numeroDoCartao[-4:]}")
                menu_deletar.configure(values=opcoes_cartoes)
                menu_deletar.set("Selecione o cartão") 
                btn_deletar_confirmar.configure(state="normal")  

    def Cadastrar(numero, cvv, validade):
        if cadastrarCartao(numero, cvv, validade) == True:
            entry_numero.delete(0, 'end')
            entry_cvv.delete(0, 'end')
            entry_validade.delete(0, 'end')
            CTkMessagebox(title="Sucesso", message="Cartão cadastrado com sucesso!",
                         icon="check", option_1="OK")

    def Deletar():
        selected_option = menu_deletar.get()
        if selected_option.startswith("Cartão "):
            indice = int(selected_option.split(" ")[1][0])  
            deletarCartao(indice)
            handleDeletarCartao()  # Atualiza a lista após deletar
            CTkMessagebox(title="Sucesso", message="Cartão deletado com sucesso!",
                         icon="check", option_1="OK")
    
    # Header
    header_frame = ctk.CTkFrame(root, fg_color="transparent")
    header_frame.pack(fill="x", pady=(20, 10), padx=20)
    
    ctk.CTkLabel(header_frame, 
                text="Gerenciamento de Cartões",
                font=("Helvetica", 22, "bold")).pack(side="left")
    
    # Botões de ação
    action_frame = ctk.CTkFrame(root, fg_color="transparent")
    action_frame.pack(pady=10)
    
    try:
        add_icon = ctk.CTkImage(light_image=Image.open("icons/add.png"))
        list_icon = ctk.CTkImage(light_image=Image.open("icons/list.png"))
        delete_icon = ctk.CTkImage(light_image=Image.open("icons/delete.png"))
    except:
        add_icon = None
        list_icon = None
        delete_icon = None
    
    btn_cadastrar = ctk.CTkButton(action_frame, 
                                 text="Cadastrar Novo",
                                 image=add_icon,
                                 command=handleCadastrarCartao,
                                 **button_style)
    btn_cadastrar.pack(side="left", padx=10)
    
    btn_listar = ctk.CTkButton(action_frame, 
                              text="Listar Cartões",
                              image=list_icon,
                              command=handleListarCartao,
                              **button_style)
    btn_listar.pack(side="left", padx=10)
    
    btn_deletar = ctk.CTkButton(action_frame, 
                               text="Remover Cartão",
                               image=delete_icon,
                               command=handleDeletarCartao,
                               **button_style)
    btn_deletar.pack(side="left", padx=10)
    
    # Frame de cadastro
    frame_cadastro = ctk.CTkFrame(root, **frame_style)
    
    label_instrucoes = ctk.CTkLabel(frame_cadastro, 
                                   text="Cadastro de Cartão", 
                                   font=("Helvetica", 18, "bold"))
    label_instrucoes.pack(pady=(10, 20))
    
    entry_numero = ctk.CTkEntry(frame_cadastro, 
                               placeholder_text="Número do Cartão", 
                               **entry_style)
    entry_numero.pack(pady=10)
    
    entry_cvv = ctk.CTkEntry(frame_cadastro, 
                            placeholder_text="CVV", 
                            **entry_style)
    entry_cvv.pack(pady=10)
    
    entry_validade = ctk.CTkEntry(frame_cadastro, 
                                 placeholder_text="Validade (mm/yy)", 
                                 **entry_style)
    entry_validade.pack(pady=10)
    
    btn_cadastrar_confirmar = ctk.CTkButton(frame_cadastro, 
                                           text="Cadastrar", 
                                           command=lambda: Cadastrar(entry_numero.get(), entry_cvv.get(), entry_validade.get()),
                                           **button_style)
    btn_cadastrar_confirmar.pack(pady=20)
    
    # Frame de listagem
    frame_listar = ctk.CTkFrame(root, **frame_style)
    
    # Frame de deleção
    frame_deletar = ctk.CTkFrame(root, **frame_style)
    
    label_selecao = ctk.CTkLabel(frame_deletar, 
                                text="Selecione o cartão para deletar:", 
                                **label_style)
    label_selecao.pack(pady=10)
    
    menu_deletar = ctk.CTkOptionMenu(frame_deletar, 
                                    values=["Carregando..."], 
                                    font=("Helvetica", 14),
                                    width=300,
                                    height=40,
                                    dropdown_font=("Helvetica", 14))
    menu_deletar.pack(pady=10)
    
    btn_deletar_confirmar = ctk.CTkButton(frame_deletar, 
                                         text="Confirmar Deleção", 
                                         command=Deletar,
                                         **button_style)
    btn_deletar_confirmar.pack(pady=20)
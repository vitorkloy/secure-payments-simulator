import customtkinter as ctk
from funcs import listarCartoes, fazerPagamento, listarPagamentos
from PIL import Image
from datetime import datetime

class PaymentWidget(ctk.CTkFrame):
    def __init__(self, master, payment_data, index):
        super().__init__(master, corner_radius=12, fg_color=("#ffffff", "#2c2c2c"), border_width=1, border_color=("#e0e0e0", "#3a3a3a"))
        self.payment_data = payment_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # Ícone de pagamento
        try:
            payment_icon = ctk.CTkImage(light_image=Image.open("icons/receipt.png"), size=(30, 30))
            ctk.CTkLabel(self, image=payment_icon, text="").grid(row=0, column=0, rowspan=3, padx=15, pady=10, sticky="nsew")
        except:
            pass
        
        # Detalhes do pagamento
        ctk.CTkLabel(self, text=f"Transação #{index}", 
                    font=("Helvetica", 14, "bold")).grid(row=0, column=1, sticky="w", padx=5)
        
        ctk.CTkLabel(self, text=f"Cartão: **** **** **** {payment_data['numero'][-4:]}", 
                    font=("Helvetica", 13)).grid(row=1, column=1, sticky="w", padx=5)
        
        # Valor com destaque
        value_frame = ctk.CTkFrame(self, fg_color="transparent")
        value_frame.grid(row=0, column=2, rowspan=2, padx=15, sticky="e")
        ctk.CTkLabel(value_frame, text="Valor:", font=("Helvetica", 10)).pack(anchor="e")
        ctk.CTkLabel(value_frame, text=f"R$ {payment_data['valor']}", 
                    font=("Helvetica", 16, "bold"), 
                    text_color="#4CAF50").pack(anchor="e")
        
        # Data formatada
        try:
            date_obj = datetime.strptime(payment_data['data'], "%Y-%m-%d %H:%M:%S")
            formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")
        except:
            formatted_date = payment_data['data']
            
        ctk.CTkLabel(self, text=f"Em {formatted_date}", 
                    font=("Helvetica", 11),
                    text_color=("gray50", "gray60")).grid(row=2, column=1, columnspan=2, sticky="w", padx=5)

def Pagamento(root):
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
        frame_pagar.pack_forget()
        frame_listar.pack_forget()

    def handlePagar():
        apagarTudo()
        frame_pagar.pack(pady=20, ipadx=20, ipady=20)

        cartoes = listarCartoes()
        
        if not cartoes:  
            menu_pagar.configure(values=["Nenhum cartão cadastrado"])
            menu_pagar.set("Nenhum cartão cadastrado")
            btn_pagar_confirmar.configure(state="disabled")  
        else:
            opcoes_cartoes = []
            for i in range(len(cartoes)):
                numeroDoCartao = cartoes[i]["numero"]
                opcoes_cartoes.append(f"Cartão {i+1}: ****{numeroDoCartao[-4:]}")
                menu_pagar.configure(values=opcoes_cartoes)
                menu_pagar.set("Selecione o cartão") 
                btn_pagar_confirmar.configure(state="normal")  

    def handleListarPags():
        apagarTudo()
        frame_listar.pack(pady=20, ipadx=20, ipady=20)

        for widget in frame_listar.winfo_children():
            widget.destroy()

        pagamentos = listarPagamentos()

        if not pagamentos:
            ctk.CTkLabel(frame_listar, text="Nenhum pagamento realizado.", **label_style).pack(pady=20)
        else:
            for i, pagamento in enumerate(pagamentos, start=1):
                PaymentWidget(frame_listar, pagamento, i).pack(pady=10, fill="x", padx=10)

    def Pagar():
        selected_option = menu_pagar.get()
        valor = entry_valor.get()
        if selected_option.startswith("Cartão ") and valor:
            indice = int(selected_option.split(" ")[1][0])  
            if fazerPagamento(indice, valor):
                CTkMessagebox(title="Sucesso", message="Pagamento realizado com sucesso!",
                             icon="check", option_1="OK")
                entry_valor.delete(0, 'end')
                handlePagar()  # Atualiza a lista de cartões
    
    # Header
    header_frame = ctk.CTkFrame(root, fg_color="transparent")
    header_frame.pack(fill="x", pady=(20, 10), padx=20)
    
    ctk.CTkLabel(header_frame, 
                text="Sistema de Pagamentos",
                font=("Helvetica", 22, "bold")).pack(side="left")
    
    # Botões de ação
    action_frame = ctk.CTkFrame(root, fg_color="transparent")
    action_frame.pack(pady=10)
    
    try:
        payment_icon = ctk.CTkImage(light_image=Image.open("icons/payment.png"))
        receipt_icon = ctk.CTkImage(light_image=Image.open("icons/receipt-list.png"))
    except:
        payment_icon = None
        receipt_icon = None
    
    btn_pagar = ctk.CTkButton(action_frame, 
                             text="Realizar Pagamento",
                             image=payment_icon,
                             command=handlePagar,
                             **button_style)
    btn_pagar.pack(side="left", padx=10)
    
    btn_listar = ctk.CTkButton(action_frame, 
                              text="Ver Extrato",
                              image=receipt_icon,
                              command=handleListarPags,
                              **button_style)
    btn_listar.pack(side="left", padx=10)
    
    # Frame de pagamento
    frame_pagar = ctk.CTkFrame(root, **frame_style)
    
    label_selecao = ctk.CTkLabel(frame_pagar, 
                                text="Selecione o cartão para pagamento:", 
                                **label_style)
    label_selecao.pack(pady=10)
    
    menu_pagar = ctk.CTkOptionMenu(frame_pagar, 
                                  values=["Carregando..."], 
                                  font=("Helvetica", 14),
                                  width=300,
                                  height=40,
                                  dropdown_font=("Helvetica", 14))
    menu_pagar.pack(pady=10)
    
    entry_valor = ctk.CTkEntry(frame_pagar, 
                              placeholder_text="Valor (R$)", 
                              **entry_style)
    entry_valor.pack(pady=10)
    
    btn_pagar_confirmar = ctk.CTkButton(frame_pagar, 
                                       text="Confirmar Pagamento", 
                                       command=Pagar,
                                       **button_style)
    btn_pagar_confirmar.pack(pady=20)
    
    # Frame de listagem
    frame_listar = ctk.CTkFrame(root, **frame_style)
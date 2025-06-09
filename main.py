import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from cartoes import Cartao
from pagamentos import Pagamento
from PIL import Image

# Configuração da janela principal
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root.title("Payment System")
root.geometry("1100x750")
root.minsize(1000, 700)

# Estilos avançados
font_title = ("Helvetica", 20, "bold")
font_subtitle = ("Helvetica", 16)
font_normal = ("Helvetica", 15)
button_style = {
    "font": font_normal,
    "height": 45,
    "width": 200,
    "corner_radius": 10,
    "fg_color": "#2b8be0",
    "hover_color": "#1f6fb9",
    "border_width": 0
}
menu_style = {
    "fg_color": ("#2b2b2b", "#1e1e1e"),
    "corner_radius": 0
}

def show_cartao():
    clear_main_frame()
    Cartao(main_frame)

def show_pagamento():
    clear_main_frame()
    Pagamento(main_frame)

# Frame do menu lateral
menu_frame = ctk.CTkFrame(root, width=250, **menu_style)
menu_frame.pack(side="left", fill="y")

# Logo/Header do menu
logo_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
logo_frame.pack(pady=(30, 40), padx=20, fill="x")

ctk.CTkLabel(logo_frame, text="PAYMENT", 
            font=("Helvetica", 24, "bold"), 
            text_color="#2b8be0").pack(anchor="w")
ctk.CTkLabel(logo_frame, text="SYSTEM", 
            font=("Helvetica", 24, "bold"), 
            text_color="white").pack(anchor="w")

# Botões do menu com ícones
try:
    card_icon = ctk.CTkImage(light_image=Image.open("icons/card.png"))
    payment_icon = ctk.CTkImage(light_image=Image.open("icons/payment.png"))
except:
    # Fallback se os ícones não existirem
    card_icon = None
    payment_icon = None

btn_style = {**button_style, "anchor": "w", "compound": "left", "text_color": "white"}
btn_cartoes = ctk.CTkButton(menu_frame, 
                           text="  Gerenciar Cartões",
                           command=show_cartao,
                           image=card_icon,
                           **btn_style)
btn_cartoes.pack(pady=8, padx=20)

btn_pagamento = ctk.CTkButton(menu_frame, 
                             text="  Realizar Pagamentos",
                             command=show_pagamento,
                             image=payment_icon,
                             **btn_style)
btn_pagamento.pack(pady=8, padx=20)


# Frame principal
main_frame = ctk.CTkFrame(root, fg_color=("#f5f5f5", "#1a1a1a"), corner_radius=0)
main_frame.pack(side="right", fill="both", expand=True)


# boas vindas
mensage_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
mensage_frame.pack(pady=(200, 100))

ctk.CTkLabel(mensage_frame, text="Seja", 
            font=("Helvetica", 50, "bold"), 
            text_color="white").pack(anchor="w")
ctk.CTkLabel(mensage_frame, text="Bem-Vindo!", 
            font=("Helvetica", 50, "bold"), 
            text_color="#2b8be0").pack(anchor="w")

# Footer
footer_label = ctk.CTkLabel(menu_frame, 
                           text="© 2025 Payment System",
                           font=("Helvetica", 10),
                           text_color=("gray60", "gray40"))
footer_label.pack(side="bottom", pady=20)

def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

root.mainloop()
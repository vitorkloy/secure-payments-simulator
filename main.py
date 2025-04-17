import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from cartoes import Cartao
from pagamentos import Pagamento

root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root.title("Sistema de pagamentos")
root.geometry("900x600")

def show_cartao():
    clear_main_frame()
    Cartao(main_frame)

def show_pagamento():
    clear_main_frame()
    Pagamento(main_frame)

menu_frame = ctk.CTkFrame(root)
menu_frame.pack(side="left", fill="y")

label_menu = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 20))
label_menu.pack(pady=10)

btn_cartoes = ctk.CTkButton(menu_frame, text="Cartões", command=show_cartao)
btn_cartoes.pack(pady=10)

btn_pagamento = ctk.CTkButton(menu_frame, text="Pagamentos", command=show_pagamento)
btn_pagamento.pack(pady=10)

main_frame = ctk.CTkFrame(root)
main_frame.pack(side="right", fill="both", expand=True)

def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

root.mainloop()
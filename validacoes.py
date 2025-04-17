from CTkMessagebox import CTkMessagebox
from datetime import datetime, date

def validarCadastro(numero, cvv, validade):
    if not numero or not cvv or not validade:
        CTkMessagebox(title="Erro", icon="cancel", message="Preencha todos os campos.")
        return False
    elif numero.isalpha() or cvv.isalpha() or validade.isalpha():
        CTkMessagebox(title="Erro", icon="cancel", message="Preencha os campos apenas com números.")
        return False
    elif len(numero) != 16:
        CTkMessagebox(title="Erro", icon="cancel", message="Número deve ter 16 dígitos.")
        return False
    elif len(cvv) != 3 or not cvv.isdigit():
        CTkMessagebox(title="Erro", icon="cancel", message="CVV deve ter 3 dígitos.")
        return False 
    else:
        try:
            validade_data = datetime.strptime("01/" + validade, "%d/%m/%y").date()
            if validade_data < date.today():
                CTkMessagebox(title="Erro", icon="cancel", message="A validade já expirou.")       
                return False
        except ValueError:
            CTkMessagebox(title="Erro", icon="cancel", message="Formato de validade incorreto. Use mm/yy.")
            return False

def validarDelecao(indice):
    if not indice:
        CTkMessagebox(title="Erro", icon="cancel", message="Campo obrigatório.")
        return False

def validarPagamento(indice, valor):
    if not indice or not valor:
        CTkMessagebox(title="Erro", icon="cancel", message="Preencha todos os campos.")
        return False
    if valor.isalpha():
        CTkMessagebox(title="Erro", icon="cancel", message="Preencha o campo apenas com números.")
        return False
    if int(valor) < 0:
        CTkMessagebox(title="Erro", icon="cancel", message="O valor não pode ser negativo.")
        return False
    return True
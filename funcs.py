from bd import connect
from CTkMessagebox import CTkMessagebox
from hashlib import sha256
from datetime import datetime
from validacoes import validarCadastro, validarDelecao, validarPagamento
from cryptography.fernet import Fernet
import os



try:
    conn = connect()
    cards = conn["cartoes"]  # Coleção para cartões
    pay = conn["pagamentos"]  # Coleção para pagamentos
except Exception as e:
    print(f"Erro: {e}")
    CTkMessagebox(title="Erro", icon="cancel", message=f"Falha na conexão com o banco de dados: {str(e)}")
    exit()


script_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(script_dir, "key.key")

if os.path.exists(key_path):
    keyfile = open(key_path, "rb")
    key = keyfile.read()
else:
    key = Fernet.generate_key()
    keyfile = open(key_path, "wb")
    keyfile.write(key)

fr = Fernet(key)

def cadastrarCartao(numero, cvv, validade):
    if validarCadastro(numero, cvv, validade) is False:
        return False
    try:
        numero_criptografado = fr.encrypt(numero.encode())
        cvv_criptografado = fr.encrypt(cvv.encode())

        cartao_existente = cards.find_one({"numero": numero_criptografado})
        if cartao_existente:
            CTkMessagebox(title="Erro", icon="cancel", message="Cartão já cadastrado.")
            return False

        cards.insert_one({
            "numero": numero_criptografado, 
            "cvv": cvv_criptografado, 
            "validade": validade
        })

        CTkMessagebox(title="Sucesso", icon="check", message="Cartão cadastrado com sucesso.")
        return True
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro: {str(e)}")
        return False

def listarCartoes():
    try:
        cartoes = list(cards.find())
        for cartao in cartoes:
            cartao["numero"] = fr.decrypt(cartao['numero']).decode()
            cartao["cvv"] = fr.decrypt(cartao['cvv']).decode()
        return cartoes
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro ao listar os cartões: A chave de criptografia foi alterada")
        return {"erro": "criptografia alterada", "status": 1}
    
def listarCartoesSemCriptografia():
    try:
        return list(cards.find())
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro ao listar os cartões: {str(e)}")

def deletarCartao(indice):
    if validarDelecao(indice) is False:
        return False
    try:
        cartoes = list(cards.find())
        if indice < 1 or indice > len(cartoes):
            CTkMessagebox(title="Erro", icon="cancel", message="Índice inválido.")
            return False
        
        cartao_a_deletar = cartoes[indice-1]
        numero_criptografado = cartao_a_deletar['numero']

        resultado = cards.delete_one({"numero": numero_criptografado})
        
        if resultado.deleted_count > 0:
            CTkMessagebox(title="Sucesso", icon="check", message="Cartão deletado com sucesso!")
        else:
            CTkMessagebox(title="Erro", icon="cancel", message="Erro ao tentar deletar o cartão.")
            return False
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro: {str(e)}")
        return False
    return True

def listarPagamentos():
    try:
        payments = list(pay.find())
        for payment in payments:
            payment["numero"] = fr.decrypt(payment['numero']).decode()
        return payments
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro ao ver extrato: A chave de criptografia foi alterada")
        return []

def fazerPagamento(indice, valor):
    if not validarPagamento(indice, valor):
        return False
    try:
        cartoes = list(cards.find())
        if indice < 1 or indice > len(cartoes):
            CTkMessagebox(title="Erro", icon="cancel", message="Índice inválido.")
            return False
        
        cartao_a_selecionar = cartoes[indice - 1]
        numero_criptografado = cartao_a_selecionar['numero']

        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')

        obj = {
            "numero": numero_criptografado,
            "valor": valor,
            "data": data_e_hora_em_texto
        }

        hash = sha256(str(obj).encode()).hexdigest()

        pay.insert_one({
            "numero": numero_criptografado, 
            "valor": valor,
            "data": data_e_hora_em_texto,
            "hash_da_transacao": hash
        })

        CTkMessagebox(title="Sucesso", icon="check", message="Pagamento realizado com sucesso.")
        return True
    except Exception as e:
        CTkMessagebox(title="Erro", icon="cancel", message=f"Ocorreu um erro: {str(e)}")
    return True
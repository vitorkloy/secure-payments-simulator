# Sistema de Pagamentos com Interface Gráfica

## 📋 Descrição
Um projeto de sistema de pagamentos desenvolvido em Python para um trabalho acadêmico/prático. Utiliza a biblioteca `customtkinter` para a interface gráfica e o  `MongoDB`  como banco de dados. O sistema permite:

- 💳 Cadastro, listagem e exclusão segura de cartões
- 💵 Simulação de pagamentos
- 📊 Extrato de transações
- 🛡️ Criptografia de dados sensíveis (cartões, CVV)

## 🔑 Funcionalidades Principais

### 1. Gerenciamento de Cartões
- **Cadastro**: Valida e criptografa número, CVV e validade
- **Listagem**: Exibe cartões de forma descriptografada segura
- **Exclusão**: Remove cartões do sistema

### 2. Operações Financeiras
- **Pagamentos**: Processa transações com validação de valor
- **Extrato**: Exibe histórico completo de transações (cartão, valor, data/hora)

## 🛠 Tecnologias Utilizadas
| Tecnologia | Finalidade |
|------------|------------|
| Python 3.x | Linguagem principal |
| CustomTkinter | Interface gráfica moderna |
| MongoDB | Armazenamento de dados |
| Cryptography | Criptografia de dados sensíveis |
| Hashlib | Geração de hash para transações |
| python-dotenv | Gerenciamento de variáveis de ambiente |

## ⚙️ Pré-requisitos
- Python 3.10 ou superior
- MongoDB Atlas ou local
- Bibliotecas listadas em `requirements.txt`

## 🔒 Configuração do Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com:

```env
MONGODB_URI=sua_string_de_conexao_mongodb_aqui
```

## 🚀 Instalação e Execução

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/secure-payments-simulator.git
cd secure-payments-simulator
```
2. Instale a dependência com pip:
```bash
pip install -r requirements.txt
```
3. Configure o `.env` como indicado acima
4. Rodar o programa:
```bash
python main.py
```

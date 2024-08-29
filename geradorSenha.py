import random
import string
import json
import sqlite3

# Função para gerar a senha de acordo com o tipo escolhido
def gerar_senha(tipo, tamanho):
    if tamanho > 15:
        tamanho = 15
    elif tamanho < 1:
        tamanho = 1
    
    if tipo == 1:
        caracteres = string.ascii_lowercase  # Apenas letras minúsculas
    elif tipo == 2:
        caracteres = string.ascii_uppercase  # Apenas letras maiúsculas
    elif tipo == 3:
        caracteres = string.digits  # Apenas números
    elif tipo == 4:
        caracteres = string.ascii_letters  # Letras maiúsculas e minúsculas
    elif tipo == 5:
        caracteres = string.ascii_letters + string.digits  # Letras e números
    elif tipo == 6:
        caracteres = string.ascii_letters + string.digits + string.punctuation  # Letras, números e caracteres especiais
    else:
        return "Tipo de senha inválido"
    
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

# Função para salvar a senha no banco de dados SQLite3
def salvar_senha(tipo, senha):
    conexao = sqlite3.connect('senhas.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS senhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo INTEGER,
            senha TEXT
        )
    ''')
    
    cursor.execute('INSERT INTO senhas (tipo, senha) VALUES (?, ?)', (tipo, senha))
    conexao.commit()
    conexao.close()

# Função principal para gerar a senha e retornar o JSON
def main():
    tipo = int(input("Escolha o tipo de senha (1-6): "))
    tamanho = int(input("Escolha o tamanho da senha (1-15): "))
    
    senha_gerada = gerar_senha(tipo, tamanho)
    
    if senha_gerada != "Tipo de senha inválido":
        salvar_senha(tipo, senha_gerada)
        resultado = {
            "tipo": tipo,
            "tamanho": tamanho,
            "senha": senha_gerada
        }
        print(json.dumps(resultado, indent=4))
    else:
        print(senha_gerada)

if __name__ == "__main__":
    main()

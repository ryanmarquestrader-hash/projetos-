import sqlite3 
import requests
import os
import sys

def caminho_banco():
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA")
    else:
        base = os.path.expanduser("~")

    pasta = os.path.join(base, "CryptoManager")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, "criptogeren.db")


db_path = caminho_banco()
conexao = sqlite3.connect(db_path)
cursor=conexao.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS criptogeren(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               moeda TEXT NOT NULL,
               quantidade REAL NOT NULL,
               preço  REAL NOT NULL,
               total REAL NOT NULL)
               ''')
def limpar():
    os.system('cls'if os.name=='nt' else 'clear')

def add_cript():
    try:
        select_name=input('digite o nome da criptomoeda:\n')
        quantidade=int(input('digite a quantidade:\n'))
        url= "https://api.coingecko.com/api/v3/simple/price"
        params={
            'ids':select_name,
            'vs_currencies':'usd'
            }
        resp=requests.get(url,params=params)
        dados=resp.json()
        preco=float(dados[select_name]['usd'])
        total=quantidade*preco

        cursor.execute('''INSERT INTO criptogeren (moeda,quantidade,preço,total) VALUES (?,?,?,?)'''
                    ,(select_name,quantidade,preco,total))
        conexao.commit()
        
        
    except ValueError:
        print('certifique que esta inserindo os dados corretamente ')
    except KeyError:
        print('certifique que digitou o nome da cripto de forma correta')
    except KeyboardInterrupt:
        exit()

def delet():
    try:
        while True:
            cursor.execute('SELECT moeda,quantidade,preço,total FROM criptogeren')
            print('-'*90)
            for moeda,quantidade,preço,total in cursor:
                print(f'moeda: {moeda:^10}    qunatidade: {quantidade:^10}    preço: {preço:^10}$    total: {total:.2f}$   ')
            print('-'*90)

            select_name=str(input('digite o nome da moeda:\n1 para sair\n'))
            if select_name=='1':
                break
            cursor.execute('''DELETE FROM criptogeren
                    WHERE moeda = ?''',(select_name,))
            conexao.commit()
            
                
    except ValueError:
        print('digite os dados corretamente')

def ler_cart():
    valor_cart=0
    cursor.execute('SELECT moeda,total FROM criptogeren')
    dados=cursor.fetchall()
    print('-'*40)
    
    for moeda,total in dados:
        print(f'moeda:{moeda:^10}   ',end=(''))
        print(f'total:{total:.2f}$')
        valor_cart+=total
    print('-'*40)
    print(f'       acumulado:  {valor_cart:.2f}$\n')
    conexao.commit()

def altera_quanti():
    cursor.execute('SELECT moeda,quantidade FROM criptogeren')
    dados=cursor.fetchall()
    print('-'*90)
    for moeda,quantidade in dados:
        print(f'moeda:{moeda}     quantidade:{quantidade}')
    print('-'*90)
    
    try:
        select_name=str(input('digite o nome da moeda: '))
        cursor.execute('SELECT quantidade,preço FROM criptogeren WHERE moeda =?',(select_name,))
        resultado=cursor.fetchone()
        if resultado is None:
            print('moeda não encontrada')
            return
        quantidade_atual,preco=resultado
        quantidade_mudar=input('digite a quantidade (sinal de "-" para retirar)')
        if quantidade_mudar.startswith('-'):
            quantidade_nova=quantidade_atual-abs(float(quantidade_mudar))
        else:
            quantidade_nova=quantidade_atual+float(quantidade_mudar)
        print(select_name,quantidade_nova)
        novo_total=preco*quantidade_nova
        cursor.execute('UPDATE criptogeren SET quantidade=?, total=? WHERE moeda =?',(quantidade_nova,novo_total,select_name)) 
        conexao.commit()
        
    except ValueError:
        print('digite os dados corretamente')


while True:
    limpar()
    ler_cart()
    print('1- para adicionar')
    print('2- para deletar')
    print('3- para alterar quantidade')
    print('4- sair')
    try:
        select=int(input())
        if select == 1:
            limpar()
            add_cript()
        elif select == 2:
            limpar()
            delet()
        elif select ==3:
            altera_quanti()
        elif select ==4:
            conexao.close()
            break
        
    except ValueError:
        print('selecione com o digito')

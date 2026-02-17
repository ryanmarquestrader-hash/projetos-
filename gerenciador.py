import sqlite3
import sys
import os

def limpar():
    os.system('cls'if os.name=='nt'else 'clear')

def caminho():
    if sys.platform.startswith('win'):
        base=os.getenv('APPDATA')
    else:
        base=os.path.expanduser('~')
    pasta=os.path.join(base,'clientes')
    os.makedirs(pasta,exist_ok=True)
    return os.path.join(pasta,'clientes.db')

db_path=caminho()
connect=sqlite3.connect(db_path)
cursor=connect.cursor()

def criando():
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL,
                pedido TEXT NOT NULL,
                cpf TEXT NOT NULL)
               ''')
    connect.commit()

def lerclientes():
    print('Clientes \n')
    try:
        cursor.execute('SELECT nome,endereco,pedido FROM clientes')
        dados=cursor.fetchall()
        for nome,endereco,pedido in dados:
            print(f'nome:{nome}\nendereço:{endereco}\npedido:{pedido}')
            print('-'*40)
        connect.commit()
    except sqlite3.OperationalError:
        print('criando tabela')
        criando()

def adicionarcliente():
    print('adicionando clientes \n')
    criando()
    try:
        nome_cliente=input('nome: ')
        endereco_cliente=input('endereço:')
        pedido_cliente=input('pedido:')
        cpf_cliente=input('CPF: ')
        cursor.execute('''INSERT INTO clientes (nome,endereco,pedido,cpf) VALUES(?,?,?,?)'''
                    ,(nome_cliente,endereco_cliente,pedido_cliente,cpf_cliente))
        connect.commit()
    except sqlite3.OperationalError:
        limpar()
        print('criando tabela')
        criando()
        
    
def buscarcliente():
    print('procurando clientes')
    try:
        cpf_cliente=input('CPF: ')
        cursor.execute('''SELECT nome,endereco,pedido FROM clientes WHERE cpf=?''',(cpf_cliente,))
        dados=cursor.fetchall()
        for nome,endereco,pedido in dados:
            print(f'nome:{nome}\nendereço:{endereco}\npedido:{pedido}')
            print('-'*40)
    except sqlite3.OperationalError:
        print('não ha clientes')
        limpar()
        

def deletarcliente():
    print('deletando clientes')
    cursor.execute('SELECT nome,endereco,pedido,cpf FROM clientes')
    dados=cursor.fetchall()
    for nome,endereco,pedido,cpf in dados:
        print(f'nome:{nome}\nendereço:{endereco}\npedido:{pedido}\ncpf:{cpf}')
        print('-'*40)
    connect.commit()
    cpf_cliente=input('CPF: ')
    if cpf_cliente == cpf:
        cursor.execute('''DELETE FROM clientes WHERE cpf=? ''',(cpf_cliente,))
        connect.commit()
        limpar()
        print('deletado')
    else:
        print('não existe')
        return 
    




def apagartabela():
    input('deletando tabela')
    info=input('1-para deletar\n2-para retornar\n')
    if info =='1':
        cursor.execute('DROP TABLE IF EXISTS clientes')
        connect.commit()
    elif info =='2':
        limpar()
    else:
        limpar()
        print('opção invalida')
    

while True:
    print('-'*40)
    try:
        select=int(input('1-ler\n2-adicionar\n3-buscar\n4-apagar tabela\n5-apagar cliente\n6-sair\n'))
        if select ==1:
            limpar()
            lerclientes()
        elif select==2:
            limpar()
            adicionarcliente()
        elif select==3:
            limpar()
            buscarcliente()
        elif select==4:
            limpar()
            apagartabela()
        elif select==5:
            limpar()
            deletarcliente()
        elif select==6:
            limpar()
            connect.close()
            break
        else:
            limpar()
            print('selecione uma opção valida')
            continue
    except ValueError:
        print('digite os dados corretamente')
        continue

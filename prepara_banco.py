import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )
    if conn.is_connected():
        print('Conectado ao MySQL!')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
    exit()

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")
cursor.execute("CREATE DATABASE `jogoteca`;")
cursor.execute("USE `jogoteca`;")

# Criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
    CREATE TABLE `jogos` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `categoria` varchar(40) NOT NULL,
    `console` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['User'] = ('''
    CREATE TABLE `user` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(300) NOT NULL,
    `email` varchar(100) NOT NULL,
    `senha` varchar(100) NOT NULL,
    `login` varchar(100) NOT NULL,
    `grupo` varchar(30) NOT NULL,
    `telefone` varchar(30) NOT NULL,
    `cargo` varchar(50),
    `setor` varchar(50),
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}:', end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserindo usuários na tabela 'usuarios'
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('SELECT * FROM usuarios')
print(' -------------  Usuários (usuarios):  -------------')
for user in cursor.fetchall():
    print(user[1])

# Inserindo usuários na tabela 'user'
user_sql = 'INSERT INTO user (nome, email, senha, login, grupo, telefone, cargo, setor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
users = [
    ("admin", "adm@agenciatechcoffee.com.br", generate_password_hash("techcoffee").decode('utf-8'), "admin", "admin", "123456789", "Gerente", "TI"),
    ("Matheus", "matheus@exemplo.com", generate_password_hash("paozinho").decode('utf-8'), "Matheus", "user", "987654321", "Assistente", "Vendas"),
    ("Guilherme Louro", "guilherme@exemplo.com", generate_password_hash("python_eh_vida").decode('utf-8'), "Guilherme", "user", "456123789", "Desenvolvedor", "TI")
]
cursor.executemany(user_sql, users)

cursor.execute('SELECT * FROM user')
print(' -------------  Usuários (user):  -------------')
for user in cursor.fetchall():
    print(user)

# Inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('SELECT * FROM jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# Commitando as alterações
conn.commit()

cursor.close()
conn.close()

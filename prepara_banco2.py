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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

TABLES['customer'] = ('''
    CREATE TABLE `customer` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `razao_social` varchar(200) NOT NULL,
    `nome_fantasia` varchar(100) NOT NULL,
    `cnpj` varchar(30),
    `cpf` varchar(30),
    `inscricao_estadual` varchar(50),
    `inscricao_municipal` varchar(50),
    `telefone` varchar(50),
    `celular` varchar(50),
    `email` varchar(100),
    `tipo_conta` varchar(20),
    `endereco` varchar(100),
    `bairro` varchar(100),
    `cidade` varchar(100),
    `estado` varchar(5),
    `numero` varchar(10),
    `cep` varchar(10),
    `complemento` varchar(100),
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

TABLES['prospect'] = ('''
    CREATE TABLE `prospect` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `data_hora_cadastro` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `nome_completo` varchar(300) NOT NULL,
    `telefone` varchar(30) NOT NULL,
    `email` varchar(100) NOT NULL,
    `observacao` text,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

TABLES['activity'] = ('''
    CREATE TABLE `activity` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `cliente_id` int(11),
    `prospect_id` int(11),
    `usuario_id` int(11),
    `consultor_id` int(11),
    `data_hora_criacao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `titulo` varchar(200) NOT NULL,
    `descricao` text,
    `status` varchar(50) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`cliente_id`) REFERENCES `customer` (`id`),
    FOREIGN KEY (`prospect_id`) REFERENCES `prospect` (`id`),
    FOREIGN KEY (`usuario_id`) REFERENCES `user` (`id`),
    FOREIGN KEY (`consultor_id`) REFERENCES `user` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print(f'Criando tabela {table_name}:', end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

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

# Inserindo clientes
cliente_sql = 'INSERT INTO `customer` (razao_social, nome_fantasia, cnpj, cpf, inscricao_estadual, inscricao_municipal, telefone, celular, email, tipo_conta, endereco, bairro, cidade, estado, numero, cep, complemento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
clientes = [
        ('Empresa A', 'Fantasia A', '00.000.000/0000-00', '000.000.000-00', '123456789', '987654321', '12345678', '87654321', 'empresaA@exemplo.com', 'corporativo', 'Rua A', 'Bairro A', 'Cidade A', 'ES', '100', '29060-100', 'Complemento A'),
        ('Empresa B', 'Fantasia B', '11.111.111/1111-11', '111.111.111-11', '223456789', '887654321', '22345678', '77654321', 'empresaB@exemplo.com', 'corporativo', 'Rua B', 'Bairro B', 'Cidade B', 'MG', '200', '30130-100', 'Complemento B'),
        ('Empresa C', 'Fantasia C', '22.222.222/2222-22', '222.222.222-22', '323456789', '787654321', '32345678', '67654321', 'empresaC@exemplo.com', 'corporativo', 'Rua C', 'Bairro C', 'Cidade C', 'SP', '300', '01000-000', 'Complemento C')
]
cursor.executemany(cliente_sql, clientes)

cursor.execute('SELECT * FROM customer')
print(' -------------  Clientes:  -------------')
for cliente in cursor.fetchall():
    print(cliente)

# Inserindo prospects
prospect_sql = 'INSERT INTO prospect (nome_completo, telefone, email, observacao) VALUES (%s, %s, %s, %s)'
prospects = [
    ('João Silva', '123456789', 'joao@exemplo.com', 'Interessado em serviços de TI'),
    ('Maria Souza', '987654321', 'maria@exemplo.com', 'Precisa de consultoria financeira'),
    ('Carlos Pereira', '456123789', 'carlos@exemplo.com', 'Solicitou proposta de marketing')
]
cursor.executemany(prospect_sql, prospects)

cursor.execute('SELECT * FROM prospect')
print(' -------------  Prospects:  -------------')
for prospect in cursor.fetchall():
    print(prospect)

# Inserindo atividades
atividade_sql = 'INSERT INTO activity (cliente_id, prospect_id, usuario_id, consultor_id, titulo, descricao, status) VALUES (%s, %s, %s, %s, %s, %s, %s)'
atividades = [
    (1, 1, 1, 2, 'Atividade 1', 'Descrição da atividade 1', 'Aberto'),
    (2, 2, 2, 3, 'Atividade 2', 'Descrição da atividade 2', 'Em Progresso'),
    (3, 3, 3, 1, 'Atividade 3', 'Descrição da atividade 3', 'Concluído')
]
cursor.executemany(atividade_sql, atividades)

cursor.execute('SELECT * FROM activity')
print(' -------------  Atividades:  -------------')
for atividade in cursor.fetchall():
    print(atividade)

# Commitando as alterações
conn.commit()

cursor.close()
conn.close()

import oracledb

SERVIDOR = 'oracle.fiap.com.br'
PORTA = 1521
SERVICO = 'ORCL'

def abre_conexao():
    try:
        conexao = oracledb.connect(
            user='rm561995',
            password='200107',
            dsn=f'{SERVIDOR}:{PORTA}/{SERVICO}'
        )
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def adicionar_colaborador():
    conn = abre_conexao()
    if not conn:
        print("Erro: Não foi possível conectar ao Banco de Dados.")
        return

    cursor = conn.cursor()

    print("\n----- Cadastro de colaborador -----")
    nome = input("Digite o nome do colaborador(a): ")
    cpf = input("Digite o CPF do colaborador(a): ")
    departamento = input("Digite o setor do colaborador(a)")

    try:
        sql = """
            INSERT INTO COLABORADOR (NOME, DEPARTAMENTO, CPF)
            VALUES (:1, :2, :3)
        """

        cursor.execute(sql, (nome, departamento, cpf))
        conn.commit()

        print("✅ Colaborador cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao cadastrar:", e)

    cursor.close()
    conn.close()
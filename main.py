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

def adicionar_colaborador(conexao, cursor):
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

def buscar_colaborador():
    conn = abre_conexao()
    if not conn:
        print("Erro: Não foi possível conectar ao Banco de Dados.")
        return

    cursor = conn.cursor()

    try:
        cpf = input("Digite o CPF do colaborador: ").strip()

        cursor.execute('''
            SELECT
                ID_COLABORADOR, NOME, DEPARTAMENTO, CPF, DATA_NASCIMENTO 
            FROM COLABORADOR
            WHERE cpf = :cpf
            ''',{'cpf': cpf}   
    )
        resultado = cursor.fetchone()

        if not resultado:
            print("Nenhum paciente encontrado com esse CPF.")     
            return
        try:
            data_nascimento = resultado[2].strftime('%Y-%m-%d')
        except:
            data_nascimento = str(resultado[2])

        print("\n----- Dados do colaborador -----")
        print(f"Matrícula colaborador: {resultado[0]}")
        print(f"Nome: {resultado[1]}")
        print(f"Departamento: {resultado[2]}")
        print(f"CPF: {resultado[3]}")
        print(f"Data de nascimento: {resultado[4]}")
         
    except Exception as e:
        print(f"Erro ao consultar paciente: {e}") 

    
    query = '''
        SELECT ID_COLABORADOR, NOME, DEPARTAMENTO, CPF
        FROM COLABORADOR
        ORDER BY ID_COLABORADOR
    '''

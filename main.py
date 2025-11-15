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
        conexao.commit()

        print("✅ Colaborador cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao cadastrar:", e)

    

def buscar_colaborador():
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
            print("Nenhum colaborador encontrado com esse CPF.")     
            return
        try:
            data_nascimento = resultado[4].strftime('%Y-%m-%d')
        except:
            data_nascimento = str(resultado[4])

        print("\n----- Dados do colaborador -----")
        print(f"Matrícula colaborador: {resultado[0]}")
        print(f"Nome: {resultado[1]}")
        print(f"Departamento: {resultado[2]}")
        print(f"CPF: {resultado[3]}")
        print(f"Data de nascimento: {data_nascimento}")
         
    except Exception as e:
        print(f"Erro ao consultar paciente: {e}") 


if __name__ == '__main__':
    conexao = abre_conexao()
    if not conexao:
        print("Erro: Não foi possível conectar ao Banco de Dados.")
        exit()
    cursor = conexao.cursor()
    em_execucao = True

    while em_execucao:
        print("\n----- Bem estar do seu colaborador -----")
        print("0 - Encerrar programa")
        print("1 - Inserir colaborador")
        print("2 - Buscar colaborador por cpf")
        print("3 - Quero registrar meus sentimentos")
        print("4 - Excluir colaborador")
        print("5 - Atualizar colaborador")
        print("6 - Números de emergência")
        try:
            opcao = int(input("Escolha uma opção"))
            print("-----")
            match opcao:
                case 0:
                    em_execucao = False
                case 1:
                    adicionar_colaborador(conexao, cursor)
                case 2:
                    buscar_colaborador()
                case 3:
                    registrar_sentimento()
                case 4:
                    excluir_colaborador()
                case 5:
                    atualizar_colaborador()
                case 6:
                    numeros_emergencia()
        except Exception as e:
            print(f"Digite sua opção entre 0 e 6. {e}")
    cursor.close()
    conexao.close()

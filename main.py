import oracledb
from datetime import datetime
import json

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
    try:
        dicionario = {
            'nome' : input("Digite o nome do colaborador(a): "),
            'cpf' : input("Digite o CPF do colaborador(a): "),
            'departamento' : input("Digite o setor do colaborador(a): "),
            'dt_nasc' : datetime.strptime(input('Digite a data de nascimento (DD/MM/YYYY): '), '%d/%m/%Y'),
        }
        query = """
            INSERT INTO COLABORADOR (NOME, DEPARTAMENTO, CPF, DATA_NASCIMENTO)
            VALUES (:nome, :departamento, :cpf, :dt_nasc )
        """

        cursor.execute(query, dicionario)
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
        ''', {'cpf': cpf})

        resultado = cursor.fetchone()

        if not resultado:
            print("Nenhum colaborador encontrado com esse CPF.")
            return

       
        try:
            data_nascimento = resultado[4].strftime('%Y-%m-%d')
        except:
            data_nascimento = str(resultado[4])

        colaborador_json = {
            "id_colaborador": resultado[0],
            "nome": resultado[1],
            "departamento": resultado[2],
            "cpf": resultado[3],
            "data_nascimento": data_nascimento
        }

       
        print("\n----- Dados do colaborador -----")
        print(f"Matrícula colaborador: {resultado[0]}")
        print(f"Nome: {resultado[1]}")
        print(f"Departamento: {resultado[2]}")
        print(f"CPF: {resultado[3]}")
        print(f"Data de nascimento: {data_nascimento}")

        
        resposta = input("\nDeseja exportar os resultados para JSON? (S/N) ")

        if resposta.upper() == "S":
            with open("resultado_consulta_colaborador.json", "w", encoding="utf-8") as arquivo:
                json.dump(colaborador_json, arquivo, indent=4, ensure_ascii=False)

            print("Resultados exportados com sucesso!")

    except Exception as e:
        print(f"Erro ao consultar colaborador: {e}")
 

def registrar_sentimento():
    while True:
        print("--- Esse é o espaço do colaborador, se sinta livre para utilizá-lo ---")
        print("1 - Registrar novo sentimento")
        print("2 - Dicas para se acalmar")
        print("0 - Voltar")

        escolha = int(input("Escolha uma opção: "))

        try:
            match escolha:
                case 0:
                    break
                case 1:
                    inserir_sentimento()
                case 2:
                    dicas_importantes()
        except:
            print("Opção inválida, escolha de 0 a 3.") 

def inserir_sentimento():
    print("--- Registre aqui seu sentimento hoje ---")
    try:
        cpf = input("Digite o CPF do colaborador: ")

        cursor.execute("""
            SELECT ID_COLABORADOR 
            FROM COLABORADOR 
            WHERE CPF = :cpf
        """, {"cpf": cpf})

        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Colaborador não encontrado!")
            return

        id_colaborador = resultado[0]
        dicionario = {
            'id_colaborador': id_colaborador,
            'humor' : int(input("De 0 a 10, qual seu humor hoje?")),
            'estresse' : int(input("De 0 a 10, qual seu nível de estresse hoje?")),
            'descricao' : input("Descreva o porque das suas notas acima: ")
        }

        query = '''
            INSERT INTO HUMOR_REGISTRO(
                ID_COLABORADOR, HUMOR, ESTRESSE, DESCRICAO
            )
            VALUES(
                :id_colaborador ,:humor, :estresse, :descricao
            )
        '''
        cursor.execute(query, dicionario)
        conexao.commit()
        print("Registro realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir registro de sentimento: {e}")

def dicas_importantes():
    print("--- Aqui estão alguns contatos importantes, você não está sozinho(a)")
    print("📞 188 — CVV (apoio emocional 24h)")
    print("📞 192 — SAMU (emergências)")
    print("📞 190 — Polícia Militar")
    print("📞 193 — Bombeiros")
    print("📞 136 — Disque Saúde")
    print("🔎 CAPS — Procure o CAPS mais próximo na sua cidade")
    print("--- Cuidar da sua saúde mental é essencial. ---")

def excluir_colaborador(conexao, cursor):
    print("\n----- Excluir colaborador -----")

    try:
        cpf = input("Digite o CPF do colaborador que deseja excluir: ").strip()

      
        cursor.execute("""
            SELECT NOME, CPF, DEPARTAMENTO FROM COLABORADOR WHERE CPF = :cpf
        """, {"cpf": cpf})

        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Nenhum colaborador encontrado com esse CPF.")
            return

        print(f"\nColaborador encontrado: {resultado[0]}")
        print(f"CPF: {resultado[1]}")
        print(f"Departamento: {resultado[2]}")
        confirm = input("Tem certeza que deseja excluir? (s/n): ").lower()

        if confirm != "s":
            print("Operação cancelada.")
            return

        cursor.execute("""
            DELETE FROM COLABORADOR WHERE CPF = :cpf
        """, {"cpf": cpf})

        conexao.commit()

        print("✅ Colaborador removido com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao remover colaborador: {e}")

def atualizar_colaborador(conexao, cursor):
    print("\n----- Atualizar colaborador -----")

    try:
        cpf = input("Digite o CPF do colaborador que deseja atualizar: ").strip()

        
        cursor.execute("""
            SELECT ID_COLABORADOR, NOME, DEPARTAMENTO, CPF, DATA_NASCIMENTO
            FROM COLABORADOR
            WHERE CPF = :cpf
        """, {"cpf": cpf})

        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Nenhum colaborador encontrado com esse CPF.")
            return

      
        id_colab = resultado[0]
        nome_atual = resultado[1]
        depto_atual = resultado[2]
        cpf_atual = resultado[3]
        data_nasc_atual = resultado[4]

        print("\n----- Dados atuais -----")
        print(f"Nome: {nome_atual}")
        print(f"Departamento: {depto_atual}")
        print(f"CPF: {cpf_atual}")
        print(f"Data de nascimento: {data_nasc_atual}")

        print("\nDeixe em branco caso NÃO deseje alterar o campo.")

        
        novo_nome = input("Novo nome: ").strip()
        novo_departamento = input("Novo departamento: ").strip()
        novo_cpf = input("Novo CPF: ").strip()
        nova_data_nasc = input("Nova data de nascimento (DD/MM/YYYY): ").strip()

        
        nome_final = novo_nome if novo_nome else nome_atual
        departamento_final = novo_departamento if novo_departamento else depto_atual
        cpf_final = novo_cpf if novo_cpf else cpf_atual

       
        if nova_data_nasc:
            try:
                from datetime import datetime
                data_obj = datetime.strptime(nova_data_nasc, "%d/%m/%Y")
                data_final = data_obj
            except:
                print("❌ Data inválida! Use o formato DD/MM/YYYY.")
                return
        else:
            data_final = data_nasc_atual

        
        cursor.execute("""
            UPDATE COLABORADOR
            SET NOME = :nome,
                DEPARTAMENTO = :departamento,
                CPF = :cpf,
                DATA_NASCIMENTO = :data_nasc
            WHERE ID_COLABORADOR = :id_colab
        """, {
            "nome": nome_final,
            "departamento": departamento_final,
            "cpf": cpf_final,
            "data_nasc": data_final,
            "id_colab": id_colab
        })

        conexao.commit()
        print("✅ Dados atualizados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao atualizar colaborador: {e}")


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
        try:
            opcao = int(input("Escolha uma opção: "))
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
                    excluir_colaborador(conexao, cursor)
                case 5:
                    atualizar_colaborador(conexao, cursor)
            
        except Exception as e:
            print(f"Digite sua opção entre 0 e 5. {e}")
    cursor.close()
    conexao.close()

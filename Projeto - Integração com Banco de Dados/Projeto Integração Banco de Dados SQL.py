#tabela utilizada no SQL server:

"""
create table usuarios(
id_usuario int primary key identity,
usuario varchar(50) unique,
senha varchar(50),
)
"""

# Conexão ao Banco de Dados SQL SERVER
import pyodbc

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-15526VS;"
    "Database=BancoDeDados;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()


def menu():
        print("\n\t\t\t\033[94m****** SEJA BEM-VINDO(a) ******\033[0m\n")
        print("\t\t\t- DIGITE 1 PARA CADASTRAR USUÁRIO")
        print("\t\t\t- DIGITE 2 PARA FAZER LOGIN")
        print("\t\t\t- DIGITE 3 PARA EXCLUIR USUÁRIO")
        print("\t\t\t- DIGITE 4 PARA MOSTRAR USUÁRIOS E SENHAS")
        print("\t\t\t- DIGITE 'SAIR' PARA ENCERRAR O PROGRAMA")
        while True:
            escolha = input("")
            if escolha == "1":
                cadastro()
                break
            elif escolha == "2":
                login()
                break
            elif escolha == "3":
                excluir()
                break
            elif escolha == "4":
                mostrar_usuarios()
                break
            elif escolha == "5":
                editar_usuario()
                break
            elif escolha.lower() == "sair":
                print("\033[96mPROGRAMA ENCERRADO\033[0m")
                break
            else:
                print("Comando Iválido, digite novamente:")


def cadastro():
        global usuario, senha
        usuario = input("\nDigite um nome de usuário para criar seu Login: ").strip()
        while usuario=="":
            usuario = input("\nNome de usuário vazio, digite um nome de usuário válido para criar seu Login:").strip()
        # Verifica se o usuário digitado existe no banco de dados
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", usuario)
        usuario_existente = cursor.fetchone()
        # Caso já exista, pedir pra digitar outro usuário
        while usuario_existente:
            print("\nUsuário já existente...")
            usuario = input("\nDigite um nome de usuário para criar seu Login: ").strip()
            while usuario == "":
                usuario = input("\nNome de usuário vazio, digite um nome de usuário válido: ").strip()
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
            usuario_existente = cursor.fetchone()

        while True:
            senha = input("Digite um senha: ").strip()
            if senha == "":
                print("\nSenha vazia...\n")
            elif " " in senha:
                print("\nSenha não pode conter espaços...\n")
            else:
                break
        #Insere usuário e senha no banco de dados
        comando = f"insert into usuarios(usuario,senha) values ('{usuario}','{senha}')"
        cursor.execute(comando)
        cursor.commit()
        print("\nMuito Bem! Usuário e senha cadastrados com sucesso!")
        print("Pressione ENTER para voltar ao menu...")
        input()
        menu()
        return


def login():
        #verifica se o banco de dados possui usuários
        cursor.execute('SELECT usuario,senha FROM usuarios')
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum usuário cadastrado, pressione ENTER para voltar para o menu...")
            input()
            menu()
            return
        usuario1 = input("\nPara entrar digite o seu usuário: ").strip()
        #verifica se o usuário digitado existe
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", usuario1)
        usuario_existente = cursor.fetchone()
        # Caso usuário não exista, pedir pra digitar outro usuário
        while not usuario_existente:
            usuario1 = input("Usuário não cadastrado, digite um usuário válido, ou pressione 3 para voltar ao menu:").strip()
            if usuario1 == "3":
                menu()
                return
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", usuario1)
            usuario_existente = cursor.fetchone()

        tentativas = 0
        while True:
            senha1 = input("Digite a sua senha:").strip()
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", usuario1)
            stored_password = cursor.fetchone()
            #Verifica se a senha digitada corresponde
            if stored_password and stored_password[0] == senha1:
                print(f"\nACESSO GARANTIDO, Bem-vindo(a) \033[34m{usuario1}\033[0m")
                print("Pressione uma tecla para acessar a Lanchonete...")
                input()
                menu_Lanchonete()
                return
            else:
                tentativas += 1
                if tentativas == 1:
                    print("\033[91mACESSO NEGADO, TENTE NOVAMENTE, 3 tentativas restantes...\n\033[0m")
                elif tentativas == 2:
                    print("\033[91mACESSO NEGADO, TENTE NOVAMENTE, 2 tentativas restantes...\n\033[0m")
                elif tentativas == 3:
                    print("\033[91mACESSO NEGADO, TENTE NOVAMENTE, 1 tentativa restantes...\n\033[0m")
                elif tentativas == 4:
                    print("\033[91mACESSO BLOQUEADO")
                    break


def excluir():
        excluir_usuario = input("\nDigite o usuário que deseja excluir:").strip()
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", excluir_usuario)
        usuario_existente = cursor.fetchone()

        while not usuario_existente:
            excluir_usuario = input("\nUsuário não cadastrado, digite um usuário válido, ou pressione 3 para voltar ao menu:").strip()
            if excluir_usuario == "3":
                menu()
                return
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", excluir_usuario)
            usuario_existente = cursor.fetchone()

        senha1 = input("Digite a sua senha:").strip()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", excluir_usuario)
        stored_password = cursor.fetchone()

        if stored_password and stored_password[0] == senha1:
            comando = f"DELETE FROM usuarios WHERE usuario = '{excluir_usuario}'"
            cursor.execute(comando)
            conexao.commit()

            print("\nUsuário excluído com sucesso. Pressione uma tecla para voltar ao menu...")
            input()
            menu()
            return
        else:
            print("\nSenha incorreta. A exclusão do usuário não pode ser realizada.")
            menu()
            return


def menu_Lanchonete():
        global precoTotal, unidadeCoxinha, unidadePaodequeijo, unidadeRocambole, unidadeBatatafrita, unidadeHamburguer, unidadeRefrigerante, unidadeSuco
        precoTotal = 0
        unidadeCoxinha = 0
        unidadePaodequeijo = 0
        unidadeRocambole = 0
        unidadeBatatafrita = 0
        unidadeHamburguer = 0
        unidadeRefrigerante = 0
        unidadeSuco = 0
        print("\n\t******Seja Bem-vindo à Lanchonete Virtual******\n\n");

        print(" 1.Coxinha---------R$5,00")
        print(" 2.Pão de Queijo---R$4,00")
        print(" 3.Rocambole-------R$5,50")
        print(" 4.Batata Frita----R$6,00")
        print(" 5.Hambúrguer------R$5,00")
        print(" 6.Refrigerante----R$3,50")
        print(" 7.Suco------------R$3,00\n\n")
        print("Digite o seu pedido, item por item (máx 20 itens), pressione 0 para encerrar o seu pedido e ir para a forma de Pagamento, digite 'voltar' para voltar para o menu principal...")

        for i in range(100):
            escolha_Produtos = input("")
            if escolha_Produtos.lower().strip() in ["coxinha", "1"]:
                unidadeCoxinha += 1
                precoTotal += 5
            elif escolha_Produtos.lower().strip() in ["pão de queijo", "2"]:
                unidadePaodequeijo += 1
                precoTotal += 4
            elif escolha_Produtos.lower().strip() in ["rocambole", "3"]:
                unidadeRocambole += 1
                precoTotal += 5.5
            elif escolha_Produtos.lower().strip() in ["batata frita", "4"]:
                unidadeBatatafrita += 1
                precoTotal += 6
            elif escolha_Produtos.lower().strip() in ["hambúrguer", "hamburguer", "5"]:
                unidadeHamburguer += 1
                precoTotal += 5
            elif escolha_Produtos.lower().strip() in ["refrigerante", "6"]:
                unidadeRefrigerante += 1
                precoTotal += 3.5
            elif escolha_Produtos.lower().strip() in ["suco", "7"]:
                unidadeSuco += 1
                precoTotal += 3
            elif escolha_Produtos.lower().strip() == "0":
                carrinho()
                return
            elif escolha_Produtos.lower().strip() == "voltar":
                menu()
                return
            else:
                print("Item não cadastrado, digite novamente:")


def carrinho():
        global formaPagamento, valordotroco
        valordotroco = 0
        print("\n***CARRINHO***")
        if (unidadeCoxinha == 1):
            print(unidadeCoxinha, "Coxinha")
        elif (unidadeCoxinha > 1):
            print(unidadeCoxinha, "Coxinhas")
        if (unidadePaodequeijo == 1):
            print(unidadePaodequeijo, "Pão de Queijo")
        elif (unidadePaodequeijo > 1):
            print(unidadePaodequeijo, "Pães de Queijo")
        if (unidadeRocambole == 1):
            print(unidadeRocambole, "Rocambole")
        elif (unidadeRocambole > 1):
            print(unidadeRocambole, "Rocamboles")
        if (unidadeBatatafrita == 1):
            print(unidadeBatatafrita, "Batata Frita")
        elif (unidadeBatatafrita > 1):
            print(unidadeBatatafrita, "Batatas Fritas")
        if (unidadeHamburguer == 1):
            print(unidadeHamburguer, "Hambúrguer")
        elif (unidadeHamburguer > 1):
            print(unidadeHamburguer, "Hambúrgueres")
        if (unidadeRefrigerante == 1):
            print(unidadeRefrigerante, "Refrigerante")
        elif (unidadeRefrigerante > 1):
            print(unidadeRefrigerante, "Refrigerantes")
        if (unidadeSuco == 1):
            print(unidadeSuco, "Suco")
        elif (unidadeSuco > 1):
            print(unidadeSuco, "Sucos")
        print(f"\nTotal a pagar:R${precoTotal}")
        print("\n\nQual a forma de pagamento:\n");
        formaPagamento = input("1-Dinheiro\n2-Cartão de Crédito\n3-Cartão de Débito\n\n");
        while formaPagamento not in ["1", "2", "3"]:
            formaPagamento = input("Comando Inválido, escolha um número equivalente a sua forma de pagamento:\n\n1-Dinheiro\n2-Cartão de Crédito\n3-Cartão de Débito\n\n");
        if formaPagamento == "1":
            opcaotroco = input("\n1-Troco\n2-Sem Troco\n\n")
            while opcaotroco not in ["1", "2"]:
                opcaotroco = input("\nComando Inválido\n1-Troco\n2-Sem Troco\n")
            if opcaotroco == "1":
                vtroco = input("\nTroco para quanto?\n")
                while True:
                    try:
                        vtroco = float(vtroco)
                        if vtroco < precoTotal:
                            vtroco = input("Dinheiro Insuficiente, digite novamente:\n")
                        else:
                            break
                    except ValueError:
                        vtroco = input("Comando Inválido, digite um número:\n")

                valordotroco = float(vtroco) - precoTotal
                PedirEndereco()
                return
            elif opcaotroco == "2":
                PedirEndereco()
                return

        else:
            PedirEndereco()
            return


def PedirEndereco():
        enderecoEntrega = []
        print("\nDigite o seu endereço para entrega:\n")
        cidade = input("CIDADE:").strip()
        while cidade.strip() == "":
            cidade = input("Campo obrigatório, CIDADE:")
        enderecoEntrega.append(cidade)
        bairro = input("BAIRRO:").strip()
        while bairro.strip() == "":
            bairro = input("Campo obrigatório, BAIRRO:")
        enderecoEntrega.append(bairro)
        nome_rua = input("NOME DA RUA:").strip()
        while nome_rua.strip() == "":
            nome_rua = input("Campo obrigatório, NOME DA RUA:")
        enderecoEntrega.append(nome_rua)
        numero = input("NÚMERO:").strip()
        while numero.strip() == "":
            numero = input("Campo obrigatório, NÚMERO:")
        enderecoEntrega.append(numero)
        print("\nPEDIDO REALIZADO!\n")
        print("**Resumo do pedido**")
        if (unidadeCoxinha == 1):
            print(f"--{unidadeCoxinha} Coxinha")
        elif (unidadeCoxinha > 1):
            print(f"--{unidadeCoxinha} Coxinhas")
        if (unidadePaodequeijo == 1):
            print(f"--{unidadePaodequeijo} Pão de Queijo")
        elif (unidadePaodequeijo > 1):
            print(f"--{unidadePaodequeijo} Pães de Queijo")
        if (unidadeRocambole == 1):
            print(f"--{unidadeRocambole} Rocambole")
        elif (unidadeRocambole > 1):
            print(f"--{unidadeRocambole} Rocamboles")
        if (unidadeBatatafrita == 1):
            print(f"--{unidadeBatatafrita} Batata Frita")
        elif (unidadeBatatafrita > 1):
            print(f"--{unidadeBatatafrita} Batatas Fritas")
        if (unidadeHamburguer == 1):
            print(f"--{unidadeHamburguer} Hambúrguer")
        elif (unidadeHamburguer > 1):
            print(f"--{unidadeHamburguer} Hambúrgueres")
        if (unidadeRefrigerante == 1):
            print(f"--{unidadeRefrigerante} Refrigerante")
        elif (unidadeRefrigerante > 1):
            print(f"--{unidadeRefrigerante} Refrigerantes")
        if (unidadeSuco == 1):
            print(f"--{unidadeSuco} Suco")
        elif (unidadeSuco > 1):
            print(f"--{unidadeSuco} Sucos")

        print("\nForma de pagamento:")
        if formaPagamento == "1":
            print("--Dinheiro")
        elif formaPagamento == "2":
            print("--Cartão de Crédito")
        elif formaPagamento == "3":
            print("--Cartão de Débito")

        if (valordotroco > 0):
            print(f"\nTroco: R${valordotroco}")
        print("\nEndereço: {}, {}, {}, {}.".format(*enderecoEntrega))


def mostrar_usuarios():
        cursor.execute('SELECT usuario,senha FROM usuarios')
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum usuário cadastrado, pressione ENTER para voltar para o menu...")
            input()
            menu()
            return
        else:
            print("USUÁRIOS E SENHAS:\n")
            for row in rows:
                usuario = row[0]
                senha = row[1]
                print(f"USUÁRIO = {usuario}")
                print(f"SENHA = {'*' * len(senha)}\n")
        print("Pressione ENTER para voltar ao menu...")
        input()
        menu()
        return

def editar_usuario():
    usuario_alterar = input("\nDigite o usuário que deseja alterar: ")
    cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", usuario_alterar)
    usuario_existente = cursor.fetchone()

    # Caso não exista, pedir para digitar outro usuário
    while not usuario_existente:
        usuario_alterar = input("Usuário não cadastrado, digite um usuário válido, ou pressione 3 para voltar ao menu:")
        if usuario_alterar == "3":
            menu()
            return
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", usuario_alterar)
        usuario_existente = cursor.fetchone()

    senha = input("Digite a senha: ")
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", usuario_alterar)
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == senha:
        novo_usuario = input("Digite o novo nome de usuário: ")
        cursor.execute("UPDATE usuarios SET usuario = ? WHERE usuario = ?", novo_usuario, usuario_alterar)
        conexao.commit()
        print("\nUsuário alterado com sucesso. Pressione uma tecla para voltar ao menu...")
        input()
        menu()
        return
    else:
        print("Senha incorreta. A alteração do usuário não pode ser realizada.")
        menu()
        return


menu()

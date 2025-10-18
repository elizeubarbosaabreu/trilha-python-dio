menu = """
[a] Listar usuários
[u] Cadastrar usuário
[b] Buscar usuário
[c] Criar conta
[l] Listar contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """

AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 500.0
usuarios = []
contas = []

# --------------------------
# Funções de usuário
# --------------------------
def filtrar_usuario(cpf, usuarios):
    for u in usuarios:
        if u["cpf"] == cpf:
            return u
    return None

def cadastrar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")
    if filtrar_usuario(cpf, usuarios):
        print("❌ Já existe um usuário com esse CPF.")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("UF: ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("✅ Usuário cadastrado com sucesso.")


def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"{u['nome']} - CPF: {u['cpf']}")


def buscar_usuario(usuarios):
    cpf = input("Digite o CPF: ")
    u = filtrar_usuario(cpf, usuarios)
    if u:
        print("\nUsuário encontrado:")
        for k, v in u.items():
            print(f"{k.title()}: {v}")
    else:
        print("❌ CPF não encontrado.")


# --------------------------
# Funções de conta
# --------------------------
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Digite o CPF do titular: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("❌ Usuário não encontrado. Cadastre o usuário primeiro.")
        return None

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0
    }
    contas.append(conta)
    print(f"✅ Conta criada: Agência {agencia} - Conta {numero_conta} | Titular: {usuario['nome']}")
    return conta


def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    print("Contas cadastradas:")
    for c in contas:
        print(f"Agência: {c['agencia']} | Conta: {c['numero_conta']} | Titular: {c['usuario']['nome']} | Saldo: R$ {c['saldo']:.2f}")


def selecionar_conta(contas):
    """Mostra lista resumida de contas e solicita o número da conta para seleção."""
    if not contas:
        print("Nenhuma conta disponível.")
        return None

    print("Selecione a conta pela número (digite o número da conta):")
    for c in contas:
        print(f"[{c['numero_conta']}] Agência {c['agencia']} - Titular: {c['usuario']['nome']}")

    try:
        numero = int(input("Número da conta: "))
    except ValueError:
        print("Entrada inválida. Informe o número da conta (inteiro).")
        return None

    for c in contas:
        if c["numero_conta"] == numero:
            return c

    print("Conta não encontrada.")
    return None


# --------------------------
# Operações bancárias (por conta)
# --------------------------
def depositar_conta(conta, valor):
    if valor <= 0:
        print("❌ Valor inválido para depósito.")
        return
    conta["saldo"] += valor
    conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
    print("✅ Depósito realizado com sucesso.")


def sacar_conta(conta, valor, limite_valor=LIMITE_SAQUE_VALOR, limite_saques=LIMITE_SAQUES):
    if valor <= 0:
        print("❌ Valor inválido.")
        return

    if valor > conta["saldo"]:
        print(f"❌ Saldo insuficiente. Saldo disponível: R$ {conta['saldo']:.2f}")
        return

    if valor > limite_valor:
        print(f"❌ Valor excede o limite por saque (limite atual: R$ {limite_valor:.2f}).")
        return

    if conta["numero_saques"] >= limite_saques:
        print(f"❌ Número máximo de saques ({limite_saques}) excedido para esta conta.")
        return

    conta["saldo"] -= valor
    conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
    conta["numero_saques"] += 1
    print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")



def exibir_extrato_conta(conta):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("=============================")


# --------------------------
# Loop principal
# --------------------------
def main():
    while True:
        opcao = input(menu).strip().lower()

        if opcao == "u":
            cadastrar_usuario(usuarios)

        elif opcao == "a":
            listar_usuarios(usuarios)

        elif opcao == "b":
            buscar_usuario(usuarios)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "d":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Informe o valor do depósito: "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                depositar_conta(conta, valor)

        elif opcao == "s":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Informe o valor do saque: "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                sacar_conta(conta, valor, limite_valor=LIMITE_SAQUE_VALOR, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            conta = selecionar_conta(contas)
            if conta:
                exibir_extrato_conta(conta)

        elif opcao == "q":
            print("Saindo... Obrigado por usar o sistema.")
            break

        else:
            print("❌ Opção inválida, por favor selecione novamente.")


if __name__ == "__main__":
    main()

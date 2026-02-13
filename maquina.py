produtos = [
    {"nome": "Coca-cola", "preco": 375, "estoque": 2},
    {"nome": "Pepsi", "preco": 367, "estoque": 5},
    {"nome": "Monster", "preco": 996, "estoque": 1},
    {"nome": "Cafe", "preco": 125, "estoque": 100},
    {"nome": "Redbull", "preco": 1399, "estoque": 2}
]

trocos = [
    {"nome": "20 R$", "valor": 2000, "estoque": 10},
    {"nome": "10 R$", "valor": 1000, "estoque": 10},
    {"nome": "5 R$", "valor": 500, "estoque": 10},
    {"nome": "2 R$", "valor": 200, "estoque": 10},
    {"nome": "1 R$", "valor": 100, "estoque": 10},
    {"nome": "50 centavos", "valor": 50, "estoque": 10},
    {"nome": "10 centavos", "valor": 10, "estoque": 10},
    {"nome": "1 centavo", "valor": 1, "estoque": 100}
]

estoqueInicialProdutos = [p["estoque"] for p in produtos]
estoqueInicialTrocos = [t["estoque"] for t in trocos]

carrinho = []
listaTroco = []
contadorCompras = 0


def centavos_para_real(valor):
    return f"{valor/100:.2f}"


def totalCarrinho():
    return sum(item["preco"] * item["qtd"] for item in carrinho)


def mostrarCarrinho():
    print("\n=== CARRINHO ===")
    for i, item in enumerate(carrinho, start=1):
        total = item["preco"] * item["qtd"]
        print(f"{i} - {item['nome']} x{item['qtd']} = R$ {centavos_para_real(total)}")
    print(f"Total: R$ {centavos_para_real(totalCarrinho())}")


def salvarLog(valorPago, troco):
    with open("historico.txt", "a", encoding="utf-8") as f:
        f.write("=== COMPRA ===\n")
        for item in carrinho:
            total = item["preco"] * item["qtd"]
            f.write(f"{item['nome']} x{item['qtd']} = R$ {centavos_para_real(total)}\n")
        f.write(f"Total: R$ {centavos_para_real(totalCarrinho())}\n")
        f.write(f"Pago: R$ {centavos_para_real(valorPago)}\n")
        f.write(f"Troco: R$ {centavos_para_real(troco)}\n\n")


def adicionarcarrinho(nome, preco):
    for item in carrinho:
        if item["nome"] == nome:
            item["qtd"] += 1
            return
    carrinho.append({"nome": nome, "preco": preco, "qtd": 1})


def removerdocarrinho(indice):
    item = carrinho[indice]
    for produto in produtos:
        if produto["nome"] == item["nome"]:
            produto["estoque"] += 1
            break

    if item["qtd"] > 1:
        item["qtd"] -= 1
    else:
        carrinho.pop(indice)


def listaprodutos():
    print("\nMAQUINA DE VENDAS")
    print("===============================")
    for i, p in enumerate(produtos):
        print(f"{i+1}-{p['nome']} - R$ {centavos_para_real(p['preco'])} - estoque {p['estoque']}")


def estoqueNotas():
    print("\nEstoque notas")
    print("===============================")
    for t in trocos:
        print(f"{t['nome']} - estoque {t['estoque']}")


def reporEstoque():
    for i in range(len(produtos)):
        produtos[i]["estoque"] = estoqueInicialProdutos[i]

    for i in range(len(trocos)):
        trocos[i]["estoque"] = estoqueInicialTrocos[i]


def menuPrincipal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Comprar")
        print("2 - Modo administrador")
        print("3 - Sair")

        escolha = input("Escolha: ")

        if escolha == "1":
            menuCompra()

        elif escolha == "2":
            senha = input("Senha: ")
            if senha == "123":
                menuAdm()
            else:
                print("Senha incorreta")

        elif escolha == "3":
            exit()


def menuCompra():
    carrinho.clear()
    listaTroco.clear()

    while True:
        listaprodutos()
        print("\n1 - Selecionar produto")
        print("2 - Ver carrinho")
        print("3 - Finalizar compra")
        print("4 - Voltar")

        escolha = input("Escolha: ")

        if escolha == "1":
            selecionarProduto()

        elif escolha == "2":
            editarCarrinho()

        elif escolha == "3":
            pagamento()
            return

        elif escolha == "4":
            return


def selecionarProduto():
    try:
        compra = int(input("Digite o ID do produto: "))
    except:
        return

    if compra < 1 or compra > len(produtos):
        return

    produto = produtos[compra-1]

    if produto["estoque"] <= 0:
        print("PRODUTO EM FALTA")
        return

    produto["estoque"] -= 1
    adicionarcarrinho(produto["nome"], produto["preco"])


def editarCarrinho():
    while True:
        if not carrinho:
            print("Carrinho vazio")
            return

        mostrarCarrinho()
        escolha = input("Remover item (número) ou 0 para voltar: ")

        if escolha == "0":
            return

        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(carrinho):
                removerdocarrinho(indice)
        except:
            pass


def pagamento():
    global contadorCompras

    if not carrinho:
        return

    while True:
        try:
            valor = float(input("Valor inserido: "))
            valorPagamento = int(round(valor * 100))
        except:
            continue

        total = totalCarrinho()

        if valorPagamento < total:
            print("Saldo insuficiente")
            continue

        troco = valorPagamento - total
        resto = troco
        n = 0

        while resto > 0 and n < len(trocos):
            moeda = trocos[n]

            if resto >= moeda["valor"] and moeda["estoque"] > 0:
                resto -= moeda["valor"]
                moeda["estoque"] -= 1
                listaTroco.append(n)
            else:
                n += 1

        print("\n=== RECIBO ===")
        mostrarCarrinho()
        print(f"Pago: R$ {centavos_para_real(valorPagamento)}")
        print(f"Troco: R$ {centavos_para_real(troco)}")

        salvarLog(valorPagamento, troco)
        contagemTroco()

        contadorCompras += 1

        if contadorCompras % 4 == 0:
            reporEstoque()

        input("\nPressione ENTER para continuar...")
        return


def contagemTroco():
    valores = set(listaTroco)

    for n in valores:
        qtd = listaTroco.count(n)
        nome = trocos[n]["nome"]
        tipo = "nota" if n < 4 else "moeda"

        if qtd > 1:
            print(f"{qtd} {tipo}s de {nome}")
        else:
            print(f"{qtd} {tipo} de {nome}")

    estoqueNotas()


def menuAdm():
    while True:
        print("\n=== MODO ADMIN ===")
        print("1 - Cadastrar produto")
        print("2 - Editar produto")
        print("3 - Remover produto")
        print("4 - Voltar")

        adm = input("Escolha: ")

        if adm == "1":
            nome = input("Nome: ")
            preco = int(round(float(input("Valor: ")) * 100))
            estoque = int(input("Estoque: "))

            produtos.append({"nome": nome, "preco": preco, "estoque": estoque})
            estoqueInicialProdutos.append(estoque)

        elif adm == "2":
            try:
                editar = int(input("ID: ")) - 1
                preco = int(round(float(input("Novo valor: ")) * 100))
                estoque = int(input("Novo estoque: "))

                produtos[editar]["preco"] = preco
                produtos[editar]["estoque"] = estoque
                estoqueInicialProdutos[editar] = estoque
            except:
                pass

        elif adm == "3":
            try:
                remover = int(input("ID: ")) - 1
                produtos.pop(remover)
                estoqueInicialProdutos.pop(remover)
            except:
                pass

        elif adm == "4":
            return


menuPrincipal()

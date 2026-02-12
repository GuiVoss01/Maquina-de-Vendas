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
    print("MAQUINA DE VENDAS")
    print("===============================")
    for i, p in enumerate(produtos):
        print(f"{i+1}-{p['nome']} - R$ {centavos_para_real(p['preco'])} - estoque {p['estoque']}")

def estoqueNotas():
    print("Estoque notas")
    print("===============================")
    for t in trocos:
        print(f"{t['nome']} - estoque {t['estoque']}")

def selecionarmodo():
    while True:
        escolha = int(input("digite a senha para modo adm ou 1 para comprar: "))
        if escolha == 123:
            modoAdm()
            break
        elif escolha == 1:
            listaprodutos()
            selecionarprodutos()
            break
        else:
            print("Senha incorreta")

def selecionarprodutos():
    while True:
        try:
            compra = int(input("Digite o ID do produto ou 0 para finalizar sua compra: "))
        except ValueError:
            print("Valor inválido")
            continue

        if compra == 0:
            pagamento()
            break

        if compra < 1 or compra > len(produtos):
            print("ID não identificado")
            continue

        produto = produtos[compra-1]

        if produto["estoque"] <= 0:
            print("PRODUTO EM FALTA")
            continue

        produto["estoque"] -= 1
        adicionarcarrinho(produto["nome"], produto["preco"])
        listaprodutos()
        mostrarCarrinho()

def editarCarrinho():
    while True:
        if not carrinho:
            return
        mostrarCarrinho()
        escolha = input("Digite o número do item para remover ou 0 para continuar: ")
        if escolha == '0':
            return
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(carrinho):
                removerdocarrinho(indice)
        except:
            pass

def reporEstoque():
    for i in range(len(produtos)):
        produtos[i]["estoque"] = estoqueInicialProdutos[i]
    for i in range(len(trocos)):
        trocos[i]["estoque"] = estoqueInicialTrocos[i]

def pagamento():
    global contadorCompras
    if not carrinho:
        selecionarprodutos()
        return

    editarCarrinho()

    while True:
        try:
            valor = float(input("Valor inserido: "))
            valorPagamento = int(round(valor * 100))
        except ValueError:
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

        while True:
            opcao = input("\n1 - Fazer nova compra\n2 - Encerrar programa\nEscolha: ")
            if opcao == '1':
                carrinho.clear()
                listaTroco.clear()
                listaprodutos()
                selecionarprodutos()
                return
            elif opcao == '2':
                exit()

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
    listaprodutos()
    estoqueNotas()

def modoAdm():
    while True:
        adm = input("deseja cadastrar, editar, remover um produto ou sair do modo? ").lower()

        if adm == 'cadastrar':
            nome = input("nome do produto: ")
            preco = int(round(float(input("valor: ")) * 100))
            estoque = int(input("estoque: "))
            produtos.append({"nome": nome, "preco": preco, "estoque": estoque})
            estoqueInicialProdutos.append(estoque)
            listaprodutos()

        if adm == "editar":
            editar = int(input("ID do produto: ")) - 1
            preco = int(round(float(input("novo valor: ")) * 100))
            estoque = int(input("novo estoque: "))
            produtos[editar]["preco"] = preco
            produtos[editar]["estoque"] = estoque
            estoqueInicialProdutos[editar] = estoque
            listaprodutos()

        if adm == 'remover':
            remover = int(input("ID do produto: ")) - 1
            produtos.pop(remover)
            estoqueInicialProdutos.pop(remover)
            listaprodutos()

        if adm == 'sair':
            listaprodutos()
            selecionarprodutos()
            break

selecionarmodo()

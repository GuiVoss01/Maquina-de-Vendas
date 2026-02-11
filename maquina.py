produtos = [
    ["Coca-cola", 3.75, 2],
    ["Pepsi", 3.67, 5],
    ["Monster", 9.96, 1],
    ["Cafe", 1.25, 100],
    ["Redbull", 13.99, 2]
]

trocos = [
    ["20 R$", 20, 10],
    ["10 R$", 10, 10],
    ["5 R$", 5, 10],
    ["2 R$", 2, 10],
    ["1 R$", 1, 10],
    ["50 centavos", 0.5, 10],
    ["10 centavos", 0.1, 10],
    ["1 centavo", 0.01, 100]
]

estoqueInicialProdutos = [p[2] for p in produtos]
estoqueInicialTrocos = [t[2] for t in trocos]

listaNomeProdutos = []
listaPrecoProdutos = []
listaTroco = []
contadorCompras = 0

def selecionarmodo():
    '''Comeco do codigo, o user recebe a possibilidade de exec o modo adm ou comprar'''
    while True:
        escolha = int(input("digite a senha para modo adm ou 1 para comprar: "))
        if escolha == 123:
            modoAdm()
            break
        elif escolha == 1:
            listaprodutos()
            selecionarprodutos()
            break
        elif escolha != 1 or escolha != 123:
            print("Senha incorreta")
            continue

def listaprodutos():
    '''Mostra a matriz produtos organizada'''
    print("MAQUINA DE VENDAS")
    print("===============================")
    for i, produto in enumerate(produtos):
        nome = produto[0]
        preco = produto[1]
        estoque = produto[2]
        print(f'{i + 1}-{produto[0]} - R$ {produto[1]} - estoque {estoque}')

def estoqueNotas():
    '''Estoque de notas'''
    print("Estoque notas")
    print("===============================")
    for i, materia in enumerate(trocos):
        nome = materia[0]
        preco = materia[1]
        estoque = materia[2]
        print(f'{materia[0]} - estoque {estoque}')

def selecionarprodutos():
    '''User pode escolher o que vai ser comprado e mostra possiveis erros como falta de estoque'''
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

        compraIndex = produtos[compra - 1]
        print(f"Você selecionou {compraIndex[0]}")

        if compraIndex[2] <= 0:
            print("PRODUTO EM FALTA")
            continue

        compraIndex[2] = compraIndex[2] - 1
        listaprodutos()
        listaNomeProdutos.append(compraIndex[0])
        listaPrecoProdutos.append(compraIndex[1])
        print(f"Produtos selecionados: {listaNomeProdutos}")
        print(f'Valor total: {sum(listaPrecoProdutos)}')

def reporEstoque():
    for i in range(len(produtos)):
        produtos[i][2] = estoqueInicialProdutos[i]
    for i in range(len(trocos)):
        trocos[i][2] = estoqueInicialTrocos[i]

def pagamento():
    '''Função traz o algoritmo do troco'''
    global contadorCompras
    n = 0
    while True:
        try:
            valorPagamento = float(input("Valor inserido: "))
        except ValueError:
            print("Valor invalido")
            continue

        total = sum(listaPrecoProdutos)
        troco = valorPagamento - total
        troco = round(troco, 2)

        if valorPagamento < total:
            print("Saldo insuficiente")
            continue

        if troco == 0:
            print("Sem troco")
        else:
            while troco != 0:
                troco = round(troco, 2)
                if n >= len(trocos):
                    break
                if trocos[n][2] < 0:
                    exit()
                if troco < trocos[n][1]:
                    n += 1
                else:
                    troco = troco - trocos[n][1]
                    trocos[n][2] = trocos[n][2] - 1
                    listaTroco.append(n)

        print("\n=== RECIBO ===")
        for i in range(len(listaNomeProdutos)):
            print(f"{listaNomeProdutos[i]} - R$ {listaPrecoProdutos[i]}")
        print(f"Total: R$ {round(total, 2)}")
        print(f"Pago: R$ {round(valorPagamento, 2)}")
        print(f"Troco: R$ {round(valorPagamento - total, 2)}")

        contagemTroco()

        contadorCompras += 1
        if contadorCompras % 4 == 0:
            reporEstoque()

        while True:
            opcao = input("\n1 - Fazer nova compra\n2 - Encerrar programa\nEscolha: ")
            if opcao == '1':
                listaNomeProdutos.clear()
                listaPrecoProdutos.clear()
                listaTroco.clear()
                listaprodutos()
                selecionarprodutos()
                return
            elif opcao == '2':
                exit()
            else:
                print("Opção inválida")

def contagemTroco():
    '''Basicamente mostra se o print vai ser no plural ou não e mostra a quantidade notas/moedas'''
    valores_contados = []
    for n in listaTroco:
        if n not in valores_contados:
            quantidade = listaTroco.count(n)
            valores_contados.append(n)
            if quantidade > 1:
                if n < 4:
                    print(f'{quantidade} notas de {trocos[n][0]}')
                else:
                    print(f'{quantidade} moedas de {trocos[n][0]}')
            else:
                if n < 4:
                    print(f'{quantidade} nota de {trocos[n][0]}')
                else:
                    print(f'{quantidade} moeda de {trocos[n][0]}')
    listaprodutos()
    estoqueNotas()

def modoAdm():
    '''Modo adm'''
    while True:
        adm = (input("deseja cadastrar, editar, remover um produto ou sair do modo? ").lower())
        if adm == 'cadastrar':
            nomecadastrado = input("qual o nome do produto você quer cadastrar? ")
            produtoCadastrado = []
            produtoCadastrado.append(nomecadastrado)
            precocadastrado = float(input("qual o valor do produto cadastrado? "))
            produtoCadastrado.append(precocadastrado)
            estoquecadastrado = int(input("qual o estoque do produto cadastrado? "))
            produtoCadastrado.append(estoquecadastrado)
            produtos.append(produtoCadastrado)
            estoqueInicialProdutos.append(estoquecadastrado)
            listaprodutos()

        if adm == "editar":
            listaEditar = []
            editar = int(input("qual o ID do produto que você quer editar? "))
            produtoEditadoIndex = editar - 1
            print(f"Você selecionou {produtos[produtoEditadoIndex]}")
            valoreditado = float(input("Digite o valor novo: "))
            estoqueeditado = int(input("Digite o estoque novo: "))
            listaEditar.append(valoreditado)
            listaEditar.append(estoqueeditado)
            produtos[produtoEditadoIndex][1:3] = listaEditar
            estoqueInicialProdutos[produtoEditadoIndex] = estoqueeditado
            listaprodutos()

        if adm == 'remover':
            remover = int(input("qual o id do produto que você quer remover? "))
            produtoremovidoIndex = remover - 1
            produtos.pop(produtoremovidoIndex)
            estoqueInicialProdutos.pop(produtoremovidoIndex)
            listaprodutos()

        if adm == 'sair':
            listaprodutos()
            selecionarprodutos()
            break

selecionarmodo()

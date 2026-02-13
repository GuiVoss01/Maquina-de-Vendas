class MaquinaVendas:

    def __init__(self):
        self.produtos = [
            {"nome": "Coca-cola", "preco": 375, "estoque": 2},
            {"nome": "Pepsi", "preco": 367, "estoque": 5},
            {"nome": "Monster", "preco": 996, "estoque": 1},
            {"nome": "Cafe", "preco": 125, "estoque": 100},
            {"nome": "Redbull", "preco": 1399, "estoque": 2}
        ]

        self.trocos = [
            {"nome": "20 R$", "valor": 2000, "estoque": 10},
            {"nome": "10 R$", "valor": 1000, "estoque": 10},
            {"nome": "5 R$", "valor": 500, "estoque": 10},
            {"nome": "2 R$", "valor": 200, "estoque": 10},
            {"nome": "1 R$", "valor": 100, "estoque": 10},
            {"nome": "50 centavos", "valor": 50, "estoque": 10},
            {"nome": "10 centavos", "valor": 10, "estoque": 10},
            {"nome": "1 centavo", "valor": 1, "estoque": 100}
        ]

        self.estoqueInicialProdutos = [p["estoque"] for p in self.produtos]
        self.estoqueInicialTrocos = [t["estoque"] for t in self.trocos]

        self.carrinho = []
        self.listaTroco = []
        self.contadorCompras = 0

    def centavos_para_real(self, valor):
        return f"{valor/100:.2f}"

    def totalCarrinho(self):
        return sum(item["preco"] * item["qtd"] for item in self.carrinho)

    def mostrarCarrinho(self):
        print("\n=== CARRINHO ===")
        for i, item in enumerate(self.carrinho, start=1):
            total = item["preco"] * item["qtd"]
            print(f"{i} - {item['nome']} x{item['qtd']} = R$ {self.centavos_para_real(total)}")
        print(f"Total: R$ {self.centavos_para_real(self.totalCarrinho())}")

    def salvarLog(self, valorPago, troco):
        with open("historico.txt", "a", encoding="utf-8") as f:
            f.write("=== COMPRA ===\n")
            for item in self.carrinho:
                total = item["preco"] * item["qtd"]
                f.write(f"{item['nome']} x{item['qtd']} = R$ {self.centavos_para_real(total)}\n")
            f.write(f"Total: R$ {self.centavos_para_real(self.totalCarrinho())}\n")
            f.write(f"Pago: R$ {self.centavos_para_real(valorPago)}\n")
            f.write(f"Troco: R$ {self.centavos_para_real(troco)}\n\n")

    def adicionarcarrinho(self, nome, preco):
        for item in self.carrinho:
            if item["nome"] == nome:
                item["qtd"] += 1
                return
        self.carrinho.append({"nome": nome, "preco": preco, "qtd": 1})

    def removerdocarrinho(self, indice):
        item = self.carrinho[indice]
        for produto in self.produtos:
            if produto["nome"] == item["nome"]:
                produto["estoque"] += 1
                break

        if item["qtd"] > 1:
            item["qtd"] -= 1
        else:
            self.carrinho.pop(indice)

    def listaprodutos(self):
        print("\nMAQUINA DE VENDAS")
        print("===============================")
        for i, p in enumerate(self.produtos):
            print(f"{i+1}-{p['nome']} - R$ {self.centavos_para_real(p['preco'])} - estoque {p['estoque']}")

    def estoqueNotas(self):
        print("\nEstoque notas")
        print("===============================")
        for t in self.trocos:
            print(f"{t['nome']} - estoque {t['estoque']}")

    def reporEstoque(self):
        for i in range(len(self.produtos)):
            self.produtos[i]["estoque"] = self.estoqueInicialProdutos[i]

        for i in range(len(self.trocos)):
            self.trocos[i]["estoque"] = self.estoqueInicialTrocos[i]

    def menuPrincipal(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1 - Comprar")
            print("2 - Modo administrador")
            print("3 - Sair")

            escolha = input("Escolha: ")

            if escolha == "1":
                self.menuCompra()

            elif escolha == "2":
                senha = input("Senha: ")
                if senha == "123":
                    self.menuAdm()
                else:
                    print("Senha incorreta")

            elif escolha == "3":
                exit()

    def menuCompra(self):
        self.carrinho.clear()
        self.listaTroco.clear()

        while True:
            self.listaprodutos()
            print("\n1 - Selecionar produto")
            print("2 - Ver carrinho")
            print("3 - Finalizar compra")
            print("4 - Voltar")

            escolha = input("Escolha: ")

            if escolha == "1":
                self.selecionarProduto()

            elif escolha == "2":
                self.editarCarrinho()

            elif escolha == "3":
                self.pagamento()
                return

            elif escolha == "4":
                return

    def selecionarProduto(self):
        try:
            compra = int(input("Digite o ID do produto: "))
        except:
            return

        if compra < 1 or compra > len(self.produtos):
            return

        produto = self.produtos[compra-1]

        if produto["estoque"] <= 0:
            print("PRODUTO EM FALTA")
            return

        produto["estoque"] -= 1
        self.adicionarcarrinho(produto["nome"], produto["preco"])

    def editarCarrinho(self):
        while True:
            if not self.carrinho:
                print("Carrinho vazio")
                return

            self.mostrarCarrinho()
            escolha = input("Remover item (número) ou 0 para voltar: ")

            if escolha == "0":
                return

            try:
                indice = int(escolha) - 1
                if 0 <= indice < len(self.carrinho):
                    self.removerdocarrinho(indice)
            except:
                pass

    def pagamento(self):
        if not self.carrinho:
            return

        while True:
            try:
                valor = float(input("Valor inserido: "))
                valorPagamento = int(round(valor * 100))
            except:
                continue

            total = self.totalCarrinho()

            if valorPagamento < total:
                print("Saldo insuficiente")
                continue

            troco = valorPagamento - total
            resto = troco
            n = 0

            while resto > 0 and n < len(self.trocos):
                moeda = self.trocos[n]

                if resto >= moeda["valor"] and moeda["estoque"] > 0:
                    resto -= moeda["valor"]
                    moeda["estoque"] -= 1
                    self.listaTroco.append(n)
                else:
                    n += 1

            print("\n=== RECIBO ===")
            self.mostrarCarrinho()
            print(f"Pago: R$ {self.centavos_para_real(valorPagamento)}")
            print(f"Troco: R$ {self.centavos_para_real(troco)}")

            self.salvarLog(valorPagamento, troco)
            self.contagemTroco()

            self.contadorCompras += 1

            if self.contadorCompras % 4 == 0:
                self.reporEstoque()

            input("\nPressione ENTER para continuar...")
            return

    def contagemTroco(self):
        valores = set(self.listaTroco)

        for n in valores:
            qtd = self.listaTroco.count(n)
            nome = self.trocos[n]["nome"]
            tipo = "nota" if n < 4 else "moeda"

            if qtd > 1:
                print(f"{qtd} {tipo}s de {nome}")
            else:
                print(f"{qtd} {tipo} de {nome}")

        self.estoqueNotas()

    def menuAdm(self):
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

                self.produtos.append({"nome": nome, "preco": preco, "estoque": estoque})
                self.estoqueInicialProdutos.append(estoque)

            elif adm == "2":
                try:
                    editar = int(input("ID: ")) - 1
                    preco = int(round(float(input("Novo valor: ")) * 100))
                    estoque = int(input("Novo estoque: "))

                    self.produtos[editar]["preco"] = preco
                    self.produtos[editar]["estoque"] = estoque
                    self.estoqueInicialProdutos[editar] = estoque
                except:
                    pass

            elif adm == "3":
                try:
                    remover = int(input("ID: ")) - 1
                    self.produtos.pop(remover)
                    self.estoqueInicialProdutos.pop(remover)
                except:
                    pass

            elif adm == "4":
                return


maquina = MaquinaVendas()
maquina.menuPrincipal()

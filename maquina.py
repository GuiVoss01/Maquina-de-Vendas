from datetime import datetime


class MaquinaVendas:

    def __init__(self):
        self.produtos = [
            {"nome": "Coca-cola", "preco": 375, "estoque": 2},
            {"nome": "Pepsi", "preco": 367, "estoque": 5},
            {"nome": "Monster", "preco": 996, "estoque": 1},
            {"nome": "Cafe", "preco": 125, "estoque": 100},
            {"nome": "Redbull", "preco": 1399, "estoque": 2}
        ]

        self.produtos_index = {p["nome"]: p for p in self.produtos}

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

    def reais(self, v): return f"{v/100:.2f}"

    def total(self): return sum(i["preco"] * i["qtd"] for i in self.carrinho)

    def mostrarCarrinho(self):
        print("\n=== CARRINHO ===")
        for i, item in enumerate(self.carrinho, 1):
            print(f"{i} - {item['nome']} x{item['qtd']} = R$ {self.reais(item['preco']*item['qtd'])}")
        print(f"Total: R$ {self.reais(self.total())}")

    def salvarLog(self, pago, troco):
        with open("historico.txt", "a", encoding="utf-8") as f:
            f.write(f"\n=== COMPRA ===\nData: {datetime.now()}\n")
            for i in self.carrinho:
                f.write(f"{i['nome']} x{i['qtd']}\n")
            f.write(f"Total: {self.reais(self.total())}\nPago: {self.reais(pago)}\nTroco: {self.reais(troco)}\n")

    def addCarrinho(self, nome, preco):
        for i in self.carrinho:
            if i["nome"] == nome:
                i["qtd"] += 1
                return
        self.carrinho.append({"nome": nome, "preco": preco, "qtd": 1})

    def removerCarrinho(self, i):
        item = self.carrinho[i]
        self.produtos_index[item["nome"]]["estoque"] += 1  

        if item["qtd"] > 1:
            item["qtd"] -= 1
        else:
            self.carrinho.pop(i)

    def listar(self):
        print("\nMAQUINA DE VENDAS\n=================")
        for i, p in enumerate(self.produtos, 1):
            print(f"{i}-{p['nome']} - R$ {self.reais(p['preco'])} - estoque {p['estoque']}")

    def calcularTroco(self, troco):
        resto, usados = troco, []
        for i, m in enumerate(self.trocos):
            while resto >= m["valor"] and m["estoque"] > 0:
                resto -= m["valor"]
                m["estoque"] -= 1
                usados.append(i)

        if resto:
            for i in usados: self.trocos[i]["estoque"] += 1
            return None
        return usados

    def pagamento(self):
        if not self.carrinho: return

        try:
            pago = int(float(input("Valor: ")) * 100)
        except:
            return

        total = self.total()
        if pago < total:
            print("Saldo insuficiente")
            return

        troco = pago - total
        usados = self.calcularTroco(troco)

        if usados is None:
            print("Sem troco")
            for i in self.carrinho:
                self.produtos_index[i["nome"]]["estoque"] += i["qtd"]
            return

        print("\n=== RECIBO ===")
        self.mostrarCarrinho()
        print(f"Pago: {self.reais(pago)} | Troco: {self.reais(troco)}")

        self.salvarLog(pago, troco)
        self.contadorCompras += 1
        self.carrinho.clear()

    def selecionar(self):
        try:
            i = int(input("ID: ")) - 1
            p = self.produtos[i]
            if p["estoque"] <= 0:
                print("Sem estoque")
                return
            p["estoque"] -= 1
            self.addCarrinho(p["nome"], p["preco"])
        except:
            pass

    def menuCompra(self):
        self.carrinho.clear()
        while True:
            self.listar()
            op = input("1-Add 2-Carrinho 3-Pagar 4-Voltar: ")

            if op == "1": self.selecionar()
            elif op == "2": self.mostrarCarrinho()
            elif op == "3": return self.pagamento()
            elif op == "4": return

    def menuAdm(self):
        while True:
            op = input("\n1-Add 2-Editar 3-Remover 4-Voltar: ")

            if op == "1":
                nome = input("Nome: ")
                preco = int(float(input("Preço: ")) * 100)
                estoque = int(input("Estoque: "))

                p = {"nome": nome, "preco": preco, "estoque": estoque}
                self.produtos.append(p)
                self.produtos_index[nome] = p  

            elif op == "2":
                try:
                    i = int(input("ID: ")) - 1
                    self.produtos[i]["preco"] = int(float(input("Preço: ")) * 100)
                    self.produtos[i]["estoque"] = int(input("Estoque: "))
                except:
                    pass

            elif op == "3":
                try:
                    i = int(input("ID: ")) - 1
                    p = self.produtos.pop(i)
                    self.produtos_index.pop(p["nome"])  
                except:
                    pass

            elif op == "4":
                return

    def menu(self):
        while True:
            op = input("\n1-Comprar 2-Admin 3-Sair: ")
            if op == "1": self.menuCompra()
            elif op == "2":
                if input("Senha: ") == "123":
                    self.menuAdm()
            elif op == "3":
                break


MaquinaVendas().menu()
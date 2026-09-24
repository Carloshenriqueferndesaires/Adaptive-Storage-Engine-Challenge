import json
import random

quantidade = int(input("Quantidade de operações:"))

operacoes = ["put", "get", "delete", "scan"]

with open("workload.jsonl", "w", encoding="utf-8") as arquivo:

    for i in range(1, quantidade + 1):

        tipo = random.choice(operacoes)

        if tipo == "put":
            operacao = {
                "id": i,
                "op": "put",
                "key": i,
                "value": f"valor-{i}"
            }

        elif tipo == "get":
            operacao = {
                "id": i,
                "op": "get",
                "key": i
            }

        elif tipo == "delete":
            operacao = {
                "id": i,
                "op": "delete",
                "key": i
            }

        elif tipo == "scan":
            inicio = max(1, i - 10)

            operacao = {
                "id": i,
                "op": "scan",
                "start": inicio,
                "end": i
            }

        arquivo.write(json.dumps(operacao) + "\n")

print(f"{quantidade} operações geradas.")
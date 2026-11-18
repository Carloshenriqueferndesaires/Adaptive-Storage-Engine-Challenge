import json

quantidade = int(input("Quantidade de operações: "))

with open("workload.jsonl", "w", encoding="utf-8") as arquivo:

    id_operacao = 1

    for i in range(1, quantidade + 1):

        tipo = (i - 1) % 3

        if tipo == 0:
            operacao = {
                "id": id_operacao,
                "op": "put",
                "key": i,
                "value": f"valor-{i}"
            }

        elif tipo == 1:
            operacao = {
                "id": id_operacao,
                "op": "get",
                "key": i
            }

        else :
            operacao = {
                "id": id_operacao,
                "op": "delete",
                "key": i
            }

        
        arquivo.write(json.dumps(operacao) + "\n")

        id_operacao += 1

print(f"{quantidade} operações geradas.")
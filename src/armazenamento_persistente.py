import struct

ARQUIVO = "dados.dat"

def put(chave, valor):

    valor_bytes = valor.encode("utf-8")

    with open(ARQUIVO, "ab") as arquivo:

        cabecalho = struct.pack(
            "<QI",
            chave,
            len(valor_bytes)
        )

        arquivo.write(cabecalho)
        arquivo.write(valor_bytes)


def get(chave):

    with open(ARQUIVO, "rb") as arquivo:

        while True:

            cabecalho = arquivo.read(12)

            if not cabecalho:
                break

            chave_lida, tamanho = struct.unpack(
                "<QI",
                cabecalho
            )

            valor_bytes = arquivo.read(tamanho)

            if chave_lida == chave:
                return valor_bytes.decode("utf-8")

    return None


def delete(chave):

    registros = []

    with open(ARQUIVO, "rb") as arquivo:

        while True:

            cabecalho = arquivo.read(12)

            if not cabecalho:
                break

            chave_lida, tamanho = struct.unpack(
                "<QI",
                cabecalho
            )

            valor_bytes = arquivo.read(tamanho)

            if chave_lida != chave:
                registros.append(
                    (chave_lida, valor_bytes)
                )

    with open(ARQUIVO, "wb") as arquivo:

        for chave_lida, valor_bytes in registros:

            cabecalho = struct.pack(
                "<QI",
                chave_lida,
                len(valor_bytes)
            )

            arquivo.write(cabecalho)
            arquivo.write(valor_bytes)



put(1, "valor-1")
put(2, "valor-2")
put(3, "valor-3")

print(get(1))

delete(2)

print(get(2))



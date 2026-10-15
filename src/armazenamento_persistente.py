import struct
import logging
from typing import Iterator
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ARQUIVO = Path("dados.dat")
ARQUIVO.touch(exist_ok=True)

def put(chave: int, valor: str) -> None:
    """Registra um valor para a chave dada.
    
    Caso a chave já exista, o valor será atualizado.
    Args:
        chave (int): A chave para o registro.
        valor (str): O valor a ser registrado.
    """

    valor_bytes = valor.encode("utf-8")
    registros = []
    encontrado = False

    for chave_lida, valor_bytes_lidos in _ler_registros():
        if chave_lida == chave:
            registros.append((chave_lida, valor_bytes))
            encontrado = True
        else:
            registros.append((chave_lida, valor_bytes_lidos))


    if not encontrado:
        registros.append((chave, valor_bytes))

    _reescrever_registros(registros)


def get(chave: int) -> str | None:
    """Pega o valor registrado para a chave dada.
    
    Args:
        chave (int): A chave para o registro.
    """

    for chave_lida, valor_bytes in _ler_registros():
        if chave_lida == chave:
            valor = valor_bytes.decode("utf-8")
            logger.info(f"|{chave}|{valor}| encontrado")
            return valor

    logger.info(f"|{chave}| não encontrada")
    return None


def delete(chave: int) -> None:
    """Deleta o valor registrado para a chave dada.
    
    Args:
        chave (int): A chave para o registro.
    """

    registros = []
    encontrado = False

    for chave_lida, valor_bytes in _ler_registros():
        if chave_lida == chave:
            encontrado = True
            continue

        registros.append((chave_lida, valor_bytes))

    _reescrever_registros(registros)

    if encontrado:
        logger.info(f"Registro |{chave}| deletado")
    else:
        logger.info(f"Registro |{chave}| não encontrado")


def _ler_registros() -> Iterator[tuple[int, bytes]]:
    """Lê os registros do arquivo."""
    
    with open(ARQUIVO, "r+b") as arquivo:
        while True:
            posicao = arquivo.tell()
            cabecalho = arquivo.read(12)

            if not cabecalho:
                break

            if len(cabecalho) != 12:
                logger.warning("Cabeçalho está incompleto!")
                arquivo.truncate(posicao)
                break

            chave_lida, tamanho = struct.unpack(
                "<QI",
                cabecalho
            )

            valor_bytes = arquivo.read(tamanho)

            if not _valida_e_recupera_registro(
                arquivo,
                valor_bytes,
                tamanho,
                posicao
            ):
                break

            yield chave_lida, valor_bytes

def _valida_e_recupera_registro(
        arquivo,
        valor_bytes: bytes, 
        tamanho: int, 
        posicao: int
    ) -> bool:
    """Valida o registros e descarta registros incompletos."""

    if len(valor_bytes) != tamanho:
        arquivo.truncate(posicao)
        logger.warning("Registo incompleto. Registro descartado...")
        return False
    return True

def _reescrever_registros(registros: list[tuple[int, bytes]]) -> None:
    """Reescreve os registros no arquivo."""

    with open(ARQUIVO, "wb") as arquivo:
        for chave_lida, valor_bytes in registros:
            cabecalho = struct.pack(
                "<QI",
                chave_lida,
                len(valor_bytes)
            )

            arquivo.write(cabecalho)
            arquivo.write(valor_bytes)


def _limpar_arquivo() -> None:
    """Limpa o arquivo de dados."""
    
    ARQUIVO.unlink(missing_ok=True)
    ARQUIVO.touch(exist_ok=True)

# Testes

_limpar_arquivo()

put(1, "valor-1")
put(2, "valor-2")
put(3, "valor-3")

get(1)
print(get(1))

delete(1)

print(get(1))
# print(get(3))



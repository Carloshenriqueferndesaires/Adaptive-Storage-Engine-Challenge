import argparse

def carregar_argumentos():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    
    return parser.parse_args()
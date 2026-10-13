#!/usr/bin/env python3
"""Assistente de terminal: manda uma pergunta a um serviço compatível com OpenAI."""
import argparse
import json
import os
import urllib.request

BASE_URL = os.environ.get("ASSISTENTE_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("ASSISTENTE_MODEL", "gpt-4o-mini")
# A chave nunca fica no código: vem do ambiente (ASSISTENTE_API_KEY).


def chave() -> str:
    """A chave da API vem do ambiente, nunca do código."""
    return os.environ.get("ASSISTENTE_API_KEY", "")


def perguntar(pergunta: str) -> str:
    if not chave():
        raise SystemExit("defina ASSISTENTE_API_KEY no ambiente")
    corpo = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": pergunta}]}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=corpo,
        headers={"Authorization": "Bearer " + chave(), "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)["choices"][0]["message"]["content"]


def main() -> None:
    """Lê a pergunta dos argumentos, consulta o modelo e imprime a resposta; não devolve valor."""
    parser = argparse.ArgumentParser(description="Pergunta ao modelo e mostra a resposta como texto.")
    parser.add_argument("pergunta", nargs="*", help="a pergunta (padrão: uma apresentação)")
    args = parser.parse_args()
    pergunta = " ".join(args.pergunta) or "Olá! O que você sabe fazer?"
    # A resposta do modelo é texto para a pessoa ler; nunca é executada.
    print(perguntar(pergunta))


if __name__ == "__main__":
    main()

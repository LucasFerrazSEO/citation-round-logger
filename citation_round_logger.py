#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
citation-round-logger — CLI para registrar "rodadas de citação": rodar o
mesmo prompt em várias IAs (ChatGPT, Claude, Gemini, Perplexity...), anotar
se cada marca do seu conjunto de comparação apareceu na resposta e em que
posição, e depois calcular o share of voice por marca e por IA.

O QUE FAZ
    `log`    — adiciona um registro de rodada (IA, prompt, data, marcas
               mencionadas e posição de cada uma) a um arquivo JSON local.
    `report` — lê o arquivo e calcula, por marca e por IA, quantas rodadas
               ela apareceu e a posição média, ou seja, o share of voice.

    Isto NÃO consulta IA nenhuma automaticamente — você roda o prompt à mão
    (ou por outra ferramenta/API) em cada assistente, lê a resposta, e
    registra aqui o que observou. É o formato estruturado do método, não um
    scraper.

USO
    python citation_round_logger.py log --ia chatgpt --prompt "melhor agencia de seo em bh" \\
        --marca "Minha Empresa" --posicao 2 --marca "Concorrente X" --posicao 1

    python citation_round_logger.py log --ia perplexity --prompt "melhor agencia de seo em bh" \\
        --marca "Minha Empresa" --ausente

    python citation_round_logger.py report
    python citation_round_logger.py report --ia chatgpt
    python citation_round_logger.py report --arquivo minhas-rodadas.json

LIMITAÇÕES
    Registro manual: a qualidade do dado depende de quem roda o prompt e lê
    a resposta com cuidado. Não normaliza variação de grafia de marca entre
    rodadas — use sempre o mesmo texto exato para a mesma marca.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença: MIT.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

ARQUIVO_PADRAO = "rodadas.json"


def carrega(caminho: str) -> list[dict]:
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def salva(caminho: str, rodadas: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(rodadas, fh, ensure_ascii=False, indent=2)


def cmd_log(args: argparse.Namespace) -> None:
    rodadas = carrega(args.arquivo)

    marcas: list[dict] = []
    if args.ausente:
        for nome in args.marca:
            marcas.append({"marca": nome, "mencionada": False, "posicao": None})
    else:
        if len(args.marca) != len(args.posicao):
            print("Cada --marca precisa de um --posicao correspondente, na mesma ordem "
                  "(ou use --ausente se nenhuma marca apareceu).", file=sys.stderr)
            sys.exit(2)
        for nome, pos in zip(args.marca, args.posicao):
            marcas.append({"marca": nome, "mencionada": True, "posicao": pos})

    registro = {
        "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ia": args.ia,
        "prompt": args.prompt,
        "marcas": marcas,
    }
    rodadas.append(registro)
    salva(args.arquivo, rodadas)
    print(f"Rodada registrada: {args.ia} | \"{args.prompt}\" | {len(marcas)} marca(s) | {args.arquivo}")


def cmd_report(args: argparse.Namespace) -> None:
    rodadas = carrega(args.arquivo)
    if args.ia:
        rodadas = [r for r in rodadas if r["ia"].lower() == args.ia.lower()]

    if not rodadas:
        print(f"Nenhuma rodada encontrada em {args.arquivo}" + (f" para a IA {args.ia}" if args.ia else ""))
        return

    por_marca_ia: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rodadas:
        for m in r["marcas"]:
            por_marca_ia[(m["marca"], r["ia"])].append(m)

    print(f"\n=== citation-round-logger: report ({len(rodadas)} rodada(s)) ===\n")
    marcas = sorted({m for m, _ in por_marca_ia})
    ias = sorted({i for _, i in por_marca_ia})

    for marca in marcas:
        print(f"-- {marca} --")
        for ia in ias:
            registros = por_marca_ia.get((marca, ia), [])
            if not registros:
                continue
            total = len(registros)
            mencoes = [r for r in registros if r["mencionada"]]
            share = len(mencoes) / total * 100
            posicoes = [r["posicao"] for r in mencoes if r["posicao"] is not None]
            pos_media = sum(posicoes) / len(posicoes) if posicoes else None
            linha = f"  {ia:<14} {len(mencoes)}/{total} rodada(s) ({share:.0f}% share of voice)"
            if pos_media is not None:
                linha += f" | posição média {pos_media:.1f}"
            print(linha)
        print()


def main() -> None:
    ap = argparse.ArgumentParser(description="Registra e resume rodadas de citação por IA.")
    ap.add_argument("--arquivo", default=ARQUIVO_PADRAO, help=f"arquivo JSON de rodadas (padrão {ARQUIVO_PADRAO})")
    sub = ap.add_subparsers(dest="comando", required=True)

    p_log = sub.add_parser("log", help="registra uma rodada")
    p_log.add_argument("--ia", required=True, help="nome da IA testada (ex.: chatgpt, claude, gemini, perplexity)")
    p_log.add_argument("--prompt", required=True, help="o prompt exato usado")
    p_log.add_argument("--marca", action="append", required=True, help="nome de uma marca do conjunto de comparação (repita por marca)")
    p_log.add_argument("--posicao", action="append", type=int, help="posição em que a marca apareceu na resposta (repita na mesma ordem de --marca)")
    p_log.add_argument("--ausente", action="store_true", help="nenhuma marca listada apareceu na resposta")
    p_log.set_defaults(func=cmd_log)

    p_report = sub.add_parser("report", help="resume as rodadas registradas")
    p_report.add_argument("--ia", default="", help="filtra por uma IA")
    p_report.set_defaults(func=cmd_report)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CLI determinístico de Engenharia Econômica. Toda saída é JSON (UTF-8) no stdout.

Exemplos:
    python econ_cli.py vpl --taxa 0.18 --fluxos -1000 300 400 500 600
    python econ_cli.py tir --fluxos -1000 300 400 500 600
    python econ_cli.py payback --fluxos -1000 300 400 500 600 --taxa 0.10
    python econ_cli.py equivalencia --vp 1000 --taxa 0.1 --n 5
    python econ_cli.py gva --planejado 400 --agregado 300 --real 450 --bac 1000
    python econ_cli.py markup --custo 700 --impostos 0.1 --margem 0.2
    python econ_cli.py saas --arpa 200 --margem 0.8 --churn 0.04 --cac 800
    python econ_cli.py priorizar --arquivo backlog.json --metodo wsjf
    python econ_cli.py comparar --taxa 0.18 --arquivo alternativas.json
    python econ_cli.py suficiente --arquivo niveis.json
    python econ_cli.py modelo --arquivo entrada.json            # VPL/TIR/payback do modelo de negócio
    python econ_cli.py cocomo --kloc 28.5
    python econ_cli.py equilibrio --taxa 0.14 --fluxos -120000 18000 45000 60000 70000
    python econ_cli.py estresse --taxa 0.14 --fator-investimento 1.25 --fluxos -120000 18000 45000 60000 70000
Para o relatório completo use gerar_relatorio.py.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, List, Optional

for _fluxo in (sys.stdout, sys.stderr):  # acentuação correta no console do Windows (cp1252)
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import econ_core as ec  # noqa: E402


def _json(obj: Any) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def _arquivo(caminho: str) -> Any:
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def construir_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="econ_cli", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def fluxo_args(p: argparse.ArgumentParser, taxa_obrig: bool = False) -> None:
        p.add_argument("--fluxos", nargs="+", type=float, required=True,
                       help="fluxo de caixa; índice 0 = hoje (saídas negativas)")
        p.add_argument("--taxa", type=float, required=taxa_obrig, help="TMA em decimal (0.18 = 18%%)")

    fluxo_args(sub.add_parser("vpl", help="Valor Presente Líquido"), True)
    fluxo_args(sub.add_parser("tir", help="Taxa Interna de Retorno"))
    p = sub.add_parser("payback", help="Payback simples (sem --taxa) ou descontado (com --taxa)")
    fluxo_args(p)
    fluxo_args(sub.add_parser("indicadores", help="VPL, TIR, TIRM, payback, IL e ROI de um fluxo"), True)

    p = sub.add_parser("equivalencia", help="VP/VF/PMT equivalentes")
    p.add_argument("--taxa", type=float, required=True)
    p.add_argument("--n", type=int, required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--vp", type=float)
    g.add_argument("--vf", type=float)
    g.add_argument("--pmt", type=float, help="parcela uniforme -> VP e VF da série")

    p = sub.add_parser("taxa", help="Conversão de taxa composta entre bases")
    p.add_argument("--taxa", type=float, required=True)
    p.add_argument("--de", type=float, required=True, help="duração do período da taxa informada (ex.: 12 meses)")
    p.add_argument("--para", type=float, required=True, help="duração do período desejado (ex.: 1 mês)")

    p = sub.add_parser("gva", help="Valor Agregado (EVM) com valores acumulados")
    for nome in ("planejado", "agregado", "real", "bac"):
        p.add_argument(f"--{nome}", type=float, required=True)

    p = sub.add_parser("gva-sprints", help="Série de GVA a partir de JSON {bac, sprints[]}")
    p.add_argument("--arquivo", required=True)

    p = sub.add_parser("markup", help="Preço por markup ou markup divisor")
    p.add_argument("--custo", type=float, required=True)
    p.add_argument("--markup", type=float, help="markup sobre o custo (0.5 = 50%%)")
    p.add_argument("--margem", type=float, help="margem desejada sobre o preço")
    p.add_argument("--impostos", type=float, default=0.0)
    p.add_argument("--outros", type=float, default=0.0)

    p = sub.add_parser("saas", help="LTV, CAC, LTV/CAC e payback do CAC")
    p.add_argument("--arpa", type=float, required=True, help="receita média por cliente/mês")
    p.add_argument("--margem", type=float, required=True, help="margem bruta (0.8 = 80%%)")
    p.add_argument("--churn", type=float, required=True, help="churn mensal")
    p.add_argument("--cac", type=float, required=True)

    p = sub.add_parser("depreciacao", help="Depreciação linear ou por soma dos dígitos")
    p.add_argument("--valor", type=float, required=True)
    p.add_argument("--vida", type=int, required=True)
    p.add_argument("--residual", type=float, default=0.0)
    p.add_argument("--metodo", choices=["linear", "soma-digitos"], default="linear")
    p.add_argument("--aliquota-ir", type=float, default=0.0)

    p = sub.add_parser("priorizar", help="Priorização econômica do backlog")
    p.add_argument("--arquivo", required=True, help="JSON: lista de itens")
    p.add_argument("--metodo", choices=["valor_esforco", "wsjf"], default="valor_esforco")

    p = sub.add_parser("comparar", help="Compara alternativas por CAUE")
    p.add_argument("--taxa", type=float, required=True)
    p.add_argument("--arquivo", required=True, help="JSON: lista de alternativas")

    p = sub.add_parser("suficiente", help="Análise marginal 'bom o suficiente'")
    p.add_argument("--arquivo", required=True, help="JSON: lista de níveis (nome, custo, beneficio acumulados)")

    p = sub.add_parser("modelo", help="Indicadores, cenários e sensibilidade de um modelo de negócio")
    p.add_argument("--arquivo", required=True, help="JSON com a chave 'modelo' (ou o próprio modelo)")

    fluxo_args(sub.add_parser("equilibrio", help="Investimento máximo e queda de receita que zeram o VPL"), True)
    p = sub.add_parser("estresse", help="Indicadores com investimento e/ou receita multiplicados por um fator")
    fluxo_args(p, True)
    p.add_argument("--fator-investimento", type=float, default=1.0, help="1.25 = custo 25%% maior")
    p.add_argument("--fator-receita", type=float, default=1.0, help="0.8 = receita 20%% menor")
    p = sub.add_parser("cocomo", help="Esforço de referência (COCOMO básico)")
    p.add_argument("--kloc", type=float, required=True)
    p.add_argument("--modo", choices=["organico", "semidestacado", "embarcado"], default="organico")
    return ap


def executar(args: argparse.Namespace) -> Any:
    c = args.cmd
    if c == "vpl":
        return {"vpl": ec.vpl(args.taxa, args.fluxos), "taxa": args.taxa, "fluxos": args.fluxos}
    if c == "tir":
        return {"tir": ec.tir(args.fluxos), "todas_as_raizes": ec.tir_todas(args.fluxos)}
    if c == "payback":
        return {"payback_periodos": ec.payback(args.fluxos, args.taxa),
                "tipo": "descontado" if args.taxa is not None else "simples"}
    if c == "indicadores":
        return {"vpl": ec.vpl(args.taxa, args.fluxos), "tir": ec.tir(args.fluxos),
                "tirm": ec.tirm(args.fluxos, args.taxa, args.taxa),
                "payback_simples": ec.payback(args.fluxos),
                "payback_descontado": ec.payback(args.fluxos, args.taxa),
                "indice_lucratividade": ec.indice_lucratividade(args.taxa, args.fluxos),
                "roi_simples": ec.roi_simples(args.fluxos),
                "roi_descontado": ec.roi_descontado(args.taxa, args.fluxos)}
    if c == "equivalencia":
        if args.vp is not None:
            return {"vf": ec.valor_futuro(args.vp, args.taxa, args.n),
                    "pmt_equivalente": ec.pmt_de_vp(args.vp, args.taxa, args.n)}
        if args.vf is not None:
            return {"vp": ec.valor_presente(args.vf, args.taxa, args.n)}
        return {"vp_serie": ec.vp_serie_uniforme(args.pmt, args.taxa, args.n),
                "vf_serie": ec.vf_serie_uniforme(args.pmt, args.taxa, args.n)}
    if c == "taxa":
        return {"taxa_equivalente": ec.taxa_equivalente(args.taxa, args.de, args.para)}
    if c == "gva":
        return ec.gva(args.planejado, args.agregado, args.real, args.bac)
    if c == "gva-sprints":
        dados = _arquivo(args.arquivo)
        return ec.gva_por_sprint(dados["sprints"], dados.get("bac"))
    if c == "markup":
        out = {}
        if args.markup is not None:
            out["preco_por_markup"] = ec.preco_markup(args.custo, args.markup)
            out["margem_equivalente"] = ec.markup_para_margem(args.markup)
        if args.margem is not None:
            out["preco_divisor"] = ec.preco_divisor(args.custo, args.impostos, args.margem, args.outros)
            out["markup_equivalente"] = ec.margem_para_markup(args.margem)
        if not out:
            raise SystemExit("informe --markup e/ou --margem")
        return out
    if c == "saas":
        return ec.ltv_cac(args.arpa, args.margem, args.churn, args.cac)
    if c == "depreciacao":
        fn = ec.depreciacao_linear if args.metodo == "linear" else ec.depreciacao_soma_digitos
        cotas = fn(args.valor, args.vida, args.residual)
        return {"cotas": cotas, "escudo_fiscal": ec.escudo_fiscal(cotas, args.aliquota_ir)}
    if c == "priorizar":
        return ec.priorizar(_arquivo(args.arquivo), args.metodo)
    if c == "comparar":
        dados = _arquivo(args.arquivo)
        return ec.comparar_alternativas(args.taxa, dados["alternativas"] if isinstance(dados, dict) else dados)
    if c == "suficiente":
        dados = _arquivo(args.arquivo)
        return ec.bom_o_suficiente(dados["niveis"] if isinstance(dados, dict) else dados)
    if c == "modelo":
        dados = _arquivo(args.arquivo)
        modelo = dados.get("modelo", dados)
        ind = ec.indicadores(modelo)
        ind.pop("detalhe")
        return {"indicadores": ind, "cenarios": ec.cenarios(modelo), "sensibilidade": ec.sensibilidade(modelo),
                "saas": ec.metricas_saas(modelo), "fator_clientes_equilibrio": ec.fator_equilibrio(modelo)}
    if c == "equilibrio":
        return ec.equilibrio_fluxo(args.taxa, args.fluxos)
    if c == "estresse":
        return ec.estresse_fluxo(args.taxa, args.fluxos, args.fator_investimento, args.fator_receita)
    if c == "cocomo":
        return ec.cocomo_basico(args.kloc, args.modo)
    raise SystemExit(f"comando desconhecido: {c}")


def main(argv: Optional[List[str]] = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        _json(executar(args))
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"erro: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

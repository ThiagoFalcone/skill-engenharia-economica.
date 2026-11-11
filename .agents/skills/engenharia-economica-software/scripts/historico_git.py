#!/usr/bin/env python3
"""Esforço, sprints e valor entregue a partir do histórico de um repositório GitHub.

Transforma commits e pull requests em evidências rastreáveis para a valoração:

* **Horas medidas** pelo método git-hours: commits do mesmo autor com intervalo menor que
  ``--gap-min`` pertencem à mesma sessão e somam o intervalo; o primeiro commit de cada
  sessão soma ``--bonus-min``. É um PISO de esforço, pois pesquisa, reuniões, testes manuais
  e planejamento não geram commit.
* **Horas estimadas** = horas medidas / ``--cobertura`` (fração do esforço que gera commit,
  premissa explícita).
* **Sprints** = janelas fixas de ``--janela-dias`` dias a partir do primeiro commit.
* **Valor agregado (VA)** de cada janela = BAC × peso dos PRs entregues (linhas alteradas),
  ignorando PRs de integração (merge/release).
* **Custo real (CR)** de cada janela = horas medidas da janela / cobertura × custo/hora.
* **Valor planejado (VP)**: plano linear (BAC / nº de janelas). BAC = pessoas × horas por
  semana por pessoa × semanas × custo/hora. O plano real da equipe, se existir, deve
  substituir esses dois parâmetros.

Uso:
    python historico_git.py --repo dono/nome --cache pasta_cache --saida historico.json
    python historico_git.py --cache pasta_cache --saida historico.json      # offline

Somente biblioteca padrão. Sem ``--token`` a API do GitHub limita 60 requisições por hora;
use a variável de ambiente GITHUB_TOKEN para mais.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sys
import urllib.request
from collections import defaultdict
from typing import Any, Dict, List, Optional

for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

API = "https://api.github.com"


def _get(url: str, token: Optional[str]) -> Any:
    cab = {"User-Agent": "engenharia-economica-skill", "Accept": "application/vnd.github+json"}
    if token:
        cab["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=30) as r:
        return json.load(r)


def _paginar(url: str, token: Optional[str]) -> List[Any]:
    saida, pagina = [], 1
    while True:
        sep = "&" if "?" in url else "?"
        dados = _get(f"{url}{sep}per_page=100&page={pagina}", token)
        saida += dados
        if len(dados) < 100:
            return saida
        pagina += 1


def coletar(repo: str, token: Optional[str]) -> Dict[str, Any]:
    commits = _paginar(f"{API}/repos/{repo}/commits", token)
    prs = _paginar(f"{API}/repos/{repo}/pulls?state=all", token)
    linhas_c = [{"sha": c["sha"][:7],
                 "autor": (c.get("author") or {}).get("login") or c["commit"]["author"]["name"],
                 "data": c["commit"]["author"]["date"],
                 "msg": c["commit"]["message"].split("\n")[0][:100]} for c in commits]
    linhas_p = []
    for p in prs:
        det = _get(f"{API}/repos/{repo}/pulls/{p['number']}", token)
        linhas_p.append({"n": p["number"], "autor": p["user"]["login"], "titulo": p["title"][:100],
                         "ramo": p["head"]["ref"], "criado": p["created_at"], "merge": p.get("merged_at"),
                         "adicoes": det.get("additions", 0), "remocoes": det.get("deletions", 0)})
    return {"repo": repo, "commits": linhas_c, "prs": linhas_p}


def _t(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def horas_git(datas: List[dt.datetime], gap_min: float, bonus_min: float) -> float:
    """Método git-hours para uma lista de instantes de um mesmo autor."""
    total, anterior = 0.0, None
    for d in sorted(datas):
        if anterior is None or (d - anterior).total_seconds() / 60 > gap_min:
            total += bonus_min / 60
        else:
            total += (d - anterior).total_seconds() / 3600
        anterior = d
    return total


def eh_integracao(pr: Dict[str, Any]) -> bool:
    t = pr["titulo"].lower()
    return t.startswith("merge") or t.startswith("release") or pr["ramo"] in ("develop", "main")


def analisar(dados: Dict[str, Any], a: argparse.Namespace) -> Dict[str, Any]:
    commits = sorted(dados["commits"], key=lambda c: c["data"])
    inicio, fim = _t(commits[0]["data"]), _t(commits[-1]["data"])
    por_autor: Dict[str, List[dt.datetime]] = defaultdict(list)
    for c in commits:
        por_autor[c["autor"]].append(_t(c["data"]))
    autores = [{"autor": k, "commits": len(v), "dias_ativos": len({d.date() for d in v}),
                "horas_medidas": round(horas_git(v, a.gap_min, a.bonus_min), 1)} for k, v in por_autor.items()]
    autores.sort(key=lambda x: -x["commits"])
    horas_medidas = sum(x["horas_medidas"] for x in autores)

    base = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
    n_jan = (fim - base).days // a.janela_dias + 1
    jan_c: Dict[int, Dict[str, List[dt.datetime]]] = defaultdict(lambda: defaultdict(list))
    for c in commits:
        d = _t(c["data"])
        jan_c[(d - base).days // a.janela_dias][c["autor"]].append(d)
    entregues = [p for p in dados["prs"] if p.get("merge") and not eh_integracao(p)]
    tam_total = sum(p["adicoes"] + p["remocoes"] for p in entregues) or 1
    jan_p: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    for p in entregues:
        jan_p[(_t(p["merge"]) - base).days // a.janela_dias].append(p)

    semanas = (fim - inicio).days / 7.0
    horas_est = horas_medidas / a.cobertura
    bac = a.pessoas * a.horas_semana_pessoa * semanas * a.custo_hora
    janelas, sprints = [], []
    for k in range(n_jan):
        h = sum(horas_git(v, a.gap_min, a.bonus_min) for v in jan_c[k].values())
        peso = sum(p["adicoes"] + p["remocoes"] for p in jan_p[k]) / tam_total
        ini = base + dt.timedelta(days=k * a.janela_dias)
        janelas.append({"sprint": k + 1, "inicio": ini.date().isoformat(),
                        "commits": sum(len(v) for v in jan_c[k].values()),
                        "horas_medidas": round(h, 1), "prs_entregues": [p["n"] for p in jan_p[k]],
                        "peso_entregue": round(peso, 4)})
        sprints.append({"sprint": k + 1, "planejado": round(bac / n_jan, 2),
                        "agregado": round(bac * peso, 2),
                        "real": round(h / a.cobertura * a.custo_hora, 2)})
    return {
        "fonte": f"https://github.com/{dados['repo']}" if dados.get("repo") else "cache local",
        "periodo": {"inicio": inicio.date().isoformat(), "fim": fim.date().isoformat(), "semanas": round(semanas, 1)},
        "commits": len(commits), "prs_total": len(dados["prs"]), "prs_entregues": len(entregues),
        "autores": autores,
        "parametros": {"gap_min": a.gap_min, "bonus_min": a.bonus_min, "cobertura": a.cobertura,
                       "janela_dias": a.janela_dias, "pessoas": a.pessoas,
                       "horas_semana_pessoa_planejadas": a.horas_semana_pessoa, "custo_hora": a.custo_hora},
        "horas_medidas": round(horas_medidas, 1),
        "horas_estimadas": round(horas_est, 1),
        "janelas": janelas,
        "gva_sprints": {"bac": round(bac, 2), "sprints": sprints},
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="dono/nome no GitHub (omitir para usar só o cache)")
    ap.add_argument("--cache", required=True, help="pasta com commits.json e prs.json (criada se --repo for usado)")
    ap.add_argument("--saida", required=True, help="arquivo JSON de saída")
    ap.add_argument("--janela-dias", type=int, default=14)
    ap.add_argument("--gap-min", type=float, default=120)
    ap.add_argument("--bonus-min", type=float, default=120)
    ap.add_argument("--cobertura", type=float, default=0.20,
                    help="fração do esforço total que gera commit (premissa; 0,20 = commits são 20%% do esforço)")
    ap.add_argument("--pessoas", type=int, default=3)
    ap.add_argument("--horas-semana-pessoa", type=float, default=6.0, help="plano: horas por semana por pessoa")
    ap.add_argument("--custo-hora", type=float, default=50.0)
    a = ap.parse_args(argv)
    if not 0 < a.cobertura <= 1:
        ap.error("--cobertura deve estar entre 0 (exclusivo) e 1")
    arq_c, arq_p = os.path.join(a.cache, "commits.json"), os.path.join(a.cache, "prs.json")
    if a.repo:
        dados = coletar(a.repo, os.environ.get("GITHUB_TOKEN"))
        os.makedirs(a.cache, exist_ok=True)
        json.dump(dados["commits"], open(arq_c, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(dados["prs"], open(arq_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        dados = {"repo": None, "commits": json.load(open(arq_c, encoding="utf-8")),
                 "prs": json.load(open(arq_p, encoding="utf-8"))}
    res = analisar(dados, a)
    if a.repo is None and os.path.exists(os.path.join(a.cache, "fonte.txt")):
        res["fonte"] = open(os.path.join(a.cache, "fonte.txt"), encoding="utf-8").read().strip()
    json.dump(res, open(a.saida, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{res['commits']} commits, {res['prs_entregues']} PRs entregues, {res['horas_medidas']} h medidas, "
          f"{res['horas_estimadas']} h estimadas, {len(res['janelas'])} sprints -> {a.saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

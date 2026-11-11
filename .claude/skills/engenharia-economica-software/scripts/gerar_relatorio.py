#!/usr/bin/env python3
"""Gera o relatório completo de valoração econômica (Markdown) a partir de um JSON de entrada.

Uso:
    python gerar_relatorio.py --entrada entrada.json --saida relatorio.md

Todos os números saem de ``econ_core`` (determinístico). Este script só orquestra e formata;
o texto de decisão é derivado dos números, nunca escrito à mão.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

for _fluxo in (sys.stdout, sys.stderr):  # acentuação correta no console do Windows (cp1252)
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import econ_core as ec  # noqa: E402


# ------------------------------- formatação -------------------------------- #
def brl(v: Optional[float], casas: int = 0) -> str:
    if v is None:
        return "n/d"
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-R$ {s}" if v < 0 else f"R$ {s}"


def pct(v: Optional[float], casas: int = 1) -> str:
    return "n/d" if v is None else f"{v * 100:.{casas}f}%".replace(".", ",")


def num(v: Optional[float], casas: int = 2) -> str:
    return "n/d" if v is None else f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def anos(v: Optional[float]) -> str:
    return "não recupera no horizonte" if v is None else f"{num(v, 2)} anos"


def tabela(cabecalho: List[str], linhas: List[List[str]]) -> str:
    out = ["| " + " | ".join(cabecalho) + " |", "|" + "|".join(["---"] * len(cabecalho)) + "|"]
    out += ["| " + " | ".join(l) + " |" for l in linhas]
    return "\n".join(out)


# ------------------------------- preparação -------------------------------- #
def custos_desenvolvimento(entrada: Dict[str, Any]) -> Dict[str, Any]:
    dev = entrada["desenvolvimento"]
    enc = float(dev.get("encargos", 0.0))
    linhas = []
    total_h = 0.0
    direto_orcado = 0.0
    for p in dev["equipe"]:
        c = ec.custo_direto_equipe(p["horas"], p["custo_hora"], enc)
        linhas.append({**p, "custo": c})
        total_h += p["horas"]
        direto_orcado += c
    ind = dev.get("custos_indiretos", {})
    indireto = ec.rateio_indireto(ind["total_periodo"], total_h, ind["horas_totais_base_rateio"]) if ind else 0.0
    outros = dev.get("outros_investimentos", {})
    direto = direto_orcado
    custo_real = None
    gva = entrada.get("gva_sprints")
    if gva:
        custo_real = sum(s["real"] for s in gva["sprints"])
        if dev.get("usar_custo_real_do_gva"):
            direto = custo_real
    return {"linhas": linhas, "horas": total_h, "direto_orcado": direto_orcado, "direto": direto,
            "custo_real_gva": custo_real, "indireto": indireto, "outros": outros}


def preparar_modelo(entrada: Dict[str, Any]) -> Dict[str, Any]:
    cd = custos_desenvolvimento(entrada)
    modelo = ec.mesclar(entrada["modelo"], {})
    itens = {"Mão de obra direta de desenvolvimento": cd["direto"],
             "Custos indiretos rateados": cd["indireto"]}
    itens.update(cd["outros"])
    itens.update(modelo["investimento"].get("itens", {}))
    modelo["investimento"]["itens"] = itens
    return modelo


def semaforo(entrada, modelo, ind, saas, cen):
    """Critérios do painel de decisão: lista de (critério, resultado, nível, regra); nível = bom|medio|ruim."""
    det = ind["detalhe"]
    tma = ind["tma"]
    capex_ = det["capex"]
    horiz = modelo["horizonte_anos"]
    gva_ = entrada.get("gva_sprints")
    ult = ec.gva_por_sprint(gva_["sprints"], gva_["bac"])[-1] if gva_ else None
    pb_d = ind["payback_descontado"]

    def nivel(bom, medio):
        return "bom" if bom else ("medio" if medio else "ruim")

    tir_ = ind["tir"]
    linhas = [
        ("VPL > 0", brl(ind["vpl"]),
         nivel(ind["vpl"] > 0.05 * capex_, abs(ind["vpl"]) <= 0.05 * capex_), "bom se > 5% do investimento"),
        ("TIR > TMA", f"{pct(tir_)} vs {pct(tma)}",
         nivel(tir_ is not None and tir_ > tma + 0.03, tir_ is not None and abs(tir_ - tma) <= 0.03),
         "bom se 3 pontos acima da TMA"),
        ("Payback descontado no horizonte", anos(pb_d),
         nivel(pb_d is not None and pb_d <= 0.7 * horiz, pb_d is not None), "bom se em até 70% do horizonte"),
        ("LTV/CAC ≥ 3", num(saas["ltv_cac"], 1), nivel(saas["ltv_cac"] >= 3, saas["ltv_cac"] >= 1),
         "referência de mercado"),
        ("Payback do CAC ≤ 12 meses", f"{num(saas['payback_cac_meses'], 1)} meses",
         nivel(saas["payback_cac_meses"] <= 12, saas["payback_cac_meses"] <= 18), "recuperação rápida do CAC"),
        ("Cenário pessimista com VPL ≥ 0", brl(cen["pessimista"]["vpl"]) if "pessimista" in cen else "n/d",
         nivel("pessimista" in cen and cen["pessimista"]["vpl"] >= 0, False), "resiliência a premissas ruins"),
    ]
    if ult:
        linhas += [
            ("IDC final ≥ 1", num(ult["idc"], 2), nivel(ult["idc"] >= 1, ult["idc"] >= 0.9), "custo versus valor entregue"),
            ("IDP final ≥ 1", num(ult["idp"], 2), nivel(ult["idp"] >= 1, ult["idp"] >= 0.9), "prazo versus planejado"),
        ]
    return linhas


# --------------------------------- relatório -------------------------------- #
def gerar(entrada: Dict[str, Any]) -> str:
    proj = entrada["projeto"]
    cd = custos_desenvolvimento(entrada)
    modelo = preparar_modelo(entrada)
    ind = ec.indicadores(modelo)
    det = ind["detalhe"]
    tma = ind["tma"]
    saas = ec.metricas_saas(modelo)
    cen_lista = ec.cenarios(modelo)
    cen = {c["cenario"]: c for c in cen_lista}
    sens = ec.sensibilidade(modelo)
    f_eq = ec.fator_equilibrio(modelo)
    f_eq_preco = ec.fator_equilibrio(modelo, "fator_preco")
    gva_ = entrada.get("gva_sprints")
    ult = ec.gva_por_sprint(gva_["sprints"], gva_["bac"])[-1] if gva_ else None
    viavel = ind["vpl"] > 0 and (ind["tir"] is not None and ind["tir"] > tma)
    L: List[str] = []
    add = L.append

    add(f"# Relatório de valoração econômica, {proj['nome']}\n")
    add("> Gerado pela skill `engenharia-economica-software` (cálculos determinísticos em `scripts/econ_core.py`).")
    add("> **Aviso:** todos os valores de mercado e de esforço são **premissas estimadas** listadas na seção 13; "
        "o resultado é tão confiável quanto essas premissas.\n")

    # 1 Sumário executivo
    add("## 1. Sumário executivo (Aula 7)\n")
    marginal = abs(ind["vpl"]) <= 0.05 * det["capex"]
    if viavel:
        veredito = ("**VIÁVEL** nas premissas do caso-base: VPL positivo e TIR acima da TMA"
                    + (", porém **no limite** (|VPL| ≤ 5% do investimento): pequenas mudanças de premissa invertem a decisão." if marginal else "."))
    elif marginal:
        veredito = ("**NO LIMITE DA VIABILIDADE (levemente negativo)** no caso-base: VPL ≤ 0 e TIR abaixo da TMA, mas |VPL| ≤ 5% do "
                    "investimento, dentro da margem de erro das premissas. A decisão depende dos cenários e das alavancas da seção 6.")
    else:
        veredito = ("**NÃO VIÁVEL no caso-base** no horizonte analisado: VPL ≤ 0 ou TIR abaixo da TMA. "
                    "Ver cenários, ponto de equilíbrio e alavancas na seção 6.")
    add(veredito + "\n")
    add(tabela(["Indicador", "Resultado"], [
        ["Investimento inicial (ano 0)", brl(det["capex"])],
        ["TMA adotada", pct(tma)],
        ["VPL", brl(ind["vpl"])],
        ["TIR", pct(ind["tir"])],
        ["TIR modificada (TIRM)", pct(ind["tirm"])],
        ["Payback simples", anos(ind["payback_simples"])],
        ["Payback descontado", anos(ind["payback_descontado"])],
        ["Índice de lucratividade (VP entradas / VP saídas)", num(ind["indice_lucratividade"], 3)],
        ["ROI descontado (VPL / VP das saídas)", pct(ind["roi_descontado"])],
        ["Fluxo acumulado nominal em " + str(modelo["horizonte_anos"]) + " anos", brl(sum(ind["fluxo"]))],
    ]))
    add("")
    add("**Painel de decisão** (semáforo calculado dos números; ✅ bom, ⚠️ atenção, ❌ crítico):\n")
    icone = {"bom": "✅", "medio": "⚠️", "ruim": "❌"}
    linhas_sem = [[c, r, icone[n], regra] for c, r, n, regra in semaforo(entrada, modelo, ind, saas, cen)]
    add(tabela(["Critério", "Resultado", "Sinal", "Regra"], linhas_sem))
    add("")
    if f_eq is not None:
        add(f"**Ponto de equilíbrio:** com os demais parâmetros fixos, o VPL zera com "
            f"**{num(f_eq * 100, 0)}% do volume de clientes** do caso-base "
            f"(≈ {num(det['linhas'][-1]['clientes_fim'] * f_eq, 0)} organizações pagantes no fim do ano "
            f"{modelo['horizonte_anos']}).\n")
    if f_eq_preco is not None:
        add(f"**Preço de equilíbrio:** o VPL zera com preço a {num(f_eq_preco * 100, 0)}% do praticado "
            f"(≈ {brl(modelo['receita']['preco_mensal'] * f_eq_preco, 2)}/mês no ano 1).\n")
    add("Principais riscos e hipóteses: ver seção 13.\n")

    # 2 Contexto de decisão
    add("## 2. Decisão e alternativas (Aulas 1 e 2)\n")
    add(f"**Decisão:** comercializar a plataforma como SaaS B2B (investindo {brl(det['capex'])} no ano 0 e arcando com a operação) "
        f"**versus** não comercializar e aplicar o capital à TMA de {pct(tma)} (custo de oportunidade).\n")
    add("**Produto avaliado:** " + proj["descricao"] + f"  \n**Stack:** {proj['stack']}  \n"
        f"**Hospedagem atual:** {proj['hospedagem_atual']}\n")
    m = proj.get("metricas_medidas_no_repositorio", {})
    if m:
        kloc = (m["java_main_linhas"] + m["java_teste_linhas"] + m["frontend_ts_tsx_linhas"]) / 1000.0
        coc = ec.cocomo_basico(kloc)
        add(f"**Tamanho medido no repositório:** {num(kloc, 1)} mil linhas "
            f"({num(m['java_main_linhas'], 0)} Java de produção, {num(m['java_teste_linhas'], 0)} Java de testes, "
            f"{num(m['frontend_ts_tsx_linhas'], 0)} TS/TSX), {m['migrations_flyway']} migrations, "
            f"{m['testes_backend_readme']} testes de backend, {m['verificacoes_api_e2e_readme']} verificações de API e "
            f"{m['testes_ui_e2e_readme']} testes de interface.  ")
        add(f"Referência COCOMO básico (modo orgânico): {num(coc['esforco_pessoa_mes'], 1)} pessoa-mês e "
            f"{num(coc['prazo_meses'], 1)} meses, o esforço declarado ({num(cd['horas'], 0)} h ≈ "
            f"{num(cd['horas'] / 160, 1)} pessoa-mês) fica bem abaixo, coerente com o uso de frameworks e ferramentas "
            f"modernas, mas é um ponto a defender (seção 13).\n")

    # 3 Custos
    add("## 3. Custo, preço e valor (Aula 4)\n")
    add("### 3.1 Custos diretos e indiretos do desenvolvimento\n")
    add(tabela(["Papel", "Horas", "Custo/hora", "Custo direto"],
               [[l["papel"], num(l["horas"], 0), brl(l["custo_hora"]), brl(l["custo"])] for l in cd["linhas"]]
               + [["**Total orçado (BAC)**", f"**{num(cd['horas'], 0)}**", "", f"**{brl(cd['direto_orcado'])}**"]]))
    add("")
    if cd["custo_real_gva"] is not None:
        desvio = cd["custo_real_gva"] / cd["direto_orcado"] - 1
        add(f"Custo real acumulado nas sprints (CR): **{brl(cd['custo_real_gva'])}** "
            f"({pct(desvio)} sobre o orçamento), usado como investimento direto no modelo.\n")
    add(tabela(["Item de investimento (CapEx, ano 0)", "Valor", "Natureza"], [
        ["Mão de obra direta", brl(cd["direto"]), "Direto"],
        ["Custos indiretos rateados por horas", brl(cd["indireto"]), "Indireto (rateio)"],
    ] + [[k, brl(v), "Outro"] for k, v in cd["outros"].items()]
        + [["**Total**", f"**{brl(det['capex'])}**", ""]]))
    add("\nO desenvolvimento é tratado como **CapEx** (ativo intangível amortizado em "
        f"{modelo['investimento'].get('vida_util_anos')} anos); manutenção, hospedagem, suporte e marketing são **OpEx**.\n")

    add("### 3.2 Preço: markup, custo unitário e valor percebido\n")
    linhas_cu = []
    mg = entrada.get("valor_percebido", {}).get("margem_alvo_para_preco_minimo", 0.20)
    aliq = modelo["tributos"].get("sobre_receita", 0.0)
    for l in det["linhas"]:
        base = l["clientes_medio"] * 12
        custo_unit = (l["custos_variaveis"] + l["custos_fixos"] + l["aquisicao_clientes"]) / base if base else None
        piso = ec.preco_divisor(custo_unit, aliq, mg) if custo_unit else None
        linhas_cu.append([str(l["ano"]), brl(l["preco_mensal"], 2), brl(custo_unit, 2), brl(piso, 2),
                          pct(ec.margem_para_markup(mg))])
    add(tabela(["Ano", "Preço praticado/mês", "Custo unitário/mês", f"Preço mínimo (margem {pct(mg, 0)} + tributos)",
                "Markup equivalente s/ custo"], linhas_cu))
    abaixo = [l["ano"] for l in det["linhas"]
              if l["clientes_medio"] and l["preco_mensal"] < (l["custos_variaveis"] + l["custos_fixos"] + l["aquisicao_clientes"]) / (l["clientes_medio"] * 12)]
    add(f"\nMargem de {pct(mg, 0)} sobre o preço equivale a markup de {pct(ec.margem_para_markup(mg))} sobre o custo "
        f"(`k = m/(1-m)`). "
        + (f"Nos anos {', '.join(map(str, abaixo))} o preço praticado fica abaixo do custo unitário pleno, porque a "
           f"base de clientes ainda não dilui os custos fixos." if abaixo
           else "O preço praticado cobre o custo unitário pleno em todos os anos.") + "\n")
    vp_ = entrada.get("valor_percebido")
    if vp_:
        valor = (vp_["horas_retrabalho_por_mes_organizacao"] * vp_["custo_hora"] * vp_["reducao_esperada"])
        add(f"**Valor percebido pelo cliente:** uma organização que gasta {vp_['horas_retrabalho_por_mes_organizacao']} h/mês em "
            f"retrabalho de requisitos a {brl(vp_['custo_hora'])}/h e reduz {pct(vp_['reducao_esperada'], 0)} "
            f"economiza **{brl(valor)}/mês**. O preço de {brl(saas['arpa_mensal'])} captura "
            f"{pct(saas['arpa_mensal'] / valor, 0)} desse valor, {'preço ancorado no valor, abaixo do valor entregue' if saas['arpa_mensal'] < valor else 'ATENÇÃO: preço acima do valor percebido'}.\n")

    # 4 Fluxo de caixa
    add("## 4. Demonstrativo e fluxo de caixa (Aulas 3 e 5)\n")
    cab = ["Item"] + ["Ano 0"] + [f"Ano {l['ano']}" for l in det["linhas"]]
    L_ = det["linhas"]

    def linha(nome, getter, ano0=""):
        return [nome, ano0] + [brl(getter(l)) for l in L_]

    add(tabela(cab, [
        ["Clientes (fim do ano)", ""] + [num(l["clientes_fim"], 0) for l in L_],
        linha("Receita bruta", lambda l: l["receita"]),
        linha("(−) Tributos sobre a receita", lambda l: -l["impostos_receita"]),
        linha("(−) Custos variáveis", lambda l: -l["custos_variaveis"]),
        linha("(−) Custos fixos (OpEx)", lambda l: -l["custos_fixos"]),
        linha("(−) Aquisição de clientes (CAC)", lambda l: -l["aquisicao_clientes"]),
        linha("**EBITDA**", lambda l: l["ebitda"]),
        linha("(−) Depreciação/amortização", lambda l: -l["depreciacao"]),
        linha("**EBIT (lucro operacional)**", lambda l: l["ebit"]),
        linha("(−) IRPJ/CSLL", lambda l: -l["ir_csll"]),
        linha("(+) Valor residual", lambda l: l["valor_residual"]),
        ["(−) Investimento (CapEx)", brl(-det["capex"])] + [""] * len(L_),
        ["**Fluxo de caixa líquido**", f"**{brl(ind['fluxo'][0])}**"] + [f"**{brl(l['fluxo_liquido'])}**" for l in L_],
    ]))
    acum, ac_l, ac_v = 0.0, [], []
    for f in ind["fluxo"]:
        acum += f
        ac_l.append(brl(acum))
        ac_v.append(acum)
    add("\n" + tabela(["", "Ano 0"] + [f"Ano {l['ano']}" for l in L_],
                      [["Fluxo acumulado", ac_l[0]] + ac_l[1:],
                       ["Fluxo descontado à TMA", brl(ind["fluxo"][0])] +
                       [brl(f / (1 + tma) ** (t + 1)) for t, f in enumerate(ind["fluxo"][1:])]]))
    maxabs = max(abs(v) for v in ac_v) or 1.0
    add("\n**Fluxo acumulado (gráfico em texto, R$ mil; █ positivo, ▒ negativo):**\n")
    add("```")
    for t_, v in enumerate(ac_v):
        barra = ("█" if v >= 0 else "▒") * max(1, int(round(abs(v) / maxabs * 30)))
        add(f"Ano {t_} | {barra} " + num(v / 1000, 1))
    add("```")
    add("\nSimplificações: valores correntes (TMA nominal), receita pela média de clientes no ano, prejuízo fiscal "
        "compensado com o limite informado, depreciação linear sem crédito de impostos quando a alíquota de IRPJ/CSLL é zero.\n")

    # 5 Viabilidade
    add("## 5. Viabilidade: VPL, TIR e Payback (Aulas 3, 5, 6 e 8)\n")
    add(f"- **VPL** = Σ FCₜ/(1+TMA)ᵗ com TMA = {pct(tma)} → **{brl(ind['vpl'])}**")
    add(f"- **TIR** (taxa que zera o VPL) = **{pct(ind['tir'])}** "
        f"({'acima' if ind['tir'] is not None and ind['tir'] > tma else 'abaixo'} da TMA); "
        f"TIRM com reinvestimento à TMA = {pct(ind['tirm'])}")
    add(f"- **Payback simples** = {anos(ind['payback_simples'])}; **descontado** = {anos(ind['payback_descontado'])}")
    add(f"- **Índice de lucratividade** = {num(ind['indice_lucratividade'], 3)} "
        f"({'> 1: cria valor' if (ind['indice_lucratividade'] or 0) > 1 else '≤ 1: não cria valor'})")
    todas = ec.tir_todas(ind["fluxo"])
    if len(todas) > 1:
        add(f"- ⚠️ O fluxo tem mais de uma TIR ({', '.join(pct(r) for r in todas)}); decidir pelo VPL/TIRM.")
    add("")
    add(f"**Depreciação (Aula 8):** CapEx de {brl(det['capex'])} amortizado linearmente em "
        f"{modelo['investimento'].get('vida_util_anos')} anos = {brl(det['linhas'][0]['depreciacao'])}/ano. "
        f"Com alíquota de IRPJ/CSLL de {pct(modelo['tributos'].get('ir_csll', 0))} no caso-base, o escudo fiscal anual seria "
        f"{brl(ec.escudo_fiscal([det['linhas'][0]['depreciacao']], modelo['tributos'].get('ir_csll', 0))[0])}; "
        f"o cenário `lucro_real` (seção 6) quantifica esse efeito.\n")

    # 6 Cenários e sensibilidade
    add("## 6. Cenários, sensibilidade e equilíbrio (Aulas 7 e 8)\n")
    add(tabela(["Cenário", "VPL", "TIR", "Payback simples", "Payback descontado"],
               [[c["cenario"], brl(c["vpl"]), pct(c["tir"]), anos(c["payback_simples"]), anos(c["payback_descontado"])]
                for c in cen_lista]))
    add("\n**Sensibilidade (tornado, ±20% em cada fator, VPL):**\n")
    nomes = {"fator_clientes": "Volume de clientes", "fator_preco": "Preço", "fator_custos": "Custos operacionais",
             "fator_capex": "Investimento inicial", "tma": "TMA"}
    add(tabela(["Fator", "VPL com −20%", "VPL com +20%", "Amplitude"],
               [[nomes.get(s["fator"], s["fator"]), brl(s["vpl_menos"]), brl(s["vpl_mais"]), brl(s["amplitude"])]
                for s in sens]))
    add("")

    # 7 SaaS
    add("## 7. Métricas de produto digital: CAC e LTV (Aula 8)\n")
    add(tabela(["Métrica", "Valor"], [
        ["ARPA (receita média por organização/mês)", brl(saas["arpa_mensal"], 2)],
        ["Margem bruta unitária (após tributos e custos variáveis)", pct(saas["margem_bruta_unitaria"])],
        ["Churn mensal / anual", f"{pct(modelo['receita']['churn_mensal'])} / {pct(ec.churn_anual(modelo['receita']['churn_mensal']))}"],
        ["Vida média do cliente", f"{num(saas['vida_media_meses'], 1)} meses"],
        ["LTV = ARPA × margem ÷ churn", brl(saas["ltv"])],
        ["CAC", brl(saas["cac"])],
        ["LTV/CAC (meta usual ≥ 3)", num(saas["ltv_cac"], 1) + ("  ✅" if saas["ltv_cac"] >= 3 else "  ⚠️")],
        ["Payback do CAC", f"{num(saas['payback_cac_meses'], 1)} meses"],
    ]))
    add("")

    # 8 GVA
    gva = entrada.get("gva_sprints")
    if gva:
        add("## 8. Eficiência ágil: Gerenciamento de Valor Agregado (Aula 9)\n")
        add(f"Orçamento total (BAC): {brl(gva['bac'])}. {gva.get('nota', '')}\n")
        serie = ec.gva_por_sprint(gva["sprints"], gva["bac"])
        add(tabela(["Sprint", "VP", "VA", "CR", "IDC", "IDP", "EAC (BAC/IDC)"],
                   [[str(s["sprint"]), brl(s["planejado"]), brl(s["agregado"]), brl(s["real"]),
                     num(s["idc"], 2), num(s["idp"], 2), brl(s["eac"])] for s in serie]))
        u = serie[-1]
        add(f"\n**Leitura final (sprint {u['sprint']}):** IDC = {num(u['idc'], 2)} "
            f"({'abaixo de 1: gastou mais do que o valor entregue' if u['idc'] < 1 else 'eficiente em custo'}), "
            f"IDP = {num(u['idp'], 2)} "
            f"({'atrasado' if u['idp'] < 1 else 'no prazo ou adiantado'}). "
            f"Variação de custos = {brl(u['variacao_custos'])}; variação de prazo = {brl(u['variacao_prazo'])}.  \n"
            f"EAC (desvio persistente) = {brl(u['eac'])}; EAC (desvio atípico) = {brl(u['eac_desvio_atipico'])}; "
            f"EAC (IDC×IDP) = {brl(u['eac_idc_idp'])}; ETC = {brl(u['etc'])}; VAC = {brl(u['vac'])}.\n")
        meio = serie[len(serie) // 2 - 1]
        add(f"*Previsão no meio do projeto (sprint {meio['sprint']}):* EAC = {brl(meio['eac'])} contra o BAC de "
            f"{brl(gva['bac'])}, a coluna EAC mostra como a previsão converge para o custo final.\n")

    # 9 Alternativas de infraestrutura
    alt = entrada.get("alternativas_infraestrutura")
    if alt:
        add("## 9. Alternativas de infraestrutura e substituição (Aulas 1, 2, 10 e 11)\n")
        add(alt["descricao"] + "\n")
        res = ec.comparar_alternativas(tma, alt["alternativas"])
        obs = {a["nome"]: a.get("observacao", "") for a in alt["alternativas"]}
        add(tabela(["#", "Alternativa", "VP dos custos", "CAUE (custo anual equivalente)", "Observação"],
                   [[str(r["ranking"]), r["nome"], brl(r["vp_custos"]), brl(-r["caue"]), obs[r["nome"]]] for r in res]))
        add(f"\n**Melhor custo econômico:** {res[0]['nome']}. Decisão final deve pesar também SLA, escala e risco "
            f"(critérios não monetários).\n")

    # 10 Priorização
    bl = entrada.get("backlog_roadmap")
    if bl:
        add("## 10. Priorização econômica do backlog (Aulas 10 a 12)\n")
        r1 = ec.priorizar(bl, "valor_esforco")
        add("**Valor ÷ Esforço** (valor 1–10, esforço em pontos):\n")
        add(tabela(["#", "Item", "Valor", "Esforço", "Score", "Quadrante"],
                   [[str(x["ranking"]), x["nome"], num(x["valor"], 0), num(x["esforco"], 0), num(x["score"], 2),
                     x["quadrante"]] for x in r1]))
        r2 = ec.priorizar(bl, "wsjf")
        add("\n**WSJF** = (valor de negócio + criticidade de tempo + redução de risco) ÷ tamanho:\n")
        add(tabela(["#", "Item", "Custo do atraso", "Tamanho", "WSJF"],
                   [[str(x["ranking"]), x["nome"], num(x["valor_total"], 0), num(x["esforco_total"], 0),
                     num(x["score"], 2)] for x in r2]))
        add("")

    # 11 Bom o suficiente
    q = entrada.get("qualidade_bom_o_suficiente")
    if q:
        add("## 11. Princípio “bom o suficiente” e custo de oportunidade (Aulas 10 a 12)\n")
        add(q["descricao"] + "\n")
        r = ec.bom_o_suficiente(q["niveis"])
        add(tabela(["Nível", "Custo acum.", "Benefício acum.", "Δ custo", "Δ benefício", "Compensa?", "Líquido"],
                   [[n["nome"], brl(n["custo"]), brl(n["beneficio"]), brl(n["custo_marginal"]),
                     brl(n["beneficio_marginal"]), "sim" if n["compensa"] else "não", brl(n["liquido"])]
                    for n in r["niveis"]]))
        nomes_n = [n["nome"] for n in r["niveis"]]
        rec = r["recomendado_regra_marginal"]
        prox = nomes_n[nomes_n.index(rec) + 1] if rec in nomes_n and nomes_n.index(rec) + 1 < len(nomes_n) else None
        add(f"\n**Recomendação (regra marginal Δbenefício ≥ Δcusto):** parar em “{rec}”. "
            f"Primeiro nível de maior benefício líquido: “{r['maior_liquido']}”."
            + (f" O nível seguinte (“{prox}”) acrescenta menos benefício do que custo: é perfeccionismo, não valor."
               if prox else "") + "\n")

    # 12 Modelo de negócio
    add("## 12. Proposta de modelo de negócio\n")
    add(f"- **Modelo:** SaaS B2B por organização, assinatura mensal (ARPA-base {brl(saas['arpa_mensal'])}), com planos "
        "Starter (1 projeto ativo, poucos membros), Pro (projetos ilimitados, pesquisa de avaliação e exportações) e "
        "Enterprise (SSO, SLA, suporte dedicado, sob consulta).")
    add("- **Canal e aquisição:** inbound com conteúdo de elicitação de requisitos, parcerias com instituições de ensino "
        "(plano educacional gratuito como geração de demanda) e outbound para consultorias e fábricas de software; "
        f"CAC-alvo de {brl(saas['cac'])} (LTV/CAC = {num(saas['ltv_cac'], 1)}).")
    add("- **Precificação:** ancorada no valor percebido (seção 3.2) e validada contra o piso de custo + margem.")
    add("- **Alavancas de VPL** (pela sensibilidade): " + ", ".join(
        nomes.get(s["fator"], s["fator"]).lower() for s in sens[:3]) + ".")
    add("- **Próximos passos:** validar o preço com 5–10 organizações-piloto, medir churn real, migrar a hospedagem "
        "para uma opção com SLA ao primeiro cliente pagante e acompanhar o IDC/IDP das próximas releases.\n")

    # 13 Hipóteses
    add("## 13. Hipóteses, premissas e riscos (Aula 7)\n")
    add(f"- TMA: {modelo.get('tma_justificativa', 'premissa informada')}")
    for h in entrada.get("hipoteses_e_riscos", []):
        add(f"- {h}")
    add("")
    # 14 Leitura por perfil
    add("## 14. Leitura por perfil de decisor\n")
    maior = nomes.get(sens[0]["fator"], sens[0]["fator"]).lower()
    pess = brl(cen["pessimista"]["vpl"]) if "pessimista" in cen else "n/d"
    add(f"- **Investidor:** investir {brl(det['capex'])} hoje dá VPL de {brl(ind['vpl'])} a {pct(tma)} a.a. "
        f"(TIR {pct(ind['tir'])}), com payback descontado de {anos(ind['payback_descontado'])}. "
        f"O risco principal é a variável {maior}; no cenário pessimista o VPL é {pess}.")
    top = ec.priorizar(entrada["backlog_roadmap"], "wsjf")[0]["nome"] if entrada.get("backlog_roadmap") else "definir o backlog"
    add(f"- **Product Owner:** o preço de {brl(saas['arpa_mensal'])}/mês dá LTV/CAC de {num(saas['ltv_cac'], 1)}; "
        f"a prioridade do roadmap é {top} (maior WSJF).")
    if ult:
        melhor = (ec.comparar_alternativas(tma, entrada["alternativas_infraestrutura"]["alternativas"])[0]["nome"]
                  if entrada.get("alternativas_infraestrutura") else "a definir")
        add(f"- **Líder técnico:** IDC final {num(ult['idc'], 2)} e IDP {num(ult['idp'], 2)} indicam "
            f"{'custo acima do valor entregue' if ult['idc'] < 1 else 'custo sob controle'} e "
            f"{'atraso' if ult['idp'] < 1 else 'prazo cumprido'}; a hospedagem de menor custo é {melhor}, "
            f"e o investimento em qualidade deve parar quando o benefício marginal não cobre o custo.")
    add("")
    add("---\n*Reprodução:* `python .agents/skills/engenharia-economica-software/scripts/gerar_relatorio.py --entrada examples/tcc-input.json --saida examples/tcc-valuation-report.md`")
    return "\n".join(L) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Gera o relatório de valoração econômica em Markdown.")
    ap.add_argument("--entrada", required=True, help="JSON de entrada (ver assets/modelo-entrada.json)")
    ap.add_argument("--saida", help="arquivo .md de saída (padrão: stdout)")
    args = ap.parse_args(argv)
    with open(args.entrada, encoding="utf-8") as fh:
        entrada = json.load(fh)
    texto = gerar(entrada)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"Relatório gravado em {args.saida}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

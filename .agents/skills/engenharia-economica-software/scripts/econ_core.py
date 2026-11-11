"""econ_core - funções determinísticas de Engenharia Econômica para projetos de software.

Somente biblioteca padrão do Python (3.9+). Nenhum cálculo financeiro deve ser feito "de
cabeça" pelo LLM: todas as fórmulas das Aulas 1 a 12 vivem aqui e são cobertas por testes.

Convenções
----------
* Taxas em decimal (0.18 = 18 %) e sempre na MESMA base de tempo dos fluxos
  (taxa anual para fluxos anuais, taxa mensal para fluxos mensais).
* Fluxos: lista onde o índice é o período; índice 0 = hoje (investimento inicial).
* Saídas de caixa negativas, entradas positivas.
* Siglas em português: VP = valor presente, VF = valor futuro, VPL, TIR, TMA,
  GVA = EVM (Valor Planejado = PV, Valor Agregado = EV, Custo Real = AC),
  IDC = CPI, IDP = SPI.  Para evitar confusão com "VP = valor presente", as funções
  de GVA usam os nomes ``planejado``, ``agregado`` e ``real``.
"""
from __future__ import annotations

import copy
import math
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Sequence

Numero = float
Fluxo = Sequence[float]


# --------------------------------------------------------------------------- #
# Aulas 3 e 5 - Valor do dinheiro no tempo (TVM) e fluxo de caixa
# --------------------------------------------------------------------------- #
def valor_futuro(vp: float, taxa: float, n: float) -> float:
    """VF = VP * (1 + i)^n  (pagamento único)."""
    return vp * (1.0 + taxa) ** n


def valor_presente(vf: float, taxa: float, n: float) -> float:
    """VP = VF / (1 + i)^n  (pagamento único)."""
    return vf / (1.0 + taxa) ** n


def vp_serie_uniforme(pmt: float, taxa: float, n: int) -> float:
    """VP de uma série uniforme postecipada: PMT * [1 - (1+i)^-n] / i."""
    if n < 0:
        raise ValueError("n deve ser >= 0")
    if taxa == 0:
        return pmt * n
    return pmt * (1.0 - (1.0 + taxa) ** -n) / taxa


def vf_serie_uniforme(pmt: float, taxa: float, n: int) -> float:
    """VF de uma série uniforme postecipada: PMT * [(1+i)^n - 1] / i."""
    if taxa == 0:
        return pmt * n
    return pmt * ((1.0 + taxa) ** n - 1.0) / taxa


def pmt_de_vp(vp: float, taxa: float, n: int) -> float:
    """Parcela uniforme equivalente a um VP: VP * i / [1 - (1+i)^-n]."""
    if n <= 0:
        raise ValueError("n deve ser > 0")
    if taxa == 0:
        return vp / n
    return vp * taxa / (1.0 - (1.0 + taxa) ** -n)


def taxa_equivalente(taxa: float, duracao_origem: float, duracao_destino: float) -> float:
    """Converte taxa composta entre bases: i_destino = (1+i)^(duracao_destino/duracao_origem) - 1.

    As durações usam a mesma unidade. Ex.: anual -> mensal: origem=12 (meses),
    destino=1 (mês) => (1+i)^(1/12) - 1.  Mensal -> anual: origem=1, destino=12.
    """
    return (1.0 + taxa) ** (duracao_destino / duracao_origem) - 1.0


def vpl(taxa: float, fluxos: Fluxo) -> float:
    """VPL = sum_{t=0..n} FC_t / (1 + TMA)^t."""
    return sum(f / (1.0 + taxa) ** t for t, f in enumerate(fluxos))


def _raizes_vpl(fluxos: Fluxo, minimo: float = -0.99, maximo: float = 10.0, passos: int = 4000) -> List[float]:
    """Todas as raízes de VPL(i)=0 em [minimo, maximo] (varredura + bisseção)."""
    if not (any(f > 0 for f in fluxos) and any(f < 0 for f in fluxos)):
        return []
    raizes: List[float] = []
    passo = (maximo - minimo) / passos
    a = minimo
    fa = vpl(a, fluxos)
    for k in range(1, passos + 1):
        b = minimo + passo * k
        fb = vpl(b, fluxos)
        if fa == 0.0:
            raizes.append(a)
        elif fa * fb < 0:
            lo, hi, flo = a, b, fa
            for _ in range(200):
                mid = (lo + hi) / 2.0
                fmid = vpl(mid, fluxos)
                if flo * fmid <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fmid
            raizes.append((lo + hi) / 2.0)
        a, fa = b, fb
    if fa == 0.0:
        raizes.append(a)
    # remove duplicatas muito próximas
    unicas: List[float] = []
    for r in raizes:
        if not unicas or abs(r - unicas[-1]) > 1e-9:
            unicas.append(r)
    return unicas


def tir_todas(fluxos: Fluxo) -> List[float]:
    """Todas as TIR reais encontradas (fluxos não convencionais podem ter várias)."""
    return _raizes_vpl(fluxos)


def tir(fluxos: Fluxo) -> Optional[float]:
    """TIR: taxa que zera o VPL. ``None`` se não existir (ex.: fluxo sem troca de sinal).

    Havendo várias raízes devolve a mais próxima de zero e o chamador deve consultar
    :func:`tir_todas`; nesses casos prefira a TIRM (:func:`tirm`).
    """
    raizes = _raizes_vpl(fluxos)
    if not raizes:
        return None
    return min(raizes, key=abs)


def tirm(fluxos: Fluxo, taxa_financiamento: float, taxa_reinvestimento: float) -> Optional[float]:
    """TIR modificada: (VF das entradas na taxa de reinvestimento / |VP das saídas|)^(1/n) - 1."""
    n = len(fluxos) - 1
    if n <= 0:
        return None
    vf_entradas = sum(f * (1.0 + taxa_reinvestimento) ** (n - t) for t, f in enumerate(fluxos) if f > 0)
    vp_saidas = sum(-f / (1.0 + taxa_financiamento) ** t for t, f in enumerate(fluxos) if f < 0)
    if vf_entradas <= 0 or vp_saidas <= 0:
        return None
    return (vf_entradas / vp_saidas) ** (1.0 / n) - 1.0


def payback(fluxos: Fluxo, taxa: Optional[float] = None) -> Optional[float]:
    """Payback em períodos, com interpolação linear dentro do período de virada.

    Sem ``taxa``  -> payback simples.  Com ``taxa`` (TMA) -> payback descontado.
    Devolve ``None`` se o investimento não é recuperado no horizonte.
    """
    acumulado = 0.0
    for t, f in enumerate(fluxos):
        valor = f / (1.0 + taxa) ** t if taxa is not None else f
        anterior = acumulado
        acumulado += valor
        if acumulado >= 0 and (t == 0 or anterior < 0):
            if t == 0:
                return 0.0
            return (t - 1) + (-anterior) / valor
    return None


def indice_lucratividade(taxa: float, fluxos: Fluxo) -> Optional[float]:
    """IL = VP das entradas / VP das saídas (> 1 => cria valor)."""
    entradas = sum(f / (1.0 + taxa) ** t for t, f in enumerate(fluxos) if f > 0)
    saidas = sum(-f / (1.0 + taxa) ** t for t, f in enumerate(fluxos) if f < 0)
    return entradas / saidas if saidas > 0 else None


def roi_simples(fluxos: Fluxo) -> Optional[float]:
    """ROI nominal = (soma das entradas - soma das saídas) / soma das saídas."""
    saidas = -sum(f for f in fluxos if f < 0)
    entradas = sum(f for f in fluxos if f > 0)
    return (entradas - saidas) / saidas if saidas > 0 else None


def roi_descontado(taxa: float, fluxos: Fluxo) -> Optional[float]:
    """ROI descontado = VPL / VP das saídas."""
    saidas = sum(-f / (1.0 + taxa) ** t for t, f in enumerate(fluxos) if f < 0)
    return vpl(taxa, fluxos) / saidas if saidas > 0 else None


def caue(valor_presente_liquido: float, taxa: float, n: int) -> float:
    """Custo/Benefício Anual Uniforme Equivalente = VPL * i / [1 - (1+i)^-n]."""
    return pmt_de_vp(valor_presente_liquido, taxa, n)


# --------------------------------------------------------------------------- #
# Aulas 1, 2, 10 e 11 - Alternativas, substituição de legado
# --------------------------------------------------------------------------- #
def comparar_alternativas(taxa: float, alternativas: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Compara alternativas mutuamente exclusivas pelo CAUE (vidas diferentes são normalizadas).

    Cada alternativa: ``nome``, ``investimento``, ``custo_anual`` (número ou lista com um
    valor por ano), ``vida`` (anos), ``valor_residual`` (opcional), ``beneficio_anual``
    (opcional, número). O menor CAUE de custos (ou maior CAUE líquido, se houver
    benefício) é a melhor opção econômica.
    """
    resultado = []
    for alt in alternativas:
        vida = int(alt["vida"])
        custo = alt.get("custo_anual", 0.0)
        custos = list(custo) if isinstance(custo, (list, tuple)) else [custo] * vida
        if len(custos) != vida:
            raise ValueError(f"{alt['nome']}: custo_anual deve ter {vida} valores")
        beneficio = float(alt.get("beneficio_anual", 0.0))
        residual = float(alt.get("valor_residual", 0.0))
        fluxos = [-float(alt["investimento"])] + [beneficio - c for c in custos]
        fluxos[-1] += residual
        vpl_alt = vpl(taxa, fluxos)
        resultado.append({
            "nome": alt["nome"],
            "vida": vida,
            "vpl": vpl_alt,
            "caue": caue(vpl_alt, taxa, vida),
            "vp_custos": (float(alt["investimento"])
                          + sum(c / (1.0 + taxa) ** t for t, c in enumerate(custos, start=1))
                          - residual / (1.0 + taxa) ** vida),
        })
    # melhor = maior CAUE (custos entram negativos, logo o "menos negativo" vence)
    resultado.sort(key=lambda r: r["caue"], reverse=True)
    for pos, r in enumerate(resultado, start=1):
        r["ranking"] = pos
    return resultado


# --------------------------------------------------------------------------- #
# Aula 4 - Custo, preço e valor
# --------------------------------------------------------------------------- #
def custo_direto_equipe(horas: float, custo_hora: float, encargos: float = 0.0) -> float:
    """Custo direto de mão de obra = horas * custo/hora * (1 + encargos)."""
    return horas * custo_hora * (1.0 + encargos)


def rateio_indireto(custo_indireto_total: float, horas_projeto: float, horas_totais: float) -> float:
    """Rateio de custo indireto (infra/licenças) proporcional às horas do projeto."""
    if horas_totais <= 0:
        raise ValueError("horas_totais deve ser > 0")
    return custo_indireto_total * horas_projeto / horas_totais


def preco_markup(custo: float, markup: float) -> float:
    """Preço = custo * (1 + markup).  (markup sobre o custo)"""
    return custo * (1.0 + markup)


def markup_para_margem(markup: float) -> float:
    """Margem sobre o preço equivalente a um markup sobre o custo: m = k/(1+k)."""
    return markup / (1.0 + markup)


def margem_para_markup(margem: float) -> float:
    """Markup sobre o custo equivalente a uma margem sobre o preço: k = m/(1-m)."""
    if margem >= 1:
        raise ValueError("margem deve ser < 1")
    return margem / (1.0 - margem)


def preco_divisor(custo: float, impostos: float, margem: float, outros_percentuais: float = 0.0) -> float:
    """Preço pelo markup divisor: P = C / (1 - impostos - outros% - margem).  (tudo sobre o preço)"""
    divisor = 1.0 - impostos - outros_percentuais - margem
    if divisor <= 0:
        raise ValueError("soma de impostos, outros% e margem deve ser < 100 %")
    return custo / divisor


# --------------------------------------------------------------------------- #
# Aulas 6 e 8 - Métricas de produtos digitais e depreciação
# --------------------------------------------------------------------------- #
def ltv(arpa_mensal: float, margem_bruta: float, churn_mensal: float) -> float:
    """LTV = ARPA * margem bruta / churn mensal  (vida média = 1/churn meses)."""
    if churn_mensal <= 0:
        raise ValueError("churn_mensal deve ser > 0")
    return arpa_mensal * margem_bruta / churn_mensal


def ltv_cac(arpa_mensal: float, margem_bruta: float, churn_mensal: float, cac: float) -> Dict[str, float]:
    """LTV, relação LTV/CAC (meta usual >= 3) e payback do CAC em meses."""
    valor = ltv(arpa_mensal, margem_bruta, churn_mensal)
    margem_mensal = arpa_mensal * margem_bruta
    return {
        "ltv": valor,
        "cac": cac,
        "ltv_cac": valor / cac if cac > 0 else math.inf,
        "payback_cac_meses": cac / margem_mensal if margem_mensal > 0 else math.inf,
        "vida_media_meses": 1.0 / churn_mensal,
    }


def churn_anual(churn_mensal: float) -> float:
    """Churn anual composto a partir do mensal."""
    return 1.0 - (1.0 - churn_mensal) ** 12


def depreciacao_linear(valor: float, vida: int, residual: float = 0.0) -> List[float]:
    """Quota anual constante: (valor - residual) / vida."""
    if vida <= 0:
        raise ValueError("vida deve ser > 0")
    return [(valor - residual) / vida] * vida


def depreciacao_soma_digitos(valor: float, vida: int, residual: float = 0.0) -> List[float]:
    """Depreciação pela soma dos dígitos dos anos (acelerada)."""
    soma = vida * (vida + 1) / 2.0
    return [(valor - residual) * (vida - k) / soma for k in range(vida)]


def escudo_fiscal(depreciacoes: Iterable[float], aliquota_ir: float) -> List[float]:
    """Economia de imposto = depreciação * alíquota de IR/CSLL (só existe se há lucro tributável)."""
    return [d * aliquota_ir for d in depreciacoes]


def cocomo_basico(kloc: float, modo: str = "organico") -> Dict[str, float]:
    """COCOMO básico (Boehm, 1981) - referência de esforço (pessoa-mês) e prazo (meses)."""
    a, b, c, d = {"organico": (2.4, 1.05, 2.5, 0.38),
                  "semidestacado": (3.0, 1.12, 2.5, 0.35),
                  "embarcado": (3.6, 1.20, 2.5, 0.32)}[modo]
    esforco = a * kloc ** b
    return {"esforco_pessoa_mes": esforco, "prazo_meses": c * esforco ** d,
            "equipe_media": esforco / (c * esforco ** d)}


# --------------------------------------------------------------------------- #
# Aula 9 - Gerenciamento de Valor Agregado (GVA / EVM)
# --------------------------------------------------------------------------- #
def gva(planejado: float, agregado: float, real: float, bac: Optional[float] = None) -> Dict[str, Optional[float]]:
    """Indicadores do GVA para valores ACUMULADOS até a data de status.

    planejado = VP/PV, agregado = VA/EV, real = CR/AC, bac = orçamento total (BAC/ONT).
    IDC = VA/CR ; IDP = VA/VP ; VC = VA-CR ; VPz = VA-VP
    EAC = BAC/IDC (desvio persistente) ; ETC = EAC - CR ; VAC = BAC - EAC
    EAC_atipico = CR + (BAC - VA) ; EAC_idc_idp = CR + (BAC - VA)/(IDC*IDP)
    IDCP (TCPI) = (BAC - VA)/(BAC - CR)
    """
    idc = agregado / real if real else None
    idp = agregado / planejado if planejado else None
    saida: Dict[str, Optional[float]] = {
        "planejado": planejado, "agregado": agregado, "real": real,
        "idc": idc, "idp": idp,
        "variacao_custos": agregado - real,
        "variacao_prazo": agregado - planejado,
    }
    if bac is not None:
        saida["bac"] = bac
        saida["eac"] = bac / idc if idc else None
        saida["etc"] = saida["eac"] - real if saida["eac"] is not None else None
        saida["vac"] = bac - saida["eac"] if saida["eac"] is not None else None
        saida["eac_desvio_atipico"] = real + (bac - agregado)
        saida["eac_idc_idp"] = real + (bac - agregado) / (idc * idp) if idc and idp else None
        saida["idcp"] = (bac - agregado) / (bac - real) if bac != real else None
        saida["percentual_concluido"] = agregado / bac if bac else None
    return saida


def gva_por_sprint(sprints: Sequence[Dict[str, float]], bac: Optional[float] = None) -> List[Dict[str, Optional[float]]]:
    """Série de GVA acumulado. Cada sprint: ``planejado``, ``agregado``, ``real`` (valores do sprint)."""
    pv = ev = ac = 0.0
    serie = []
    for i, s in enumerate(sprints, start=1):
        pv += s["planejado"]
        ev += s["agregado"]
        ac += s["real"]
        linha = gva(pv, ev, ac, bac)
        linha["sprint"] = s.get("sprint", i)
        serie.append(linha)
    return serie


# --------------------------------------------------------------------------- #
# Aulas 10 a 12 - Priorização econômica e "bom o suficiente"
# --------------------------------------------------------------------------- #
def priorizar(itens: Sequence[Dict[str, Any]], metodo: str = "valor_esforco") -> List[Dict[str, Any]]:
    """Ordena o backlog por critério econômico.

    metodo="valor_esforco": score = valor / esforco  (itens: nome, valor, esforco)
    metodo="wsjf": score = (valor_negocio + criticidade_tempo + reducao_risco) / tamanho
    Também classifica em quadrantes pela mediana: quick_win, projeto_estrategico,
    preenchimento, evitar.
    """
    if not itens:
        return []
    linhas = []
    for it in itens:
        if metodo == "wsjf":
            custo_atraso = it["valor_negocio"] + it["criticidade_tempo"] + it["reducao_risco"]
            score = custo_atraso / it["tamanho"]
            valor, esforco = custo_atraso, it["tamanho"]
        elif metodo == "valor_esforco":
            valor, esforco = it["valor"], it["esforco"]
            score = valor / esforco
        else:
            raise ValueError("metodo deve ser 'valor_esforco' ou 'wsjf'")
        linhas.append({**it, "valor_total": valor, "esforco_total": esforco, "score": score})
    mv = median(l["valor_total"] for l in linhas)
    me = median(l["esforco_total"] for l in linhas)
    for l in linhas:
        alto_valor = l["valor_total"] >= mv
        baixo_esforco = l["esforco_total"] <= me
        l["quadrante"] = ("quick_win" if alto_valor and baixo_esforco else
                          "projeto_estrategico" if alto_valor else
                          "preenchimento" if baixo_esforco else "evitar")
    linhas.sort(key=lambda l: l["score"], reverse=True)
    for pos, l in enumerate(linhas, start=1):
        l["ranking"] = pos
    return linhas


def bom_o_suficiente(niveis: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Análise marginal para o princípio "bom o suficiente".

    ``niveis`` em ordem crescente de qualidade, com ``nome``, ``custo`` e ``beneficio``
    ACUMULADOS. Recomenda parar no último nível cujo benefício marginal ainda cobre o
    custo marginal (regra: Δbenefício >= Δcusto) e também informa o nível de maior
    benefício líquido.
    """
    anterior_c = anterior_b = 0.0
    linhas = []
    parar_em: Optional[str] = None
    quebrou = False
    for n in niveis:
        dc = n["custo"] - anterior_c
        db = n["beneficio"] - anterior_b
        compensa = db >= dc
        if not compensa:
            quebrou = True
        elif not quebrou:
            parar_em = n["nome"]
        linhas.append({**n, "custo_marginal": dc, "beneficio_marginal": db,
                       "liquido": n["beneficio"] - n["custo"], "compensa": compensa})
        anterior_c, anterior_b = n["custo"], n["beneficio"]
    melhor = max(linhas, key=lambda l: l["liquido"])
    return {"niveis": linhas, "recomendado_regra_marginal": parar_em,
            "maior_liquido": melhor["nome"]}


# --------------------------------------------------------------------------- #
# Modelo de negócio -> fluxo de caixa (Aulas 3, 4, 5, 6, 7, 8)
# --------------------------------------------------------------------------- #
def mesclar(base: Dict[str, Any], sobre: Dict[str, Any]) -> Dict[str, Any]:
    """Merge profundo de dicionários (listas e escalares são substituídos)."""
    novo = copy.deepcopy(base)
    for k, v in sobre.items():
        if isinstance(v, dict) and isinstance(novo.get(k), dict):
            novo[k] = mesclar(novo[k], v)
        else:
            novo[k] = copy.deepcopy(v)
    return novo


def _valor_ano(v: Any, ano: int, padrao: float = 0.0) -> float:
    """Aceita escalar (igual todos os anos) ou lista indexada por ano-1."""
    if isinstance(v, (list, tuple)):
        return float(v[ano - 1]) if ano - 1 < len(v) else float(v[-1])
    return float(v) if v is not None else padrao


def construir_fluxo(modelo: Dict[str, Any]) -> Dict[str, Any]:
    """Gera DRE simplificada e fluxo de caixa anual (ano 0 = investimento) a partir de um modelo.

    Campos do modelo (ver references/formato-entrada.md):
      horizonte_anos, tma, ajustes{fator_clientes,fator_preco,fator_custos,fator_capex},
      investimento{itens:{nome:valor}, vida_util_anos, valor_residual},
      receita{preco_mensal, reajuste_anual, clientes_fim_ano[], churn_mensal},
      custos{variavel_pct_receita, variavel_por_cliente_mes, fixos_anuais{nome:valor|lista},
             cac},
      tributos{sobre_receita, ir_csll, limite_compensacao_prejuizo}
    """
    n = int(modelo["horizonte_anos"])
    aj = {"fator_clientes": 1.0, "fator_preco": 1.0, "fator_custos": 1.0, "fator_capex": 1.0}
    aj.update(modelo.get("ajustes", {}))
    inv = modelo["investimento"]
    capex0 = sum(inv["itens"].values()) * aj["fator_capex"]
    vida = int(inv.get("vida_util_anos", n))
    residual = float(inv.get("valor_residual", 0.0))
    rec = modelo["receita"]
    cus = modelo["custos"]
    trib = modelo.get("tributos", {})
    aliq_rec = float(trib.get("sobre_receita", 0.0))
    aliq_ir = float(trib.get("ir_csll", 0.0))
    lim_comp = float(trib.get("limite_compensacao_prejuizo", 1.0))
    churn_m = float(rec.get("churn_mensal", 0.0))
    ch_a = churn_anual(churn_m)

    depre_anual = depreciacao_linear(capex0, vida, 0.0)
    linhas: List[Dict[str, Any]] = []
    clientes_ini = 0.0
    saldo_prejuizo = 0.0
    for ano in range(1, n + 1):
        clientes_fim = _valor_ano(rec["clientes_fim_ano"], ano) * aj["fator_clientes"]
        clientes_medio = (clientes_ini + clientes_fim) / 2.0
        novos = max(0.0, clientes_fim - clientes_ini) + clientes_ini * ch_a
        preco = float(rec["preco_mensal"]) * aj["fator_preco"] * (1.0 + float(rec.get("reajuste_anual", 0.0))) ** (ano - 1)
        receita = clientes_medio * preco * 12.0
        impostos_rec = receita * aliq_rec
        var = (receita * float(cus.get("variavel_pct_receita", 0.0))
               + clientes_medio * float(cus.get("variavel_por_cliente_mes", 0.0)) * 12.0) * aj["fator_custos"]
        fixos = sum(_valor_ano(v, ano) for v in cus.get("fixos_anuais", {}).values()) * aj["fator_custos"]
        aquisicao = novos * float(cus.get("cac", 0.0)) * aj["fator_custos"]
        ebitda = receita - impostos_rec - var - fixos - aquisicao
        deprec = depre_anual[ano - 1] if ano <= vida else 0.0
        ebit = ebitda - deprec
        # compensação de prejuízos fiscais (limite % do lucro tributável)
        if ebit < 0:
            saldo_prejuizo += -ebit
            tributavel = 0.0
        else:
            compensavel = min(saldo_prejuizo, ebit * lim_comp)
            saldo_prejuizo -= compensavel
            tributavel = ebit - compensavel
        ir = tributavel * aliq_ir
        fluxo_op = ebitda - ir
        vr = residual if ano == n else 0.0
        linhas.append({
            "ano": ano, "clientes_fim": clientes_fim, "clientes_medio": clientes_medio,
            "clientes_novos": novos, "preco_mensal": preco, "receita": receita,
            "impostos_receita": impostos_rec, "custos_variaveis": var, "custos_fixos": fixos,
            "aquisicao_clientes": aquisicao, "ebitda": ebitda, "depreciacao": deprec,
            "ebit": ebit, "ir_csll": ir, "fluxo_operacional": fluxo_op,
            "valor_residual": vr, "fluxo_liquido": fluxo_op + vr,
        })
        clientes_ini = clientes_fim
    fluxo = [-capex0] + [l["fluxo_liquido"] for l in linhas]
    return {"capex": capex0, "linhas": linhas, "fluxo": fluxo, "tma": float(modelo["tma"])}


def indicadores(modelo: Dict[str, Any]) -> Dict[str, Any]:
    """VPL, TIR, TIRM, payback simples/descontado, IL e ROI do modelo."""
    f = construir_fluxo(modelo)
    fluxo, tma = f["fluxo"], f["tma"]
    return {
        "fluxo": fluxo, "tma": tma,
        "vpl": vpl(tma, fluxo),
        "tir": tir(fluxo),
        "tirm": tirm(fluxo, tma, tma),
        "payback_simples": payback(fluxo),
        "payback_descontado": payback(fluxo, tma),
        "indice_lucratividade": indice_lucratividade(tma, fluxo),
        "roi_simples": roi_simples(fluxo),
        "roi_descontado": roi_descontado(tma, fluxo),
        "detalhe": f,
    }


def sensibilidade(modelo: Dict[str, Any], variacao: float = 0.20) -> List[Dict[str, Any]]:
    """Análise tornado: efeito de ±variação em cada fator sobre o VPL (ordenado por impacto)."""
    base = indicadores(modelo)["vpl"]
    saidas = []
    for fator in ("fator_clientes", "fator_preco", "fator_custos", "fator_capex"):
        atual = modelo.get("ajustes", {}).get(fator, 1.0)
        v = {}
        for rotulo, mult in (("menos", 1 - variacao), ("mais", 1 + variacao)):
            m = mesclar(modelo, {"ajustes": {fator: atual * mult}})
            v[rotulo] = indicadores(m)["vpl"]
        saidas.append({"fator": fator, "vpl_menos": v["menos"], "vpl_mais": v["mais"],
                       "amplitude": abs(v["mais"] - v["menos"]), "vpl_base": base})
    for rotulo, delta in (("tma", variacao),):
        m_menos = mesclar(modelo, {"tma": modelo["tma"] * (1 - delta)})
        m_mais = mesclar(modelo, {"tma": modelo["tma"] * (1 + delta)})
        a, b = indicadores(m_menos)["vpl"], indicadores(m_mais)["vpl"]
        saidas.append({"fator": rotulo, "vpl_menos": a, "vpl_mais": b,
                       "amplitude": abs(a - b), "vpl_base": base})
    saidas.sort(key=lambda s: s["amplitude"], reverse=True)
    return saidas


def cenarios(modelo: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Avalia o caso-base e cada cenário em ``modelo['cenarios']`` (overrides por merge profundo)."""
    resultado = []
    todos = {"base": {}}
    todos.update(modelo.get("cenarios", {}))
    for nome, override in todos.items():
        ind = indicadores(mesclar(modelo, override))
        resultado.append({"cenario": nome, "vpl": ind["vpl"], "tir": ind["tir"],
                          "payback_simples": ind["payback_simples"],
                          "payback_descontado": ind["payback_descontado"]})
    return resultado


def metricas_saas(modelo: Dict[str, Any]) -> Dict[str, float]:
    """ARPA, margem bruta unitária, LTV, CAC, LTV/CAC e payback do CAC do modelo."""
    rec, cus = modelo["receita"], modelo["custos"]
    arpa = float(rec["preco_mensal"]) * modelo.get("ajustes", {}).get("fator_preco", 1.0)
    aliq = float(modelo.get("tributos", {}).get("sobre_receita", 0.0))
    custo_var = arpa * float(cus.get("variavel_pct_receita", 0.0)) + float(cus.get("variavel_por_cliente_mes", 0.0))
    margem = (arpa - arpa * aliq - custo_var) / arpa
    out = ltv_cac(arpa, margem, float(rec["churn_mensal"]), float(cus.get("cac", 0.0)))
    out.update({"arpa_mensal": arpa, "margem_bruta_unitaria": margem})
    return out


def fator_equilibrio(modelo: Dict[str, Any], fator: str = "fator_clientes",
                     minimo: float = 0.05, maximo: float = 10.0) -> Optional[float]:
    """Valor do ``fator`` de ajuste (multiplicador) que leva o VPL a zero (bisseção).

    Ex.: ``fator_clientes = 1.3`` => é preciso 30 % mais clientes que o caso-base para
    o VPL empatar. ``None`` se o VPL não troca de sinal no intervalo.
    """
    def f(x: float) -> float:
        return indicadores(mesclar(modelo, {"ajustes": {fator: x}}))["vpl"]

    lo, hi = minimo, maximo
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if flo * fhi > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2.0
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2.0

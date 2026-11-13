#!/usr/bin/env python3
"""Gera docs/apresentacao-workshop.pdf (slides 16:9) com os números do motor da skill.

Requer reportlab (apenas para gerar o PDF; a skill em si não tem dependências):
    python -m pip install reportlab
    python docs/gerar_apresentacao.py
"""
import json
import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, ".agents", "skills", "engenharia-economica-software", "scripts"))
import econ_core as ec  # noqa: E402
import gerar_relatorio as gr  # noqa: E402

from reportlab.lib.colors import HexColor, white  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

W, H = 1280, 720
NAVY, TEAL, AMBER = HexColor("#0F2A43"), HexColor("#0E9F8E"), HexColor("#E8A317")
RED, INK, MUTED = HexColor("#C0392B"), HexColor("#1D2B3A"), HexColor("#5B6B7B")
LIGHT, LINE = HexColor("#EEF3F7"), HexColor("#D5DEE6")

EQUIPE = ["Thiago Matheus Honório Ribeiro Pinheiro", "Gubio Garcia", "Luiz Fernando"]

# --- fontes (Segoe UI se existir; senão Helvetica) ---------------------------------
FONT, BOLD = "Helvetica", "Helvetica-Bold"
try:
    pdfmetrics.registerFont(TTFont("Seg", r"C:\Windows\Fonts\segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("SegB", r"C:\Windows\Fonts\segoeuib.ttf"))
    FONT, BOLD = "Seg", "SegB"
except Exception:
    pass
UNICODE_OK = FONT == "Seg"


def t(s: str) -> str:
    """Troca símbolos que a fonte de reserva não tem."""
    if UNICODE_OK:
        return s
    return (s.replace("→", "->").replace("≥", ">=").replace("≤", "<=").replace("−", "-")
             .replace("Σ", "soma").replace("×", "x").replace("÷", "/").replace("✓", "OK")
             .replace("•", "-").replace("Δ", "D").replace("ᵗ", "^t").replace("₀", "0"))


class Deck:
    def __init__(self, caminho):
        self.c = canvas.Canvas(caminho, pagesize=(W, H))
        self.c.setTitle("Engenharia Econômica Agêntica, Mini Workshop")
        self.c.setAuthor(", ".join(EQUIPE))
        self.n = 0

    # primitivas
    def texto(self, x, y, s, size=22, cor=INK, fonte=None, anchor="l"):
        self.c.setFillColor(cor)
        self.c.setFont(fonte or FONT, size)
        s = t(s)
        {"l": self.c.drawString, "c": self.c.drawCentredString, "r": self.c.drawRightString}[anchor](x, y, s)

    def quebra(self, s, largura, size, fonte=None):
        palavras, linhas, atual = t(s).split(), [], ""
        f = fonte or FONT
        for p in palavras:
            teste = (atual + " " + p).strip()
            if pdfmetrics.stringWidth(teste, f, size) <= largura:
                atual = teste
            else:
                linhas.append(atual)
                atual = p
        if atual:
            linhas.append(atual)
        return linhas

    def paragrafo(self, x, y, s, largura, size=22, cor=INK, fonte=None, espaco=1.35):
        for linha in self.quebra(s, largura, size, fonte):
            self.texto(x, y, linha, size, cor, fonte)
            y -= size * espaco
        return y

    def bullets(self, x, y, itens, largura=1000, size=24, gap=14):
        for it in itens:
            self.c.setFillColor(TEAL)
            self.c.circle(x + 6, y + size * 0.32, 5, fill=1, stroke=0)
            y = self.paragrafo(x + 28, y, it, largura - 28, size) - gap
        return y

    def rect(self, x, y, w, h, cor, raio=12, stroke=None):
        self.c.setFillColor(cor)
        if stroke:
            self.c.setStrokeColor(stroke)
        self.c.roundRect(x, y, w, h, raio, fill=1, stroke=1 if stroke else 0)

    def slide(self, titulo, sub=None):
        if self.n:
            self.c.showPage()
        self.n += 1
        self.c.setFillColor(white)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)
        self.c.setFillColor(NAVY)
        self.c.rect(0, H - 110, W, 110, fill=1, stroke=0)
        self.c.setFillColor(TEAL)
        self.c.rect(0, H - 114, W, 4, fill=1, stroke=0)
        self.texto(60, H - 68, titulo, 38, white, BOLD)
        if sub:
            self.texto(60, H - 98, sub, 18, HexColor("#9FC6D9"))
        self.texto(W - 60, 28, f"{self.n}", 14, MUTED, anchor="r")
        self.texto(60, 28, "Engenharia Econômica Agêntica · Faculdade SENAI FATESG", 14, MUTED)

    def card(self, x, y, w, h, titulo, valor, cor=TEAL, nota=None):
        self.rect(x, y, w, h, LIGHT)
        self.rect(x, y, 8, h, cor, raio=4)
        self.texto(x + 28, y + h - 36, titulo, 17, MUTED)
        self.texto(x + 28, y + h - 86, valor, 38, INK, BOLD)
        if nota:
            self.texto(x + 28, y + 22, nota, 15, MUTED)

    def tabela(self, x, y, colw, cab, linhas, size=17, rh=38):
        self.rect(x, y - rh + 6, sum(colw), rh, NAVY, raio=6)
        cx = x
        for w, h in zip(colw, cab):
            self.texto(cx + 12, y - rh + 18, h, size, white, BOLD)
            cx += w
        y -= rh
        for i, lin in enumerate(linhas):
            if i % 2 == 0:
                self.rect(x, y - rh + 6, sum(colw), rh, LIGHT, raio=0)
            cx = x
            for w, cel in zip(colw, lin):
                negrito = cel.startswith("**")
                self.texto(cx + 12, y - rh + 18, cel.strip("*"), size, INK, BOLD if negrito else FONT)
                cx += w
            y -= rh
        return y

    def barras(self, x, y, w, h, rotulos, valores, titulo, fmt, cor_pos=TEAL, cor_neg=RED):
        self.texto(x, y + h + 14, titulo, 18, INK, BOLD)
        vmax = max(max(valores), 0)
        vmin = min(min(valores), 0)
        esc = (h - 30) / ((vmax - vmin) or 1)
        base = y - vmin * esc
        n = len(valores)
        bw = w / n * 0.62
        self.c.setStrokeColor(LINE)
        self.c.line(x, base, x + w, base)
        for i, (r, v) in enumerate(zip(rotulos, valores)):
            bx = x + (i + 0.5) * w / n - bw / 2
            self.c.setFillColor(cor_pos if v >= 0 else cor_neg)
            alt = v * esc
            self.c.rect(bx, base if v >= 0 else base + alt, bw, abs(alt), fill=1, stroke=0)
            self.texto(bx + bw / 2, (base + alt + 6) if v >= 0 else (base + alt - 18), fmt(v), 14, INK, anchor="c")
            self.texto(bx + bw / 2, y - 46, r, 14, MUTED, anchor="c")

    def linhas(self, x, y, w, h, series, titulo, ref=None):
        """series: [(rotulo, cor, valores)] ; ref: valor de referência (linha tracejada)."""
        self.texto(x, y + h + 14, titulo, 18, INK, BOLD)
        todos = [v for _, _, vs in series for v in vs] + ([ref] if ref is not None else [])
        vmin, vmax = min(todos) * 0.95, max(todos) * 1.05
        n = len(series[0][2])
        px = lambda i: x + i * w / (n - 1)
        py = lambda v: y + (v - vmin) / ((vmax - vmin) or 1) * h
        self.c.setStrokeColor(LINE)
        self.c.rect(x, y, w, h, fill=0, stroke=1)
        if ref is not None:
            self.c.setDash(6, 4)
            self.c.setStrokeColor(MUTED)
            self.c.line(x, py(ref), x + w, py(ref))
            self.c.setDash()
            self.texto(x + w + 8, py(ref) - 5, f"{ref:g}", 14, MUTED)
        for rot, cor, vs in series:
            self.c.setStrokeColor(cor)
            self.c.setLineWidth(3)
            p = self.c.beginPath()
            p.moveTo(px(0), py(vs[0]))
            for i, v in enumerate(vs[1:], start=1):
                p.lineTo(px(i), py(v))
            self.c.drawPath(p, stroke=1, fill=0)
            self.c.setLineWidth(1)
        lx = x
        for rot, cor, _ in series:
            self.c.setFillColor(cor)
            self.c.rect(lx, y - 40, 22, 6, fill=1, stroke=0)
            self.texto(lx + 30, y - 44, rot, 15, INK)
            lx += 170
        for i in range(n):
            self.texto(px(i), y - 20, str(i + 1), 12, MUTED, anchor="c")

    def salvar(self):
        self.c.save()


def main():
    with open(os.path.join(RAIZ, "examples", "tcc-input.json"), encoding="utf-8") as fh:
        entrada = json.load(fh)
    entrada = gr.normalizar(entrada)
    hist = entrada.get("historico")
    modelo = gr.preparar_modelo(entrada)
    ind = ec.indicadores(modelo)
    det = ind["detalhe"]
    cd = gr.custos_desenvolvimento(entrada)
    saas = ec.metricas_saas(modelo)
    cen = {c["cenario"]: c for c in ec.cenarios(modelo)}
    sens = ec.sensibilidade(modelo)
    f_eq = ec.fator_equilibrio(modelo)
    gva = entrada["gva_sprints"]
    serie = ec.gva_por_sprint(gva["sprints"], gva["bac"])
    alt = ec.comparar_alternativas(ind["tma"], entrada["alternativas_infraestrutura"]["alternativas"])
    wsjf = ec.priorizar(entrada["backlog_roadmap"], "wsjf")
    bs = ec.bom_o_suficiente(entrada["qualidade_bom_o_suficiente"]["niveis"])
    m = entrada["projeto"]["metricas_medidas_no_repositorio"]
    kloc = (m["java_main_linhas"] + m["java_teste_linhas"] + m["frontend_ts_tsx_linhas"]) / 1000
    brl, pct, num = gr.brl, gr.pct, gr.num

    d = Deck(os.path.join(RAIZ, "docs", "apresentacao-workshop.pdf"))

    # 1 capa
    d.n = 1
    d.c.setFillColor(NAVY)
    d.c.rect(0, 0, W, H, fill=1, stroke=0)
    d.c.setFillColor(TEAL)
    d.c.rect(0, 0, 18, H, fill=1, stroke=0)
    d.texto(90, 560, "SITUAÇÃO DE APRENDIZAGEM · ENGENHARIA ECONÔMICA", 18, HexColor("#9FC6D9"))
    d.paragrafo(90, 500, "Engenharia Econômica Agêntica", 1100, 62, white, BOLD, 1.1)
    d.paragrafo(90, 430, "Valoração e viabilidade de projetos de software com Agent Skills", 1100, 34, HexColor("#CFE6F0"))
    d.texto(90, 300, "Estudo de caso: Plataforma de Governança de Projetos de Software (TCC)", 22, AMBER)
    y = 230
    for nome in EQUIPE:
        d.texto(90, y, nome, 24, white, BOLD)
        y -= 36
    d.texto(90, 90, "Faculdade SENAI FATESG · Bacharelado em Engenharia de Software · Mini Workshop, 24/11/2026", 17, HexColor("#9FC6D9"))
    d.texto(90, 62, "Docente: Msc. Ujeverson Tavares Sampaio", 17, HexColor("#9FC6D9"))

    # 2 desafio
    d.slide("O desafio", "Decisões de engenharia são decisões econômicas")
    d.bullets(60, 570, [
        "Software excelente tecnicamente, mas sem viabilidade financeira, é insustentável.",
        "Missão: criar uma Skill de IA que calcule, projete e defenda o valor econômico de um projeto de software.",
        "Aplicar a skill aos dados do nosso próprio TCC: fluxo de caixa, VPL, TIR, payback, GVA e modelo de negócio.",
        "Entregas: repositório público no GitHub, README, relatório do TCC e este workshop ao vivo.",
    ], 1150)
    d.card(60, 150, 360, 160, "Prompt solto", "frágil", RED, "retrabalho, resultado diferente a cada vez")
    d.card(460, 150, 360, 160, "Skill", "repetível", TEAL, "modular, versionável, testável")
    d.card(860, 150, 360, 160, "Cálculo", "determinístico", AMBER, "scripts Python, nada de conta de cabeça")

    # 3 arquitetura
    d.slide("Arquitetura da skill", "Padrão aberto Agent Skills · divulgação progressiva em 3 camadas")
    camadas = [("Camada 1 · Catálogo", "~100 tokens", "name + description (YAML) carregados na abertura da sessão", TEAL),
               ("Camada 2 · Instruções", "< 5.000 tokens", "Corpo do SKILL.md lido só quando o pedido combina com a descrição", AMBER),
               ("Camada 3 · Recursos", "sob demanda", "references/*.md (teoria por aula) e scripts/*.py (cálculo) só quando o fluxo exige", NAVY)]
    y = 590
    for tit, tam, desc, cor in camadas:
        d.rect(60, y - 120, 1160, 120, LIGHT)
        d.rect(60, y - 120, 14, 120, cor, raio=4)
        d.texto(100, y - 40, tit, 26, INK, BOLD)
        d.texto(1190, y - 40, tam, 22, cor, BOLD, "r")
        d.paragrafo(100, y - 78, desc, 1050, 20, MUTED)
        y -= 150
    d.texto(60, 110, "Instalação no Claude Code: python instalar.py --destino claude-projeto  (ou .agents/skills/ no padrão genérico)", 17, MUTED)

    # 4 estrutura
    d.slide("O que tem no repositório", "skill + prova de que funciona")
    d.tabela(60, 590, [420, 740], ["Pasta / arquivo", "Papel"], [
        [".agents/skills/engenharia-economica-software/", "Skill canônica: SKILL.md, scripts/, references/, assets/"],
        ["scripts/econ_core.py", "Fórmulas das aulas 1–12 (somente biblioteca padrão)"],
        ["scripts/econ_cli.py", "18 comandos: vpl, tir, payback, gva, markup, equilibrio..."],
        ["scripts/gerar_relatorio.py", "Relatório Markdown completo a partir de um JSON"],
        ["references/ (9 arquivos)", "Teoria e critérios de decisão, um tema por arquivo"],
        ["examples/", "tcc-input.json e tcc-valuation-report.md (valoração do TCC)"],
        ["evals/ · tests/", "10 evals e 65 testes (fórmulas, CLI, estrutura, relatório)"],
    ], 17, 46)

    # 5 aulas
    d.slide("Cobertura das Aulas 1 a 12", "Cada aula vira função testada e critério de decisão")
    d.tabela(60, 590, [190, 460, 510], ["Aulas", "Tópico", "O que a skill calcula"], [
        ["1 e 2", "Decisão e alternativas", "Alternativas incl. \"não fazer\"; CAUE"],
        ["3 e 5", "TVM e fluxo de caixa", "VP, VF, séries, TMA, CapEx/OpEx"],
        ["4", "Custo, preço e valor", "Custo direto/indireto, markup e markup divisor"],
        ["6 e 8", "Viabilidade, tributos, depreciação", "VPL, TIR, payback, CAC, LTV, IR/CSLL"],
        ["7", "Proposta econômica", "Sumário executivo, cenários, equilíbrio, riscos"],
        ["9", "GVA / EVM", "IDC, IDP, EAC, ETC, VAC, IDCP por sprint"],
        ["10 a 12", "Estratégia e priorização", "Legado, bom o suficiente, valor×esforço, WSJF"],
    ], 18, 50)

    # 6 confiabilidade
    d.slide("Por que dá para confiar nos números", "O LLM orquestra; o Python calcula")
    d.card(60, 440, 360, 150, "Testes automatizados", "61", TEAL, "fórmulas conferidas à mão")
    d.card(460, 440, 360, 150, "Evals", "10", AMBER, "7 numéricos reexecutados no teste")
    d.card(860, 440, 360, 150, "Dependências", "0", NAVY, "só biblioteca padrão do Python")
    d.bullets(60, 370, [
        "Teste de fumaça independente: um agente novo, só com o SKILL.md, calculou VPL, GVA e o relatório do TCC.",
        "A skill recusa manipular premissas para \"dar positivo\" e mostra equilíbrio e sensibilidade.",
        "CI no GitHub regenera o relatório e compara byte a byte com o versionado.",
    ], 1160, 22)

    # 7 TCC
    d.slide("O TCC avaliado", "Plataforma de Governança de Projetos de Software")
    d.bullets(60, 555, [
        f"SaaS B2B para discovery e elicitação de requisitos: projetos, requisitos, rastreabilidade, modelagem de dados, auditoria e pesquisa.",
        f"Tamanho medido no repositório: {num(kloc, 1)} mil linhas (Java e TypeScript), {m['testes_backend_readme']} testes de backend, {m['testes_ui_e2e_readme']} de interface.",
        "Stack: Java 21 + Spring Boot 4, React 19, Keycloak, PostgreSQL 15, Docker. Hospedagem: VM Oracle Always Free.",
        f"Equipe de 3 pessoas, {len(gva['sprints'])} janelas de 2 semanas ({hist['periodo']['inicio'][8:]}/{hist['periodo']['inicio'][5:7]} a {hist['periodo']['fim'][8:]}/{hist['periodo']['fim'][5:7]}/2026), sprints planejadas com o orientador, ferramentas gratuitas e pouco Claude pago.",
    ], 1160, 22)
    d.rect(60, 120, 1160, 110, HexColor("#FFF6E0"), stroke=AMBER)
    d.paragrafo(90, 195, f"Medido: tamanho do código e histórico real do GitHub ({hist['commits']} commits, {hist['prs_entregues']} PRs de entrega, {num(hist['horas_medidas'], 1)} h). Estimado, com fonte: horas totais (cobertura de {hist['parametros']['cobertura'] * 100:.0f}%), custo por hora, preço, clientes, churn e TMA.", 1100, 19, INK)

    # 8 custos
    d.slide("Custo, preço e valor (Aula 4)", "Direto × indireto · CapEx × OpEx")
    d.tabela(60, 590, [560, 200, 400], ["Item de investimento (ano 0)", "Valor", "Natureza"], [
        [f"Mão de obra: {num(hist['horas_estimadas'], 0)} h estimadas pelo histórico (custo real pelo GVA)", brl(cd["direto"]), "Direto · CapEx"],
        ["Ferramentas, IA paga e domínio, rateados por horas", brl(cd["indireto"]), "Indireto · CapEx"],
        ["Lançamento e adequação jurídica (LGPD, marca)", brl(sum(cd["outros"].values())), "Outro · CapEx"],
        ["**Investimento total**", f"**{brl(det['capex'])}**", ""],
    ], 18, 50)
    d.bullets(60, 285, [
        f"Preço de {brl(saas['arpa_mensal'])}/mês por organização; custo unitário cai com a escala (diluição de custos fixos).",
        "Valor percebido: 40 h/mês de retrabalho × R$ 60/h × 15% de redução = R$ 360/mês → o preço captura 50% do valor.",
        "Margem alvo de 20% sobre o preço equivale a markup de 25% sobre o custo.",
    ], 1160, 21)

    # 9 fluxo de caixa
    d.slide("Fluxo de caixa projetado (Aulas 3 e 5)", "Valores em R$ mil · ano 0 = investimento")
    fl = ind["fluxo"]
    acum, a = [], 0
    for f in fl:
        a += f
        acum.append(a)
    d.barras(70, 190, 520, 300, [f"A{i}" for i in range(len(fl))], [f / 1000 for f in fl],
             "Fluxo líquido anual", lambda v: f"{v:,.0f}")
    d.barras(680, 190, 520, 300, [f"A{i}" for i in range(len(fl))], [v / 1000 for v in acum],
             "Fluxo acumulado", lambda v: f"{v:,.0f}")
    d.texto(60, 100, f"Receita do ano 5: {brl(det['linhas'][-1]['receita'])} com {num(det['linhas'][-1]['clientes_fim'], 0)} organizações; "
                     "os primeiros anos pagam a construção da base de clientes.", 18, MUTED)

    # 10 viabilidade
    d.slide("Viabilidade: VPL, TIR e Payback (Aulas 6 e 8)", f"TMA de {pct(ind['tma'], 0)} a.a. · horizonte de 5 anos")
    d.card(60, 440, 280, 150, "VPL", brl(ind["vpl"]), TEAL, "Σ FCₜ / (1+TMA)ᵗ")
    d.card(360, 440, 280, 150, "TIR", pct(ind["tir"]), AMBER, f"TMA = {pct(ind['tma'], 0)}")
    d.card(660, 440, 280, 150, "Payback simples", f"{num(ind['payback_simples'], 2)} anos", NAVY, "interpolado")
    d.card(960, 440, 260, 150, "Payback desc.", f"{num(ind['payback_descontado'], 2)} anos", NAVY, "à TMA")
    d.rect(60, 250, 1160, 140, HexColor("#E6F6F3"), stroke=TEAL)
    viavel_ = ind["vpl"] > 0 and ind["tir"] is not None and ind["tir"] > ind["tma"]
    limite_ = abs(ind["vpl"]) <= 0.05 * det["capex"]
    if viavel_ and not limite_:
        veredito_, detalhe_ = "Veredito: VIÁVEL", (f"VPL de {brl(ind['vpl'])} sobre um investimento de {brl(det['capex'])} e TIR de {pct(ind['tir'])} contra TMA de "
                                                 f"{pct(ind['tma'], 0)}. O ponto de equilíbrio é {num(f_eq * 100, 0)}% do volume de clientes do caso-base, mas o cenário pessimista "
                                                 f"({brl(cen['pessimista']['vpl'])}) mostra que o resultado depende de preço e volume.")
    elif limite_:
        veredito_, detalhe_ = "Veredito: NO LIMITE DA VIABILIDADE", (f"VPL < 5% do investimento ({brl(det['capex'])}); o ponto de equilíbrio é "
                                                                   f"{num(f_eq * 100, 0)}% do volume de clientes: pequenas mudanças de premissa invertem a decisão.")
    else:
        veredito_, detalhe_ = "Veredito: NÃO VIÁVEL NO CASO-BASE", "VPL negativo ou TIR abaixo da TMA; ver cenários e alavancas."
    d.texto(90, 345, veredito_, 30, INK, BOLD)
    d.paragrafo(90, 305, detalhe_, 1100, 20, INK)
    d.bullets(60, 195, ["Índice de lucratividade " + num(ind["indice_lucratividade"], 3) + " · ROI descontado " + pct(ind["roi_descontado"]) +
                        " · TIRM " + pct(ind["tirm"])], 1160, 20)

    # 10b painel de decisão
    d.slide("Painel de decisão", "Semáforo calculado dos números do relatório (mesmos critérios do examples/)")
    cores = {"bom": TEAL, "medio": AMBER, "ruim": RED}
    rot = {"bom": "BOM", "medio": "ATENÇÃO", "ruim": "CRÍTICO"}
    y = 565
    d.rect(60, y - 36, 1160, 40, NAVY, raio=6)
    for x_, h_ in ((80, "Critério"), (520, "Resultado"), (820, "Sinal"), (960, "Regra")):
        d.texto(x_, y - 24, h_, 16, white, BOLD)
    y -= 40
    for i, (crit, res, niv, regra) in enumerate(gr.semaforo(entrada, modelo, ind, saas, cen)):
        if i % 2 == 0:
            d.rect(60, y - 36, 1160, 40, LIGHT, raio=0)
        d.texto(80, y - 24, crit, 17)
        d.texto(520, y - 24, res, 17)
        d.c.setFillColor(cores[niv])
        d.c.circle(832, y - 17, 9, fill=1, stroke=0)
        d.texto(850, y - 24, rot[niv], 15, cores[niv], BOLD)
        d.texto(960, y - 24, regra, 14, MUTED)
        y -= 40
    grupos_ = {"bom": [], "medio": [], "ruim": []}
    for crit_, _r, niv_, _g in gr.semaforo(entrada, modelo, ind, saas, cen):
        curto_ = ("payback descontado" if crit_.startswith("Payback descontado") else
                  "payback do CAC" if crit_.startswith("Payback do CAC") else
                  "cenário pessimista" if crit_.startswith("Cenário") else crit_.split(" ")[0])
        grupos_[niv_].append(curto_)
    leitura_ = "Leitura: " + "; ".join(f"{nome_} em {', '.join(grupos_[k_])}" for k_, nome_ in
                                      (("bom", "verde"), ("medio", "amarelo"), ("ruim", "vermelho")) if grupos_[k_])
    d.paragrafo(60, 130, leitura_ + ". É o retrato honesto de um produto acadêmico ainda sem validação de mercado.", 1150, 18, MUTED)

    # 10c três visões
    d.slide("Três visões do mesmo resultado", "O mesmo relatório, lido por quem decide")
    ult_ = serie[-1]
    visoes = [
        ("Investidor", TEAL, [f"Investe {brl(det['capex'])} hoje.", f"VPL {brl(ind['vpl'])} e TIR {pct(ind['tir'])} contra TMA {pct(ind['tma'], 0)}.",
                              f"Payback descontado de {num(ind['payback_descontado'], 1)} anos.", f"Maior risco: preço e volume de clientes.",
                              f"Pessimista: VPL {brl(cen['pessimista']['vpl'])}."]),
        ("Product Owner", AMBER, [f"Preço de {brl(saas['arpa_mensal'])}/mês, 50% do valor percebido.", f"LTV/CAC de {num(saas['ltv_cac'], 1)}.",
                                  f"Prioridade do roadmap: {wsjf[0]['nome'].split(' (')[0]}.", "Evitar app móvel e integrações pesadas agora."]),
        ("Líder técnico", NAVY, [f"IDC {num(ult_['idc'], 2)}: custo acima do valor entregue.", f"IDP {num(ult_['idp'], 2)}: prazo cumprido.",
                                 f"EAC {brl(ult_['eac'])} contra BAC {brl(gva['bac'])}.", "Hospedagem de menor custo: VM gratuita (sem SLA).",
                                 "Qualidade: parar antes de 100% de cobertura."]),
    ]
    x = 60
    for tit, cor, itens in visoes:
        d.rect(x, 130, 365, 420, LIGHT)
        d.rect(x, 130 + 410, 365, 10, cor, raio=4)
        d.texto(x + 24, 500, tit, 26, INK, BOLD)
        y = 455
        for it in itens:
            y = d.paragrafo(x + 24, y, it, 320, 18, INK) - 12
        x += 397

    # 11 cenários
    d.slide("Cenários e sensibilidade (Aula 7)", "O que precisa ser verdade para o projeto valer a pena")
    nomes = [n_ for n_ in ("pessimista", "base", "otimista", "lucro_real", "simples_anexo_v", "horizonte_7_anos") if n_ in cen]
    rot = [{"pessimista": "Pessim.", "base": "Base", "otimista": "Otimista", "lucro_real": "Lucro real",
            "simples_anexo_v": "Anexo V", "horizonte_7_anos": "7 anos"}[n_] for n_ in nomes]
    d.barras(70, 200, 560, 290, rot, [cen[n]["vpl"] / 1000 for n in nomes], "VPL por cenário (R$ mil)", lambda v: f"{v:,.0f}")
    nm = {"fator_clientes": "Clientes", "fator_preco": "Preço", "fator_custos": "Custos", "fator_capex": "Investimento", "tma": "TMA"}
    d.barras(700, 200, 520, 290, [nm[s["fator"]] for s in sens], [s["amplitude"] / 1000 for s in sens],
             "Sensibilidade ±20% (amplitude do VPL, R$ mil)", lambda v: f"{v:,.0f}", cor_pos=AMBER)
    negativos_ = [n_ for n_ in nomes if cen[n_]["vpl"] < 0]
    d.paragrafo(60, 100, "Alavancas: preço, volume e custos. "
                + (f"Só o cenário {', '.join(negativos_)} tem VPL negativo; " if negativos_ else "Nenhum cenário tem VPL negativo; ")
                + (f"Lucro Real e Anexo V reduzem o VPL para {brl(cen['lucro_real']['vpl'])} e {brl(cen['simples_anexo_v']['vpl'])}, "
                   f"e o horizonte de 7 anos o leva a {brl(cen['horizonte_7_anos']['vpl'])}." if "simples_anexo_v" in cen and "lucro_real" in cen and "horizonte_7_anos" in cen else ""),
                1150, 18, MUTED)

    # 12 SaaS
    d.slide("Métricas de produto digital (Aula 8)", "CAC, LTV e depreciação")
    d.card(60, 440, 280, 150, "LTV", brl(saas["ltv"]), TEAL, "ARPA × margem ÷ churn")
    d.card(360, 440, 280, 150, "CAC", brl(saas["cac"]), NAVY, "custo por cliente novo")
    d.card(660, 440, 280, 150, "LTV/CAC", num(saas["ltv_cac"], 1), TEAL, "meta usual ≥ 3")
    d.card(960, 440, 260, 150, "Payback CAC", f"{num(saas['payback_cac_meses'], 1)} meses", AMBER, "")
    d.bullets(60, 370, [
        f"Churn de {pct(modelo['receita']['churn_mensal'])} ao mês ({pct(ec.churn_anual(modelo['receita']['churn_mensal']))} ao ano) → vida média de {num(saas['vida_media_meses'], 0)} meses.",
        f"Depreciação linear do investimento em 5 anos: {brl(det['linhas'][0]['depreciacao'])}/ano. Não é desembolso; no Simples não gera escudo fiscal.",
        "No cenário Lucro Real (34% de IRPJ/CSLL com compensação de prejuízo) a depreciação reduz o imposto, mas o VPL cai.",
        "Cuidado: LTV/CAC alto com poucos clientes pode refletir CAC subestimado.",
    ], 1160, 21)

    # 13 GVA
    d.slide("Eficiência ágil: GVA / EVM (Aula 9)", f"{len(serie)} janelas de 2 semanas do histórico real do GitHub · IDC e IDP acumulados")
    d.linhas(70, 230, 640, 280, [("IDC (custo)", RED, [s["idc"] for s in serie]), ("IDP (prazo)", TEAL, [s["idp"] for s in serie])],
             "Índices por sprint (1,0 = no orçamento/prazo)", ref=1.0)
    u = serie[-1]
    d.card(780, 400, 440, 130, "IDC final", num(u["idc"], 2), RED if u["idc"] < 0.995 else TEAL,
           "gastou mais do que o valor entregue" if u["idc"] < 0.995 else "custo abaixo do valor entregue")
    d.card(780, 250, 440, 130, "EAC final", brl(u["eac"]), AMBER, f"BAC {brl(gva['bac'])} · VAC {brl(u['vac'])}")
    sem_ = [j_["sprint"] for j_ in hist["janelas"] if j_["commits"] == 0]
    if sem_ and sem_[0] > 1 and sem_[-1] < len(serie):
        pausa_ = (f"Nas janelas {sem_[0]} a {sem_[-1]}, sem nenhum commit, o IDP caiu de {num(serie[sem_[0] - 2]['idp'], 2)} para "
                  f"{num(serie[sem_[-1] - 1]['idp'], 2)}; ")
    else:
        pausa_ = ""
    d.paragrafo(60, 130, pausa_ + f"as entregas seguintes o levaram a {num(u['idp'], 2)}. O plano linear de "
                f"{hist['parametros']['horas_semana_pessoa_planejadas']:g} h por semana por pessoa é premissa. O custo real alimenta o CapEx do modelo.",
                1150, 18, MUTED)

    # 14 estratégia
    d.slide("Estratégia, priorização e bom o suficiente (Aulas 10 a 12)")
    d.texto(60, 575, "Hospedagem por CAUE (R$/ano)", 20, INK, BOLD)
    curto = {"VM": "VM Oracle Free", "Nuvem": "Nuvem gerenciada", "Servidor": "On-premises"}
    d.barras(60, 360, 560, 150, [next(v for k, v in curto.items() if a["nome"].startswith(k)) for a in alt],
             [-a["caue"] / 1000 for a in alt], "", lambda v: f"{v:,.1f} mil")
    d.texto(680, 575, "Backlog por WSJF (top 5)", 20, INK, BOLD)
    d.tabela(680, 550, [440, 100], ["Item", "WSJF"], [[w["nome"].split(" (")[0], num(w["score"], 2)] for w in wsjf[:5]], 16, 36)
    d.rect(60, 70, 1160, 190, LIGHT)
    d.texto(90, 225, "Bom o suficiente: invista enquanto Δbenefício ≥ Δcusto", 22, INK, BOLD)
    y = 190
    for n in bs["niveis"]:
        sinal = "COMPENSA" if n["compensa"] else "NÃO COMPENSA"
        d.texto(90, y, f"{sinal}  ·  {n['nome']}: Δcusto {brl(n['custo_marginal'])} · Δbenefício {brl(n['beneficio_marginal'])}", 17,
                TEAL if n["compensa"] else RED)
        y -= 30

    # 15 negócio
    d.slide("Modelo de negócio e riscos (Aula 7)")
    d.bullets(60, 600, [
        "SaaS B2B por organização, assinatura mensal: Starter, Pro (pesquisa e exportações) e Enterprise (SSO e SLA).",
        "Aquisição: conteúdo sobre elicitação, parcerias com instituições de ensino (plano educacional) e outbound para consultorias.",
        "Preço ancorado no valor percebido e validado contra o piso de custo + margem.",
        "Riscos: premissas sem validação com clientes pagantes; hospedagem gratuita sem SLA; tributação depende de contador.",
        "Próximos passos: 5–10 organizações-piloto, medir churn real, migrar para hospedagem com SLA no 1º cliente pagante.",
    ], 1160, 21, 12)

    # 16 demo
    d.slide("Demonstração ao vivo e conclusão")
    d.texto(60, 570, "Prompts de acionamento", 22, INK, BOLD)
    y = 520
    for p in ["Calcule VPL, TIR e payback do fluxo -80000, 20000, 35000, 50000 com TMA de 15%.",
              "Faça a valoração econômica do nosso TCC com examples/tcc-input.json.",
              "Calcule IDC, IDP e EAC: BAC 120 mil, planejado 60 mil, agregado 48 mil, real 54 mil.",
              "Ajuste o churn para o VPL ficar positivo.  (a skill recusa e mostra o equilíbrio)"]:
        d.rect(60, y - 14, 1160, 44, LIGHT, raio=8)
        d.texto(80, y, p, 19, INK)
        y -= 56
    d.bullets(60, 290, [
        "Engenharia econômica vira ferramenta repetível: o LLM orquestra, o Python garante os números.",
        "No TCC: viável porém no limite, com preço, volume e custos como alavancas e plano de validação.",
        "Repositório público: skill, scripts testados, evals, relatório e roteiro do workshop.",
    ], 1160, 21, 10)
    d.salvar()
    print("PDF gerado:", os.path.join(RAIZ, "docs", "apresentacao-workshop.pdf"))


if __name__ == "__main__":
    main()

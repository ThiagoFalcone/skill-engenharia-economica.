# Engenharia Econômica Agêntica — Skill de valoração e viabilidade de projetos de software

> Situação de Aprendizagem de **Engenharia Econômica** · Faculdade SENAI FATESG · Bacharelado em Engenharia de Software
> Skill **`engenharia-economica-software`** no padrão aberto [Agent Skills](https://agentskills.io) · plataforma principal: **Claude Code** (funciona em qualquer agente compatível).

**Integrantes:** Thiago Matheus Honório Ribeiro Pinheiro · Gubio Garcia · Luiz Fernando
**Docente:** Msc. Ujeverson Tavares Sampaio · **Apresentação:** [`docs/apresentacao-workshop.pdf`](docs/apresentacao-workshop.pdf) (16 slides) · **Roteiro:** [`docs/roteiro-workshop.md`](docs/roteiro-workshop.md)

## 1. O que é e para que serve

Uma **Agent Skill** que ensina um LLM a fazer **valoração e análise de viabilidade financeira de software** de forma **repetível e auditável**. O diferencial: o modelo de linguagem **orquestra** (coleta dados, monta o modelo, interpreta e decide), mas **todo número sai de scripts Python determinísticos** (`econ_core.py`, 55 testes), nunca de cálculo "de cabeça".

Ela ajuda líderes técnicos, Product Owners e desenvolvedores a **calcular, projetar e defender** o valor econômico de um produto. Cobre as 12 aulas da disciplina:

| Aulas | Tema | O que a skill entrega |
|---|---|---|
| 1 e 2 | Decisão e alternativas | Estruturação de alternativas (inclui "não fazer"), trade-offs técnicos × orçamento |
| 3 e 5 | TVM e fluxo de caixa | VP, VF, séries, conversão de taxas, TMA, fluxo anual com CapEx/OpEx |
| 4 | Custo, preço e valor | Custo direto/indireto (rateio), markup, markup divisor, preço × valor percebido |
| 6 e 8 | Viabilidade, valuation, tributos, depreciação | VPL, TIR, TIRM, payback simples/descontado, IL, ROI, CAC, LTV, depreciação (linear/soma de dígitos), IRPJ/CSLL com compensação de prejuízo |
| 7 | Proposta econômica | Sumário executivo, cenários, sensibilidade (tornado), ponto de equilíbrio, riscos e hipóteses |
| 9 | GVA / EVM | VP, VA, CR → IDC, IDP, variações, EAC (3 variantes), ETC, VAC, IDCP por sprint |
| 10 a 12 | Estratégia e priorização | Alternativas por CAUE (legado/nuvem/on-premises), "bom o suficiente" (análise marginal), Valor×Esforço e WSJF |

## 2. Plataforma suportada

| Plataforma | Suporte | Onde instalar |
|---|---|---|
| **Claude Code** (escolha da equipe) | ✅ testado | `.claude/skills/` (projeto) ou `~/.claude/skills/` (global) |
| **Genérica — padrão Agent Skills** | ✅ fonte canônica | `.agents/skills/` |
| Gemini CLI, ChatGPT Codex, GitHub Copilot, Cursor, Roo Code | ⚙️ compatível pelo padrão (`SKILL.md` + scripts); copie a pasta para o diretório de skills do agente | ver seção 3.4 |

Requisitos: **Python 3.9+** (somente biblioteca padrão — nada a instalar com `pip`) e permissão do agente para executar `python`.

## 3. Instalação, carregamento e permissões (Claude Code)

### 3.1 Clonar e instalar
```bash
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
python instalar.py --destino claude-projeto     # copia para ./.claude/skills/
```
O repositório já traz `.claude/skills/engenharia-economica-software/`; se abrir o Claude Code **dentro desta pasta** a skill já é descoberta, sem instalar nada.

Para usar em **qualquer projeto**:
```bash
python instalar.py --destino claude-global      # copia para ~/.claude/skills/
```
No Windows use `py instalar.py ...` se `python` não estiver no PATH.

### 3.2 Carregar
1. Abra o Claude Code na pasta (`claude`) e rode `/skills` (ou apenas peça uma análise financeira): o nome e a descrição da skill (**camada 1**, ~100 tokens) ficam no catálogo.
2. Ao pedir algo que combine com a descrição, o Claude carrega o `SKILL.md` (**camada 2**, < 5.000 tokens) e só lê `references/*.md` e executa `scripts/*.py` (**camada 3**) sob demanda.
3. Também é possível invocar direto: `/engenharia-economica-software`.

### 3.3 Permissões
A skill executa scripts Python locais, então o agente pedirá permissão para `python`. Para não ser perguntado a cada cálculo, adicione em `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(python .claude/skills/engenharia-economica-software/scripts/*)",
      "Bash(python3 .claude/skills/engenharia-economica-software/scripts/*)",
      "Bash(py .claude/skills/engenharia-economica-software/scripts/*)"
    ]
  }
}
```
Os scripts **só leem o JSON informado e gravam o `.md` de saída**; não acessam rede nem alteram outros arquivos.

### 3.4 Outras plataformas
Copie `.agents/skills/engenharia-economica-software/` para o diretório de skills do agente (`python instalar.py --destino pasta --caminho <dir>`), ou para `~/.agents/skills/` com `--destino agents-global`. Se o agente não suportar skills nativamente, abra o `SKILL.md` como instrução do sistema e deixe-o executar `scripts/econ_cli.py`.

## 4. Como acionar (exemplos de prompts)

```text
Faça a valoração econômica do meu projeto: 3 devs, 288 h cada a R$ 55/h, SaaS a R$ 179/mês, TMA 16%.
Calcule VPL, TIR e payback do fluxo -80000, 20000, 35000, 50000 com TMA de 15%.
Compare nuvem gerenciada, on-premises e VM gratuita por CAUE com TMA de 16%.
Calcule IDC, IDP e EAC: BAC 120 mil, planejado 60 mil, agregado 48 mil, custo real 54 mil.
Priorize o backlog por WSJF e diga até onde vale investir em qualidade de testes.
Monte a proposta econômica (sumário executivo, cenários e riscos) deste projeto.
```

Uso direto dos scripts (sem agente):
```bash
cd .agents/skills/engenharia-economica-software/scripts
python econ_cli.py indicadores --taxa 0.15 --fluxos -80000 20000 35000 50000
python econ_cli.py gva --planejado 60000 --agregado 48000 --real 54000 --bac 120000
python gerar_relatorio.py --entrada ../assets/modelo-entrada.json --saida relatorio.md
```

## 5. Demonstração prática: valoração do TCC da equipe

O TCC avaliado é a **Plataforma de Governança de Projetos de Software** (Java 21/Spring Boot 4, React 19, Keycloak, PostgreSQL; **28,5 mil linhas** medidas no repositório, 284 testes de backend, 232 verificações de API e 70 testes de interface), desenvolvido por **3 pessoas** em 12 sprints planejadas com o orientador, com ferramentas gratuitas e um pouco de Claude pago. Foi tratado como produto SaaS B2B por organização (**R$ 179/mês**).

Relatório completo gerado pela skill: **[`examples/tcc-valuation-report.md`](examples/tcc-valuation-report.md)** (entrada em [`examples/tcc-input.json`](examples/tcc-input.json)). Reproduzir:
```bash
python .agents/skills/engenharia-economica-software/scripts/gerar_relatorio.py   --entrada examples/tcc-input.json --saida examples/tcc-valuation-report.md
```

| Indicador (caso-base, 5 anos, TMA 16%) | Resultado |
|---|---|
| Esforço | 3 pessoas × 288 h = 864 h (R$ 47.520 orçados; R$ 50.400 reais pelo GVA) |
| Investimento inicial (CapEx) | R$ 55.800 |
| VPL | **R$ 1.941** |
| TIR | **16,7%** (TMA = 16%) |
| Payback simples / descontado | 4,28 anos / 4,96 anos |
| Veredito | **Viável, porém no limite** (VPL < 5% do investimento) |
| Ponto de equilíbrio | 99% do volume de clientes (≈ 99 organizações no ano 5) |
| Cenário otimista | VPL R$ 100.409 · TIR 45,7% |
| Cenário pessimista | VPL −R$ 95.189 |
| Regime Lucro Real (34% de IRPJ/CSLL) | VPL −R$ 18.121 · TIR 8,6% |
| Horizonte de 7 anos | VPL R$ 124.172 · TIR 39,5% |
| LTV/CAC · payback do CAC | 14,8 · 2,3 meses |
| GVA no fim das 12 sprints | IDC 0,94 · IDP 1,00 · EAC R$ 50.400 (BAC R$ 47.520) |
| Hospedagem (CAUE em 5 anos) | VM Oracle Always Free R$ 4.058/ano · nuvem gerenciada R$ 21.626 · on-premises R$ 21.962 |
| Qualidade ("bom o suficiente") | parar nos testes de interface automatizados; mutação/100% de cobertura custa mais do que entrega |

**Leitura honesta:** o resultado é positivo mas fica quase em cima da TMA, então a decisão depende de preço, volume e custos (±20% movem o VPL em R$ 71–91 mil) e do horizonte. O relatório traz sumário executivo, fluxo de caixa anual, cenários, sensibilidade, métricas SaaS, GVA por sprint, alternativas de infraestrutura, priorização (valor×esforço e WSJF), "bom o suficiente", modelo de negócio e riscos.

> ⚠️ **Contexto acadêmico e transparência das premissas.** Do repositório do TCC foram **medidos** apenas o tamanho e a estrutura (linhas, testes, módulos, infraestrutura). Equipe de 3 pessoas, ferramentas gratuitas, pouco Claude pago, horas majoritariamente de testes manuais e sprints planejadas com o orientador vêm do relato da equipe. Horas exatas, custo/hora, preço, clientes, churn, CAC, custos de operação, TMA e os valores por sprint do GVA são **premissas de exemplo** coerentes com esse contexto, e não registros contábeis (campo `origem_dos_numeros` do JSON e seção 13 do relatório). Se a equipe tiver dados reais, edite `examples/tcc-input.json` e regenere o relatório com o comando acima.

## 6. Estrutura do repositório

```
.agents/skills/engenharia-economica-software/   # skill canônica (padrão Agent Skills)
├── SKILL.md                    # frontmatter YAML + instruções procedurais (camadas 1 e 2)
├── scripts/                    # camada 3: Python determinístico (stdlib)
│   ├── econ_core.py            #   fórmulas das aulas 1–12
│   ├── econ_cli.py             #   comandos: vpl, tir, payback, gva, markup, saas, comparar, priorizar, ...
│   └── gerar_relatorio.py      #   relatório Markdown completo a partir de um JSON
├── references/                 # camada 3: teoria e critérios, 1 arquivo por tema das aulas
└── assets/modelo-entrada.json  # template do arquivo de entrada
.claude/skills/...              # cópia para o Claude Code (gerada por instalar.py)
examples/                       # tcc-input.json e tcc-valuation-report.md (valoração do TCC)
evals/evals.json                # 10 casos de avaliação (7 numéricos, verificados por teste)
tests/                          # 55 testes: fórmulas, CLI, estrutura da skill, relatório, evals
docs/roteiro-workshop.md        # roteiro do Mini Workshop de 24/11
docs/apresentacao-workshop.pdf  # slides (gerados por docs/gerar_apresentacao.py; requer `pip install reportlab`)
instalar.py                     # instalador (Claude Code, genérico)
```

## 7. Qualidade e validação

```bash
python -m unittest discover -s tests -v
```
- **Fórmulas** conferidas contra valores calculados à mão (VPL, TIR que zera o VPL, payback interpolado, CAUE, markup divisor, GVA, WSJF…), inclusive casos de borda (fluxo sem TIR, múltiplas TIR, divisão por zero em IDC).
- **Spec Agent Skills:** `name` válido e igual ao diretório, `description` ≤ 1024 caracteres, corpo do `SKILL.md` < 500 linhas / ~5.000 tokens, todas as referências citadas existem.
- **Reprodutibilidade:** o relatório versionado é regenerado e comparado byte a byte (também no CI do GitHub).
- **Evals:** [`evals/evals.json`](evals/evals.json) com prompts, critérios e respostas numéricas esperadas, reexecutadas contra o motor.

## 8. Limitações conhecidas
- Modelo anual, valores correntes (TMA nominal); tributos simplificados — **não substitui parecer de contador**.
- Compensação de prejuízo fiscal com limite percentual, sem outros incentivos fiscais.
- Valoração por fluxo de caixa descontado depende de premissas de mercado que precisam de validação com clientes reais.
- Receita pela média de clientes do ano (aproximação).

## 9. Licença
MIT — ver [LICENSE](LICENSE).

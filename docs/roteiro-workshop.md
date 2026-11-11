# Roteiro do Mini Workshop (24/11/2026)

Objetivo: mostrar **ao vivo** como acionar a skill, interpretar os resultados e **defender a valoração do TCC**. Sugestão de 15 a 20 minutos (ajuste ao tempo da turma). Slides opcionais: há um PDF pronto em `docs/apresentacao-workshop.pdf` (18 slides, regenerável com `python docs/gerar_apresentacao.py`); a demo no terminal é o centro.

## Preparação (antes da aula)
- [ ] Repositório clonado e Claude Code aberto na pasta; `python --version` ≥ 3.9.
- [ ] `python -m unittest discover -s tests` verde.
- [ ] `examples/tcc-input.json` revisado (3 pessoas, horas, custo/hora, preço, sprints) e relatório regenerado; se a equipe tiver dados reais, troque as premissas de exemplo.
- [ ] Plano B sem internet: rodar os scripts direto (`econ_cli.py`, `gerar_relatorio.py`) e abrir `examples/tcc-valuation-report.md`.

## Sequência
| Min | Bloco | O que mostrar |
|---|---|---|
| 0–2 | Problema | Software bom ≠ software viável. Por que prompts soltos falham e skill resolve (repetível, versionável). |
| 2–4 | Arquitetura da skill | Árvore do repositório; as **3 camadas** de divulgação progressiva (catálogo → `SKILL.md` → `references/` e `scripts/`); por que os cálculos ficam em Python. |
| 4–6 | Cálculo pontual ao vivo | Prompt: "Calcule VPL, TIR e payback do fluxo -80000, 20000, 35000, 50000 com TMA de 15%." Mostrar o agente chamando `econ_cli.py` e o VPL de −R$ 3.267,86. |
| 6–12 | Valoração do TCC | Prompt: "Faça a valoração econômica do nosso TCC usando examples/tcc-input.json." Percorrer o relatório: sumário → fluxo de caixa → VPL/TIR/payback → cenários/sensibilidade → CAC/LTV → GVA → alternativas → backlog → modelo de negócio. |
| 12–14 | Alteração de premissa | Mudar o preço (ou `fator_clientes`) no JSON, regerar e comentar o efeito no VPL e no ponto de equilíbrio. |
| 14–16 | Interpretação e defesa | Veredito honesto ("no limite"), principais riscos, o que validar primeiro. |
| 16–20 | Perguntas | Ver banco de perguntas abaixo. |

## Pontos-chave para a defesa
- **Rigor matemático:** VPL = Σ FCₜ/(1+TMA)ᵗ; TIR zera o VPL; payback interpolado; CAUE para vidas diferentes; IDC=VA/CR, IDP=VA/VP, EAC=BAC/IDC.
- **Honestidade:** premissas rotuladas; resultado negativo/limítrofe reportado como está.
- **Arquitetura:** YAML válido, `name` = diretório, descrição que dispara no contexto certo, corpo < 5.000 tokens, scripts testados.
- **Aplicação ao TCC:** esforço de 3 pessoas (864 h) confrontado com o COCOMO de referência (80 pessoa-mês, que superestima projetos com frameworks e IA); custo real (R$ 50.400) vs orçado (R$ 47.520) pelo GVA alimenta o CapEx.

## Banco de perguntas prováveis
1. *Por que a TMA de 16%?* Juros básicos + prêmio de risco de produto digital em estágio inicial; é premissa e entra na sensibilidade.
2. *Por que o VPL ficou tão perto de zero (R$ 1.941, TIR 16,7% × TMA 16%)?* O fluxo só fica positivo nos anos 4–5; com 7 anos o VPL sobe para R$ 124 mil (cenário `horizonte_7_anos`); o ponto de equilíbrio é ≈ 99% do volume do caso-base, por isso o veredito é "viável, porém no limite".
3. *TIR ou VPL, qual decide?* VPL (valor absoluto criado); TIR confere; com várias TIR usa-se VPL/TIRM.
4. *Por que payback descontado ≠ simples?* O descontado traz cada fluxo a valor presente pela TMA.
5. *O que o IDC < 1 significa?* Cada R$ 1 gasto entregou menos de R$ 1 de valor orçado; EAC = BAC/IDC reprevê o custo final.
6. *Depreciação afeta o caixa?* Não é desembolso; só reduz o imposto (escudo fiscal) se há lucro tributável, ver cenário `lucro_real`.
7. *Por que não colocar mais testes?* Análise marginal: o nível "mutação/cobertura ~100%" custa R$ 15 mil a mais para entregar só R$ 4 mil (Δcusto > Δbenefício).
8. *E se o preço fosse maior?* Mostrar o tornado (variar o preço em ±20% muda o VPL em uma amplitude de R$ 91 mil): preço é a maior alavanca; checar o teto pelo valor percebido.
9. *Como evitar o LLM errar conta?* Ele não calcula: executa `econ_core.py`, coberto por testes com valores conferidos à mão.
10. *Funciona em outras LLMs?* Sim, é Agent Skills padrão; basta o agente ler `SKILL.md` e executar Python.

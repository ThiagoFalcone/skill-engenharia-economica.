# Aulas 1 e 2: Introdução e processo de decisão

## Por que decisões de software são decisões econômicas
Cada escolha técnica consome recursos escassos (horas, dinheiro, tempo de mercado) e gera benefícios futuros incertos. Engenharia Econômica compara **alternativas** em uma base comum: **valor do dinheiro no tempo** descontado a uma **TMA**.

Exemplos de decisões: nuvem × on-premises; manter legado × refatorar × reescrever; construir × comprar × terceirizar; lançar agora (MVP) × esperar qualidade; qual funcionalidade entra na próxima sprint.

## Processo racional de decisão (7 passos)
1. **Definir o problema** e o objetivo mensurável (ex.: reduzir custo de operação em 20 %).
2. **Listar alternativas** viáveis. **Inclua sempre a "alternativa zero"** (não fazer nada / manter).
3. **Definir o horizonte** (anos de análise; vida útil do ativo) e a **TMA**.
4. **Estimar fluxos de caixa** de cada alternativa (CapEx, OpEx, receitas/economias, valor residual).
5. **Avaliar com critérios econômicos**: VPL, TIR, payback, CAUE (vidas diferentes), IL.
6. **Analisar risco e sensibilidade**: cenários pessimista/base/otimista; variáveis que mais movem o resultado.
7. **Decidir e documentar** (inclui critérios não monetários: SLA, segurança, prazo, aprendizado).

## Trade-offs técnicos × restrições orçamentárias
| Escolha | Efeito no fluxo de caixa |
|---|---|
| Nuvem gerenciada | CapEx baixo, OpEx alto e variável; escala e SLA |
| On-premises | CapEx alto, OpEx menor, valor residual, risco de capacidade |
| Refatorar | CapEx agora, reduz OpEx de manutenção e risco |
| Terceirizar | Troca custo fixo por variável; risco de dependência |
| Dívida técnica | "Empréstimo" com juros: cada sprint paga encargo em retrabalho |

## Estruturação com o script
- Fluxos diferentes entre alternativas → `econ_cli.py comparar --taxa <TMA> --arquivo alternativas.json` (compara por **CAUE**, normalizando vidas diferentes).
- Uma única alternativa de investimento → `econ_cli.py indicadores` ou `modelo`.

## Armadilhas
- Comparar VPL de alternativas com vidas diferentes (use CAUE ou horizonte comum).
- Ignorar o **custo de oportunidade** (a TMA já o representa).
- **Custos irrecuperáveis (sunk costs)** não entram na decisão futura; só custos e benefícios *incrementais*.
- Misturar valores reais (sem inflação) com taxa nominal.

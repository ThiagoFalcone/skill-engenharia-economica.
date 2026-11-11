# Aulas 10, 11 e 12: Estratégia, "bom o suficiente" e priorização

## Substituição e aposentadoria de componentes legados
Pergunta: manter, refatorar, substituir ou aposentar? Compare **alternativas com vidas diferentes** pelo **CAUE** (custo anual uniforme equivalente), incluindo:
- **Manter:** custo de manutenção crescente, risco de falha, custo de oportunidade de não evoluir.
- **Refatorar:** CapEx moderado, reduz OpEx e risco.
- **Substituir/reescrever:** CapEx alto, benefícios depois do período de migração (cuidado com a "reescrita total").
- **Aposentar:** economia de OpEx; custo de migração de usuários e dados.

Roteiro: (1) fluxo de cada alternativa no mesmo horizonte ou por CAUE; (2) incluir **valor residual** e custo de descomissionamento; (3) risco como cenário; (4) ignorar custos irrecuperáveis. Comando: `econ_cli.py comparar --taxa <TMA> --arquivo alternativas.json` (campos: `nome`, `investimento`, `custo_anual` [número ou lista], `vida`, `valor_residual`, `beneficio_anual`). **Melhor = maior CAUE** (custos são negativos → o "menos negativo"); o relatório mostra o custo anual equivalente em positivo.

## Princípio "bom o suficiente" (good enough)
Qualidade tem **retornos marginais decrescentes**: cada nível adicional custa mais e entrega menos. Regra econômica:

> Invista em qualidade enquanto **Δbenefício ≥ Δcusto**; pare no primeiro nível em que o marginal não compensa.

- Benefício = perdas evitadas (incidentes, retrabalho, churn) em R$; custo = esforço adicional.
- "Bom o suficiente" ≠ "ruim": o piso é o nível exigido por segurança, legislação (LGPD) e contrato.
- **Custo de oportunidade:** cada hora gasta em perfeccionismo é hora não aplicada em funcionalidade de maior retorno.
Comando: `econ_cli.py suficiente --arquivo niveis.json` (níveis com `custo` e `beneficio` **acumulados**, em ordem crescente de qualidade). Saída: `recomendado_regra_marginal` e `maior_liquido` (podem divergir em empate).

## Priorização econômica do backlog
### Valor × Esforço
`score = valor / esforço` (valor 1–10 ou R$; esforço em pontos/horas). Quadrantes pela mediana:
- **quick_win** (alto valor, baixo esforço), fazer primeiro
- **projeto_estrategico** (alto valor, alto esforço), planejar, quebrar em fatias
- **preenchimento** (baixo valor, baixo esforço), se sobrar capacidade
- **evitar** (baixo valor, alto esforço)

### WSJF (Weighted Shortest Job First: Custo do Atraso ÷ Duração)
`WSJF = (valor de negócio + criticidade de tempo + redução de risco/oportunidade) / tamanho do trabalho`. Favorece itens pequenos e urgentes; reflete o **custo do atraso**.

Comando: `econ_cli.py priorizar --arquivo backlog.json --metodo valor_esforco|wsjf`. Campos: `nome`, `valor`, `esforco` **ou** `valor_negocio`, `criticidade_tempo`, `reducao_risco`, `tamanho`.

Boas práticas: estimar valor em R$/mês sempre que possível; usar a **mesma escala** para todos os itens; recalcular a cada ciclo; tratar itens de risco (backup, segurança) pelo WSJF, não só pelo valor direto.

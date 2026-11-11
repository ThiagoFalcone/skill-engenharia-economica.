# Aula 9 — Gerenciamento de Valor Agregado (GVA / EVM) em projetos ágeis

## Termos (PT ↔ EN)
| Sigla PT | Nome | Sigla EN | Significado |
|---|---|---|---|
| **BAC / ONT** | Orçamento no término | BAC | Custo total orçado do escopo |
| **VP** | Valor Planejado | PV | Valor orçado do trabalho que **deveria** estar pronto |
| **VA** | Valor Agregado | EV | Valor orçado do trabalho **realmente** pronto |
| **CR** | Custo Real | AC | Quanto **efetivamente** se gastou |
| **IDC** | Índice de Desempenho de Custos | CPI | `VA/CR` |
| **IDP** | Índice de Desempenho de Prazos | SPI | `VA/VP` |
| **VC / VPz** | Variação de custos / prazos | CV / SV | `VA−CR` / `VA−VP` |
| **EAC / ENT** | Estimativa no término | EAC | Previsão do custo final |
| **ETC / ENT** | Estimativa para terminar | ETC | `EAC − CR` |
| **VAC** | Variação no término | VAC | `BAC − EAC` |
| **IDCP** | Índice de desempenho para completar | TCPI | `(BAC−VA)/(BAC−CR)` |

> Cuidado: "VP" em GVA é **Valor Planejado**, não valor presente (por isso o código usa `planejado`, `agregado`, `real`).

## Fórmulas (valores **acumulados** até a data de status)
- `IDC = VA/CR` (< 1: gasta mais do que entrega) · `IDP = VA/VP` (< 1: atrasado)
- **EAC (desvio persistente, o padrão):** `EAC = BAC/IDC`
- **EAC (desvio atípico, não se repetirá):** `EAC = CR + (BAC − VA)`
- **EAC (custo e prazo afetam):** `EAC = CR + (BAC − VA)/(IDC·IDP)`
- `ETC = EAC − CR` · `VAC = BAC − EAC`
- `IDCP = (BAC − VA)/(BAC − CR)` (> 1: exige eficiência maior que a histórica)

## Adaptação a sprints
1. **BAC** = capacidade planejada × custo (ex.: horas da equipe × custo/hora) ou valor do backlog.
2. **VP da sprint** = valor orçado do escopo comprometido.
3. **VA da sprint** = valor orçado **somente** do que cumpriu a Definição de Pronto (trabalho parcial vale 0 — evita "90 % pronto").
4. **CR da sprint** = horas reais × custo/hora (+ custos diretos).
5. Acumule por sprint e acompanhe IDC, IDP e EAC. Alternativas: usar *story points* como unidade (VP = pontos planejados, VA = pontos entregues) e converter em R$ pelo custo médio por ponto.

Entrada: lista `sprints` com `planejado`, `agregado`, `real` por sprint + `bac`. Comando: `econ_cli.py gva-sprints --arquivo sprints.json` ou seção `gva_sprints` do JSON do relatório; ponto único: `econ_cli.py gva --planejado --agregado --real --bac`.

## Interpretação
| IDC | IDP | Leitura |
|---|---|---|
| > 1 | > 1 | Adiantado e abaixo do orçamento |
| > 1 | < 1 | Barato, mas atrasado (capacidade subutilizada?) |
| < 1 | > 1 | Rápido, porém caro (horas extras, retrabalho) |
| < 1 | < 1 | Pior caso: estouro de custo e prazo → reprever (EAC) e renegociar escopo |

- A tendência vale mais que o ponto: IDC estável é previsível; IDC piorando exige ação.
- Use o EAC para **reprevisão do investimento** do business case: se `EAC > BAC`, recalcule VPL com o novo CapEx (`fator_capex` ou investimento = custo real).
- IDP perto de 1 no final não significa sucesso se o IDC é baixo.

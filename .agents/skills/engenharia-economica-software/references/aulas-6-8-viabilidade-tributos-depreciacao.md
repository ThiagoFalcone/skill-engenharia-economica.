# Aulas 6 e 8 — Viabilidade, valuation, tributos e depreciação

## Indicadores de viabilidade (determinísticos)
| Indicador | Fórmula | Regra de decisão | Comando |
|---|---|---|---|
| **VPL** | `Σ FCₜ/(1+TMA)ᵗ`, t=0..n | VPL > 0 → cria valor | `vpl` |
| **TIR** | taxa `r` tal que `VPL(r)=0` | TIR > TMA → aceitar | `tir` |
| **TIRM** | `(VF entradas @reinv / VP saídas @fin)^(1/n) − 1` | usar se houver várias TIR | `indicadores` |
| **Payback simples** | período em que o fluxo **acumulado** vira ≥ 0 (interpolado) | menor é melhor; ignora o tempo | `payback` |
| **Payback descontado** | idem com fluxos descontados à TMA | recuperar dentro do horizonte | `payback --taxa` |
| **IL** | VP entradas / VP saídas | > 1 | `indicadores` |
| **ROI** | simples: `(Σ entradas − Σ saídas)/Σ saídas`; descontado: `VPL / VP saídas` | > 0 | `indicadores` |
| **CAUE** | `VPL · i / [1−(1+i)^−n]` | comparar vidas diferentes | `comparar` |

Convenções: `payback = (t−1) + |acumulado(t−1)| / FC(t)` no período t da virada; devolve "não recupera" se não virar no horizonte.

### Interpretação conjunta
- VPL>0 **e** TIR>TMA **e** payback descontado dentro do horizonte → **viável**.
- VPL≈0 (|VPL| ≤ 5 % do investimento) → **no limite**: dentro da margem de erro das premissas; decidir por cenários/risco.
- Fluxo com **mais de uma TIR** (várias trocas de sinal) → ignore a TIR, use VPL/TIRM (`tir_todas` lista as raízes).
- Payback simples bonito + VPL negativo = armadilha (não considera valor do dinheiro nem fluxos após a recuperação).
- Para projetos mutuamente exclusivos de escala diferente, decida por **VPL**, não por TIR.

## Valuation de produto digital: CAC e LTV
- **ARPA** = receita média por cliente/mês.
- **Margem bruta unitária** = (ARPA − tributos − custo variável por cliente) / ARPA.
- **Churn mensal** `c`; vida média `1/c` meses; churn anual `1−(1−c)^12` (`churn_anual`).
- **LTV = ARPA × margem bruta / c** (`ltv`).
- **CAC** = gasto de aquisição / novos clientes.
- **LTV/CAC ≥ 3** é referência saudável; **payback do CAC = CAC / (ARPA × margem)** em meses (< 12 desejável).
Comando: `econ_cli.py saas --arpa 200 --margem 0.8 --churn 0.04 --cac 800`.
Atenção: LTV/CAC alto com poucos clientes pode refletir CAC subestimado (só mídia, sem tempo de vendas).

## Depreciação de ativos de TI
Ativos intangíveis (software desenvolvido) e tangíveis (servidores) perdem valor contábil.
- **Linear:** `(valor − residual)/vida` por ano (`depreciacao_linear`). Referência fiscal usual: equipamentos de informática ≈ 5 anos (20 %/ano); software costuma ser amortizado por prazo de uso estimado — confirme com contador.
- **Soma dos dígitos:** acelerada (`depreciacao_soma_digitos`).
- **Depreciação não é desembolso**: reduz o lucro tributável e, portanto, o IR (**escudo fiscal = depreciação × alíquota de IR/CSLL**). Só gera economia se há lucro tributável.

## Tributos (Brasil — simplificado; confirmar com contador)
| Regime | Como entra no modelo |
|---|---|
| Simples Nacional | Alíquota efetiva **sobre a receita** (`tributos.sobre_receita`), já inclui IRPJ/CSLL → `ir_csll = 0` |
| Lucro Presumido | Tributos sobre receita (PIS/COFINS/ISS) + IR/CSLL sobre base presumida (aproximar como % da receita) |
| Lucro Real | PIS/COFINS/ISS sobre receita (≈ 8,65 % no exemplo) + **IRPJ/CSLL ≈ 34 % sobre o EBIT**, com compensação de prejuízo limitada a 30 % do lucro |

O modelo aplica `ir_csll × lucro tributável`, com `limite_compensacao_prejuizo`. Isso é simplificação: **não substitui parecer tributário**.

## Valor residual e horizonte
Se o produto continua gerando caixa após o horizonte, o horizonte curto subestima o VPL. Teste um horizonte maior como cenário (`horizonte_anos`) e/ou inclua `valor_residual`. Não esconda a escolha: mostre ambos.

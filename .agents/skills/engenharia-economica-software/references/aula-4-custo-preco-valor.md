# Aula 4 — Custo, preço e valor em TI

## Custo
| Tipo | Definição | Exemplos | Cálculo |
|---|---|---|---|
| **Direto** | Atribuível ao projeto sem rateio | Horas da equipe × custo/hora | `custo_direto_equipe(horas, custo_hora, encargos)` |
| **Indireto** | Compartilhado; precisa de rateio | Infra, licenças, aluguel, gestão | `rateio_indireto(total, horas_projeto, horas_totais)` |
| **Fixo** | Não varia com o volume | Hospedagem base, salários | — |
| **Variável** | Varia com clientes/uso | Gateway de pagamento, storage por cliente | — |

Custo/hora de **mercado** valora esforço mesmo quando ninguém foi pago (ex.: TCC): é custo de oportunidade. Diga isso explicitamente. Encargos (CLT ≈ 70–100 %) só se a mão de obra for CLT; PJ/freelancer, 0.

## Preço
### Markup sobre o custo
`Preço = Custo × (1 + k)` · `margem sobre preço m = k/(1+k)` · `k = m/(1−m)`.
Ex.: markup 25 % ⇔ margem 20 % sobre o preço.

### Markup divisor (tudo sobre o preço)
`Preço = Custo / (1 − impostos − comissões − margem)`. Ex.: custo 700, impostos 10 %, margem 20 % → 700/0,70 = **1.000**.
Comando: `econ_cli.py markup --custo 700 --impostos 0.1 --margem 0.2`.

### Preço baseado em valor percebido
`Valor percebido = economia gerada ao cliente (ou receita extra)`. Regra prática: preço entre o **piso** (custo unitário pleno + margem + tributos) e o **teto** (valor percebido). Capturar 20–50 % do valor entregue é comum em SaaS B2B.

```
horas de retrabalho evitadas/mês × custo/hora × redução esperada = valor/mês
```

## Custo unitário em SaaS
`custo unitário/mês = (custos variáveis + fixos + CAC do ano) / (clientes médios × 12)`. É alto no início (poucos clientes diluem custos fixos) e cai com a escala — por isso o preço pode ficar abaixo do custo pleno nos primeiros anos; isso é um **investimento de crescimento**, deve ser explícito.

## Armadilhas
- Precificar só por custo ignora a disposição a pagar (deixa dinheiro na mesa ou perde mercado).
- Confundir markup com margem (25 % ≠ 20 %).
- Esquecer tributos e comissões no preço.
- Ratear indiretos por critério arbitrário; use horas ou nº de clientes e documente.

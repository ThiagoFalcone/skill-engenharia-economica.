# Aulas 3 e 5: Valor do dinheiro no tempo (TVM), TMA e fluxo de caixa

## Fórmulas (todas implementadas em `scripts/econ_core.py`)
| Conceito | Fórmula | Função / comando |
|---|---|---|
| Valor futuro (pagamento único) | `VF = VP·(1+i)^n` | `valor_futuro` · `equivalencia --vp` |
| Valor presente (pagamento único) | `VP = VF/(1+i)^n` | `valor_presente` · `equivalencia --vf` |
| VP de série uniforme | `VP = PMT·[1−(1+i)^−n]/i` | `vp_serie_uniforme` · `equivalencia --pmt` |
| VF de série uniforme | `VF = PMT·[(1+i)^n−1]/i` | `vf_serie_uniforme` |
| Parcela equivalente a um VP | `PMT = VP·i/[1−(1+i)^−n]` | `pmt_de_vp` |
| Conversão de taxa composta | `i₂ = (1+i₁)^(d₂/d₁) − 1` | `taxa_equivalente` · `taxa` |

Exemplo: 18 % a.a. ≈ `(1,18)^(1/12) − 1 = 1,39 % a.m.` (não 18/12 = 1,5 %, que é taxa proporcional/nominal).

## Equivalência financeira
Valores só são comparáveis na **mesma data**. R$ 1.000 hoje ≠ R$ 1.000 em 3 anos. Dois fluxos são equivalentes se têm o mesmo VP à mesma taxa.

## Taxa Mínima de Atratividade (TMA)
Menor retorno aceitável; representa o **custo de oportunidade** do capital. Referências para compor: taxa livre de risco (ex.: Selic/Tesouro) + prêmio de risco do projeto (+ inflação se o fluxo é nominal). Projetos de software em estágio inicial costumam usar prêmio alto. **Sempre justifique a TMA e atualize com a taxa vigente.** Se o usuário não informar, proponha um valor e rotule como premissa.

## Fluxo de caixa de projeto de software
Estrutura anual (ano 0 = hoje):

```
Receita bruta
(−) Tributos sobre a receita
(−) Custos variáveis
(−) Custos fixos (OpEx)
(−) Aquisição de clientes (CAC)
= EBITDA
(−) Depreciação/amortização        <- não é caixa; só afeta o imposto
= EBIT
(−) IRPJ/CSLL sobre o EBIT (com compensação de prejuízo)
→ Fluxo operacional = EBITDA − IR    (depreciação "volta" porque não é desembolso)
(−) CapEx (ano 0 e reinvestimentos)
(+) Valor residual (último ano)
= Fluxo de caixa líquido
```

### CapEx × OpEx em software
- **CapEx (investimento capitalizável):** desenvolvimento inicial do produto, compra de servidores, licenças perpétuas, migração. É amortizado/depreciado.
- **OpEx (despesa operacional):** hospedagem, assinaturas, suporte, manutenção corretiva, marketing, salários recorrentes.
- Fase de pesquisa → despesa; fase de desenvolvimento de produto com viabilidade comprovada → pode ser capitalizada (CPC 04). Confirme com contador.

## Como usar
`econ_cli.py modelo --arquivo entrada.json` ou `gerar_relatorio.py` constroem o fluxo a partir do JSON (`econ_core.construir_fluxo`). Pressupostos do modelo: valores correntes, receita pela média de clientes no ano, depreciação linear, compensação de prejuízo com limite percentual.

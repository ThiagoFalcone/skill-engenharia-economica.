# Formato do arquivo de entrada (JSON)

Modelo para copiar: `assets/modelo-entrada.json`. Exemplo preenchido: `examples/tcc-input.json` na raiz do repositório.
Seções opcionais podem ser omitidas; o relatório pula as seções correspondentes. Chaves obrigatórias: `projeto`, `desenvolvimento`, `modelo`.

## `projeto`
`nome`, `descricao`, `stack`, `hospedagem_atual` (textos); `metricas_medidas_no_repositorio` (opcional: `java_main_linhas`, `java_teste_linhas`, `frontend_ts_tsx_linhas`, `migrations_flyway`, `testes_backend_readme`, `verificacoes_api_e2e_readme`, `testes_ui_e2e_readme`, …) usado para tamanho e COCOMO de referência; `origem_dos_numeros`.

## `desenvolvimento`
| Campo | Significado |
|---|---|
| `equipe[]` | `{papel, horas, custo_hora}` |
| `encargos` | % sobre mão de obra (0.0 se PJ/mercado) |
| `custos_indiretos` | `{total_periodo, horas_totais_base_rateio}` → rateio por horas |
| `outros_investimentos` | `{descricao: valor}` (jurídico, marca, setup) |
| `usar_custo_real_do_gva` | `true` → mão de obra direta = soma do `real` das sprints (em vez do orçado) |

## `gva_sprints` (opcional)
`bac` e `sprints[]` com `{sprint, planejado, agregado, real}` em R$ **por sprint** (não acumulado).

## `modelo` (núcleo financeiro)
| Campo | Significado |
|---|---|
| `horizonte_anos` | anos de operação analisados (ano 0 = investimento) |
| `tma` | taxa mínima de atratividade anual (0.18 = 18 %) |
| `ajustes` | multiplicadores `fator_clientes`, `fator_preco`, `fator_custos`, `fator_capex` (padrão 1.0) |
| `investimento.itens` | `{nome: valor}` adicional ao calculado em `desenvolvimento`; `vida_util_anos` (depreciação linear), `valor_residual` |
| `receita.preco_mensal` | preço por cliente/mês no ano 1 |
| `receita.reajuste_anual` | reajuste de preço por ano |
| `receita.clientes_fim_ano[]` | clientes ao final de cada ano (se a lista for menor que o horizonte repete o último) |
| `receita.churn_mensal` | cancelamento mensal (gera reposição de clientes no CAC) |
| `custos.variavel_pct_receita` | % da receita (gateway, comissão) |
| `custos.variavel_por_cliente_mes` | R$ por cliente/mês |
| `custos.fixos_anuais` | `{nome: número \| lista por ano}` |
| `custos.cac` | R$ por cliente novo (novos = crescimento líquido + reposição de churn) |
| `tributos.sobre_receita` | alíquota sobre a receita (Simples/PIS/COFINS/ISS) |
| `tributos.ir_csll` | alíquota sobre o EBIT positivo (0 no Simples) |
| `tributos.limite_compensacao_prejuizo` | fração do lucro que pode ser abatida por prejuízo acumulado |
| `cenarios` | `{nome: override}` — merge profundo no modelo (ex.: `{"ajustes":{"fator_clientes":0.7}}`) |
| `tma_justificativa` | texto exibido no relatório |

Para modelar economia de custos (em vez de receita) use `preco_mensal` × `clientes` como "usuários internos beneficiados" ou, mais simples, zere a receita e informe a economia como receita equivalente em um cliente único (`clientes_fim_ano: [1,1,…]`, `preco_mensal` = economia mensal; o ano 1 usa a média de 0,5 cliente, então a economia do primeiro ano é metade).

## `valor_percebido` (opcional)
`horas_retrabalho_por_mes_organizacao`, `custo_hora`, `reducao_esperada`, `margem_alvo_para_preco_minimo`.

## `alternativas_infraestrutura` (opcional)
`descricao`, `alternativas[]` com `nome`, `investimento`, `custo_anual` (número ou lista), `vida`, `valor_residual`, `observacao`.

## `backlog_roadmap` (opcional)
Lista de `{nome, valor, esforco, valor_negocio, criticidade_tempo, reducao_risco, tamanho}`.

## `qualidade_bom_o_suficiente` (opcional)
`descricao`, `niveis[]` com `{nome, custo, beneficio}` **acumulados**.

## `hipoteses_e_riscos` (opcional)
Lista de textos exibidos na seção final.

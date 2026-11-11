# Coleta de dados para a valoração

## Perguntas ao usuário (faça só as que faltam, agrupadas)
**Esforço e custo do desenvolvimento**
1. Quantas pessoas, por quantas semanas e horas/semana? Há registro de horas por sprint?
2. Qual o custo/hora de mercado de cada papel (ou salário + encargos)?
3. Custos indiretos: licenças, domínio, hospedagem de homologação, ferramentas?
4. Quanto foi realmente gasto/entregue por sprint (para o GVA)?

**Receita ou benefício**
5. Quem paga e como (assinatura por organização/usuário, licença, serviço)? Preço pretendido?
6. Quantos clientes em 1, 2, 3… anos (conservador)? Churn esperado?
7. Se for ferramenta interna: quantas horas/mês economiza × custo/hora?

**Operação**
8. Hospedagem hoje e quando escala? Quem faz suporte e quantas horas? Manutenção evolutiva (h/ano)?
9. Marketing/vendas e CAC estimado?

**Contexto financeiro**
10. TMA (taxa de referência) e horizonte (anos)? Regime tributário (Simples, Presumido, Real)?

Se o usuário não souber, **proponha valores de mercado conservadores, rotule como "estimativa" e peça validação**. Nunca apresente estimativa como dado.

## Medir o tamanho do software em um repositório (somente leitura)
Use contagens simples, sem alterar o projeto: nº de arquivos e linhas de código de produção × testes por linguagem (ex.: `find … -name '*.java' | xargs wc -l`), nº de migrações de banco, nº de módulos/funcionalidades, testes automatizados e CI/CD, infraestrutura (Docker, deploy), README. Exclua dependências e artefatos gerados (`node_modules`, `target`, `dist`).

Use o tamanho para **sanidade** do esforço: `econ_cli.py cocomo --kloc <milhares de linhas>` dá uma referência (COCOMO básico), costuma superestimar projetos que usam frameworks modernos e IA; justifique a diferença em vez de forçar o número.

## Fontes de mercado (citar no relatório)
Custo/hora: pesquisas salariais de TI (guias de remuneração, Glassdoor, Robert Half), convertidas para custo/hora (÷ ~160 h/mês, + encargos se CLT). Preço: concorrentes diretos e planos públicos. Juros: Selic/Tesouro vigentes. Tributos: tabela do Simples Nacional/contador. Sempre indique data da consulta.

## Esforço real a partir do histórico do GitHub
Quando o projeto tem repositório, o esforço deixa de ser chute: `python scripts/historico_git.py --repo dono/nome --cache pasta --saida historico.json` baixa commits e pull requests e calcula:
- **Horas medidas** pelo método git-hours (commits do mesmo autor com intervalo menor que 120 minutos formam uma sessão; cada sessão ganha 120 minutos de bônus). É um **piso**, pois pesquisa, reuniões, testes manuais e planejamento não geram commit.
- **Horas estimadas** = horas medidas ÷ `--cobertura` (fração do esforço que gera commit; premissa, padrão 20%). Mostre a sensibilidade do investimento a essa premissa.
- **Sprints** em janelas de 14 dias, com **valor agregado** pelos pull requests entregues (ponderados pelas linhas alteradas, ignorando merges e releases) e **custo real** pelas horas da janela.
- **Valor planejado** linear, a partir de `--horas-semana-pessoa` (plano da equipe). Se existir o plano real das sprints, substitua.

Limitações a declarar: quem não faz commit (testes manuais, pesquisa, documentação) não aparece nas horas medidas; histórico com squash ou commits grandes subestima o esforço; o plano linear é uma simplificação. Sem rede, use `--cache` com os arquivos `commits.json` e `prs.json` já baixados.

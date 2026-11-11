# Engenharia Econômica Agêntica

**Skill de valoração e viabilidade financeira de projetos de software**, no padrão aberto [Agent Skills](https://agentskills.io), com Claude Code como plataforma principal.

![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Dependências](https://img.shields.io/badge/dependências-0-brightgreen) ![Testes](https://img.shields.io/badge/testes-61-brightgreen) ![Licença](https://img.shields.io/badge/licença-MIT-lightgrey)

| | |
|---|---|
| **Integrantes** | Thiago Matheus Honório Ribeiro Pinheiro, Gubio Garcia, Luiz Fernando |
| **Disciplina** | Engenharia Econômica, Faculdade SENAI FATESG, Bacharelado em Engenharia de Software |
| **Docente** | Msc. Ujeverson Tavares Sampaio |
| **Apresentação** | [`docs/apresentacao-workshop.pdf`](docs/apresentacao-workshop.pdf) (18 slides) e [`docs/roteiro-workshop.md`](docs/roteiro-workshop.md) |
| **Relatório do TCC** | [`examples/tcc-valuation-report.md`](examples/tcc-valuation-report.md) |

## 1. O que é

Uma Agent Skill que ensina um LLM a fazer **valoração e análise de viabilidade de software** de forma repetível e auditável. O modelo de linguagem **orquestra** (coleta dados, monta o modelo, interpreta e recomenda), mas **todo número sai de scripts Python determinísticos** (`econ_core.py`), nunca de cálculo de cabeça. Ela ajuda líderes técnicos, Product Owners e desenvolvedores a calcular, projetar e defender o valor econômico de um produto.

## 2. Conformidade com a atividade

Cada exigência do PDF da situação de aprendizagem e onde ela está atendida:

| Exigência do professor | Onde está | Situação |
|---|---|---|
| Repositório público no GitHub | Este repositório | Atendido |
| Pasta da skill com `SKILL.md` (YAML válido e instruções procedurais) | [`.agents/skills/engenharia-economica-software/SKILL.md`](.agents/skills/engenharia-economica-software/SKILL.md) | Atendido (validado com parser YAML) |
| `scripts/` com Python documentado | `econ_core.py`, `econ_cli.py`, `gerar_relatorio.py` | Atendido (docstrings, 0 dependências) |
| `references/` e `assets/` | 9 referências por aula e 5 modelos JSON de entrada | Atendido |
| Divulgação progressiva em 3 camadas | Catálogo (name e description), corpo do `SKILL.md` com menos de 5.000 tokens, referências e scripts sob demanda | Atendido (limites verificados em teste) |
| README: descrição e propósito | Seções 1 e 3 | Atendido |
| README: plataforma suportada | Seção 4 | Atendido |
| README: instalação, carregamento e permissões | Seção 5 | Atendido |
| README: exemplos de prompts de acionamento | Seção 6 | Atendido |
| README: demonstração sobre o TCC | Seção 7 | Atendido |
| Relatório em `examples/tcc-valuation-report.md` com fluxo de caixa, VPL, TIR, payback, GVA e modelo de negócio | Seções 4, 5, 8 e 12 do relatório | Atendido |
| Conteúdo das Aulas 1 a 12 | Tabela da seção 3 | Atendido |
| Mini workshop com demonstração ao vivo | Slides em PDF e roteiro com banco de perguntas | Material pronto |
| Estimativas reais de esforço e premissas de mercado | Esforço medido no histórico do GitHub (`examples/dados/`) e premissas com fonte na seção 15 do relatório | Atendido com ressalvas declaradas (ver seção 7) |

**Como cada critério de avaliação é sustentado:**

| Critério (peso) | Evidência no repositório |
|---|---|
| Fundamentação em engenharia econômica (3,0) | 61 testes com valores conferidos à mão, inclusive casos de borda (sem TIR, várias TIR, divisão por zero) |
| Engenharia e arquitetura da skill (2,5) | Validação automática de YAML, tamanho do corpo, referências citadas e cópia `.claude` idêntica à canônica |
| Documentação e repositório (1,5) | Este README, `CONTRIBUTING.md`, `CHANGELOG.md`, CI no GitHub em Python 3.9 e 3.12 |
| Aplicação prática no TCC (1,5) | Relatório com 15 seções, esforço medido no histórico real do GitHub, premissas com fonte e reprodução byte a byte por comando |
| Mini workshop (1,5) | `docs/roteiro-workshop.md` com tempos por bloco, defesa e 10 perguntas prováveis |

## 3. Cobertura das Aulas 1 a 12

| Aulas | Tema | O que a skill entrega |
|---|---|---|
| 1 e 2 | Decisão e alternativas | Alternativas incluindo "não fazer", trade-offs técnicos e orçamentários, CAUE |
| 3 e 5 | TVM e fluxo de caixa | VP, VF, séries uniformes, conversão de taxas, TMA, fluxo anual com CapEx e OpEx |
| 4 | Custo, preço e valor | Custo direto e indireto (rateio), markup, markup divisor, preço versus valor percebido |
| 6 e 8 | Viabilidade, valuation, tributos e depreciação | VPL, TIR, TIRM, payback simples e descontado, IL, ROI, CAC, LTV, depreciação linear e por soma de dígitos, IRPJ/CSLL com compensação de prejuízo |
| 7 | Proposta econômica | Sumário executivo, painel de decisão, cenários, sensibilidade, ponto de equilíbrio, riscos e hipóteses |
| 9 | GVA / EVM | VP, VA, CR, IDC, IDP, variações, EAC (3 variantes), ETC, VAC e IDCP por sprint |
| 10 a 12 | Estratégia e priorização | Legado e infraestrutura por CAUE, "bom o suficiente" por análise marginal, valor por esforço e WSJF |

### Diferenciais desta skill

- **Painel de decisão com semáforo:** oito critérios (VPL, TIR, payback, LTV/CAC, payback do CAC, cenário pessimista, IDC e IDP) classificados em bom, atenção ou crítico.
- **Leitura por perfil de decisor:** o mesmo resultado explicado ao investidor, ao Product Owner e ao líder técnico.
- **Honestidade por construção:** veredito em três níveis (viável, no limite, não viável) e recusa explícita a ajustar premissa só para o VPL ficar positivo.
- **Ponto de equilíbrio e preço de equilíbrio** calculados por bisseção, mais sensibilidade em formato tornado.
- **Esforço real a partir do histórico do GitHub:** o `historico_git.py` mede horas (git-hours), sprints e valor entregue por pull requests, e o GVA nasce desses dados.
- **Integração entre GVA e fluxo de caixa:** o custo real das sprints vira o CapEx do modelo.
- **Fontes e confiança declaradas:** cada premissa de mercado traz fonte, data da consulta e nível de confiança (seção 15 do relatório).
- **Gráfico em texto** do fluxo acumulado dentro do próprio Markdown.
- **Reprodutibilidade:** o relatório versionado é regenerado no CI e comparado byte a byte.
- **Sem dependências:** só biblioteca padrão do Python, funcionando em qualquer agente.

```mermaid
flowchart LR
    U[Pedido do usuário] --> A[Agente carrega SKILL.md]
    A --> D[Coleta dados e monta o JSON de entrada]
    D --> S[Scripts Python determinísticos]
    S --> R[Relatório Markdown e resumo de 5 linhas]
    A -. sob demanda .-> F[references: teoria por aula]
    F --> A
```

## 4. Plataforma suportada

| Plataforma | Suporte | Onde instalar |
|---|---|---|
| **Claude Code** (escolha da equipe) | Estrutura de skill do Claude Code | `.claude/skills/` (projeto) ou `~/.claude/skills/` (global) |
| **Genérica, padrão Agent Skills** | Fonte canônica do repositório | `.agents/skills/` |
| Gemini CLI, ChatGPT Codex, GitHub Copilot, Cursor, Roo Code | Compatível pelo padrão (`SKILL.md` e scripts); copie a pasta para o diretório de skills do agente | Ver seção 5.4 |

Requisitos: **Python 3.9 ou superior** (nada a instalar com `pip`) e permissão do agente para executar `python`.

## 5. Instalação, carregamento e permissões (Claude Code)

### 5.1 Clonar e instalar
```bash
git clone https://github.com/ThiagoFalcone/skill-engenharia-economica..git
```
```bash
cd skill-engenharia-economica.
```
```bash
python instalar.py --destino claude-projeto
```
O repositório já traz `.claude/skills/engenharia-economica-software/`. Abrindo o Claude Code **dentro desta pasta**, a skill é descoberta sem instalar nada. Para usar em qualquer projeto, rode `python instalar.py --destino claude-global`. No Windows use `py instalar.py ...` se `python` não estiver no PATH.

### 5.2 Carregar
1. Abra o Claude Code na pasta (`claude`) e peça uma análise financeira. O nome e a descrição da skill (camada 1, cerca de 100 tokens) ficam no catálogo.
2. Quando o pedido combina com a descrição, o Claude lê o `SKILL.md` (camada 2) e só abre `references/*.md` e executa `scripts/*.py` (camada 3) se o fluxo exigir.
3. Também dá para invocar direto com `/engenharia-economica-software`.

### 5.3 Permissões
A skill executa scripts Python locais, então o agente pede permissão para `python`. Para não ser perguntado a cada cálculo, adicione em `.claude/settings.json`:
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
Os scripts só leem o JSON informado e gravam o `.md` de saída. Não acessam a rede nem alteram outros arquivos.

### 5.4 Outras plataformas
Copie `.agents/skills/engenharia-economica-software/` para o diretório de skills do agente (`python instalar.py --destino pasta --caminho <diretório>`) ou para `~/.agents/skills/` com `--destino agents-global`. Se o agente não suportar skills nativamente, use o `SKILL.md` como instrução de sistema e deixe-o executar `scripts/econ_cli.py`.

## 6. Como acionar (exemplos de prompts)

```text
Faça a valoração econômica do meu projeto: 3 devs, 288 h cada a R$ 55/h, SaaS a R$ 179/mês, TMA 16%.
Calcule VPL, TIR e payback do fluxo -80000, 20000, 35000, 50000 com TMA de 15%.
Compare nuvem gerenciada, on-premises e VM gratuita por CAUE com TMA de 16%.
Calcule IDC, IDP e EAC: BAC 120 mil, planejado 60 mil, agregado 48 mil, custo real 54 mil.
Priorize o backlog por WSJF e diga até onde vale investir em qualidade de testes.
Monte a proposta econômica (sumário executivo, cenários e riscos) deste projeto.
```

Esforço real de um repositório (usa a API pública do GitHub):
```bash
python .agents/skills/engenharia-economica-software/scripts/historico_git.py --repo GubioGarcia/Plataforma-Governanca-Software --cache examples/dados --saida historico.json
```

Uso direto dos scripts, sem agente:
```bash
cd .agents/skills/engenharia-economica-software/scripts
python econ_cli.py indicadores --taxa 0.15 --fluxos -80000 20000 35000 50000
python econ_cli.py gva --planejado 60000 --agregado 48000 --real 54000 --bac 120000
python econ_cli.py priorizar --arquivo ../assets/exemplo-backlog.json --metodo wsjf
python gerar_relatorio.py --entrada ../assets/modelo-entrada.json --saida relatorio.md
```

## 7. Demonstração prática: valoração do TCC da equipe

O TCC avaliado é a **Plataforma de Governança de Projetos de Software** (Java 21 com Spring Boot 4, React 19, Keycloak, PostgreSQL; 28,5 mil linhas medidas no repositório, 284 testes de backend, 232 verificações de API e 70 testes de interface), desenvolvida por **3 pessoas** com ferramentas gratuitas e um pouco de Claude pago, sprints planejadas com o orientador. Foi tratada como produto SaaS B2B por organização, a **R$ 179 por mês**.

**Esforço real, medido no GitHub.** O script `historico_git.py` leu o [repositório do TCC](https://github.com/GubioGarcia/Plataforma-Governanca-Software): 132 commits de 10/03 a 02/11/2026 (34 semanas) e 26 pull requests de entrega. Pelo método git-hours são **103,5 h medidas** (Gubio 94,4 h, Thiago 9,1 h), um piso, porque pesquisa, testes manuais e reuniões não geram commit. Com cobertura de 20% (premissa explícita) o esforço estimado é **517,5 h**, a R$ 50 por hora. O histórico também revelou uma pausa de 8 semanas sem commits (junho e julho), que derruba o IDP no GVA. Os dados ficam em [`examples/dados/`](examples/dados/) para qualquer pessoa reproduzir.

Reprodução do relatório completo:
```bash
python .agents/skills/engenharia-economica-software/scripts/gerar_relatorio.py --entrada examples/tcc-input.json --saida examples/tcc-valuation-report.md
```

| Indicador (caso-base, 5 anos, TMA de 17%) | Resultado |
|---|---|
| Esforço | 103,5 h medidas, 517,5 h estimadas, custo real de R$ 25.866 (BAC do plano de R$ 30.471) |
| Investimento inicial (CapEx) | R$ 31.266 |
| VPL | **R$ 24.456** |
| TIR | **29,3%** (TMA de 17%) |
| Payback simples e descontado | 4,02 anos e 4,46 anos |
| Veredito | **Viável**; payback descontado em atenção e cenário pessimista negativo |
| Ponto de equilíbrio | 86% do volume de clientes ou 89% do preço |
| Cenário otimista | VPL de R$ 117.264 e TIR de 64,6% |
| Cenário pessimista | VPL de -R$ 64.818 |
| Lucro Real (34% de IRPJ/CSLL) e Simples Anexo V (15,5%) | VPL de R$ 5.866 e R$ 4.003 |
| Horizonte de 7 anos | VPL de R$ 138.913 e TIR de 52,1% |
| LTV/CAC e payback do CAC | 14,6 e 2,3 meses |
| GVA ao fim das 17 janelas | IDC 1,18, IDP 1,00, EAC de R$ 25.866; o IDP caiu de 0,54 para 0,34 na pausa de commits |
| Hospedagem (CAUE em 5 anos) | VM Oracle Always Free R$ 4.069 por ano; nuvem gerenciada R$ 21.589; on-premises R$ 22.227 |
| Qualidade ("bom o suficiente") | Parar nos testes de interface automatizados; mutação e 100% de cobertura custam mais do que entregam |

**Leitura honesta:** o projeto se paga, mas o resultado depende de preço, volume e custos (variar cada um em 20% muda o VPL em R$ 67 a 87 mil) e o cenário pessimista é negativo.

**Premissas de mercado com fonte** (seção 15 do relatório, consultadas em 11/11/2026): Selic de 13,75% (Copom, a confirmar no Banco Central), faixa salarial de desenvolvedor pleno da Robert Half com fator de senioridade de 0,7, preço do Jira Standard (cerca de US$ 7,91 por usuário) como âncora de preço, churn de 3% a 5% ao mês para SaaS B2B de pequenas e médias empresas e as faixas do Simples Nacional. Várias fontes são blogs; a confiança de cada uma está declarada.

> **Transparência.** São **medidos**: tamanho do código, histórico de commits e pull requests. São **estimados com fonte**: cobertura de commits (20%), custo por hora, preço, clientes, churn, CAC, custos de operação e TMA. O **plano das sprints com o orientador** não estava disponível, então o valor planejado do GVA é linear (6 h por semana por pessoa); com o plano real, basta informá-lo. Luiz Fernando não tem commits e seu esforço está embutido na cobertura.

## 8. Estrutura do repositório

```
.agents/skills/engenharia-economica-software/   skill canônica (padrão Agent Skills)
  SKILL.md                    frontmatter YAML e instruções procedurais (camadas 1 e 2)
  scripts/                    camada 3, Python determinístico
    econ_core.py              fórmulas das aulas 1 a 12
    econ_cli.py               16 comandos: vpl, tir, payback, gva, markup, saas, comparar, priorizar...
    gerar_relatorio.py        relatório Markdown completo a partir de um JSON
    historico_git.py          esforço, sprints e valor entregue a partir do histórico do GitHub
  references/                 teoria e critérios de decisão, um arquivo por tema das aulas
  assets/                     modelo-entrada.json e 4 exemplos de entrada do CLI
.claude/skills/...            cópia para o Claude Code (gerada por instalar.py)
examples/                     tcc-input.json, tcc-valuation-report.md e dados/ (snapshot do histórico do TCC)
evals/evals.json              10 casos de avaliação (7 numéricos, verificados por teste)
tests/                        61 testes: fórmulas, CLI, estrutura da skill, relatório e evals
docs/                         roteiro do workshop, slides em PDF e o gerador dos slides
instalar.py                   instalador (Claude Code e genérico)
```

## 9. Qualidade e validação

```bash
python -m unittest discover -s tests -v
```
- **Fórmulas** conferidas contra valores calculados à mão (VPL, TIR que zera o VPL, payback interpolado, CAUE, markup divisor, GVA, WSJF), inclusive casos de borda.
- **Especificação Agent Skills:** `name` válido e igual ao diretório, `description` com até 1024 caracteres, corpo do `SKILL.md` com menos de 500 linhas e cerca de 5.000 tokens, todas as referências citadas existentes.
- **Reprodutibilidade:** o relatório versionado é regenerado e comparado byte a byte, localmente e no CI do GitHub.
- **Evals:** [`evals/evals.json`](evals/evals.json) com prompts, critérios e respostas numéricas esperadas, reexecutadas contra o motor.
- **Teste independente:** um agente iniciado sem contexto, apenas com o `SKILL.md`, calculou VPL, GVA e o relatório do TCC e recusou manipular premissas. Os atritos que ele encontrou (caminhos, `null` no payback, qual EAC reportar) foram corrigidos na skill.

## 10. Limitações conhecidas
- Modelo anual, em valores correntes (TMA nominal), com tributos simplificados. Não substitui parecer de contador.
- Compensação de prejuízo fiscal com limite percentual, sem outros incentivos fiscais.
- A valoração por fluxo de caixa descontado depende de premissas de mercado que precisam de validação com clientes reais.
- Receita calculada pela média de clientes do ano (aproximação).

## 11. Contribuição e padrão Git
Mensagens de commit seguem o [Conventional Commits](https://www.conventionalcommits.org/pt-br/) e o versionamento é semântico. Detalhes em [`CONTRIBUTING.md`](CONTRIBUTING.md); histórico de versões em [`CHANGELOG.md`](CHANGELOG.md).

## 12. Licença
MIT, ver [LICENSE](LICENSE).

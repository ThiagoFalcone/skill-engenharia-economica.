# Changelog

## [1.1.0] - 2026-11-11
### Adicionado
- `historico_git.py`: esforço medido (git-hours), sprints e valor entregue por pull requests a partir do histórico do GitHub.
- 4 testes novos (61 no total) e valoração do TCC com esforço real (132 commits, 26 pull requests), seção 3.0 de evidências e seção 15 de fontes de mercado com data e confiança.
- Cenário `simples_anexo_v` para o risco tributário.

### Alterado
- GVA do TCC calculado do histórico real, em vez de valores ilustrativos; TMA de 17% com base na Selic.

## [1.0.0] - 2026-11-11
### Adicionado
- Skill `engenharia-economica-software` no padrão Agent Skills, com `SKILL.md`, 9 referências por aula e 5 modelos JSON.
- Scripts Python determinísticos: `econ_core.py`, `econ_cli.py` (16 comandos) e `gerar_relatorio.py`.
- Relatório de valoração com 14 seções, incluindo painel de decisão com semáforo, gráfico em texto e leitura por perfil de decisor.
- Valoração do TCC (`examples/`), 10 evals, 57 testes e CI em Python 3.9 e 3.12.
- Apresentação do workshop em PDF (18 slides) e roteiro com banco de perguntas.

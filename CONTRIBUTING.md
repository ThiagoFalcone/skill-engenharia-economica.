# Contribuindo

## Mensagens de commit (Conventional Commits)
Formato: `tipo(escopo opcional): descrição no imperativo, em português`

| Tipo | Quando usar |
|---|---|
| `feat` | nova capacidade da skill, do CLI ou do relatório |
| `fix` | correção de cálculo ou de comportamento |
| `docs` | README, referências, roteiro e slides |
| `test` | novos testes ou evals |
| `refactor` | mudança interna sem alterar resultado |
| `ci` | workflow do GitHub Actions |
| `chore` | manutenção (gitignore, instalador, dependências) |

Exemplos: `feat(relatorio): adicionar painel de decisão com semáforo`, `fix(gva): tratar custo real igual a zero`.

## Fluxo de trabalho
1. Crie uma branch a partir de `main` (`feat/nome`, `fix/nome`, `docs/nome`).
2. Rode `python -m unittest discover -s tests` antes de abrir o pull request.
3. Se mudou a skill, rode `python instalar.py --destino claude-projeto` para sincronizar a cópia `.claude` (um teste confere isso).
4. Se mudou dados ou o gerador do relatório, regenere `examples/tcc-valuation-report.md` e `docs/apresentacao-workshop.pdf`.

## Versionamento
Semântico (`MAJOR.MINOR.PATCH`) com tags `vX.Y.Z`. As mudanças ficam em `CHANGELOG.md`.

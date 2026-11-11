# Aula 7: Propostas econômicas de software

Objetivo: permitir que uma pessoa que decide (diretoria, investidor, cliente) aprove ou recuse com base em números e riscos **transparentes**.

## Estrutura do sumário executivo (1 página)
1. **Veredito** em uma frase: viável / no limite / não viável, e por quê.
2. **Números-chave:** investimento, TMA, VPL, TIR, payback (simples e descontado), ROI, ponto de equilíbrio.
3. **Decisão pedida** (o que se quer aprovar) e a alternativa "não fazer".
4. **Cenários** (pessimista, base, otimista) lado a lado.
5. **Principais riscos** e como mitigar; **hipóteses** que, se falsas, derrubam o resultado.
6. **Próximos passos** com marcos (o que validar antes de gastar mais, gates de decisão).

## Justificativa de ROI
- ROI descontado = `VPL / VP das saídas`.
- Apresente também o **ponto de equilíbrio** (volume ou preço em que VPL = 0): é mais útil que o ROI isolado. Comando: `modelo` (campo `fator_clientes_equilibrio`).

## Transparência de riscos e hipóteses
Para cada hipótese: valor usado, origem (medido/estimado/benchmark), impacto no VPL (tornado da sensibilidade) e plano de validação. Ordene pela **amplitude** da sensibilidade: valide primeiro o que mais move o VPL.

## Escrita
- Números sempre com unidade (R$, %, anos).
- Sem adjetivos vagos ("excelente retorno"); use o indicador.
- Separe fatos de premissas com marcação visível.
- Não omita cenário ruim. Uma proposta crível mostra onde falha.

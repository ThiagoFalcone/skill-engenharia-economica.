# Relatório de valoração econômica, Plataforma de Governança de Projetos de Software

> Gerado pela skill `engenharia-economica-software` (cálculos determinísticos em `scripts/econ_core.py`).
> **Aviso:** todos os valores de mercado e de esforço são **premissas estimadas** listadas na seção 13; o resultado é tão confiável quanto essas premissas.

## 1. Sumário executivo (Aula 7)

**VIÁVEL** nas premissas do caso-base: VPL positivo e TIR acima da TMA.

| Indicador | Resultado |
|---|---|
| Investimento inicial (ano 0) | R$ 31.266 |
| TMA adotada | 17,0% |
| VPL | R$ 24.456 |
| TIR | 29,3% |
| TIR modificada (TIRM) | 26,8% |
| Payback simples | 4,02 anos |
| Payback descontado | 4,46 anos |
| Índice de lucratividade (VP entradas / VP saídas) | 1,497 |
| ROI descontado (VPL / VP das saídas) | 49,7% |
| Fluxo acumulado nominal em 5 anos | R$ 97.520 |

**Painel de decisão** (semáforo calculado dos números; ✅ bom, ⚠️ atenção, ❌ crítico):

| Critério | Resultado | Sinal | Regra |
|---|---|---|---|
| VPL > 0 | R$ 24.456 | ✅ | bom se > 5% do investimento |
| TIR > TMA | 29,3% vs 17,0% | ✅ | bom se 3 pontos acima da TMA |
| Payback descontado no horizonte | 4,46 anos | ⚠️ | bom se em até 70% do horizonte |
| LTV/CAC ≥ 3 | 14,6 | ✅ | referência de mercado |
| Payback do CAC ≤ 12 meses | 2,3 meses | ✅ | recuperação rápida do CAC |
| Cenário pessimista com VPL ≥ 0 | -R$ 64.818 | ❌ | resiliência a premissas ruins |
| IDC final ≥ 1 | 1,18 | ✅ | custo versus valor entregue |
| IDP final ≥ 1 | 1,00 | ✅ | prazo versus planejado |

**Ponto de equilíbrio:** com os demais parâmetros fixos, o VPL zera com **86% do volume de clientes** do caso-base (≈ 86 organizações pagantes no fim do ano 5).

**Preço de equilíbrio:** o VPL zera com preço a 89% do praticado (≈ R$ 158,79/mês no ano 1).

Principais riscos e hipóteses: ver seção 13.

## 2. Decisão e alternativas (Aulas 1 e 2)

**Decisão:** comercializar a plataforma como SaaS B2B (investindo R$ 31.266 no ano 0 e arcando com a operação) **versus** não comercializar e aplicar o capital à TMA de 17,0% (custo de oportunidade).

**Produto avaliado:** SaaS B2B de apoio ao discovery e à elicitação de requisitos: organizações, projetos, requisitos com aprovação formal, rastreabilidade, modelagem de dados, solicitações, auditoria, analytics e pesquisa de avaliação.  
**Stack:** Java 21 + Spring Boot 4, React 19 + TypeScript, Keycloak, PostgreSQL 15, Docker/Nginx  
**Hospedagem atual:** VM Oracle Cloud Always Free com HTTPS (Let's Encrypt)

**Tamanho medido no repositório:** 28,5 mil linhas (6.005 Java de produção, 2.076 Java de testes, 20.397 TS/TSX), 6 migrations, 284 testes de backend, 232 verificações de API e 70 testes de interface.  
Referência COCOMO básico (modo orgânico): 80,8 pessoa-mês e 13,3 meses, o esforço estimado (518 h ≈ 3,2 pessoa-mês) fica bem abaixo, coerente com o uso de frameworks e ferramentas modernas, mas é um ponto a defender (seção 13).

## 3. Custo, preço e valor (Aula 4)

### 3.0 Evidência real: esforço medido no histórico do GitHub

Fonte: https://github.com/GubioGarcia/Plataforma-Governanca-Software (snapshot em `examples/dados/`). Período de 2026-03-10 a 2026-11-02 (33,9 semanas), 132 commits e 26 pull requests de entrega (de 30, excluídos os de integração).

| Autor | Commits | Dias ativos | Horas medidas (git-hours) |
|---|---|---|---|
| GubioGarcia | 123 | 34 | 94,4 |
| ThiagoFalcone | 9 | 4 | 9,1 |
| **Total medido** | **132** |  | **103,5** |

**Método:** git-hours (commits com intervalo menor que 120 min formam uma sessão; cada sessão ganha 120 min de bônus). As horas medidas são um **piso**: pesquisa, reuniões, testes manuais e planejamento não geram commit. Com cobertura de 20% (premissa), o esforço estimado é **517,5 h** (172 h por pessoa), a R$ 50/h = R$ 25.875.

| Sprint | Início | Commits | Horas medidas | PRs entregues | Peso da entrega |
|---|---|---|---|---|---|
| 1 | 2026-03-10 | 10 | 2,8 | nenhum | 0,0% |
| 2 | 2026-03-24 | 6 | 8,2 | #1 | 3,6% |
| 3 | 2026-04-07 | 10 | 8,6 | #4, #3, #2 | 5,0% |
| 4 | 2026-04-21 | 3 | 6,0 | nenhum | 0,0% |
| 5 | 2026-05-05 | 3 | 6,0 | #5 | 13,6% |
| 6 | 2026-05-19 | 4 | 7,3 | nenhum | 0,0% |
| 7 | 2026-06-02 | 7 | 5,0 | nenhum | 0,0% |
| 8 | 2026-06-16 | 0 | 0,0 | nenhum | 0,0% |
| 9 | 2026-06-30 | 0 | 0,0 | nenhum | 0,0% |
| 10 | 2026-07-14 | 0 | 0,0 | nenhum | 0,0% |
| 11 | 2026-07-28 | 0 | 0,0 | nenhum | 0,0% |
| 12 | 2026-08-11 | 2 | 2,4 | nenhum | 0,0% |
| 13 | 2026-08-25 | 10 | 12,3 | #12, #11, #10, #9, #8 | 24,4% |
| 14 | 2026-09-08 | 3 | 4,2 | #13 | 4,1% |
| 15 | 2026-09-22 | 16 | 11,0 | #14 | 0,5% |
| 16 | 2026-10-06 | 26 | 13,2 | #17, #15 | 29,2% |
| 17 | 2026-10-20 | 32 | 16,6 | #29, #28, #27, #26, #25, #24, #23, #22, #21, #20, #19, #18 | 19,7% |

As janelas 8 a 11 não têm nenhum commit (pausa no desenvolvimento), o que pesa no IDP da seção 8.

### 3.1 Custos diretos e indiretos do desenvolvimento

| Papel | Horas | Custo/hora | Custo direto |
|---|---|---|---|
| Equipe de 3 pessoas (horas estimadas a partir do histórico do GitHub) | 518 | R$ 50 | R$ 25.875 |
| **Total estimado** | **518** |  | **R$ 25.875** |

Custo real acumulado (CR): **R$ 25.866**, 15,1% abaixo do orçamento do plano (BAC de R$ 30.471); usado como investimento direto no modelo.

| Item de investimento (CapEx, ano 0) | Valor | Natureza |
|---|---|---|
| Mão de obra direta | R$ 25.866 | Direto |
| Custos indiretos rateados por horas | R$ 1.400 | Indireto (rateio) |
| Lançamento e adequação jurídica (LGPD, termos de uso, marca) | R$ 4.000 | Outro |
| **Total** | **R$ 31.266** |  |

O desenvolvimento é tratado como **CapEx** (ativo intangível amortizado em 5 anos); manutenção, hospedagem, suporte e marketing são **OpEx**.

### 3.2 Preço: markup, custo unitário e valor percebido

| Ano | Preço praticado/mês | Custo unitário/mês | Preço mínimo (margem 20% + tributos) | Markup equivalente s/ custo |
|---|---|---|---|---|
| 1 | R$ 179,00 | R$ 551,70 | R$ 755,76 | 25,0% |
| 2 | R$ 187,95 | R$ 254,84 | R$ 349,10 | 25,0% |
| 3 | R$ 197,35 | R$ 164,00 | R$ 224,66 | 25,0% |
| 4 | R$ 207,21 | R$ 124,80 | R$ 170,96 | 25,0% |
| 5 | R$ 217,58 | R$ 104,53 | R$ 143,19 | 25,0% |

Margem de 20% sobre o preço equivale a markup de 25,0% sobre o custo (`k = m/(1-m)`). Nos anos 1, 2 o preço praticado fica abaixo do custo unitário pleno, porque a base de clientes ainda não dilui os custos fixos.

**Valor percebido pelo cliente:** uma organização que gasta 40 h/mês em retrabalho de requisitos a R$ 60/h e reduz 15% economiza **R$ 360/mês**. O preço de R$ 179 captura 50% desse valor, preço ancorado no valor, abaixo do valor entregue.

## 4. Demonstrativo e fluxo de caixa (Aulas 3 e 5)

| Item | Ano 0 | Ano 1 | Ano 2 | Ano 3 | Ano 4 | Ano 5 |
|---|---|---|---|---|---|---|
| Clientes (fim do ano) |  | 5 | 18 | 40 | 70 | 100 |
| Receita bruta |  | R$ 5.370 | R$ 25.937 | R$ 68.677 | R$ 136.762 | R$ 221.927 |
| (−) Tributos sobre a receita |  | -R$ 376 | -R$ 1.816 | -R$ 4.807 | -R$ 9.573 | -R$ 15.535 |
| (−) Custos variáveis |  | -R$ 401 | -R$ 1.882 | -R$ 4.844 | -R$ 9.383 | -R$ 14.818 |
| (−) Custos fixos (OpEx) |  | -R$ 14.400 | -R$ 28.200 | -R$ 42.600 | -R$ 58.200 | -R$ 73.800 |
| (−) Aquisição de clientes (CAC) |  | -R$ 1.750 | -R$ 5.086 | -R$ 9.629 | -R$ 14.786 | -R$ 18.001 |
| **EBITDA** |  | -R$ 11.557 | -R$ 11.046 | R$ 6.796 | R$ 44.819 | R$ 99.774 |
| (−) Depreciação/amortização |  | -R$ 6.253 | -R$ 6.253 | -R$ 6.253 | -R$ 6.253 | -R$ 6.253 |
| **EBIT (lucro operacional)** |  | -R$ 17.810 | -R$ 17.300 | R$ 543 | R$ 38.566 | R$ 93.520 |
| (−) IRPJ/CSLL |  | R$ 0 | R$ 0 | R$ 0 | R$ 0 | R$ 0 |
| (+) Valor residual |  | R$ 0 | R$ 0 | R$ 0 | R$ 0 | R$ 0 |
| (−) Investimento (CapEx) | -R$ 31.266 |  |  |  |  |  |
| **Fluxo de caixa líquido** | **-R$ 31.266** | **-R$ 11.557** | **-R$ 11.046** | **R$ 6.796** | **R$ 44.819** | **R$ 99.774** |

|  | Ano 0 | Ano 1 | Ano 2 | Ano 3 | Ano 4 | Ano 5 |
|---|---|---|---|---|---|---|
| Fluxo acumulado | -R$ 31.266 | -R$ 42.823 | -R$ 53.869 | -R$ 47.073 | -R$ 2.253 | R$ 97.520 |
| Fluxo descontado à TMA | -R$ 31.266 | -R$ 9.878 | -R$ 8.070 | R$ 4.243 | R$ 23.918 | R$ 45.508 |

**Fluxo acumulado (gráfico em texto, R$ mil; █ positivo, ▒ negativo):**

```
Ano 0 | ▒▒▒▒▒▒▒▒▒▒ -31,3
Ano 1 | ▒▒▒▒▒▒▒▒▒▒▒▒▒ -42,8
Ano 2 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -53,9
Ano 3 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -47,1
Ano 4 | ▒ -2,3
Ano 5 | ██████████████████████████████ 97,5
```

Simplificações: valores correntes (TMA nominal), receita pela média de clientes no ano, prejuízo fiscal compensado com o limite informado, depreciação linear sem crédito de impostos quando a alíquota de IRPJ/CSLL é zero.

## 5. Viabilidade: VPL, TIR e Payback (Aulas 3, 5, 6 e 8)

- **VPL** = Σ FCₜ/(1+TMA)ᵗ com TMA = 17,0% → **R$ 24.456**
- **TIR** (taxa que zera o VPL) = **29,3%** (acima da TMA); TIRM com reinvestimento à TMA = 26,8%
- **Payback simples** = 4,02 anos; **descontado** = 4,46 anos
- **Índice de lucratividade** = 1,497 (> 1: cria valor)

**Depreciação (Aula 8):** CapEx de R$ 31.266 amortizado linearmente em 5 anos = R$ 6.253/ano. Com alíquota de IRPJ/CSLL de 0,0% no caso-base, o escudo fiscal anual seria R$ 0; o cenário `lucro_real` (seção 6) quantifica esse efeito.

## 6. Cenários, sensibilidade e equilíbrio (Aulas 7 e 8)

| Cenário | VPL | TIR | Payback simples | Payback descontado |
|---|---|---|---|---|
| base | R$ 24.456 | 29,3% | 4,02 anos | 4,46 anos |
| pessimista | -R$ 64.818 | -32,4% | não recupera no horizonte | não recupera no horizonte |
| otimista | R$ 117.264 | 64,6% | 3,07 anos | 3,35 anos |
| lucro_real | R$ 5.866 | 20,3% | 4,20 anos | 4,83 anos |
| horizonte_7_anos | R$ 138.913 | 52,1% | 4,02 anos | 4,46 anos |
| simples_anexo_v | R$ 4.003 | 19,2% | 4,28 anos | 4,89 anos |

**Sensibilidade (tornado, ±20% em cada fator, VPL):**

| Fator | VPL com −20% | VPL com +20% | Amplitude |
|---|---|---|---|
| Preço | -R$ 18.856 | R$ 67.768 | R$ 86.624 |
| Volume de clientes | -R$ 11.533 | R$ 60.446 | R$ 71.979 |
| Custos operacionais | R$ 58.068 | -R$ 9.155 | R$ 67.223 |
| TMA | R$ 34.287 | R$ 16.173 | R$ 18.115 |
| Investimento inicial | R$ 30.709 | R$ 18.203 | R$ 12.506 |

## 7. Métricas de produto digital: CAC e LTV (Aula 8)

| Métrica | Valor |
|---|---|
| ARPA (receita média por organização/mês) | R$ 179,00 |
| Margem bruta unitária (após tributos e custos variáveis) | 85,5% |
| Churn mensal / anual | 3,0% / 30,6% |
| Vida média do cliente | 33,3 meses |
| LTV = ARPA × margem ÷ churn | R$ 5.103 |
| CAC | R$ 350 |
| LTV/CAC (meta usual ≥ 3) | 14,6  ✅ |
| Payback do CAC | 2,3 meses |

## 8. Eficiência ágil: Gerenciamento de Valor Agregado (Aula 9)

Orçamento total (BAC): R$ 30.471. Dados do histórico do GitHub (2026-03-10 a 2026-11-02): custo real = horas medidas por commit ÷ cobertura de 20% × custo/hora; valor agregado = pull requests entregues ponderados pelas linhas alteradas; valor planejado linear (plano de 6 h por semana por pessoa, premissa).

| Sprint | VP | VA | CR | IDC | IDP | EAC (BAC/IDC) |
|---|---|---|---|---|---|---|
| 1 | R$ 1.792 | R$ 0 | R$ 700 | 0,00 | 0,00 | n/d |
| 2 | R$ 3.585 | R$ 1.099 | R$ 2.738 | 0,40 | 0,31 | R$ 75.876 |
| 3 | R$ 5.377 | R$ 2.611 | R$ 4.888 | 0,53 | 0,49 | R$ 57.039 |
| 4 | R$ 7.170 | R$ 2.611 | R$ 6.388 | 0,41 | 0,36 | R$ 74.542 |
| 5 | R$ 8.962 | R$ 6.754 | R$ 7.888 | 0,86 | 0,75 | R$ 35.590 |
| 6 | R$ 10.755 | R$ 6.754 | R$ 9.720 | 0,69 | 0,63 | R$ 43.854 |
| 7 | R$ 12.547 | R$ 6.754 | R$ 10.968 | 0,62 | 0,54 | R$ 49.487 |
| 8 | R$ 14.340 | R$ 6.754 | R$ 10.968 | 0,62 | 0,47 | R$ 49.487 |
| 9 | R$ 16.132 | R$ 6.754 | R$ 10.968 | 0,62 | 0,42 | R$ 49.487 |
| 10 | R$ 17.924 | R$ 6.754 | R$ 10.968 | 0,62 | 0,38 | R$ 49.487 |
| 11 | R$ 19.717 | R$ 6.754 | R$ 10.968 | 0,62 | 0,34 | R$ 49.487 |
| 12 | R$ 21.509 | R$ 6.754 | R$ 11.560 | 0,58 | 0,31 | R$ 52.156 |
| 13 | R$ 23.302 | R$ 14.183 | R$ 14.629 | 0,97 | 0,61 | R$ 31.428 |
| 14 | R$ 25.094 | R$ 15.431 | R$ 15.667 | 0,98 | 0,61 | R$ 30.937 |
| 15 | R$ 26.887 | R$ 15.577 | R$ 18.411 | 0,85 | 0,58 | R$ 36.015 |
| 16 | R$ 28.679 | R$ 24.470 | R$ 21.721 | 1,13 | 0,85 | R$ 27.048 |
| 17 | R$ 30.471 | R$ 30.471 | R$ 25.866 | 1,18 | 1,00 | R$ 25.866 |

**Leitura final (sprint 17):** IDC = 1,18 (eficiente em custo), IDP = 1,00 (no prazo ou adiantado). Variação de custos = R$ 4.606; variação de prazo = -R$ 0.  
EAC (desvio persistente) = R$ 25.866; EAC (desvio atípico) = R$ 25.866; EAC (IDC×IDP) = R$ 25.866; ETC = R$ 0; VAC = R$ 4.606.

*Previsão no meio do projeto (sprint 8):* EAC = R$ 49.487 contra o BAC de R$ 30.471, a coluna EAC mostra como a previsão converge para o custo final.

## 9. Alternativas de infraestrutura e substituição (Aulas 1, 2, 10 e 11)

Decisão de hospedagem em produção (aulas 1, 2, 10 e 11): comparadas por CAUE em 5 anos, com a TMA do modelo.

| # | Alternativa | VP dos custos | CAUE (custo anual equivalente) | Observação |
|---|---|---|---|---|
| 1 | VM Oracle Cloud Always Free (atual) | R$ 13.018 | R$ 4.069 | Custo quase zero, mas sem SLA contratual e com limite de recursos; exige 60 h/ano de administração. |
| 2 | Nuvem gerenciada (containers + banco gerenciado) | R$ 69.071 | R$ 21.589 | Escala e SLA, custo cresce com o uso. |
| 3 | Servidor on-premises | R$ 71.112 | R$ 22.227 | CapEx alto, energia, link e administração; valor residual do hardware. |

**Melhor custo econômico:** VM Oracle Cloud Always Free (atual). Decisão final deve pesar também SLA, escala e risco (critérios não monetários).

## 10. Priorização econômica do backlog (Aulas 10 a 12)

**Valor ÷ Esforço** (valor 1–10, esforço em pontos):

| # | Item | Valor | Esforço | Score | Quadrante |
|---|---|---|---|---|---|
| 1 | Notificações por e-mail e alertas | 6 | 3 | 2,00 | quick_win |
| 2 | Templates de projeto (onboarding) | 6 | 3 | 2,00 | quick_win |
| 3 | Relatório executivo em PDF | 5 | 3 | 1,67 | preenchimento |
| 4 | SSO corporativo (OIDC/SAML via Keycloak) | 7 | 5 | 1,40 | quick_win |
| 5 | Cobrança e planos (billing) | 9 | 8 | 1,12 | projeto_estrategico |
| 6 | Backup/DR e monitoramento | 5 | 5 | 1,00 | preenchimento |
| 7 | API pública e webhooks | 5 | 8 | 0,62 | evitar |
| 8 | Integração Jira/GitHub Issues | 8 | 13 | 0,62 | projeto_estrategico |
| 9 | Sugestão de requisitos com IA | 7 | 13 | 0,54 | projeto_estrategico |
| 10 | Aplicativo móvel (PWA) | 4 | 13 | 0,31 | evitar |

**WSJF** = (valor de negócio + criticidade de tempo + redução de risco) ÷ tamanho:

| # | Item | Custo do atraso | Tamanho | WSJF |
|---|---|---|---|---|
| 1 | Templates de projeto (onboarding) | 14 | 3 | 4,67 |
| 2 | Notificações por e-mail e alertas | 13 | 3 | 4,33 |
| 3 | Backup/DR e monitoramento | 18 | 5 | 3,60 |
| 4 | SSO corporativo (OIDC/SAML via Keycloak) | 16 | 5 | 3,20 |
| 5 | Relatório executivo em PDF | 9 | 3 | 3,00 |
| 6 | Cobrança e planos (billing) | 20 | 8 | 2,50 |
| 7 | API pública e webhooks | 10 | 8 | 1,25 |
| 8 | Integração Jira/GitHub Issues | 14 | 13 | 1,08 |
| 9 | Sugestão de requisitos com IA | 13 | 13 | 1,00 |
| 10 | Aplicativo móvel (PWA) | 7 | 13 | 0,54 |

## 11. Princípio “bom o suficiente” e custo de oportunidade (Aulas 10 a 12)

Níveis acumulados de investimento em qualidade de testes (custo) versus perdas evitadas por incidentes e retrabalho (benefício), em R$ ao longo do horizonte.

| Nível | Custo acum. | Benefício acum. | Δ custo | Δ benefício | Compensa? | Líquido |
|---|---|---|---|---|---|---|
| Testes unitários das regras de negócio | R$ 5.000 | R$ 18.000 | R$ 5.000 | R$ 18.000 | sim | R$ 13.000 |
| + testes de API/integração ponta a ponta | R$ 9.000 | R$ 30.000 | R$ 4.000 | R$ 12.000 | sim | R$ 21.000 |
| + testes de interface automatizados (Playwright) | R$ 15.000 | R$ 36.000 | R$ 6.000 | R$ 6.000 | sim | R$ 21.000 |
| + mutação, carga e cobertura próxima de 100 % | R$ 30.000 | R$ 40.000 | R$ 15.000 | R$ 4.000 | não | R$ 10.000 |

**Recomendação (regra marginal Δbenefício ≥ Δcusto):** parar em “+ testes de interface automatizados (Playwright)”. Primeiro nível de maior benefício líquido: “+ testes de API/integração ponta a ponta”. O nível seguinte (“+ mutação, carga e cobertura próxima de 100 %”) acrescenta menos benefício do que custo: é perfeccionismo, não valor.

## 12. Proposta de modelo de negócio

- **Modelo:** SaaS B2B por organização, assinatura mensal (ARPA-base R$ 179), com planos Starter (1 projeto ativo, poucos membros), Pro (projetos ilimitados, pesquisa de avaliação e exportações) e Enterprise (SSO, SLA, suporte dedicado, sob consulta).
- **Canal e aquisição:** inbound com conteúdo de elicitação de requisitos, parcerias com instituições de ensino (plano educacional gratuito como geração de demanda) e outbound para consultorias e fábricas de software; CAC-alvo de R$ 350 (LTV/CAC = 14,6).
- **Precificação:** ancorada no valor percebido (seção 3.2) e validada contra o piso de custo + margem.
- **Alavancas de VPL** (pela sensibilidade): preço, volume de clientes, custos operacionais.
- **Próximos passos:** validar o preço com 5–10 organizações-piloto, medir churn real, migrar a hospedagem para uma opção com SLA ao primeiro cliente pagante e acompanhar o IDC/IDP das próximas releases.

## 13. Hipóteses, premissas e riscos (Aula 7)

- TMA: Selic de 13,75% a.a. (Copom, nov/2026, a confirmar no site do Banco Central) + prêmio de risco de produto digital em estágio inicial de cerca de 3,25 pontos percentuais = 17% a.a.
- Preço, clientes, churn e CAC são premissas ancoradas em fontes públicas, mas não validadas com clientes pagantes.
- As horas medidas (103,5 h) são um piso derivado dos horários dos commits; a cobertura de 20% (horas estimadas = 517,5 h) é premissa e entra na sensibilidade do investimento.
- Luiz Fernando não tem commits próprios no repositório; ele editou documentos, contribuiu com ideias e com parte do código, e esse esforço está embutido na cobertura de 20% e não em horas próprias.
- O plano das sprints com o orientador não estava disponível: o valor planejado é linear, com 6 horas por semana por pessoa. Substitua pelo plano real para um GVA exato.
- O custo por hora de mercado valora o esforço (custo de oportunidade), não é desembolso: a equipe não foi remunerada.
- A hospedagem gratuita não tem SLA; vender como SaaS exige migrar ou contratar suporte.
- O enquadramento tributário real depende de contador; o cenário simples_anexo_v mostra o risco de cair no Anexo V.
- Fluxos em valores correntes e TMA nominal; sem inflação além do reajuste anual do preço.

## 14. Leitura por perfil de decisor

- **Investidor:** investir R$ 31.266 hoje dá VPL de R$ 24.456 a 17,0% a.a. (TIR 29,3%), com payback descontado de 4,46 anos. O risco principal é a variável preço; no cenário pessimista o VPL é -R$ 64.818.
- **Product Owner:** o preço de R$ 179/mês dá LTV/CAC de 14,6; a prioridade do roadmap é Templates de projeto (onboarding) (maior WSJF).
- **Líder técnico:** IDC final 1,18 e IDP 1,00 indicam custo sob controle e prazo cumprido; a hospedagem de menor custo é VM Oracle Cloud Always Free (atual), e o investimento em qualidade deve parar quando o benefício marginal não cobre o custo.

## 15. Fontes e evidências

Consulta às fontes em 11/11/2026. Evidência medida: histórico do GitHub e tamanho do código do TCC. Fontes de mercado: valores públicos, com a confiança que o autor atribuiu a cada uma.

| Tema | Dado usado | Fonte | Confiança |
|---|---|---|---|
| Taxa básica de juros (base da TMA) | Selic de 13,75% a.a. mantida pelo Copom em novembro de 2026; antes, 15% (jan/2026) e 14% (ago/2026) | [JB Economia; Infomoney](https://www.infomoney.com.br/economia/banco-central-copom-decisao-selic-05082026/) | média: notícias; confirmar no comunicado do Copom em bcb.gov.br |
| Custo por hora da equipe | Desenvolvedor pleno: mediana de R$ 11.350 (Brasília, back-end) a R$ 12.000 (Porto Alegre e Curitiba) por mês, ou cerca de R$ 71 a 75 por hora; com fator de senioridade de 0,7 para equipe estudantil, R$ 50 por hora | [Robert Half, tabelas salariais por cidade](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno/brasilia) | média: faixas por cidade, amostra e data não confirmadas; o fator 0,7 é premissa da equipe |
| Preço de referência (concorrente) | Jira Standard a cerca de US$ 7,91 por usuário por mês (US$ 79 para 10 usuários); o preço de R$ 179 por organização é plano único para a equipe | [Atlassian e blogs de preços (valores divergem por faixa de usuários)](https://www.atlassian.com/software/jira/pricing) | média: página oficial inconsistente nas buscas; conferir o valor vigente |
| Churn mensal | SaaS B2B para pequenas e médias empresas: 3% a 5% ao mês é típico, 2,5% a 5% é considerado bom; o modelo usa 3% | [Lenny's Newsletter e blogs de benchmarks](https://www.lennysnewsletter.com/p/monthly-churn-benchmarks) | baixa a média: fontes secundárias que citam umas às outras |
| Tributação | Simples Nacional Anexo III: 6% até R$ 180 mil de receita em 12 meses e 11,2% com dedução de R$ 9.360 até R$ 360 mil; serviços de TI com Fator R abaixo de 28% caem no Anexo V (15,5%) | [Agilize e Conta Azul (tabelas do Simples Nacional); LC 123/2006](https://agilize.com.br/artigos/?p=470) | média: confirmar com contador |
| Hospedagem gratuita | VM Oracle Cloud Always Free sem custo de infraestrutura e sem SLA contratual (README e deploy do próprio TCC) | [Repositório do TCC](https://github.com/GubioGarcia/Plataforma-Governanca-Software) | alta (medido) |

---
*Reprodução:* `python .agents/skills/engenharia-economica-software/scripts/gerar_relatorio.py --entrada examples/tcc-input.json --saida examples/tcc-valuation-report.md`

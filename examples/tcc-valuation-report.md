# Relatório de valoração econômica, Plataforma de Governança de Projetos de Software

> Gerado pela skill `engenharia-economica-software` (cálculos determinísticos em `scripts/econ_core.py`).
> **Aviso:** todos os valores de mercado e de esforço são **premissas estimadas** listadas na seção 13; o resultado é tão confiável quanto essas premissas.

## 1. Sumário executivo (Aula 7)

**VIÁVEL** nas premissas do caso-base: VPL positivo e TIR acima da TMA, porém **no limite** (|VPL| ≤ 5% do investimento): pequenas mudanças de premissa invertem a decisão.

| Indicador | Resultado |
|---|---|
| Investimento inicial (ano 0) | R$ 55.800 |
| TMA adotada | 16,0% |
| VPL | R$ 1.941 |
| TIR | 16,7% |
| TIR modificada (TIRM) | 16,6% |
| Payback simples | 4,28 anos |
| Payback descontado | 4,96 anos |
| Índice de lucratividade (VP entradas / VP saídas) | 1,026 |
| ROI descontado (VPL / VP das saídas) | 2,6% |
| Fluxo acumulado nominal em 5 anos | R$ 72.473 |

**Painel de decisão** (semáforo calculado dos números; ✅ bom, ⚠️ atenção, ❌ crítico):

| Critério | Resultado | Sinal | Regra |
|---|---|---|---|
| VPL > 0 | R$ 1.941 | ⚠️ | bom se > 5% do investimento |
| TIR > TMA | 16,7% vs 16,0% | ⚠️ | bom se 3 pontos acima da TMA |
| Payback descontado no horizonte | 4,96 anos | ⚠️ | bom se em até 70% do horizonte |
| LTV/CAC ≥ 3 | 14,8 | ✅ | referência de mercado |
| Payback do CAC ≤ 12 meses | 2,3 meses | ✅ | recuperação rápida do CAC |
| Cenário pessimista com VPL ≥ 0 | -R$ 95.189 | ❌ | resiliência a premissas ruins |
| IDC final ≥ 1 | 0,94 | ⚠️ | custo versus valor entregue |
| IDP final ≥ 1 | 1,00 | ✅ | prazo versus planejado |

**Ponto de equilíbrio:** com os demais parâmetros fixos, o VPL zera com **99% do volume de clientes** do caso-base (≈ 99 organizações pagantes no fim do ano 5).

**Preço de equilíbrio:** o VPL zera com preço a 99% do praticado (≈ R$ 177,47/mês no ano 1).

Principais riscos e hipóteses: ver seção 13.

## 2. Decisão e alternativas (Aulas 1 e 2)

**Decisão:** comercializar a plataforma como SaaS B2B (investindo R$ 55.800 no ano 0 e arcando com a operação) **versus** não comercializar e aplicar o capital à TMA de 16,0% (custo de oportunidade).

**Produto avaliado:** SaaS B2B de apoio ao discovery e à elicitação de requisitos: organizações, projetos, requisitos com aprovação formal, rastreabilidade, modelagem de dados, solicitações, auditoria, analytics e pesquisa de avaliação.  
**Stack:** Java 21 + Spring Boot 4, React 19 + TypeScript, Keycloak, PostgreSQL 15, Docker/Nginx  
**Hospedagem atual:** VM Oracle Cloud Always Free com HTTPS (Let's Encrypt)

**Tamanho medido no repositório:** 28,5 mil linhas (6.005 Java de produção, 2.076 Java de testes, 20.397 TS/TSX), 6 migrations, 284 testes de backend, 232 verificações de API e 70 testes de interface.  
Referência COCOMO básico (modo orgânico): 80,8 pessoa-mês e 13,3 meses, o esforço declarado (864 h ≈ 5,4 pessoa-mês) fica bem abaixo, coerente com o uso de frameworks e ferramentas modernas, mas é um ponto a defender (seção 13).

## 3. Custo, preço e valor (Aula 4)

### 3.1 Custos diretos e indiretos do desenvolvimento

| Papel | Horas | Custo/hora | Custo direto |
|---|---|---|---|
| Desenvolvedor full stack / arquitetura | 288 | R$ 60 | R$ 17.280 |
| Desenvolvedor backend / DevOps | 288 | R$ 55 | R$ 15.840 |
| Desenvolvedor frontend / testes | 288 | R$ 50 | R$ 14.400 |
| **Total orçado (BAC)** | **864** |  | **R$ 47.520** |

Custo real acumulado nas sprints (CR): **R$ 50.400** (6,1% sobre o orçamento), usado como investimento direto no modelo.

| Item de investimento (CapEx, ano 0) | Valor | Natureza |
|---|---|---|
| Mão de obra direta | R$ 50.400 | Direto |
| Custos indiretos rateados por horas | R$ 1.400 | Indireto (rateio) |
| Lançamento e adequação jurídica (LGPD, termos de uso, marca) | R$ 4.000 | Outro |
| **Total** | **R$ 55.800** |  |

O desenvolvimento é tratado como **CapEx** (ativo intangível amortizado em 5 anos); manutenção, hospedagem, suporte e marketing são **OpEx**.

### 3.2 Preço: markup, custo unitário e valor percebido

| Ano | Preço praticado/mês | Custo unitário/mês | Preço mínimo (margem 20% + tributos) | Markup equivalente s/ custo |
|---|---|---|---|---|
| 1 | R$ 179,00 | R$ 571,70 | R$ 772,57 | 25,0% |
| 2 | R$ 187,95 | R$ 261,36 | R$ 353,19 | 25,0% |
| 3 | R$ 197,35 | R$ 167,45 | R$ 226,29 | 25,0% |
| 4 | R$ 207,21 | R$ 126,62 | R$ 171,11 | 25,0% |
| 5 | R$ 217,58 | R$ 105,70 | R$ 142,84 | 25,0% |

Margem de 20% sobre o preço equivale a markup de 25,0% sobre o custo (`k = m/(1-m)`). Nos anos 1, 2 o preço praticado fica abaixo do custo unitário pleno, porque a base de clientes ainda não dilui os custos fixos.

**Valor percebido pelo cliente:** uma organização que gasta 40 h/mês em retrabalho de requisitos a R$ 60/h e reduz 15% economiza **R$ 360/mês**. O preço de R$ 179 captura 50% desse valor, preço ancorado no valor, abaixo do valor entregue.

## 4. Demonstrativo e fluxo de caixa (Aulas 3 e 5)

| Item | Ano 0 | Ano 1 | Ano 2 | Ano 3 | Ano 4 | Ano 5 |
|---|---|---|---|---|---|---|
| Clientes (fim do ano) |  | 5 | 18 | 40 | 70 | 100 |
| Receita bruta |  | R$ 5.370 | R$ 25.937 | R$ 68.677 | R$ 136.762 | R$ 221.927 |
| (−) Tributos sobre a receita |  | -R$ 322 | -R$ 1.556 | -R$ 4.121 | -R$ 8.206 | -R$ 13.316 |
| (−) Custos variáveis |  | -R$ 401 | -R$ 1.882 | -R$ 4.844 | -R$ 9.383 | -R$ 14.818 |
| (−) Custos fixos (OpEx) |  | -R$ 15.000 | -R$ 29.100 | -R$ 43.800 | -R$ 59.400 | -R$ 75.000 |
| (−) Aquisição de clientes (CAC) |  | -R$ 1.750 | -R$ 5.086 | -R$ 9.629 | -R$ 14.786 | -R$ 18.001 |
| **EBITDA** |  | -R$ 12.103 | -R$ 11.687 | R$ 6.283 | R$ 44.987 | R$ 100.793 |
| (−) Depreciação/amortização |  | -R$ 11.160 | -R$ 11.160 | -R$ 11.160 | -R$ 11.160 | -R$ 11.160 |
| **EBIT (lucro operacional)** |  | -R$ 23.263 | -R$ 22.847 | -R$ 4.877 | R$ 33.827 | R$ 89.633 |
| (−) IRPJ/CSLL |  | R$ 0 | R$ 0 | R$ 0 | R$ 0 | R$ 0 |
| (+) Valor residual |  | R$ 0 | R$ 0 | R$ 0 | R$ 0 | R$ 0 |
| (−) Investimento (CapEx) | -R$ 55.800 |  |  |  |  |  |
| **Fluxo de caixa líquido** | **-R$ 55.800** | **-R$ 12.103** | **-R$ 11.687** | **R$ 6.283** | **R$ 44.987** | **R$ 100.793** |

|  | Ano 0 | Ano 1 | Ano 2 | Ano 3 | Ano 4 | Ano 5 |
|---|---|---|---|---|---|---|
| Fluxo acumulado | -R$ 55.800 | -R$ 67.903 | -R$ 79.590 | -R$ 73.307 | -R$ 28.320 | R$ 72.473 |
| Fluxo descontado à TMA | -R$ 55.800 | -R$ 10.434 | -R$ 8.685 | R$ 4.025 | R$ 24.846 | R$ 47.989 |

**Fluxo acumulado (gráfico em texto, R$ mil; █ positivo, ▒ negativo):**

```
Ano 0 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -55,8
Ano 1 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -67,9
Ano 2 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -79,6
Ano 3 | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ -73,3
Ano 4 | ▒▒▒▒▒▒▒▒▒▒▒ -28,3
Ano 5 | ███████████████████████████ 72,5
```

Simplificações: valores correntes (TMA nominal), receita pela média de clientes no ano, prejuízo fiscal compensado com o limite informado, depreciação linear sem crédito de impostos quando a alíquota de IRPJ/CSLL é zero.

## 5. Viabilidade: VPL, TIR e Payback (Aulas 3, 5, 6 e 8)

- **VPL** = Σ FCₜ/(1+TMA)ᵗ com TMA = 16,0% → **R$ 1.941**
- **TIR** (taxa que zera o VPL) = **16,7%** (acima da TMA); TIRM com reinvestimento à TMA = 16,6%
- **Payback simples** = 4,28 anos; **descontado** = 4,96 anos
- **Índice de lucratividade** = 1,026 (> 1: cria valor)

**Depreciação (Aula 8):** CapEx de R$ 55.800 amortizado linearmente em 5 anos = R$ 11.160/ano. Com alíquota de IRPJ/CSLL de 0,0% no caso-base, o escudo fiscal anual seria R$ 0; o cenário `lucro_real` (seção 6) quantifica esse efeito.

## 6. Cenários, sensibilidade e equilíbrio (Aulas 7 e 8)

| Cenário | VPL | TIR | Payback simples | Payback descontado |
|---|---|---|---|---|
| base | R$ 1.941 | 16,7% | 4,28 anos | 4,96 anos |
| pessimista | -R$ 95.189 | -36,2% | não recupera no horizonte | não recupera no horizonte |
| otimista | R$ 100.409 | 45,7% | 3,33 anos | 3,78 anos |
| lucro_real | -R$ 18.121 | 8,6% | 4,56 anos | não recupera no horizonte |
| horizonte_7_anos | R$ 124.172 | 39,5% | 4,28 anos | 4,96 anos |

**Sensibilidade (tornado, ±20% em cada fator, VPL):**

| Fator | VPL com −20% | VPL com +20% | Amplitude |
|---|---|---|---|
| Preço | -R$ 43.395 | R$ 47.277 | R$ 90.672 |
| Volume de clientes | -R$ 35.834 | R$ 39.716 | R$ 75.549 |
| Custos operacionais | R$ 37.223 | -R$ 33.341 | R$ 70.564 |
| Investimento inicial | R$ 13.101 | -R$ 9.219 | R$ 22.320 |
| TMA | R$ 11.643 | -R$ 6.302 | R$ 17.945 |

## 7. Métricas de produto digital: CAC e LTV (Aula 8)

| Métrica | Valor |
|---|---|
| ARPA (receita média por organização/mês) | R$ 179,00 |
| Margem bruta unitária (após tributos e custos variáveis) | 86,5% |
| Churn mensal / anual | 3,0% / 30,6% |
| Vida média do cliente | 33,3 meses |
| LTV = ARPA × margem ÷ churn | R$ 5.163 |
| CAC | R$ 350 |
| LTV/CAC (meta usual ≥ 3) | 14,8  ✅ |
| Payback do CAC | 2,3 meses |

## 8. Eficiência ágil: Gerenciamento de Valor Agregado (Aula 9)

Orçamento total (BAC): R$ 47.520. Valores de EXEMPLO em R$ por sprint, coerentes com 3 pessoas e muitas horas de teste manual (retrabalho no início eleva o custo real). Substitua pelos registros do quadro, se houver. planejado = valor planejado (VP/PV); agregado = valor agregado (VA/EV, escopo realmente entregue valorizado ao custo orçado); real = custo real (CR/AC).

| Sprint | VP | VA | CR | IDC | IDP | EAC (BAC/IDC) |
|---|---|---|---|---|---|---|
| 1 | R$ 3.960 | R$ 2.600 | R$ 3.300 | 0,79 | 0,66 | R$ 60.314 |
| 2 | R$ 7.920 | R$ 6.100 | R$ 7.300 | 0,84 | 0,77 | R$ 56.868 |
| 3 | R$ 11.880 | R$ 10.000 | R$ 11.500 | 0,87 | 0,84 | R$ 54.648 |
| 4 | R$ 15.840 | R$ 14.100 | R$ 15.800 | 0,89 | 0,89 | R$ 53.249 |
| 5 | R$ 19.800 | R$ 18.300 | R$ 20.200 | 0,91 | 0,92 | R$ 52.454 |
| 6 | R$ 23.760 | R$ 22.600 | R$ 24.700 | 0,91 | 0,95 | R$ 51.936 |
| 7 | R$ 27.720 | R$ 26.900 | R$ 29.100 | 0,92 | 0,97 | R$ 51.406 |
| 8 | R$ 31.680 | R$ 30.900 | R$ 33.400 | 0,93 | 0,98 | R$ 51.365 |
| 9 | R$ 35.640 | R$ 35.000 | R$ 37.700 | 0,93 | 0,98 | R$ 51.186 |
| 10 | R$ 39.600 | R$ 39.300 | R$ 42.100 | 0,93 | 0,99 | R$ 50.906 |
| 11 | R$ 43.560 | R$ 43.500 | R$ 46.400 | 0,94 | 1,00 | R$ 50.688 |
| 12 | R$ 47.520 | R$ 47.520 | R$ 50.400 | 0,94 | 1,00 | R$ 50.400 |

**Leitura final (sprint 12):** IDC = 0,94 (abaixo de 1: gastou mais do que o valor entregue), IDP = 1,00 (no prazo ou adiantado). Variação de custos = -R$ 2.880; variação de prazo = R$ 0.  
EAC (desvio persistente) = R$ 50.400; EAC (desvio atípico) = R$ 50.400; EAC (IDC×IDP) = R$ 50.400; ETC = R$ 0; VAC = -R$ 2.880.

*Previsão no meio do projeto (sprint 6):* EAC = R$ 51.936 contra o BAC de R$ 47.520, a coluna EAC mostra como a previsão converge para o custo final.

## 9. Alternativas de infraestrutura e substituição (Aulas 1, 2, 10 e 11)

Decisão de hospedagem em produção (aulas 1, 2, 10 e 11): comparadas por CAUE em 5 anos, com a TMA do modelo.

| # | Alternativa | VP dos custos | CAUE (custo anual equivalente) | Observação |
|---|---|---|---|---|
| 1 | VM Oracle Cloud Always Free (atual) | R$ 13.287 | R$ 4.058 | Custo quase zero, mas sem SLA contratual e com limite de recursos; exige 60 h/ano de administração. |
| 2 | Nuvem gerenciada (containers + banco gerenciado) | R$ 70.808 | R$ 21.626 | Escala e SLA, custo cresce com o uso. |
| 3 | Servidor on-premises | R$ 71.911 | R$ 21.962 | CapEx alto, energia, link e administração; valor residual do hardware. |

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
- **Canal e aquisição:** inbound com conteúdo de elicitação de requisitos, parcerias com instituições de ensino (plano educacional gratuito como geração de demanda) e outbound para consultorias e fábricas de software; CAC-alvo de R$ 350 (LTV/CAC = 14,8).
- **Precificação:** ancorada no valor percebido (seção 3.2) e validada contra o piso de custo + margem.
- **Alavancas de VPL** (pela sensibilidade): preço, volume de clientes, custos operacionais.
- **Próximos passos:** validar o preço com 5–10 organizações-piloto, medir churn real, migrar a hospedagem para uma opção com SLA ao primeiro cliente pagante e acompanhar o IDC/IDP das próximas releases.

## 13. Hipóteses, premissas e riscos (Aula 7)

- TMA: Premissa acadêmica: taxa básica de juros de referência + prêmio de risco de produto digital em estágio inicial (cerca de 16 % a.a.). Atualizar com a taxa vigente.
- Trabalho acadêmico: nenhum número de mercado (preço, clientes, churn, CAC, suporte) foi validado com clientes pagantes; são premissas de exemplo.
- O custo/hora é de mercado (valoração do esforço), não um desembolso: a equipe de 3 estudantes não foi remunerada.
- A maior parte das horas foi de testes manuais; isso aumenta o custo real (IDC < 1) e é um ponto de melhoria (automatizar) discutido em 'bom o suficiente'.
- Os dados de GVA por sprint são ilustrativos; as sprints foram planejadas com o orientador e podem ser substituídas pelos registros reais.
- A hospedagem gratuita não tem SLA; vender como SaaS exige migrar ou contratar suporte.
- A conta-base considera Simples Nacional; o enquadramento tributário real depende de contador.
- Fluxos em valores correntes e TMA nominal; sem inflação além do reajuste anual do preço.

## 14. Leitura por perfil de decisor

- **Investidor:** investir R$ 55.800 hoje dá VPL de R$ 1.941 a 16,0% a.a. (TIR 16,7%), com payback descontado de 4,96 anos. O risco principal é a variável preço; no cenário pessimista o VPL é -R$ 95.189.
- **Product Owner:** o preço de R$ 179/mês dá LTV/CAC de 14,8; a prioridade do roadmap é Templates de projeto (onboarding) (maior WSJF).
- **Líder técnico:** IDC final 0,94 e IDP 1,00 indicam custo acima do valor entregue e prazo cumprido; a hospedagem de menor custo é VM Oracle Cloud Always Free (atual), e o investimento em qualidade deve parar quando o benefício marginal não cobre o custo.

---
*Reprodução:* `python .agents/skills/engenharia-economica-software/scripts/gerar_relatorio.py --entrada examples/tcc-input.json --saida examples/tcc-valuation-report.md`

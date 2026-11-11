"""Testes das fórmulas. Execute: python -m unittest discover -s tests -v"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".agents", "skills",
                                "engenharia-economica-software", "scripts"))
import econ_core as ec  # noqa: E402


class TestTVM(unittest.TestCase):
    def test_vf_vp(self):
        self.assertAlmostEqual(ec.valor_futuro(1000, 0.10, 3), 1331.0, places=6)
        self.assertAlmostEqual(ec.valor_presente(1331, 0.10, 3), 1000.0, places=6)

    def test_serie_uniforme(self):
        # VP de 5 parcelas de 1000 a 10 % = 3790,787...
        self.assertAlmostEqual(ec.vp_serie_uniforme(1000, 0.10, 5), 3790.7868, places=3)
        self.assertAlmostEqual(ec.vf_serie_uniforme(1000, 0.10, 5), 6105.10, places=2)
        self.assertAlmostEqual(ec.pmt_de_vp(3790.7868, 0.10, 5), 1000.0, places=2)
        self.assertEqual(ec.vp_serie_uniforme(100, 0, 4), 400)

    def test_taxa_equivalente(self):
        mensal = ec.taxa_equivalente(0.1268250301, 12, 1)  # anual -> mensal ~ 1 % a.m.
        self.assertAlmostEqual(mensal, 0.01, places=6)
        anual = ec.taxa_equivalente(0.01, 1, 12)  # mensal -> anual
        self.assertAlmostEqual(anual, 1.01 ** 12 - 1, places=9)


class TestViabilidade(unittest.TestCase):
    FLUXO = [-1000, 300, 400, 500, 600]

    def test_vpl(self):
        # a 10 %: -1000 + 272,727 + 330,579 + 375,657 + 409,808 = 388,771
        self.assertAlmostEqual(ec.vpl(0.10, self.FLUXO), 388.7710, places=3)

    def test_tir_zera_vpl(self):
        r = ec.tir(self.FLUXO)
        self.assertIsNotNone(r)
        self.assertAlmostEqual(ec.vpl(r, self.FLUXO), 0.0, places=6)
        self.assertAlmostEqual(r, 0.2488, places=3)

    def test_tir_inexistente(self):
        self.assertIsNone(ec.tir([-100, -50, -10]))
        self.assertIsNone(ec.tir([100, 50]))

    def test_tir_multiplas_raizes(self):
        # -1000, 3000, -2000 => raízes 0 % e 100 %
        raizes = ec.tir_todas([-1000, 3000, -2000])
        self.assertTrue(any(abs(r - 1.0) < 1e-6 for r in raizes))
        self.assertTrue(any(abs(r - 0.0) < 1e-6 for r in raizes))

    def test_payback_simples(self):
        # acumulado: -1000, -700, -300, +200 => 2 + 300/500 = 2,6
        self.assertAlmostEqual(ec.payback(self.FLUXO), 2.6, places=6)

    def test_payback_descontado(self):
        # a 10 %: -1000, -727,27, -396,69, -21,03, +388,77 => 3 + 21,03/409,81
        self.assertAlmostEqual(ec.payback(self.FLUXO, 0.10), 3.0513, places=3)

    def test_payback_nao_recupera(self):
        self.assertIsNone(ec.payback([-1000, 100, 100]))

    def test_indices(self):
        self.assertAlmostEqual(ec.indice_lucratividade(0.10, self.FLUXO), 1.388771, places=5)
        self.assertAlmostEqual(ec.roi_simples(self.FLUXO), 0.8, places=6)
        self.assertAlmostEqual(ec.roi_descontado(0.10, self.FLUXO), 0.388771, places=5)

    def test_tirm(self):
        r = ec.tirm(self.FLUXO, 0.10, 0.10)
        vf_in = 300 * 1.1 ** 3 + 400 * 1.1 ** 2 + 500 * 1.1 + 600
        self.assertAlmostEqual(r, (vf_in / 1000) ** 0.25 - 1, places=9)

    def test_caue(self):
        self.assertAlmostEqual(ec.caue(1000, 0.10, 5), 263.7975, places=3)


class TestAlternativas(unittest.TestCase):
    def test_comparacao_vidas_diferentes(self):
        alts = [
            {"nome": "A", "investimento": 1000, "custo_anual": 100, "vida": 5},
            {"nome": "B", "investimento": 500, "custo_anual": 300, "vida": 2},
        ]
        r = ec.comparar_alternativas(0.10, alts)
        por_nome = {x["nome"]: x for x in r}
        # A: VPL = -(1000 + 100*3,790787) = -1379,0787 -> CAUE = -363,797
        self.assertAlmostEqual(por_nome["A"]["caue"], -363.7975, places=3)
        self.assertAlmostEqual(por_nome["A"]["vp_custos"], 1379.0787, places=3)
        # B: VPL = -(500 + 300*1,735537) = -1020,661 -> CAUE = -588,095
        self.assertAlmostEqual(por_nome["B"]["caue"], -588.0952, places=3)
        self.assertEqual(r[0]["nome"], "A")
        self.assertEqual(r[0]["ranking"], 1)

    def test_valor_residual(self):
        r = ec.comparar_alternativas(0.10, [
            {"nome": "X", "investimento": 1000, "custo_anual": 0, "vida": 1, "valor_residual": 1100}])
        self.assertAlmostEqual(r[0]["vpl"], 0.0, places=9)


class TestPreco(unittest.TestCase):
    def test_markup(self):
        self.assertAlmostEqual(ec.preco_markup(100, 0.5), 150.0)
        self.assertAlmostEqual(ec.markup_para_margem(0.5), 1 / 3, places=9)
        self.assertAlmostEqual(ec.margem_para_markup(0.25), 1 / 3, places=9)

    def test_divisor(self):
        # custo 700, impostos 10 %, margem 20 % => 700/0,7 = 1000
        self.assertAlmostEqual(ec.preco_divisor(700, 0.10, 0.20), 1000.0)
        with self.assertRaises(ValueError):
            ec.preco_divisor(100, 0.6, 0.5)

    def test_custo_direto_indireto(self):
        self.assertAlmostEqual(ec.custo_direto_equipe(100, 50, 0.5), 7500.0)
        self.assertAlmostEqual(ec.rateio_indireto(1000, 100, 400), 250.0)


class TestSaaS(unittest.TestCase):
    def test_ltv_cac(self):
        r = ec.ltv_cac(arpa_mensal=200, margem_bruta=0.8, churn_mensal=0.04, cac=800)
        self.assertAlmostEqual(r["ltv"], 4000.0)
        self.assertAlmostEqual(r["ltv_cac"], 5.0)
        self.assertAlmostEqual(r["payback_cac_meses"], 5.0)
        self.assertAlmostEqual(r["vida_media_meses"], 25.0)

    def test_churn_anual(self):
        self.assertAlmostEqual(ec.churn_anual(0.01), 1 - 0.99 ** 12, places=9)


class TestDepreciacao(unittest.TestCase):
    def test_linear(self):
        self.assertEqual(ec.depreciacao_linear(1000, 5, 0), [200.0] * 5)
        self.assertEqual(ec.depreciacao_linear(1000, 4, 200), [200.0] * 4)

    def test_soma_digitos(self):
        d = ec.depreciacao_soma_digitos(1500, 5, 0)
        self.assertAlmostEqual(sum(d), 1500.0)
        self.assertAlmostEqual(d[0], 500.0)
        self.assertAlmostEqual(d[-1], 100.0)

    def test_escudo(self):
        self.assertEqual(ec.escudo_fiscal([200, 200], 0.34), [68.0, 68.0])

    def test_cocomo(self):
        r = ec.cocomo_basico(10)
        self.assertAlmostEqual(r["esforco_pessoa_mes"], 2.4 * 10 ** 1.05, places=6)


class TestGVA(unittest.TestCase):
    def test_indicadores(self):
        # BAC 1000; VP 400, VA 300, CR 450
        g = ec.gva(400, 300, 450, 1000)
        self.assertAlmostEqual(g["idc"], 300 / 450)
        self.assertAlmostEqual(g["idp"], 0.75)
        self.assertAlmostEqual(g["variacao_custos"], -150)
        self.assertAlmostEqual(g["variacao_prazo"], -100)
        self.assertAlmostEqual(g["eac"], 1500.0)  # 1000 / 0,6667
        self.assertAlmostEqual(g["etc"], 1050.0)
        self.assertAlmostEqual(g["vac"], -500.0)
        self.assertAlmostEqual(g["eac_desvio_atipico"], 1150.0)
        self.assertAlmostEqual(g["idcp"], 700 / 550)
        self.assertAlmostEqual(g["percentual_concluido"], 0.30)

    def test_serie_acumulada(self):
        sprints = [{"planejado": 100, "agregado": 80, "real": 100},
                   {"planejado": 100, "agregado": 120, "real": 100}]
        s = ec.gva_por_sprint(sprints, bac=400)
        self.assertEqual(len(s), 2)
        self.assertAlmostEqual(s[1]["agregado"], 200)
        self.assertAlmostEqual(s[1]["idc"], 1.0)
        self.assertAlmostEqual(s[1]["idp"], 1.0)

    def test_zero_real(self):
        self.assertIsNone(ec.gva(0, 0, 0, 100)["idc"])


class TestPriorizacao(unittest.TestCase):
    def test_valor_esforco(self):
        itens = [{"nome": "A", "valor": 8, "esforco": 2},
                 {"nome": "B", "valor": 9, "esforco": 9},
                 {"nome": "C", "valor": 2, "esforco": 1},
                 {"nome": "D", "valor": 1, "esforco": 8}]
        r = ec.priorizar(itens)
        self.assertEqual([x["nome"] for x in r], ["A", "C", "B", "D"])  # 4, 2, 1, 0,125
        quad = {x["nome"]: x["quadrante"] for x in r}
        self.assertEqual(quad["A"], "quick_win")
        self.assertEqual(quad["B"], "projeto_estrategico")
        self.assertEqual(quad["C"], "preenchimento")
        self.assertEqual(quad["D"], "evitar")

    def test_wsjf(self):
        r = ec.priorizar([
            {"nome": "X", "valor_negocio": 8, "criticidade_tempo": 5, "reducao_risco": 2, "tamanho": 5},
            {"nome": "Y", "valor_negocio": 3, "criticidade_tempo": 3, "reducao_risco": 3, "tamanho": 1}],
            metodo="wsjf")
        self.assertEqual(r[0]["nome"], "Y")  # 9/1 > 15/5
        self.assertAlmostEqual(r[1]["score"], 3.0)

    def test_metodo_invalido(self):
        with self.assertRaises(ValueError):
            ec.priorizar([{"nome": "a", "valor": 1, "esforco": 1}], metodo="x")


class TestBomSuficiente(unittest.TestCase):
    def test_para_quando_marginal_nao_compensa(self):
        niveis = [{"nome": "basico", "custo": 100, "beneficio": 300},
                  {"nome": "bom", "custo": 200, "beneficio": 450},
                  {"nome": "perfeito", "custo": 500, "beneficio": 500}]
        r = ec.bom_o_suficiente(niveis)
        self.assertEqual(r["recomendado_regra_marginal"], "bom")
        self.assertEqual(r["maior_liquido"], "bom")  # líquidos: 200, 250, 0
        self.assertFalse(r["niveis"][2]["compensa"])


class TestModelo(unittest.TestCase):
    def modelo(self):
        return {
            "horizonte_anos": 3, "tma": 0.10,
            "investimento": {"itens": {"dev": 1000}, "vida_util_anos": 4, "valor_residual": 0},
            "receita": {"preco_mensal": 100, "reajuste_anual": 0.0,
                        "clientes_fim_ano": [10, 10, 10], "churn_mensal": 0.0},
            "custos": {"variavel_pct_receita": 0.0, "fixos_anuais": {"infra": 100}, "cac": 0},
            "tributos": {"sobre_receita": 0.10, "ir_csll": 0.0},
        }

    def test_fluxo_simples(self):
        f = ec.construir_fluxo(self.modelo())
        # ano 1: média 5 clientes => 6000; ano 2/3: 10 clientes => 12000
        self.assertAlmostEqual(f["linhas"][0]["receita"], 6000.0)
        self.assertAlmostEqual(f["linhas"][1]["receita"], 12000.0)
        # fluxo ano 1 = 6000 - 600 (trib.) - 100 (infra) = 5300
        self.assertAlmostEqual(f["fluxo"][1], 5300.0)
        self.assertAlmostEqual(f["fluxo"][0], -1000.0)
        self.assertAlmostEqual(f["linhas"][0]["depreciacao"], 250.0)

    def test_ir_com_compensacao_de_prejuizo(self):
        m = self.modelo()
        m["receita"]["clientes_fim_ano"] = [1, 10, 10]
        m["tributos"] = {"sobre_receita": 0.0, "ir_csll": 0.34, "limite_compensacao_prejuizo": 0.30}
        f = ec.construir_fluxo(m)
        l1, l2 = f["linhas"][0], f["linhas"][1]
        # ano 1: receita 600; ebitda 500; dep 250; ebit 250 > 0
        self.assertAlmostEqual(l1["ebit"], 250.0)
        self.assertAlmostEqual(l1["ir_csll"], 250 * 0.34)
        # ano 2: receita (1+10)/2*100*12 = 6600; ebitda 6500; ebit 6250
        self.assertAlmostEqual(l2["ebit"], 6250.0)

    def test_prejuizo_nao_gera_ir(self):
        m = self.modelo()
        m["custos"]["fixos_anuais"] = {"infra": 50000}
        m["tributos"] = {"sobre_receita": 0.0, "ir_csll": 0.34}
        f = ec.construir_fluxo(m)
        self.assertTrue(all(l["ir_csll"] == 0 for l in f["linhas"]))

    def test_indicadores_coerentes(self):
        ind = ec.indicadores(self.modelo())
        self.assertAlmostEqual(ind["vpl"], ec.vpl(0.10, ind["fluxo"]))
        self.assertAlmostEqual(ec.vpl(ind["tir"], ind["fluxo"]), 0.0, places=5)
        self.assertLess(ind["payback_simples"], ind["payback_descontado"])

    def test_cenarios_e_sensibilidade(self):
        m = self.modelo()
        m["cenarios"] = {"pessimista": {"ajustes": {"fator_clientes": 0.5}}}
        c = {x["cenario"]: x for x in ec.cenarios(m)}
        self.assertLess(c["pessimista"]["vpl"], c["base"]["vpl"])
        s = ec.sensibilidade(m)
        self.assertEqual(len(s), 5)
        self.assertGreaterEqual(s[0]["amplitude"], s[-1]["amplitude"])

    def test_metricas_saas(self):
        m = self.modelo()
        m["receita"]["churn_mensal"] = 0.02
        m["custos"]["cac"] = 400
        r = ec.metricas_saas(m)
        self.assertAlmostEqual(r["margem_bruta_unitaria"], 0.9)
        self.assertAlmostEqual(r["ltv"], 100 * 0.9 / 0.02)

    def test_fator_equilibrio(self):
        m = self.modelo()
        x = ec.fator_equilibrio(m)
        self.assertIsNotNone(x)
        m2 = ec.mesclar(m, {"ajustes": {"fator_clientes": x}})
        self.assertAlmostEqual(ec.indicadores(m2)["vpl"], 0.0, places=4)

    def test_mesclar_nao_muta(self):
        base = {"a": {"b": 1}, "c": [1, 2]}
        novo = ec.mesclar(base, {"a": {"b": 2}})
        self.assertEqual(base["a"]["b"], 1)
        self.assertEqual(novo["a"]["b"], 2)


if __name__ == "__main__":
    unittest.main()

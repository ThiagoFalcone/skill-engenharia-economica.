"""Valida a estrutura da skill (spec Agent Skills), o CLI e a reprodutibilidade do relatório do TCC."""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(RAIZ, ".agents", "skills", "engenharia-economica-software")
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
import gerar_relatorio  # noqa: E402


def frontmatter(texto: str):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    assert m, "SKILL.md precisa começar com frontmatter YAML"
    campos, atual = {}, None
    for linha in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", linha):
            k, _, v = linha.partition(":")
            atual = k.strip()
            campos[atual] = v.strip()
        elif atual and linha.startswith("  "):
            campos.setdefault(atual + "__filhos", []).append(linha.strip())
    return campos, m.end()


class TestEstruturaSkill(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            self.texto = fh.read()
        self.fm, self.fim = frontmatter(self.texto)

    def test_name_valido_e_igual_ao_diretorio(self):
        nome = self.fm["name"]
        self.assertEqual(nome, os.path.basename(SKILL))
        self.assertRegex(nome, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(nome), 64)

    def test_description(self):
        d = self.fm["description"]
        self.assertTrue(0 < len(d) <= 1024, len(d))
        for termo in ("VPL", "TIR", "payback", "GVA", "backlog"):
            self.assertIn(termo, d)

    def test_compatibility_e_corpo_enxuto(self):
        self.assertLessEqual(len(self.fm["compatibility"]), 500)
        corpo = self.texto[self.fim:]
        self.assertLess(len(corpo.splitlines()), 500)
        # ~5.000 tokens ≈ 20.000 caracteres (camada 2 da divulgação progressiva)
        self.assertLess(len(corpo), 20000)

    def test_referencias_citadas_existem(self):
        citados = set(re.findall(r"`((?:references|assets|scripts)/[\w.\-]+)`", self.texto))
        self.assertGreaterEqual(len(citados), 4)
        for rel in citados:
            self.assertTrue(os.path.exists(os.path.join(SKILL, rel)), rel)

    def test_todas_as_referencias_sao_usadas(self):
        for nome in os.listdir(os.path.join(SKILL, "references")):
            self.assertIn(nome, self.texto, f"{nome} não é citado no SKILL.md")


class TestCopiaClaude(unittest.TestCase):
    def test_copia_claude_identica_a_canonica(self):
        copia = os.path.join(RAIZ, ".claude", "skills", "engenharia-economica-software")
        if not os.path.isdir(copia):
            self.skipTest("rode python instalar.py --destino claude-projeto")

        def arquivos(base):
            saida = {}
            for pasta, _, nomes in os.walk(base):
                if "__pycache__" in pasta:
                    continue
                for n in nomes:
                    caminho = os.path.join(pasta, n)
                    with open(caminho, "rb") as fh:
                        saida[os.path.relpath(caminho, base)] = fh.read().replace(b"\r\n", b"\n")
            return saida

        self.assertEqual(arquivos(SKILL), arquivos(copia))


class TestCLI(unittest.TestCase):
    def rodar(self, *args):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "econ_cli.py"), *args],
                           capture_output=True, text=True, encoding="utf-8")
        return r

    def test_vpl(self):
        r = self.rodar("vpl", "--taxa", "0.1", "--fluxos", "-1000", "300", "400", "500", "600")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertAlmostEqual(json.loads(r.stdout)["vpl"], 388.7712587937979, places=6)

    def test_tir_e_payback(self):
        r = json.loads(self.rodar("tir", "--fluxos", "-1000", "300", "400", "500", "600").stdout)
        self.assertAlmostEqual(r["tir"], 0.24888, places=4)
        p = json.loads(self.rodar("payback", "--fluxos", "-1000", "300", "400", "500", "600").stdout)
        self.assertAlmostEqual(p["payback_periodos"], 2.6)

    def test_gva_markup_saas(self):
        g = json.loads(self.rodar("gva", "--planejado", "400", "--agregado", "300", "--real", "450",
                                  "--bac", "1000").stdout)
        self.assertAlmostEqual(g["eac"], 1500.0)
        m = json.loads(self.rodar("markup", "--custo", "700", "--impostos", "0.1", "--margem", "0.2").stdout)
        self.assertAlmostEqual(m["preco_divisor"], 1000.0)
        s = json.loads(self.rodar("saas", "--arpa", "200", "--margem", "0.8", "--churn", "0.04",
                                  "--cac", "800").stdout)
        self.assertAlmostEqual(s["ltv_cac"], 5.0)

    def test_modelo_e_arquivos(self):
        entrada = os.path.join(RAIZ, "examples", "tcc-input.json")
        with open(entrada, encoding="utf-8") as fh:
            dados = json.load(fh)
        # o CLI "modelo" exige itens de investimento; usa o modelo do template
        modelo = os.path.join(SKILL, "assets", "modelo-entrada.json")
        with open(modelo, encoding="utf-8") as fh:
            m = json.load(fh)["modelo"]
        m["investimento"]["itens"] = {"dev": 50000}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
            json.dump(m, tmp)
        try:
            r = self.rodar("modelo", "--arquivo", tmp.name)
            self.assertEqual(r.returncode, 0, r.stderr)
            saida = json.loads(r.stdout)
            self.assertIn("indicadores", saida)
            self.assertGreaterEqual(len(saida["cenarios"]), 3)
        finally:
            os.unlink(tmp.name)
        self.assertIn("modelo", dados)

    def test_erro_de_entrada(self):
        r = self.rodar("priorizar", "--arquivo", "nao-existe.json")
        self.assertEqual(r.returncode, 2)
        self.assertIn("erro", r.stderr)


class TestRelatorio(unittest.TestCase):
    def test_relatorio_tcc_reproduzivel(self):
        with open(os.path.join(RAIZ, "examples", "tcc-input.json"), encoding="utf-8") as fh:
            entrada = json.load(fh)
        gerado = gerar_relatorio.gerar(entrada)
        with open(os.path.join(RAIZ, "examples", "tcc-valuation-report.md"), encoding="utf-8", newline="") as fh:
            versionado = fh.read()
        self.assertEqual(gerado.replace("\r\n", "\n"), versionado.replace("\r\n", "\n"),
                         "examples/tcc-valuation-report.md está desatualizado: regenere com gerar_relatorio.py")

    def test_secoes_obrigatorias_da_atividade(self):
        with open(os.path.join(RAIZ, "examples", "tcc-input.json"), encoding="utf-8") as fh:
            texto = gerar_relatorio.gerar(json.load(fh))
        for secao in ("Fluxo de caixa", "VPL", "TIR", "Payback", "Gerenciamento de Valor Agregado",
                      "modelo de negócio", "IDC", "IDP", "EAC", "CAC", "WSJF", "bom o suficiente"):
            self.assertIn(secao.lower(), texto.lower(), secao)

    def test_template_gera_relatorio(self):
        with open(os.path.join(SKILL, "assets", "modelo-entrada.json"), encoding="utf-8") as fh:
            texto = gerar_relatorio.gerar(json.load(fh))
        self.assertIn("## 13.", texto)

    def test_formatacao_brasileira(self):
        self.assertEqual(gerar_relatorio.brl(1234567.891, 2), "R$ 1.234.567,89")
        self.assertEqual(gerar_relatorio.brl(-50), "-R$ 50")
        self.assertEqual(gerar_relatorio.pct(0.1234), "12,3%")


class TestEvals(unittest.TestCase):
    def test_evals_validos(self):
        with open(os.path.join(RAIZ, "evals", "evals.json"), encoding="utf-8") as fh:
            ev = json.load(fh)
        self.assertEqual(ev["skill_name"], "engenharia-economica-software")
        self.assertGreaterEqual(len(ev["evals"]), 6)
        for e in ev["evals"]:
            self.assertTrue(e["prompt"] and e["assertions"])

    def test_evals_deterministicos_batem_com_o_motor(self):
        """Os valores esperados dos evals numéricos são reexecutados contra o CLI."""
        with open(os.path.join(RAIZ, "evals", "evals.json"), encoding="utf-8") as fh:
            ev = json.load(fh)
        executados = 0
        for e in ev["evals"]:
            cmd = e.get("comando_verificacao")
            if not cmd:
                continue
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "econ_cli.py"), *cmd],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            saida = json.loads(r.stdout)
            for chave, esperado in e["esperado"].items():
                self.assertAlmostEqual(saida[chave], esperado, places=3, msg=f"{e['id']}:{chave}")
            executados += 1
        self.assertGreaterEqual(executados, 5)


if __name__ == "__main__":
    unittest.main()

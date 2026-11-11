#!/usr/bin/env python3
"""Instala (copia) a skill no diretório esperado pelo seu agente.

    python instalar.py --destino claude-projeto   # ./.claude/skills/  (Claude Code, projeto atual)
    python instalar.py --destino claude-global    # ~/.claude/skills/  (Claude Code, todos os projetos)
    python instalar.py --destino agents-global    # ~/.agents/skills/  (padrão aberto Agent Skills)
    python instalar.py --destino pasta --caminho /meu/projeto/.agents/skills

A fonte canônica é .agents/skills/engenharia-economica-software/. Não há dependências externas.
"""
import argparse
import os
import shutil
import sys

NOME = "engenharia-economica-software"
RAIZ = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(RAIZ, ".agents", "skills", NOME)


def destino_base(args) -> str:
    if args.destino == "claude-projeto":
        return os.path.join(RAIZ, ".claude", "skills")
    if args.destino == "claude-global":
        return os.path.join(os.path.expanduser("~"), ".claude", "skills")
    if args.destino == "agents-global":
        return os.path.join(os.path.expanduser("~"), ".agents", "skills")
    if not args.caminho:
        sys.exit("--caminho é obrigatório com --destino pasta")
    return os.path.abspath(args.caminho)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--destino", required=True,
                    choices=["claude-projeto", "claude-global", "agents-global", "pasta"])
    ap.add_argument("--caminho", help="pasta de skills (somente com --destino pasta)")
    args = ap.parse_args()
    if not os.path.isfile(os.path.join(FONTE, "SKILL.md")):
        sys.exit(f"SKILL.md não encontrado em {FONTE}")
    alvo = os.path.join(destino_base(args), NOME)
    if os.path.exists(alvo):
        shutil.rmtree(alvo)
    shutil.copytree(FONTE, alvo, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"Skill instalada em: {alvo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

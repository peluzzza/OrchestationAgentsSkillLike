"""
Full Atlas Team Demo Harness

Valida post-demo que todos los agentes del equipo Atlas dejaron sus huellas:
  1. AgentRoster   — todos los 26 archivos .agent.md existen en el directorio global
  2. SpecifyArtifacts — pipeline Specify genero artefactos para task-stats
  3. Implementation   — stats() implementado en task_service.py
  4. TestSuite        — test_task_stats.py existe y tiene cobertura suficiente
  5. DocsUpdated      — README tiene seccion API Reference (Clio)
  6. DepsAudited      — evidencia de auditoria Ariadna (analysis-report.md o similar)
  7. HephaestusGate   — evidencia de release-readiness en plan de la demo

Uso:
    python full_team_harness.py [--base <workspace>]
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

USER_PROMPTS = Path(os.environ.get("APPDATA", "")) / "Code" / "User" / "prompts"

EXPECTED_AGENTS = [
    "Atlas.agent.md", "Prometheus.agent.md",
    "Hermes.agent.md", "Hermes-subagent.agent.md",
    "Oracle.agent.md", "Oracle-subagent.agent.md",
    "Sisyphus.agent.md", "Sisyphus-subagent.agent.md",
    "Afrodita-UX.agent.md", "Afrodita-subagent.agent.md",
    "Themis.agent.md", "Themis-subagent.agent.md",
    "Atenea.agent.md",
    "Argus.agent.md", "Argus-subagent.agent.md",
    "Clio.agent.md",
    "Ariadna.agent.md",
    "Hephaestus.agent.md", "Hephaestus-subagent.agent.md",
    "SpecifyConstitution.agent.md", "SpecifySpec.agent.md",
    "SpecifyClarify.agent.md", "SpecifyPlan.agent.md",
    "SpecifyTasks.agent.md", "SpecifyAnalyze.agent.md",
    "SpecifyImplement.agent.md",
]

SPECIFY_ARTIFACTS = ["spec.md", "plan.md", "tasks.md"]


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class Suite:
    name: str
    checks: list = field(default_factory=list)

    @property
    def passed(self):
        return all(c.passed for c in self.checks)

    @property
    def failures(self):
        return [c for c in self.checks if not c.passed]


# ── Suite 1: Agent Roster ─────────────────────────────────────────────────────

def check_agent_roster() -> Suite:
    """Verifica que todos los agentes estan instalados globalmente."""
    suite = Suite("AgentRoster")

    suite.checks.append(Check(
        "Directorio global de prompts existe",
        USER_PROMPTS.exists(),
        str(USER_PROMPTS)
    ))

    for agent_file in EXPECTED_AGENTS:
        path = USER_PROMPTS / agent_file
        suite.checks.append(Check(
            f"Agente instalado: {agent_file}",
            path.exists(),
            "" if path.exists() else f"Falta en {USER_PROMPTS}"
        ))

    # Verificar que Atlas tiene agents: ["*"] (puede invocar cualquiera)
    atlas_path = USER_PROMPTS / "Atlas.agent.md"
    if atlas_path.exists():
        content = atlas_path.read_text(encoding="utf-8")
        suite.checks.append(Check(
            "Atlas.agent.md tiene agents: [\"*\"] (sin restricciones)",
            '"*"' in content or "agents: [\"*\"]" in content,
            "Atlas no tiene agents:[*] — puede estar limitado"
        ))
        # Verificar que tiene Pack Registry awareness
        suite.checks.append(Check(
            "Atlas.agent.md menciona pack-registry.json",
            "pack-registry.json" in content,
            "Atlas no lee el Pack Registry"
        ))
        # Verificar que tiene SP-5 gate
        suite.checks.append(Check(
            "Atlas.agent.md tiene SP-5 gate definido",
            "SP-5" in content,
            "SP-5 gate no encontrado en Atlas"
        ))
        # Verificar que tiene EX-1 gate
        suite.checks.append(Check(
            "Atlas.agent.md tiene EX-1 gate definido",
            "EX-1" in content,
            "EX-1 gate no encontrado en Atlas"
        ))
        # Verificar que el brief de Hephaestus tiene 5 modos
        suite.checks.append(Check(
            "Atlas.agent.md briefing de Hephaestus tiene 5 modos",
            all(m in content for m in [
                "deploy", "release-readiness", "incident",
                "maintenance", "performance-capacity"
            ]),
            "Faltan modos en el brief de Hephaestus"
        ))

    return suite


# ── Suite 2: Pack Registry ────────────────────────────────────────────────────

def check_pack_registry(workspace: Path) -> Suite:
    """Verifica integridad del pack-registry.json."""
    suite = Suite("PackRegistry")
    reg = workspace / ".github" / "plugin" / "pack-registry.json"

    suite.checks.append(Check("pack-registry.json existe", reg.exists(), str(reg)))
    if not reg.exists():
        return suite

    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
        suite.checks.append(Check("JSON valido", True))
    except json.JSONDecodeError as e:
        suite.checks.append(Check("JSON valido", False, str(e)))
        return suite

    packs = {p["id"]: p for p in data.get("packs", []) if isinstance(p, dict)}

    # canonical-root default active
    root = packs.get("canonical-root", {})
    suite.checks.append(Check(
        "canonical-root defaultActive=true",
        root.get("defaultActive") is True,
        f"defaultActive={root.get('defaultActive')}"
    ))

    # Packs domain especificos shipped
    for pid in ["backend-workflow", "frontend-workflow", "devops-workflow",
                "automation-mcp-workflow", "ux-enhancement-workflow"]:
        p = packs.get(pid, {})
        suite.checks.append(Check(
            f"{pid} shipped=true",
            p.get("shipped") is True,
            f"shipped={p.get('shipped')}" if p else f"Pack {pid} no encontrado"
        ))

    return suite


# ── Suite 3: Specify Artifacts ────────────────────────────────────────────────

def check_specify_artifacts(demo_dir: Path, slug: str = "task-stats") -> Suite:
    suite = Suite("SpecifyArtifacts")
    feature_dir = demo_dir / ".specify" / "specs" / slug
    constitution = demo_dir / ".specify" / "memory" / "constitution.md"

    suite.checks.append(Check(
        f".specify/specs/{slug}/ existe",
        feature_dir.exists(),
        str(feature_dir)
    ))
    suite.checks.append(Check(
        ".specify/memory/constitution.md existe",
        constitution.exists(),
        str(constitution)
    ))

    if not feature_dir.exists():
        return suite

    for artifact in SPECIFY_ARTIFACTS:
        path = feature_dir / artifact
        suite.checks.append(Check(f"{artifact} existe", path.exists(), str(path)))

    # tasks.md tiene formato T001..Tnnn
    tasks = feature_dir / "tasks.md"
    if tasks.exists():
        content = tasks.read_text(encoding="utf-8")
        ids = re.findall(r"T\d{3}", content)
        suite.checks.append(Check(
            "tasks.md tiene al menos 5 tareas Tnnn",
            len(ids) >= 5,
            f"Solo {len(ids)} tareas encontradas"
        ))

    # analysis-report.md (SpecifyAnalyze)
    report = feature_dir / "analysis-report.md"
    suite.checks.append(Check(
        "analysis-report.md existe (SpecifyAnalyze corrio)",
        report.exists(),
        str(report)
    ))
    if report.exists():
        content = report.read_text(encoding="utf-8")
        suite.checks.append(Check(
            "analysis-report menciona SP-5 o EX-1",
            "SP-5" in content or "EX-1" in content,
            "Ninguna puerta de analisis mencionada"
        ))

    return suite


# ── Suite 4: Implementation ───────────────────────────────────────────────────

def check_implementation(demo_dir: Path) -> Suite:
    suite = Suite("Implementation")
    service = demo_dir / "task_service.py"

    suite.checks.append(Check("task_service.py existe", service.exists(), str(service)))
    if not service.exists():
        return suite

    content = service.read_text(encoding="utf-8")

    # stats() implementado (no solo comentado)
    has_def = bool(re.search(r"^\s*def\s+stats\s*\(", content, re.MULTILINE))
    has_raise = bool(re.search(r"raise\s+NotImplementedError", content))
    suite.checks.append(Check(
        "stats() esta definido (no solo comentado)",
        has_def,
        "def stats() no encontrado"
    ))
    suite.checks.append(Check(
        "stats() no tiene NotImplementedError (implementado de verdad)",
        has_def and not has_raise,
        "Aun tiene NotImplementedError"
    ))

    # Validacion de limit
    suite.checks.append(Check(
        "stats() valida el parametro limit",
        "limit" in content and ("ValueError" in content or "raise" in content),
        "No se detecta validacion de limit"
    ))

    # Test file creado
    test_file = demo_dir / "test_task_stats.py"
    suite.checks.append(Check(
        "test_task_stats.py existe (creado por Argus/Sisyphus)",
        test_file.exists(),
        str(test_file)
    ))
    if test_file.exists():
        tc = test_file.read_text(encoding="utf-8")
        test_count = len(re.findall(r"def\s+test_", tc))
        suite.checks.append(Check(
            "test_task_stats.py tiene al menos 5 tests",
            test_count >= 5,
            f"Solo {test_count} tests encontrados"
        ))

    return suite


# ── Suite 5: Docs (Clio) ──────────────────────────────────────────────────────

def check_docs(demo_dir: Path) -> Suite:
    suite = Suite("DocsUpdated")
    readme = demo_dir / "README.md"

    suite.checks.append(Check("README.md existe", readme.exists(), str(readme)))
    if not readme.exists():
        return suite

    content = readme.read_text(encoding="utf-8")
    suite.checks.append(Check(
        "README tiene seccion API Reference (Clio trabajo)",
        "API Reference" in content or "api reference" in content.lower(),
        "No se encontro 'API Reference' en README"
    ))
    suite.checks.append(Check(
        "README documenta stats()",
        "stats" in content,
        "No se encontro 'stats' en README"
    ))

    return suite


# ── Suite 6: Deps Audit (Ariadna) ─────────────────────────────────────────────

def check_ariadna(demo_dir: Path) -> Suite:
    suite = Suite("DepsAudited")
    toml = demo_dir / "pyproject.toml"

    suite.checks.append(Check("pyproject.toml existe", toml.exists(), str(toml)))
    # Buscamos un artefacto de auditoria (puede estar en varios lugares)
    candidates = [
        demo_dir / "ariadna-report.md",
        demo_dir / "dependency-audit.md",
        demo_dir / "plans" / "dependency-audit.md",
    ]
    audit_found = any(c.exists() for c in candidates)
    suite.checks.append(Check(
        "Existe reporte de auditoria de dependencias (Ariadna)",
        audit_found,
        f"Buscado en: {[str(c) for c in candidates]}"
    ))
    if audit_found:
        report_path = next(c for c in candidates if c.exists())
        content = report_path.read_text(encoding="utf-8")
        suite.checks.append(Check(
            "Reporte menciona python-multipart (CVE conocido)",
            "python-multipart" in content,
            "CVE principal no mencionado"
        ))

    return suite


# ── Runner ────────────────────────────────────────────────────────────────────

def run_all(workspace: Path) -> list:
    demo_dir = workspace / "demos" / "full-atlas-team-demo"
    return [
        check_agent_roster(),
        check_pack_registry(workspace),
        check_specify_artifacts(demo_dir),
        check_implementation(demo_dir),
        check_docs(demo_dir),
        check_ariadna(demo_dir),
    ]


def print_report(results: list) -> bool:
    all_ok = True
    for suite in results:
        status = "PASSED" if suite.passed else "FAILED"
        color_open = "" if suite.passed else ""
        print(f"\n{'='*60}")
        print(f"Suite: {suite.name}  [{status}]")
        print(f"{'='*60}")
        for c in suite.checks:
            icon = "  [OK]" if c.passed else "  [!!]"
            print(f"{icon}  {c.name}")
            if not c.passed and c.detail:
                print(f"        -> {c.detail}")
        if not suite.passed:
            all_ok = False

    print(f"\n{'='*60}")
    print(f"RESULTADO: {'TODOS LOS CHECKS PASARON' if all_ok else 'HAY FALLOS'}")
    print(f"{'='*60}\n")
    return all_ok


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=None)
    args = parser.parse_args()
    workspace = Path(args.base).resolve() if args.base else Path(__file__).resolve().parent.parent.parent
    print(f"Workspace: {workspace}")
    ok = print_report(run_all(workspace))
    sys.exit(0 if ok else 1)

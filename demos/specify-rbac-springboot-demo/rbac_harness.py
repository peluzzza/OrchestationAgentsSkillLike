"""
RBAC Specify Demo Harness

Valida que el pipeline Specify y los nuevos features del ecosistema Atlas
funcionaron correctamente tras ejecutar la demo con @Atlas.

Comprueba:
  1. Pack Registry — pack-registry.json tiene los packs requeridos con los campos correctos
  2. Specify Artifacts — artefactos .specify/ existen y tienen estructura válida
  3. Hephaestus Maintenance — scripts Flyway de migración presentes (post-implementación)
  4. Implementation Smoke — clases Java de dominio creadas (post-implementación)

Uso:
    python rbac_harness.py [--base <ruta_workspace>]
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class SuiteResult:
    suite: str
    checks: list  # list[Check]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def failures(self) -> list:
        return [c for c in self.checks if not c.passed]


# ---------------------------------------------------------------------------
# Suite 1 — Pack Registry
# ---------------------------------------------------------------------------

REQUIRED_PACK_IDS = {"canonical-root", "backend-workflow", "atlas-orchestration-team"}
REQUIRED_PACK_FIELDS = {"id", "name", "installPath", "shipped", "defaultActive", "conductor"}


def validate_pack_registry(workspace: Path) -> SuiteResult:
    """Valida pack-registry.json: existencia, estructura, packs requeridos."""
    registry_path = workspace / ".github" / "plugin" / "pack-registry.json"
    checks = []

    # Existencia
    checks.append(Check(
        "pack-registry.json existe",
        registry_path.exists(),
        str(registry_path) if not registry_path.exists() else ""
    ))
    if not registry_path.exists():
        return SuiteResult("PackRegistry", checks)

    # JSON válido
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        checks.append(Check("pack-registry.json es JSON válido", True))
    except json.JSONDecodeError as exc:
        checks.append(Check("pack-registry.json es JSON válido", False, str(exc)))
        return SuiteResult("PackRegistry", checks)

    # Campo version
    checks.append(Check(
        "Tiene campo 'version'",
        "version" in data,
        "" if "version" in data else "Campo 'version' ausente"
    ))

    # Campo packs es lista
    packs = data.get("packs", [])
    checks.append(Check(
        "Campo 'packs' es lista no vacía",
        isinstance(packs, list) and len(packs) > 0,
        f"packs tiene {len(packs)} entradas"
    ))

    # Packs requeridos presentes
    pack_ids = {p.get("id") for p in packs if isinstance(p, dict)}
    for required_id in sorted(REQUIRED_PACK_IDS):
        checks.append(Check(
            f"Pack '{required_id}' presente",
            required_id in pack_ids,
            "" if required_id in pack_ids else f"'{required_id}' no encontrado en {pack_ids}"
        ))

    # Campos requeridos en cada pack
    for pack in packs:
        if not isinstance(pack, dict):
            continue
        pid = pack.get("id", "<sin-id>")
        missing = REQUIRED_PACK_FIELDS - set(pack.keys())
        checks.append(Check(
            f"Pack '{pid}' tiene todos los campos requeridos",
            len(missing) == 0,
            f"Campos faltantes: {missing}" if missing else ""
        ))

    # canonical-root debe ser defaultActive=true
    root_pack = next((p for p in packs if p.get("id") == "canonical-root"), None)
    if root_pack:
        checks.append(Check(
            "canonical-root tiene defaultActive=true",
            root_pack.get("defaultActive") is True,
            f"defaultActive={root_pack.get('defaultActive')}"
        ))

    # backend-workflow debe tener shipped=true
    backend_pack = next((p for p in packs if p.get("id") == "backend-workflow"), None)
    if backend_pack:
        checks.append(Check(
            "backend-workflow tiene shipped=true",
            backend_pack.get("shipped") is True,
            f"shipped={backend_pack.get('shipped')}"
        ))

    return SuiteResult("PackRegistry", checks)


# ---------------------------------------------------------------------------
# Suite 2 — Specify Artifacts
# ---------------------------------------------------------------------------

SPECIFY_ARTIFACTS = [
    "constitution.md",       # SP-1
    "spec.md",               # SP-2
    "plan.md",               # SP-4
    "tasks.md",              # SP-5
]

SPEC_REQUIRED_SECTIONS = {
    "spec.md": ["## Overview", "## User Stories", "## Acceptance Criteria"],
    "plan.md": ["## Phase", "migration", "Flyway"],
    "tasks.md": ["T001", "[P]"],
}


def validate_specify_artifacts(workspace: Path, feature_slug: str = "rbac-spring") -> SuiteResult:
    """Valida que los artefactos Specify del pipeline existen y tienen estructura mínima."""
    checks = []

    # Buscar en location canónica dentro del proyecto demo
    specify_dir = workspace / "user-management-demo" / ".specify" / "specs" / feature_slug
    constitution_path = workspace / "user-management-demo" / ".specify" / "memory" / "constitution.md"

    # Directorio .specify/ existe
    checks.append(Check(
        ".specify/specs/rbac-spring/ existe",
        specify_dir.exists() and specify_dir.is_dir(),
        str(specify_dir)
    ))

    # constitution.md
    checks.append(Check(
        ".specify/memory/constitution.md existe",
        constitution_path.exists(),
        str(constitution_path)
    ))

    if constitution_path.exists():
        content = constitution_path.read_text(encoding="utf-8")
        checks.append(Check(
            "constitution.md tiene principios (líneas con 'P1'..ó 'Principle')",
            bool(re.search(r"\bP\d\b|Principle|principle", content)),
            "No se encontraron principios"
        ))

    if not specify_dir.exists():
        # Skip artifact checks if directory not present yet
        return SuiteResult("SpecifyArtifacts", checks)

    # Cada artefacto
    for artifact in SPECIFY_ARTIFACTS:
        path = specify_dir / artifact
        checks.append(Check(
            f"Artefacto {artifact} existe",
            path.exists(),
            str(path)
        ))
        if path.exists() and artifact in SPEC_REQUIRED_SECTIONS:
            content = path.read_text(encoding="utf-8")
            for section in SPEC_REQUIRED_SECTIONS[artifact]:
                checks.append(Check(
                    f"{artifact} contiene '{section}'",
                    section in content,
                    f"Sección/palabra '{section}' no encontrada en {artifact}"
                ))

    # tasks.md: contiene marcadores [P] (paralelismo) y formato Tnnn
    tasks_path = specify_dir / "tasks.md"
    if tasks_path.exists():
        content = tasks_path.read_text(encoding="utf-8")
        task_ids = re.findall(r"T\d{3}", content)
        checks.append(Check(
            "tasks.md tiene al menos 5 tareas Tnnn",
            len(task_ids) >= 5,
            f"Sólo {len(task_ids)} tareas encontradas: {task_ids[:5]}"
        ))

    return SuiteResult("SpecifyArtifacts", checks)


# ---------------------------------------------------------------------------
# Suite 3 — Hephaestus Maintenance (Flyway migrations)
# ---------------------------------------------------------------------------

FLYWAY_MIGRATIONS = ["V2__add_roles.sql", "V3__add_user_roles.sql"]


def validate_hephaestus_maintenance(workspace: Path) -> SuiteResult:
    """Valida que los scripts Flyway de la Fase 4 fueron creados por Hephaestus."""
    checks = []
    migration_dir = workspace / "user-management-demo" / "src" / "main" / "resources" / "db" / "migration"

    checks.append(Check(
        "Directorio db/migration/ existe",
        migration_dir.exists(),
        str(migration_dir)
    ))

    for migration_file in FLYWAY_MIGRATIONS:
        path = migration_dir / migration_file
        checks.append(Check(
            f"Flyway {migration_file} existe",
            path.exists(),
            str(path)
        ))
        if path.exists():
            sql = path.read_text(encoding="utf-8").upper()
            # Basic safety: no DROP TABLE on existing tables
            has_risky_drop = bool(re.search(r"DROP\s+TABLE\s+(?!IF\s+EXISTS\s+ROLES|IF\s+EXISTS\s+USER_ROLES)", sql))
            checks.append(Check(
                f"{migration_file} no elimina tablas existentes sin IF EXISTS",
                not has_risky_drop,
                "DROP TABLE detectado sin guardia IF EXISTS en tabla no RBAC"
            ))

    return SuiteResult("HephaestusMaintenanceMigrations", checks)


# ---------------------------------------------------------------------------
# Suite 4 — Implementation Smoke (Java domain classes)
# ---------------------------------------------------------------------------

EXPECTED_DOMAIN_FILES = [
    "domain/model/Permission.java",
    "domain/model/Role.java",
    "domain/port/IAuthorizationPort.java",
    "domain/port/IRoleRepository.java",
]

EXPECTED_APPLICATION_FILES = [
    "application/service/RoleService.java",
]


def validate_implementation_smoke(workspace: Path) -> SuiteResult:
    """Valida que Sisyphus creó los archivos Java de dominio esperados."""
    checks = []
    java_root = workspace / "user-management-demo" / "src" / "main" / "java" / "com" / "accenture" / "usermgmt"

    for relative in EXPECTED_DOMAIN_FILES + EXPECTED_APPLICATION_FILES:
        path = java_root / relative
        checks.append(Check(
            f"Java: {relative} existe",
            path.exists(),
            str(path)
        ))

    # IAuthorizationPort no debe importar clases de Spring Security directamente
    auth_port = java_root / "domain" / "port" / "IAuthorizationPort.java"
    if auth_port.exists():
        content = auth_port.read_text(encoding="utf-8")
        imports_spring_security = "org.springframework.security" in content
        checks.append(Check(
            "IAuthorizationPort no depende de Spring Security (dominio limpio)",
            not imports_spring_security,
            "import org.springframework.security encontrado en puerto de dominio"
        ))

    return SuiteResult("ImplementationSmoke", checks)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all(workspace: Path) -> list:
    results = [
        validate_pack_registry(workspace),
        validate_specify_artifacts(workspace),
        validate_hephaestus_maintenance(workspace),
        validate_implementation_smoke(workspace),
    ]
    return results


def print_report(results: list) -> bool:
    """Imprime el informe y devuelve True si todo pasó."""
    all_passed = True
    for suite in results:
        status = "✅ PASSED" if suite.passed else "❌ FAILED"
        print(f"\n{'='*60}")
        print(f"Suite: {suite.suite}  {status}")
        print(f"{'='*60}")
        for check in suite.checks:
            icon = "  ✅" if check.passed else "  ❌"
            line = f"{icon}  {check.name}"
            if not check.passed and check.detail:
                line += f"\n       → {check.detail}"
            print(line)
        if not suite.passed:
            all_passed = False

    print(f"\n{'='*60}")
    print(f"RESULTADO GLOBAL: {'✅ TODOS LOS CHECKS PASARON' if all_passed else '❌ HAY FALLOS'}")
    print(f"{'='*60}\n")
    return all_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RBAC Specify Demo Harness")
    parser.add_argument(
        "--base",
        default=None,
        help="Ruta raíz del workspace (por defecto: 2 niveles arriba de este script)"
    )
    args = parser.parse_args()

    if args.base:
        workspace = Path(args.base).resolve()
    else:
        workspace = Path(__file__).resolve().parent.parent.parent  # demos/../..

    print(f"Workspace: {workspace}")
    results = run_all(workspace)
    ok = print_report(results)
    sys.exit(0 if ok else 1)

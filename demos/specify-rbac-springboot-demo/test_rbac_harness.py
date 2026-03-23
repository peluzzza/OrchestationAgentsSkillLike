"""
Test suite for rbac_harness.py

Cubre:
  TestHarnessUnit        — lógica interna de checks y SuiteResult
  TestPackRegistry       — valida el pack-registry.json real del workspace
  TestSpecifyArtifacts   — valida artefactos .specify/ (SKIP si no existen: pre-demo)
  TestImplementationSmoke — valida clases Java (SKIP si no existen: pre-demo)

Ejecución:
    cd demos/specify-rbac-springboot-demo
    py -m unittest -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Añadir el directorio del script al path para importar rbac_harness
sys.path.insert(0, str(Path(__file__).parent))
import rbac_harness as harness

# Ruta al workspace (2 niveles arriba de este archivo)
WORKSPACE = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# TestHarnessUnit — lógica interna pura, sin ficheros reales
# ---------------------------------------------------------------------------

class TestHarnessUnit(unittest.TestCase):

    def test_check_passed(self):
        c = harness.Check("mi check", True)
        self.assertTrue(c.passed)

    def test_check_failed(self):
        c = harness.Check("mi check", False, "detalle del fallo")
        self.assertFalse(c.passed)
        self.assertEqual(c.detail, "detalle del fallo")

    def test_suite_result_all_pass(self):
        checks = [harness.Check("a", True), harness.Check("b", True)]
        suite = harness.SuiteResult("MySuite", checks)
        self.assertTrue(suite.passed)
        self.assertEqual(len(suite.failures), 0)

    def test_suite_result_with_failure(self):
        checks = [harness.Check("a", True), harness.Check("b", False, "error")]
        suite = harness.SuiteResult("MySuite", checks)
        self.assertFalse(suite.passed)
        self.assertEqual(len(suite.failures), 1)
        self.assertEqual(suite.failures[0].name, "b")

    def test_pack_registry_invalid_json(self):
        """Un JSON malformado debe producir un check de fallo."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_dir = tmp_path / ".github" / "plugin"
            registry_dir.mkdir(parents=True)
            (registry_dir / "pack-registry.json").write_text("{invalid json", encoding="utf-8")

            result = harness.validate_pack_registry(tmp_path)
            names = [c.name for c in result.checks if not c.passed]
            self.assertTrue(any("JSON válido" in n for n in names))

    def test_pack_registry_missing_required_pack(self):
        """Si falta canonical-root el check debe fallar."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_dir = tmp_path / ".github" / "plugin"
            registry_dir.mkdir(parents=True)
            data = {
                "version": "1.0.0",
                "packs": [
                    {"id": "other-pack", "name": "Other", "installPath": "plugins/other",
                     "shipped": True, "defaultActive": False, "conductor": "X"}
                ]
            }
            (registry_dir / "pack-registry.json").write_text(json.dumps(data), encoding="utf-8")

            result = harness.validate_pack_registry(tmp_path)
            failed_names = [c.name for c in result.checks if not c.passed]
            self.assertTrue(any("canonical-root" in n for n in failed_names))

    def test_specify_artifacts_missing_dir(self):
        """Si no existe .specify/, los checks de artefactos deben ser skipped/failed sin excepción."""
        with tempfile.TemporaryDirectory() as tmp:
            result = harness.validate_specify_artifacts(Path(tmp), "rbac-spring")
            # No debe lanzar excepción; la suite debe incluir al menos 1 check
            self.assertIsInstance(result, harness.SuiteResult)
            self.assertGreater(len(result.checks), 0)

    def test_flyway_risky_drop_detection(self):
        """validate_hephaestus_maintenance detecta DROP TABLE peligroso."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            migration_dir = (
                tmp_path / "user-management-demo" / "src" / "main"
                / "resources" / "db" / "migration"
            )
            migration_dir.mkdir(parents=True)
            # Script con DROP TABLE en tabla existente (no RBAC)
            risky_sql = "DROP TABLE users;\nCREATE TABLE roles (id INT);"
            (migration_dir / "V2__add_roles.sql").write_text(risky_sql, encoding="utf-8")

            result = harness.validate_hephaestus_maintenance(tmp_path)
            failed = [c for c in result.checks if not c.passed]
            self.assertTrue(any("elimina tablas" in c.name for c in failed),
                            f"Checks fallidos: {[c.name for c in failed]}")

    def test_print_report_returns_false_on_failure(self):
        results = [
            harness.SuiteResult("S1", [harness.Check("c1", True)]),
            harness.SuiteResult("S2", [harness.Check("c2", False, "error")]),
        ]
        ok = harness.print_report(results)
        self.assertFalse(ok)

    def test_print_report_returns_true_on_all_pass(self):
        results = [
            harness.SuiteResult("S1", [harness.Check("c1", True)]),
        ]
        ok = harness.print_report(results)
        self.assertTrue(ok)


# ---------------------------------------------------------------------------
# TestPackRegistry — valida el pack-registry.json REAL del workspace
# ---------------------------------------------------------------------------

class TestPackRegistry(unittest.TestCase):
    """
    Valida el pack-registry.json real del workspace.
    Esta suite debe pasar SIEMPRE (pre y post demo).
    """

    def setUp(self):
        self.result = harness.validate_pack_registry(WORKSPACE)

    def test_registry_exists(self):
        registry_check = next(
            (c for c in self.result.checks if "existe" in c.name), None
        )
        self.assertIsNotNone(registry_check, "No se encontró check de existencia")
        self.assertTrue(registry_check.passed, registry_check.detail)

    def test_registry_is_valid_json(self):
        json_check = next(
            (c for c in self.result.checks if "JSON válido" in c.name), None
        )
        self.assertIsNotNone(json_check, "No se encontró check de JSON válido")
        self.assertTrue(json_check.passed, json_check.detail)

    def test_canonical_root_pack_present(self):
        check = next((c for c in self.result.checks if "canonical-root" in c.name and "presente" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de canonical-root")
        self.assertTrue(check.passed, check.detail)

    def test_backend_workflow_pack_present(self):
        check = next((c for c in self.result.checks if "backend-workflow" in c.name and "presente" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de backend-workflow")
        self.assertTrue(check.passed, check.detail)

    def test_atlas_orchestration_team_present(self):
        check = next((c for c in self.result.checks if "atlas-orchestration-team" in c.name and "presente" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de atlas-orchestration-team")
        self.assertTrue(check.passed, check.detail)

    def test_canonical_root_is_default_active(self):
        check = next((c for c in self.result.checks if "defaultActive=true" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de defaultActive")
        self.assertTrue(check.passed, check.detail)

    def test_backend_workflow_is_shipped(self):
        check = next((c for c in self.result.checks if "backend-workflow tiene shipped" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de shipped para backend-workflow")
        self.assertTrue(check.passed, check.detail)

    def test_all_packs_have_required_fields(self):
        field_checks = [c for c in self.result.checks if "todos los campos" in c.name]
        self.assertGreater(len(field_checks), 0, "No se encontraron checks de campos")
        failures = [c for c in field_checks if not c.passed]
        self.assertEqual(len(failures), 0, f"Packs con campos faltantes: {[(c.name, c.detail) for c in failures]}")


# ---------------------------------------------------------------------------
# TestSpecifyArtifacts — SKIP si no se ha ejecutado el pipeline todavía
# ---------------------------------------------------------------------------

class TestSpecifyArtifacts(unittest.TestCase):
    """
    Valida artefactos .specify/ generados por el pipeline.
    Se salta automáticamente si aún no se ha ejecutado la demo (pre-demo state).
    """

    FEATURE_SLUG = "rbac-spring"

    def setUp(self):
        self.specify_dir = (
            WORKSPACE / "user-management-demo" / ".specify" / "specs" / self.FEATURE_SLUG
        )
        if not self.specify_dir.exists():
            self.skipTest(
                f"Pipeline Specify no ejecutado aún — .specify/specs/{self.FEATURE_SLUG}/ no existe. "
                "Ejecuta la demo con @Atlas primero."
            )
        self.result = harness.validate_specify_artifacts(WORKSPACE, self.FEATURE_SLUG)

    def test_constitution_exists(self):
        check = next((c for c in self.result.checks if "constitution.md existe" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_constitution_has_principles(self):
        check = next((c for c in self.result.checks if "principios" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_spec_exists(self):
        check = next((c for c in self.result.checks if "spec.md existe" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_plan_exists(self):
        check = next((c for c in self.result.checks if "plan.md existe" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_tasks_exists(self):
        check = next((c for c in self.result.checks if "tasks.md existe" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_tasks_has_minimum_task_ids(self):
        check = next((c for c in self.result.checks if "al menos 5 tareas" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_plan_mentions_flyway(self):
        check = next((c for c in self.result.checks if "Flyway" in c.name and "plan.md" in c.name), None)
        self.assertIsNotNone(check, "No se encontró check de Flyway en plan.md")
        self.assertTrue(check.passed, check.detail)


# ---------------------------------------------------------------------------
# TestImplementationSmoke — SKIP si la implementación no se ha ejecutado
# ---------------------------------------------------------------------------

class TestImplementationSmoke(unittest.TestCase):
    """
    Valida que Sisyphus creó los archivos Java de dominio esperados.
    Se salta automáticamente si las clases RBAC no existen (pre-implementación).
    """

    def setUp(self):
        auth_port = (
            WORKSPACE / "user-management-demo" / "src" / "main" / "java"
            / "com" / "accenture" / "usermgmt" / "domain" / "port" / "IAuthorizationPort.java"
        )
        if not auth_port.exists():
            self.skipTest(
                "Implementación RBAC no ejecutada aún — IAuthorizationPort.java no existe. "
                "Ejecuta la demo con @Atlas (Opción A) primero."
            )
        self.result = harness.validate_implementation_smoke(WORKSPACE)

    def test_permission_enum_exists(self):
        check = next((c for c in self.result.checks if "Permission.java" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_role_entity_exists(self):
        check = next((c for c in self.result.checks if "Role.java" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_authorization_port_exists(self):
        check = next((c for c in self.result.checks if "IAuthorizationPort.java" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_authorization_port_is_framework_free(self):
        check = next((c for c in self.result.checks if "Spring Security" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_role_repository_port_exists(self):
        check = next((c for c in self.result.checks if "IRoleRepository.java" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)

    def test_role_service_exists(self):
        check = next((c for c in self.result.checks if "RoleService.java" in c.name), None)
        self.assertIsNotNone(check)
        self.assertTrue(check.passed, check.detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)

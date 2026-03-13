from __future__ import annotations

from pathlib import Path
import sys
import unittest


_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import fixtures
from selection_engine import select_source


class TestSelectionEngine(unittest.TestCase):
    def test_deterministic_tie_break(self):
        task = fixtures.make_backend_task()
        forward = select_source(fixtures.make_tie_break_sources(), task)
        reverse = select_source(list(reversed(fixtures.make_tie_break_sources())), task)

        self.assertIsNotNone(forward.selected)
        self.assertIsNotNone(reverse.selected)
        self.assertEqual(forward.selected.source_id, "alpha-router")
        self.assertEqual(reverse.selected.source_id, "alpha-router")

    def test_capability_matching_by_task_type(self):
        result = select_source(
            fixtures.make_capability_sources(),
            fixtures.make_ui_task(),
        )

        self.assertIsNotNone(result.selected)
        self.assertEqual(result.selected.source_id, "ui-specialist")

    def test_github_precedence_on_duplicate_source(self):
        result = select_source(
            fixtures.make_duplicate_sources(),
            fixtures.make_backend_task(),
        )

        self.assertIsNotNone(result.selected)
        self.assertEqual(result.selected.source_id, "shared-flow")
        self.assertEqual(result.selected.origin, "github")

    def test_fallback_when_preferred_source_unavailable(self):
        result = select_source(
            fixtures.make_preferred_fallback_sources(),
            fixtures.make_task_with_unavailable_preference(),
        )

        self.assertIsNotNone(result.selected)
        self.assertEqual(result.selected.source_id, "fallback-flow")
        self.assertIn("fallback", " ".join(result.rationale).lower())

    def test_selects_preferred_source_when_available_and_compatible(self):
        result = select_source(
            fixtures.make_preferred_selected_sources(),
            fixtures.make_task_with_preference(),
        )

        self.assertIsNotNone(result.selected)
        self.assertEqual(result.selected.source_id, "preferred-flow")
        self.assertIn("preferred source is available and compatible", " ".join(result.rationale).lower())


if __name__ == "__main__":
    unittest.main()

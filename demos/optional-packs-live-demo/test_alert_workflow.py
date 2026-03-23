"""Tests for AlertWorkflow — threshold-based alert firing."""
import unittest
from alert_workflow import AlertWorkflow


# ===================================================================== #
#  PASSING — constructor validation (no stubs needed)                   #
# ===================================================================== #

class TestAlertWorkflowInit(unittest.TestCase):

    def test_positive_threshold_ok(self):
        wf = AlertWorkflow(threshold=10)
        self.assertEqual(wf.threshold, 10)

    def test_zero_threshold_raises(self):
        with self.assertRaises(ValueError):
            AlertWorkflow(threshold=0)

    def test_negative_threshold_raises(self):
        with self.assertRaises(ValueError):
            AlertWorkflow(threshold=-5)


# ===================================================================== #
#  FAILING until is_triggered() and execute() are implemented           #
# ===================================================================== #

class TestIsTriggered(unittest.TestCase):

    def test_below_threshold_not_triggered(self):
        wf = AlertWorkflow(threshold=5)
        self.assertFalse(wf.is_triggered(3))

    def test_at_threshold_not_triggered(self):
        """Strictly greater-than: equal does NOT trigger."""
        wf = AlertWorkflow(threshold=5)
        self.assertFalse(wf.is_triggered(5))

    def test_above_threshold_triggered(self):
        wf = AlertWorkflow(threshold=5)
        self.assertTrue(wf.is_triggered(6))

    def test_well_above_threshold_triggered(self):
        wf = AlertWorkflow(threshold=5)
        self.assertTrue(wf.is_triggered(100))

    def test_threshold_boundary_one(self):
        """threshold=1: 1 does not trigger, 2 does."""
        wf = AlertWorkflow(threshold=1)
        self.assertFalse(wf.is_triggered(1))
        self.assertTrue(wf.is_triggered(2))


class TestExecute(unittest.TestCase):

    def test_execute_calls_handler_when_triggered(self):
        wf = AlertWorkflow(threshold=3)
        fired: list[int] = []
        result = wf.execute(10, lambda n: fired.append(n))
        self.assertTrue(result, "execute should return True when handler called")
        self.assertEqual(fired, [10])

    def test_execute_does_not_call_handler_when_not_triggered(self):
        wf = AlertWorkflow(threshold=10)
        fired: list[int] = []
        result = wf.execute(5, lambda n: fired.append(n))
        self.assertFalse(result, "execute should return False when below threshold")
        self.assertEqual(fired, [])

    def test_execute_returns_false_at_exact_threshold(self):
        wf = AlertWorkflow(threshold=10)
        result = wf.execute(10, lambda n: None)
        self.assertFalse(result)

    def test_execute_passes_total_to_handler(self):
        wf = AlertWorkflow(threshold=1)
        received: list[int] = []
        wf.execute(42, lambda n: received.append(n))
        self.assertEqual(received, [42])


if __name__ == "__main__":
    unittest.main()

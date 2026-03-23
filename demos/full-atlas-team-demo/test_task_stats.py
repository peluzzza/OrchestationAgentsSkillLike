import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from task_service import TaskService


class TestTaskStats(unittest.TestCase):

    def setUp(self):
        self.svc = TaskService()

    def _add(self, title, priority, done=False, tags=None, days_ago=0):
        task = self.svc.create(title, priority=priority, tags=tags or [])
        task.created_at = datetime.utcnow() - timedelta(days=days_ago)
        if done:
            self.svc.complete(task.id)
        return task

    # 1 — empty store returns all zeros; all 5 priority keys present
    def test_stats_empty_store(self):
        result = self.svc.stats()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["done"], 0)
        self.assertEqual(result["pending"], 0)
        self.assertEqual(set(result["by_priority"].keys()), {1, 2, 3, 4, 5})
        self.assertTrue(all(v == 0 for v in result["by_priority"].values()))
        self.assertEqual(result["by_tag"], {})

    # 2 — mixed done/pending: verify total/done/pending
    def test_stats_basic_totals(self):
        self._add("a", 1, done=True)
        self._add("b", 2, done=False)
        self._add("c", 3, done=True)
        result = self.svc.stats()
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["done"], 2)
        self.assertEqual(result["pending"], 1)
        self.assertEqual(result["done"] + result["pending"], result["total"])

    # 3 — aggregation per priority level
    def test_stats_by_priority(self):
        self._add("p1a", 1)
        self._add("p1b", 1)
        self._add("p3",  3)
        self._add("p5",  5)
        result = self.svc.stats()
        self.assertEqual(result["by_priority"][1], 2)
        self.assertEqual(result["by_priority"][2], 0)
        self.assertEqual(result["by_priority"][3], 1)
        self.assertEqual(result["by_priority"][4], 0)
        self.assertEqual(result["by_priority"][5], 1)

    # 4 — single and multi-tag tasks
    def test_stats_by_tag(self):
        self._add("t1", 1, tags=["python"])
        self._add("t2", 2, tags=["python", "backend"])
        self._add("t3", 3, tags=["frontend"])
        result = self.svc.stats()
        self.assertEqual(result["by_tag"]["python"], 2)
        self.assertEqual(result["by_tag"]["backend"], 1)
        self.assertEqual(result["by_tag"]["frontend"], 1)

    # 5 — tasks before/after cutoff; only recent ones counted
    def test_stats_since_filter(self):
        self._add("old",   1, days_ago=10)
        self._add("recent", 2, days_ago=1)
        cutoff = datetime.utcnow() - timedelta(days=5)
        result = self.svc.stats(since=cutoff)
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["pending"], 1)

    # 6 — since in future returns zeros
    def test_stats_since_future(self):
        self._add("a", 1)
        self._add("b", 2)
        future = datetime.utcnow() + timedelta(days=1)
        result = self.svc.stats(since=future)
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["done"], 0)
        self.assertEqual(result["pending"], 0)
        self.assertEqual(result["by_tag"], {})
        self.assertEqual(set(result["by_priority"].keys()), {1, 2, 3, 4, 5})

    # 7 — limit=1 with 5 tasks; only 1 counted
    def test_stats_limit_applied(self):
        for i in range(5):
            self._add(f"task{i}", 1)
        result = self.svc.stats(limit=1)
        self.assertEqual(result["total"], 1)

    # 8 — limit=1 and limit=500 do NOT raise
    def test_stats_limit_boundary_valid(self):
        self._add("a", 1)
        self.svc.stats(limit=1)
        self.svc.stats(limit=500)

    # 9 — float limit raises ValueError
    def test_stats_limit_float_raises(self):
        with self.assertRaises(ValueError):
            self.svc.stats(limit=1.5)

    # 10 — string since raises TypeError
    def test_stats_since_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.svc.stats(since="2024-01-01")

    # 9 — limit=0 raises ValueError
    def test_stats_limit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.svc.stats(limit=0)

    # 10 — limit=501 raises ValueError
    def test_stats_limit_over_max_raises(self):
        with self.assertRaises(ValueError):
            self.svc.stats(limit=501)

    # 11 — task with tags=[] not counted in by_tag
    def test_stats_by_tag_empty_tags(self):
        self._add("no-tags", 1, tags=[])
        result = self.svc.stats()
        self.assertEqual(result["by_tag"], {})

    # 12 — all 5 priority keys present even with sparse data
    def test_stats_all_priorities_present(self):
        self._add("a", 1)
        self._add("b", 3)
        result = self.svc.stats()
        self.assertEqual(set(result["by_priority"].keys()), {1, 2, 3, 4, 5})
        self.assertEqual(result["by_priority"][2], 0)
        self.assertEqual(result["by_priority"][4], 0)
        self.assertEqual(result["by_priority"][5], 0)

    # 13 — done + pending == total invariant holds with filters
    def test_stats_done_pending_sum_equals_total(self):
        self._add("a", 1, done=True,  days_ago=2)
        self._add("b", 2, done=False, days_ago=2)
        self._add("c", 3, done=True,  days_ago=1)
        cutoff = datetime.utcnow() - timedelta(days=3)
        result = self.svc.stats(since=cutoff, limit=10)
        self.assertEqual(result["done"] + result["pending"], result["total"])

    # 14 — since=None includes all tasks regardless of age
    def test_stats_since_none_includes_all(self):
        self._add("old", 1, days_ago=100)
        self._add("new", 2, days_ago=0)
        result = self.svc.stats(since=None)
        self.assertEqual(result["total"], 2)

    # 15 — combined since + limit; limit applied after since filter
    def test_stats_since_and_limit_combined(self):
        self._add("old",     1, days_ago=10)
        self._add("recent1", 2, days_ago=1)
        self._add("recent2", 3, days_ago=1)
        cutoff = datetime.utcnow() - timedelta(days=5)
        result = self.svc.stats(since=cutoff, limit=1)
        self.assertEqual(result["total"], 1)

    # 16 — bool limit raises ValueError (bool is subclass of int, must be rejected)
    def test_stats_limit_bool_raises(self):
        with self.assertRaises(ValueError):
            self.svc.stats(limit=True)
        with self.assertRaises(ValueError):
            self.svc.stats(limit=False)

    # 17 — since=task.created_at is inclusive (>= boundary)
    def test_stats_since_exact_boundary(self):
        task = self._add("boundary", 2)
        result = self.svc.stats(since=task.created_at)
        self.assertEqual(result["total"], 1)

    # 18 — datetime.date raises TypeError (not a datetime instance)
    def test_stats_since_date_type_raises(self):
        import datetime as dt
        with self.assertRaises(TypeError):
            self.svc.stats(since=dt.date.today())

    # 19 — limit=None raises ValueError
    def test_stats_limit_none_raises(self):
        with self.assertRaises(ValueError):
            self.svc.stats(limit=None)

    # 20 — returned dict is independent; mutating it does not affect next call
    def test_stats_return_is_independent(self):
        result1 = self.svc.stats()
        result1["by_priority"][1] = 999
        result2 = self.svc.stats()
        self.assertNotEqual(result2["by_priority"][1], 999)


if __name__ == "__main__":
    unittest.main()

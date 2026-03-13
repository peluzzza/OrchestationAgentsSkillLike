"""
Tests for Task API - Some tests FAIL due to validation bug.

Run with: py -m unittest discover -s demos/atlas-orchestration-smoke -v
Or from demo folder: py -m unittest -v
"""
import unittest
from datetime import date, timedelta
from task_api import (
    TaskRepository, Task, TaskStatus, Priority, ValidationError
)


class TestTaskCreation(unittest.TestCase):
    """Tests for task creation and validation."""
    
    def setUp(self):
        self.repo = TaskRepository()
    
    def test_create_valid_task(self):
        """Should create task with valid data."""
        task = self.repo.create("Fix login bug", 3)
        self.assertEqual(task.title, "Fix login bug")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertIsNotNone(task.id)
    
    def test_create_with_due_date(self):
        """Should create task with future due date."""
        future = date.today() + timedelta(days=7)
        task = self.repo.create("Deploy v2", 4, due_date=future)
        self.assertEqual(task.due_date, future)
    
    def test_title_whitespace_trimmed(self):
        """Should trim whitespace from title."""
        task = self.repo.create("  Refactor API  ", 2)
        self.assertEqual(task.title, "Refactor API")
    
    # === Title Validation ===
    
    def test_empty_title_raises(self):
        """Should reject empty title."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("", 2)
        self.assertIn("empty", str(ctx.exception).lower())
    
    def test_whitespace_only_title_raises(self):
        """Should reject whitespace-only title."""
        with self.assertRaises(ValidationError):
            self.repo.create("   ", 2)
    
    def test_title_too_long_raises(self):
        """Should reject title over 200 chars."""
        long_title = "x" * 201
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create(long_title, 2)
        self.assertIn("200", str(ctx.exception))
    
    def test_title_with_invalid_chars_raises(self):
        """Should reject title with < > { } characters."""
        with self.assertRaises(ValidationError):
            self.repo.create("Task <script>", 2)
    
    # === Priority Validation - THESE FAIL DUE TO BUG ===
    
    def test_priority_zero_raises(self):
        """Should reject priority 0."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("Task", 0)
        self.assertIn("priority", str(ctx.exception).lower())
    
    def test_priority_negative_raises(self):
        """Should reject negative priority."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("Task", -1)
        self.assertIn("priority", str(ctx.exception).lower())
    
    def test_priority_five_raises(self):
        """Should reject priority 5 (only 1-4 valid)."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("Task", 5)
        self.assertIn("priority", str(ctx.exception).lower())
    
    def test_priority_hundred_raises(self):
        """Should reject priority 100."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("Task", 100)
        self.assertIn("priority", str(ctx.exception).lower())
    
    # === Due Date Validation ===
    
    def test_past_due_date_raises(self):
        """Should reject due date in the past."""
        yesterday = date.today() - timedelta(days=1)
        with self.assertRaises(ValidationError) as ctx:
            self.repo.create("Task", 2, due_date=yesterday)
        self.assertIn("past", str(ctx.exception).lower())


class TestTaskStatusTransitions(unittest.TestCase):
    """Tests for status transition validation."""
    
    def setUp(self):
        self.repo = TaskRepository()
        self.task = self.repo.create("Test task", 2)
    
    def test_todo_to_in_progress(self):
        """Should allow TODO -> IN_PROGRESS."""
        updated = self.repo.update_status(self.task.id, TaskStatus.IN_PROGRESS)
        self.assertEqual(updated.status, TaskStatus.IN_PROGRESS)
    
    def test_todo_to_blocked(self):
        """Should allow TODO -> BLOCKED."""
        updated = self.repo.update_status(self.task.id, TaskStatus.BLOCKED)
        self.assertEqual(updated.status, TaskStatus.BLOCKED)
    
    def test_todo_to_done_raises(self):
        """Should NOT allow TODO -> DONE directly."""
        with self.assertRaises(ValidationError):
            self.repo.update_status(self.task.id, TaskStatus.DONE)
    
    def test_done_to_any_raises(self):
        """Should NOT allow any transition from DONE."""
        # First, get to DONE state
        self.repo.update_status(self.task.id, TaskStatus.IN_PROGRESS)
        self.repo.update_status(self.task.id, TaskStatus.DONE)
        
        # Try to transition out
        with self.assertRaises(ValidationError):
            self.repo.update_status(self.task.id, TaskStatus.TODO)
    
    def test_nonexistent_task_raises(self):
        """Should raise for non-existent task ID."""
        with self.assertRaises(ValidationError) as ctx:
            self.repo.update_status(999, TaskStatus.DONE)
        self.assertIn("not found", str(ctx.exception).lower())


class TestTaskQueries(unittest.TestCase):
    """Tests for task queries."""
    
    def setUp(self):
        self.repo = TaskRepository()
        self.repo.create("Low task", 1)
        self.repo.create("Medium task", 2)
        self.repo.create("High task", 3)
        self.repo.create("Critical task", 4)
    
    def test_list_by_priority_high(self):
        """Should return HIGH and CRITICAL tasks."""
        tasks = self.repo.list_by_priority(Priority.HIGH)
        self.assertEqual(len(tasks), 2)
        titles = {t.title for t in tasks}
        self.assertEqual(titles, {"High task", "Critical task"})
    
    def test_list_by_priority_all(self):
        """Should return all tasks for LOW priority."""
        tasks = self.repo.list_by_priority(Priority.LOW)
        self.assertEqual(len(tasks), 4)
    
    def test_get_existing_task(self):
        """Should return task by ID."""
        task = self.repo.get(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Low task")
    
    def test_get_nonexistent_returns_none(self):
        """Should return None for non-existent ID."""
        task = self.repo.get(999)
        self.assertIsNone(task)


if __name__ == "__main__":
    unittest.main()

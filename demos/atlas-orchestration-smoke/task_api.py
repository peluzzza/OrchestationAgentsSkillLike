"""
Simple Task API module - Contains a validation bug for Atlas demo.

This simulates a REST API data layer with:
- Task creation with priority validation
- Task status transitions
- Due date validation
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
import re


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    title: str
    priority: Priority
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None


class ValidationError(Exception):
    """Raised when task data fails validation."""
    pass


class TaskRepository:
    """In-memory task storage with validation."""
    
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
    
    def create(self, title: str, priority: int, due_date: Optional[date] = None) -> Task:
        """
        Create a new task.
        
        Args:
            title: Task title (non-empty, max 200 chars)
            priority: Priority level (1-4)
            due_date: Optional due date (must be in future)
        
        Returns:
            Created Task object
        
        Raises:
            ValidationError: If any validation fails
        """
        # Validate title
        self._validate_title(title)
        
        # Validate priority - BUG: allows any integer, should only allow 1-4
        priority_enum = self._validate_priority(priority)
        
        # Validate due date
        if due_date:
            self._validate_due_date(due_date)
        
        # Create task
        task = Task(
            id=self._next_id,
            title=title.strip(),
            priority=priority_enum,
            due_date=due_date
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        
        return task
    
    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self._tasks.get(task_id)
    
    def update_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """Update task status with transition validation."""
        task = self._tasks.get(task_id)
        if not task:
            raise ValidationError(f"Task {task_id} not found")
        
        # Validate status transition
        self._validate_status_transition(task.status, new_status)
        task.status = new_status
        return task
    
    def list_by_priority(self, min_priority: Priority) -> list[Task]:
        """List tasks at or above given priority."""
        return [
            t for t in self._tasks.values()
            if t.priority.value >= min_priority.value
        ]
    
    def _validate_title(self, title: str) -> None:
        """Validate task title."""
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")
        # Check for invalid characters
        if re.search(r'[<>{}]', title):
            raise ValidationError("Title contains invalid characters")
    
    def _validate_priority(self, priority: int) -> Priority:
        """
        Validate and convert priority integer to enum.
        
        BUG: This implementation doesn't properly reject invalid values!
        It should raise ValidationError for values outside 1-4.
        """
        if priority < 1 or priority > 4:
            raise ValidationError("priority must be between 1 and 4")
        return Priority(priority)
    
    def _validate_due_date(self, due_date: date) -> None:
        """Validate due date is not in the past."""
        if due_date < date.today():
            raise ValidationError("Due date cannot be in the past")
    
    def _validate_status_transition(self, current: TaskStatus, new: TaskStatus) -> None:
        """Validate status transition is allowed."""
        # Define allowed transitions
        allowed = {
            TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED},
            TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.BLOCKED, TaskStatus.TODO},
            TaskStatus.BLOCKED: {TaskStatus.TODO, TaskStatus.IN_PROGRESS},
            TaskStatus.DONE: set()  # No transitions from DONE
        }
        
        if new not in allowed[current]:
            raise ValidationError(
                f"Cannot transition from {current.value} to {new.value}"
            )

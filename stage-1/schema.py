"""
Stage 1: Schema Validation Engine for SwarmForge Dark Factory.
"""
from typing import Dict, Any, Tuple, List
try:
    from .models import TaskNode, SeatConfig, FactoryState
except ImportError:
    from models import TaskNode, SeatConfig, FactoryState

class SchemaValidator:
    REQUIRED_TASK_FIELDS = {"id", "name", "stage", "seat", "action"}
    VALID_SEATS = {"architect", "builder", "verifier", "supervisor", "fixer"}
    VALID_STATUSES = {"PENDING", "RUNNING", "COMPLETED", "FAILED", "HEALED"}

    @classmethod
    def validate_task_dict(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        for field in cls.REQUIRED_TASK_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")

        seat = data.get("seat", "")
        if seat and seat.lower() not in cls.VALID_SEATS:
            errors.append(f"Invalid seat '{seat}'. Must be one of: {cls.VALID_SEATS}")

        status = data.get("status", "PENDING")
        if status not in cls.VALID_STATUSES:
            errors.append(f"Invalid status '{status}'. Must be one of: {cls.VALID_STATUSES}")

        return (len(errors) == 0, errors)

    @classmethod
    def validate_plan_schema(cls, plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if "tasks" not in plan or not isinstance(plan["tasks"], list):
            return False, ["Plan must contain a 'tasks' list."]

        seen_ids = set()
        for i, task_data in enumerate(plan["tasks"]):
            is_valid, task_errors = cls.validate_task_dict(task_data)
            if not is_valid:
                errors.extend([f"Task[{i}] error: {e}" for e in task_errors])
            task_id = task_data.get("id")
            if task_id in seen_ids:
                errors.append(f"Duplicate task id detected: '{task_id}'")
            if task_id:
                seen_ids.add(task_id)

        # Check cyclic or missing dependencies
        for task_data in plan["tasks"]:
            for dep in task_data.get("dependencies", []):
                if dep not in seen_ids:
                    errors.append(f"Task '{task_data.get('id')}' references non-existent dependency '{dep}'")

        return (len(errors) == 0, errors)

"""
Unit tests for Stage 1: Data Models & Schema Validation.
"""
import unittest
import os
import sys

# Ensure stage directory is in path
stage_dir = os.path.dirname(os.path.abspath(__file__))
if stage_dir not in sys.path:
    sys.path.insert(0, stage_dir)

from models import TaskNode, SeatConfig, FactoryState
from schema import SchemaValidator

class TestStage1(unittest.TestCase):
    def test_model_instantiation_and_serialization(self):
        seat = SeatConfig(
            seat_id="seat-01",
            role_name="Architect",
            mandate_file="mandates/01_architect.md",
            provider_binary="opencode"
        )
        task = TaskNode(
            id="t1",
            name="Scaffold Schema",
            stage=1,
            seat="architect",
            action="Generate JSON schemas"
        )
        factory = FactoryState(
            factory_id="fact-001",
            project_name="DarkFactory-Test",
            seats={"architect": seat},
            tasks={"t1": task}
        )
        
        json_output = factory.to_json()
        self.assertIn("DarkFactory-Test", json_output)
        self.assertIn("Scaffold Schema", json_output)

    def test_schema_validator_valid_plan(self):
        plan = {
            "tasks": [
                {"id": "task-1", "name": "Init", "stage": 1, "seat": "architect", "action": "Plan"},
                {"id": "task-2", "name": "Build", "stage": 2, "seat": "builder", "action": "Code", "dependencies": ["task-1"]}
            ]
        }
        is_valid, errors = SchemaValidator.validate_plan_schema(plan)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_schema_validator_catches_invalid_dependency(self):
        plan = {
            "tasks": [
                {"id": "task-1", "name": "Init", "stage": 1, "seat": "architect", "action": "Plan", "dependencies": ["ghost-task"]}
            ]
        }
        is_valid, errors = SchemaValidator.validate_plan_schema(plan)
        self.assertFalse(is_valid)
        self.assertTrue(any("ghost-task" in e for e in errors))

if __name__ == "__main__":
    unittest.main()

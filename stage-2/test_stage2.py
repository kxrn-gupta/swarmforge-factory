"""
Unit tests for Stage 2: DAG Scheduler & Parallel Wave Execution.
"""
import unittest
import os
import sys

stage_dir = os.path.dirname(os.path.abspath(__file__))
if stage_dir not in sys.path:
    sys.path.insert(0, stage_dir)

from dag_scheduler import DAGScheduler

class TestStage2(unittest.TestCase):
    def test_linear_dependency_waves(self):
        tasks = [
            {"id": "t1", "name": "Plan", "seat": "architect", "dependencies": []},
            {"id": "t2", "name": "Build", "seat": "builder", "dependencies": ["t1"]},
            {"id": "t3", "name": "Verify", "seat": "verifier", "dependencies": ["t2"]}
        ]
        scheduler = DAGScheduler(tasks)
        waves = scheduler.compute_parallel_waves()
        self.assertEqual(waves, [["t1"], ["t2"], ["t3"]])

    def test_diamond_parallel_waves(self):
        tasks = [
            {"id": "root", "name": "Root Plan", "seat": "architect", "dependencies": []},
            {"id": "sub_a", "name": "Subservice A", "seat": "builder", "dependencies": ["root"]},
            {"id": "sub_b", "name": "Subservice B", "seat": "builder", "dependencies": ["root"]},
            {"id": "join", "name": "Join Verification", "seat": "verifier", "dependencies": ["sub_a", "sub_b"]}
        ]
        scheduler = DAGScheduler(tasks)
        waves = scheduler.compute_parallel_waves()
        self.assertEqual(len(waves), 3)
        self.assertEqual(waves[0], ["root"])
        self.assertEqual(sorted(waves[1]), ["sub_a", "sub_b"])
        self.assertEqual(waves[2], ["join"])

    def test_cycle_detection(self):
        tasks = [
            {"id": "t1", "name": "Task 1", "seat": "builder", "dependencies": ["t2"]},
            {"id": "t2", "name": "Task 2", "seat": "builder", "dependencies": ["t1"]}
        ]
        scheduler = DAGScheduler(tasks)
        with self.assertRaises(ValueError):
            scheduler.compute_parallel_waves()

if __name__ == "__main__":
    unittest.main()

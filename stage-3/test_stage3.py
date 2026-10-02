"""
Unit tests for Stage 3: AST Diff Inspection & Self-Healing Loop.
"""
import unittest
import os
import sys

stage_dir = os.path.dirname(os.path.abspath(__file__))
if stage_dir not in sys.path:
    sys.path.insert(0, stage_dir)

from ast_diff import ASTInspector
from self_healer import SelfHealer

class TestStage3(unittest.TestCase):
    def test_valid_syntax_inspection(self):
        code = "def hello():\n    return 'world'\n"
        is_valid, err = ASTInspector.validate_syntax(code)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_invalid_syntax_detection(self):
        broken_code = "def broken(\n    pass"
        is_valid, err = ASTInspector.validate_syntax(broken_code)
        self.assertFalse(is_valid)
        self.assertIn("SyntaxError", err)

    def test_unified_diff_generation(self):
        old_code = "def calculate(x):\n    return x + 1\n"
        new_code = "def calculate(x):\n    return x * 2\n"
        diff = ASTInspector.generate_unified_diff(old_code, new_code)
        self.assertIn("-    return x + 1", diff)
        self.assertIn("+    return x * 2", diff)

    def test_autonomous_syntax_self_healing(self):
        broken_code = "def add(a, b)\n    return a + b"
        is_healed, healed_code, diff = SelfHealer.attempt_syntax_repair(broken_code)
        self.assertTrue(is_healed)
        self.assertIn("def add(a, b):", healed_code)
        self.assertIn("+def add(a, b):", diff)

if __name__ == "__main__":
    unittest.main()

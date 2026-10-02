"""
Stage 3: AST-Level Diff Inspection & Syntax Verification Engine.
Standard library ast & difflib implementation.
"""
import ast
import difflib
from typing import Dict, Any, Tuple, Optional

class ASTInspector:
    @staticmethod
    def validate_syntax(source_code: str) -> Tuple[bool, Optional[str]]:
        """Parses Python source code into an AST to verify syntax validity."""
        try:
            ast.parse(source_code)
            return True, None
        except SyntaxError as e:
            return False, f"SyntaxError at line {e.lineno}: {e.msg}"

    @staticmethod
    def generate_unified_diff(old_code: str, new_code: str, fromfile: str = "original.py", tofile: str = "healed.py") -> str:
        """Produces a Git-style unified diff of source changes."""
        old_lines = old_code.splitlines(keepends=True)
        new_lines = new_code.splitlines(keepends=True)
        diff = difflib.unified_diff(old_lines, new_lines, fromfile=fromfile, tofile=tofile)
        return "".join(diff)

    @staticmethod
    def compute_ast_complexity(source_code: str) -> int:
        """Computes simple cyclomatic / node complexity of the AST."""
        try:
            tree = ast.parse(source_code)
            return len(list(ast.walk(tree)))
        except Exception:
            return 0
